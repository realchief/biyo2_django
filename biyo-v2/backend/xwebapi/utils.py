from xml.etree import ElementTree

import requests
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


XML_TEMPLATE = """
<?xml version="1.0?>
<GatewayRequest>
{0}
\t<TransactionType>{1}</TransactionType>
{2}
</GatewayRequest>
"""

XML_NODE_TEMPLATE = """\t<{0}>{1}</{0}>"""

AP_ENDPOINTS = {
    'test': 'https://test.t3secure.net/x-chargeweb.dll',
    'production': 'https://gw.t3secure.net/x-chargeweb.dll'
}


def dict_to_xml(header_fields, transaction_type, transaction_fields):
    header_xml = []
    transaction_xml = []
    for field_name, field_value in header_fields.iteritems():
        header_xml.append(XML_NODE_TEMPLATE.format(field_name, field_value))
    for field_name, field_value in transaction_fields.iteritems():
        transaction_xml.append(
            XML_NODE_TEMPLATE.format(field_name, field_value))

    return XML_TEMPLATE.format(
        "\n".join(header_xml),
        transaction_type,
        "\n".join(transaction_xml),
    )


def prepare_header():
    xwebid = getattr(settings, "ACCELERATED_PAY_XWEBID", None)
    terminalid = getattr(settings, "ACCELERATED_PAY_TERMINALID", None)
    authkey = getattr(settings, "ACCELERATED_PAY_AUTHKEY", None)
    postype = getattr(settings, "ACCELERATED_PAY_POSTYPE", "PC")
    industry = getattr(settings, "ACCELERATED_PAY_INDUSTRY", None)

    if not xwebid:
        raise ImproperlyConfigured("ACCELERATED_PAY_XWEBID is not set")
    if not terminalid:
        raise ImproperlyConfigured("ACCELERATED_PAY_TERMINALID is not set")
    if not authkey:
        raise ImproperlyConfigured("ACCELERATED_PAY_AUTHKEY is not set")
    if not industry:
        raise ImproperlyConfigured("ACCELERATED_PAY_INDUSTRY is not set")

    header = {}
    header["XWebID"] = xwebid
    header["TerminalID"] = terminalid
    header["AuthKey"] = authkey
    header["SpecVersion"] = "XWeb3.4"
    header["Industry"] = industry
    header["POSType"] = postype
    header["PinCapabilities"] = "TRUE"
    header["TrackCapabilities"] = "BOTH"
    return header


def send_message(transaction_type, transaction_fields):
    mode = getattr(settings, "ACCELERATED_PAY_MODE", None)

    if not mode:
        raise ImproperlyConfigured("ACCELERATED_PAY_MODE is not set, available values: 'test', 'production'")
    if not mode in AP_ENDPOINTS.iterkeys():
        raise ImproperlyConfigured("ACCELERATED_PAY_MODE is invalid, available values: 'test', 'production'")

    header = prepare_header()
    data = dict_to_xml(header, transaction_type, transaction_fields)

    endpoint = AP_ENDPOINTS[mode]
    headers = {'Content-Type': 'application/xml'}
    response = requests.post(endpoint, data=data, headers=headers)
    output = {}
    if response.status_code != 200:
        output["status"] = "network_error"
        output["error_code"] = response.status_code
        return output
    output["status"] = "success"

    resp_xml = ElementTree.fromstring(response.text)

    output["ResponseCode"] = resp_xml.find("ResponseCode").text
    output["ResponseDescription"] = resp_xml.find("ResponseDescription").text
    output["TransactionID"] = resp_xml.find("TransactionID").text
    output["raw_xml"] = resp_xml
    return output
