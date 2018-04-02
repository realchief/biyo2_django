
from django.db import connection


def get_default_db_connection(request):
    # TODO: to implement multiple dbs support (for different customers)
    return connection
