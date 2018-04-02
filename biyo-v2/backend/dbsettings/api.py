from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from models import DBSettings
from serializers import PaginatedDBSettingSerializer
from products.models import Terminal
from terminalapi.views import get_serialized_page


@api_view(['GET'])
def get_all_dbsettings(request):
    settings = DBSettings.objects.all()
    page = get_serialized_page(request, settings, PaginatedDBSettingSerializer, size=50)
    return Response(data=page.data)


@api_view(['GET'])
def get_settings_by_terminal_pk(request, pk=None):
    '''
    Get all available settings by terminal PK
    If you provide empty PK it return all records who didn't have terminal
    '''
    terminal = Terminal.objects.filter(pk=pk).first()
    try:
        settings = DBSettings.objects.filter(terminal=terminal)
    except DBSettings.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    page = get_serialized_page(request, settings, PaginatedDBSettingSerializer, size=50)
    return Response(data=page.data)
