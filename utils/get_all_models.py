from django.apps import apps
from django.utils.translation import gettext_lazy as _


def get_all_models():
    models_list = []
    for model in apps.get_models():
        model_info = {
            'app_label': model._meta.app_label,
            'model_name': model._meta.model_name,
            'verbose_name': str(model._meta.verbose_name),  # Convert to string
            # Convert to string
            'verbose_name_plural': str(model._meta.verbose_name_plural),
            'model_class': model
        }
        models_list.append(model_info)
    return models_list
