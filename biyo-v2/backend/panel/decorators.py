# -*- coding: utf-8 -*-
from django.utils.decorators import method_decorator


def dispatch_decorator(view_decorator):
    """
    Patch class based view with decorator
    """
    def class_decorator(class_obj):
        decorator = method_decorator(view_decorator)
        class_obj.dispatch = decorator(class_obj.dispatch)
        return class_obj
    return class_decorator


def return_view(decorating_method):
    """
    Set that this method returns a view
    """
    decorating_method.is_get_view = True
    decorating_method.is_for_single = False
    return decorating_method


def return_detail_view(decorating_method):
    """
    Set that method returns a view and this view
    will work with single object(pk)
    """
    decorating_method.is_return_view = True
    decorating_method.is_for_single = True
    return decorating_method

