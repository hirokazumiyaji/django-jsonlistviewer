import json
import os

from django.conf import settings
from django.http import HttpResponse
from django.views.generic.base import TemplateView, View

from .models import Node


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        return {'node': Node(settings.DATA_DIR)}


class DetailView(TemplateView):
    template_name = 'detail.html'

    def get_context_data(self, **kwargs):
        return {'url_path': kwargs.get('path', '')}


class DetailDataView(View):

    def get(self, request, *args, **kwargs):
        filename = os.path.join(settings.DATA_DIR, kwargs.get('path', ''))
        response = {'columns': [],
                    'records': []}
        if not self._check_file(filename):
            return self.render_to_response(response)
        data_list = self._load_data(filename)
        if not data_list:
            return self.render_to_response(response)
        columns = self._gen_columns(data_list[0])
        records = []
        for data in data_list:
            records.append(self._gen_record(columns, data))

        response['columns'] = ['id'] + columns
        response['records'] = records
        return self.render_to_response(response)

    def _check_file(self, filename):
        return os.path.exists(filename) and os.path.isfile(filename)

    def _load_data(self, filename):
        return json.loads(open(filename).read())

    def _gen_columns(self, data):
        return [name for name in data['fields'].keys() if name != 'id']

    def _gen_record(self, columns, data):
        record = [data['pk']]
        record.extend([data['fields'][column] for column in columns])
        return record

    def render_to_response(self, context):
        return HttpResponse(json.dumps(context), content_type='application/json')
