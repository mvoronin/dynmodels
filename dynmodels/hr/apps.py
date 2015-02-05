from django.apps import AppConfig
from hr.models import get_model_class, cls_dict_list


class HRConfig(AppConfig):
    name = 'hr'
    verbose_name = "HR"

    def ready(self):
        for cls_dict in cls_dict_list:
            get_model_class(cls_dict)
        super(HRConfig, self).ready()
