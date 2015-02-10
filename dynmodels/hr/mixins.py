# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import json
import logging
from django.core import serializers
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest, HttpResponseNotAllowed
from django.views.decorators.http import require_http_methods

logger = logging.getLogger(__name__)


class RequestCheckMixin(object):

    def dispatch(self, request, *args, **kwargs):
        if not request.is_ajax():
            return HttpResponseBadRequest()
        return super(RequestCheckMixin, self).dispatch(request, *args, **kwargs)


class AJAXListMixin(RequestCheckMixin):
    def get_context_data(self, context_format='object', **kwargs):
        """
        Get the context for this view.
        """
        queryset = kwargs.pop('object_list', self.object_list)
        page_size = self.get_paginate_by(queryset)
        context_object_name = self.get_context_object_name(queryset)
        if page_size:
            paginator, page, queryset, is_paginated = self.paginate_queryset(queryset, page_size)
            if context_format == 'object':
                context = {
                    'paginator': paginator,
                    'page_obj': page,
                    'is_paginated': is_paginated,
                    'object_list': queryset
                }
            elif context_format == 'json':
                context = {
                    'paginator': {
                        'count': paginator.count,
                        'num_pages': paginator.num_pages,
                        'page_range': paginator.page_range
                    },
                    'page_obj': {
                        'object_list': page.object_list.values(),
                        'number': page.number,
                        'has_next': page.has_next(),
                        'has_previous': page.has_previous(),
                        'has_other_pages': page.has_other_pages(),
                        'next_page_number': page.next_page_number(),
                        'previous_page_number': page.previous_page_number()
                    },
                    'is_paginated': is_paginated,
                    'object_list': json.loads(serializers.serialize("json", queryset))
                }
        else:
            if context_format == 'object':
                context = {
                    'paginator': None,
                    'page_obj': None,
                    'is_paginated': False,
                    'object_list': queryset
                }
            elif context_format == 'json':
                context = {
                    'paginator': None,
                    'page_obj': None,
                    'is_paginated': False,
                    'object_list': json.loads(serializers.serialize("json", queryset))
                }
        if context_format == 'object':
            if context_object_name is not None:
                context[context_object_name] = queryset
            context.update(kwargs)
            return super(AJAXListMixin, self).get_context_data(**context)
        else:
            return context

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()

        if self.request.is_ajax():
            context = self.get_context_data(context_format='json')
            return HttpResponse(json.dumps(context))
        else:
            context = self.get_context_data()
            return self.render_to_response(context)


class AJAXCreateView(RequestCheckMixin):
    def form_valid(self, form):
        if self.request.is_ajax():
            return HttpResponse(json.dumps({'result': 'ok'}))
        else:
            return super(AJAXCreateView, self).form_valid(form)

    def form_invalid(self, form):
        if self.request.is_ajax():
            return HttpResponseBadRequest(json.dumps({'result': 'invalid', 'error': form.errors}))
        else:
            return super(AJAXCreateView, self).form_invalid(form)


class AJAXUpdateView(AJAXCreateView):
    pass


class AJAXDeleteView(RequestCheckMixin):

    def dispatch(self, request, *args, **kwargs):
        if request.method not in ['POST']:
            logger.warning('Method Not Allowed (%s): %s', request.method, request.path,
                           extra={'status_code': 405, 'request': request})
            return HttpResponseNotAllowed(['POST'])
        return super(AJAXDeleteView, self).dispatch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()

        if self.request.is_ajax():
            return HttpResponse(json.dumps({'result': 'ok'}))
        else:
            return HttpResponseRedirect(success_url)
