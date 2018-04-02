# -*- coding: utf-8 -*-
# TODO: Refactor CRUD with decorators
import inspect

from django.db import models
from django.conf.urls import patterns, url
from django.views import generic as cbv

from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponseRedirect
from django.views.generic.detail import (SingleObjectTemplateResponseMixin, BaseDetailView)


class DeletionMixin(object):
    success_url = None

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.archived = True
        self.object.save()
        return HttpResponseRedirect(success_url)

    def post(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def get_success_url(self):
        if self.success_url:
            return self.success_url % self.object.__dict__
        else:
            raise ImproperlyConfigured(
                "No URL to redirect to. Provide a success_url.")


class BaseDeleteView(DeletionMixin, BaseDetailView):
    pass


class DeleteView(SingleObjectTemplateResponseMixin, BaseDeleteView):
    template_name_suffix = '_confirm_delete'


class GetTemplateMixin(object):
    """
    Add method for getting template
    """
    def get_or_build_template_name(self, template_attr, template_pattern):
        template_name = getattr(self, template_attr, None)
        return template_name or template_pattern % self.prefix


class ListViewMixin(GetTemplateMixin):
    """
    Functions for get list view
    """
    list_class_view = cbv.ListView

    def get_list_template_name(self):
        return self.get_or_build_template_name(
            'list_template_name',
            '%s_list.html'
        )

    def get_list_kwargs(self):
        return {}

    def get_list_view(self):
        return self.list_class_view.as_view(
            model=self.model,
            template_name=self.get_list_template_name(),
            **self.get_list_kwargs()
        )


class CreateViewMixin(GetTemplateMixin):
    """
    Functions for getting create view
    """
    create_class_view = cbv.CreateView

    def get_create_template_name(self):
        return self.get_or_build_template_name(
            'create_template_name',
            '%s_create.html'
        )

    def get_create_kwargs(self):
        return {}

    def get_create_view(self):
        return self.create_class_view.as_view(
            model=self.model,
            template_name=self.get_create_template_name(),
            **self.get_create_kwargs()
        )


class DetailViewMixin(GetTemplateMixin):
    """
    Functions for getting detail view
    """
    detail_class_view = cbv.DetailView

    def get_detail_template_name(self):
        return self.get_or_build_template_name(
            'detail_template_name',
            '%s_detail.html'
        )

    def get_detail_kwargs(self):
        return {}

    def get_detail_view(self):
        return self.detail_class_view.as_view(
            model=self.model,
            template_name=self.get_detail_template_name(),
            **self.get_detail_kwargs()
        )


class UpdateViewMixin(GetTemplateMixin):
    """
    Functions for getting update view
    """
    update_class_view = cbv.UpdateView

    def get_update_template_name(self):
        return self.get_or_build_template_name(
            'detail_template_name',
            '%s_update.html'
        )

    def get_update_kwargs(self):
        return {}

    def get_update_view(self):
        return self.update_class_view.as_view(
            model=self.model,
            template_name=self.get_update_template_name(),
            **self.get_update_kwargs()
        )


class DeleteViewMixin(GetTemplateMixin):
    """
    Functions for delete
    """
    delete_class_view = DeleteView

    def get_delete_template_name(self):
        return self.get_or_build_template_name(
            'delete_template_name',
            '%s_delete_confirm.html'
        )

    def get_delete_kwargs(self):
        return {}

    def get_delete_view(self):
        return self.delete_class_view.as_view(
            model=self.model,
            template_name=self.get_delete_template_name(),
            **self.get_delete_kwargs()
        )


class AbstractModelCRUD(object):
    """
    Class for generating views for list, create, read, update, delete
    of the model
    """
    model = None
    prefix = None
    default_decorators = None
    list_decorators = None
    create_decorators = None
    detail_decorators = None
    update_decorators = None
    delete_decorators = None

    def __init__(self, model=None, prefix=None, **kwargs):
        """
        Initialize crud object. Setting model, url_prefix,
        """
        self.model = model or self.model
        assert not model is None, "Model should be set for crud views"

        assert_msg = "model should be type of model not %s" % type(self.model)
        assert issubclass(self.model, models.Model), assert_msg

        self.prefix = (
            prefix or
            self.prefix or
            self.model.__name__.lower()
        )

        for key, value in kwargs.iteritems():
            if not hasattr(self, key):
                raise TypeError(
                    "%s received an invalid keyword %r "
                    "only accepts arguments that are already "
                    "attributes of the class." % (self.__class__.__name__, key)
                )
            setattr(self, key, value)

        if self.default_decorators is None:
            self.default_decorators = []

    def get_list_view(self):
        raise NotImplemented

    def get_create_view(self):
        raise NotImplemented

    def get_detail_view(self):
        raise NotImplemented

    def get_update_view(self):
        raise NotImplemented

    def get_delete_view(self):
        raise NotImplemented

    @property
    def list_url_name(self):
        return '%s_list' % self.prefix

    @property
    def detail_url_name(self):
        return '%s_detail' % self.prefix

    @property
    def create_url_name(self):
        return '%s_create' % self.prefix

    @property
    def update_url_name(self):
        return '%s_update' % self.prefix

    @property
    def delete_url_name(self):
        return '%s_delete' % self.prefix

    def wrap_view(self, view=None, decorators_list=None):
        """
        Wraps view with decorators
        """
        for decorator in decorators_list:
            view = decorator(view)
        return view

    def get_default_urls(self):
        return(
            url(
                r'^%s/$' % self.prefix,
                self.wrap_view(
                    self.get_list_view(),
                    (
                        getattr(self, 'list_decorators', None) or
                        self.default_decorators
                    )
                ),
                name=self.list_url_name
            ),
            url(
                r'^%s/add/$' % self.prefix,
                self.wrap_view(
                    self.get_create_view(),
                    (
                        getattr(self, 'create_decorators', None) or
                        self.default_decorators
                    )
                ),
                name=self.create_url_name
            ),
            url(
                r'^%s/-?(?P<pk>\d+)/$' % self.prefix,
                self.wrap_view(
                    self.get_detail_view(),
                    (
                        getattr(self, 'detail_decorators', None) or
                        self.default_decorators
                    )
                ),
                name=self.detail_url_name
            ),
            url(
                r'^%s/(?P<pk>\d+)/edit/$' % self.prefix,
                self.wrap_view(
                    self.get_update_view(),
                    (
                        getattr(self, 'detail_decorators', None) or
                        self.default_decorators
                    )
                ),
                name=self.update_url_name
            ),
            url(
                r'^%s/(?P<pk>\d+)/delete/$' % self.prefix,
                self.wrap_view(
                    self.get_delete_view(),
                    (
                        getattr(self, 'delete_decorators', None) or
                        self.default_decorators
                    )
                ),
                name=self.delete_url_name
            )
        )

    def get_extra_urls(self):
        attr_names = [
            x for x in dir(self) if not x.startswith('_')
            and x != 'urls'
        ]
        url_list = []
        for attr_name in attr_names:
            attr = getattr(self, attr_name)
            if inspect.ismethod(attr) and hasattr(attr, 'is_return_view'):
                if attr.is_for_single:
                    decorators = (
                        getattr(self, '%s_decorators' % attr_name, None) or
                        self.default_decorators
                    )
                    url_list.append(
                        url(
                            r'^%s/%s/(?P<pk>\d+)/$' % (self.prefix, attr_name),
                            self.wrap_view(
                                attr(),
                                decorators
                            ),
                            name='%s_%s' % (self.prefix, attr_name)
                        )
                    )
                else:
                    decorators = (
                        getattr(self, '%s_decorators' % attr_name, None) or
                        self.default_decorators
                    )
                    url_list.append(
                        url(
                            r'^%s/%s/$' % (self.prefix, attr_name),
                            self.wrap_view(
                                attr(),
                                decorators
                            ),
                            name='%s_%s' % (self.prefix, attr_name)
                        )
                    )
        return tuple(url_list)

    def get_urls(self):
        return self.get_default_urls() + self.get_extra_urls()

    @property
    def urls(self):
        """
        Gets urls for model views
        """
        return patterns(
            "",
            *self.get_urls()
        )


class BaseModelCRUD(ListViewMixin, CreateViewMixin, DetailViewMixin,
                    UpdateViewMixin, DeleteViewMixin, AbstractModelCRUD):
    pass

