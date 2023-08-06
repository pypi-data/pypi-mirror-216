from wagtail.admin.ui.tables import Column


class RadioShowPodcastsColumn(Column):
    cell_template_name = 'wagtail_webradio/tables/radio_show_podcasts_cell.html'

    def __init__(self, name, get_url, width='10%'):
        super().__init__(name, label='', width=width)
        self._get_url_func = get_url

    def get_cell_context_data(self, instance, parent_context):
        return {
            'column': self,
            'instance': instance,
            'podcasts_url': self._get_url_func(instance),
            'request': parent_context.get('request'),
        }
