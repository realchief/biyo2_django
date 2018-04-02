from xwebapi import utils


def create(acct_num, exp_date, card_code=None, address=None, zipcode=None):
    body = {
        "AcctNum": acct_num,
        "ExpDate": exp_date
    }

    if card_code:
        body["CardCode"] = card_code
    if address:
        body["Address"] = address
    if zipcode:
        body["ZipCode"] = zipcode

    response = utils.send_message("AliasCreateTransaction", body)

    if response["status"] != 'success':
        return response
    if response["ResponseCode"] != "005":
        response["status"] = "failed"
        return response

    response["Alias"] = response["raw_xml"].find("Alias").text
    response["CardType"] = response["raw_xml"].find("CardType").text
    response["MaskedAcctNum"] = response["raw_xml"].find("MaskedAcctNum").text
    response["ExpDate"] = response["raw_xml"].find("ExpDate").text
    del response["raw_xml"]

    return response


def delete(alias):
    body = {
        "Alias": alias,
    }

    response = utils.send_message("AliasDeleteTransaction", body)

    if response["status"] != 'success':
        return response
    if response["ResponseCode"] != "005":
        response["status"] = "failed"
        return response

    del response["raw_xml"]
    return response
