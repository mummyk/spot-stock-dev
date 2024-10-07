from django.apps import apps


def get_choices():
    choices = []
    for model_info in get_all_models():
        choices.append(
            (model_info['model_name'], model_info['verbose_name']))
    return choices


def get_all_models():
    models_list = []
    for model in apps.get_models():
        model_info = {
            'app_label': model._meta.app_label,
            'model_name': model._meta.model_name,
            'verbose_name': str(model._meta.verbose_name),
            'verbose_name_plural': str(model._meta.verbose_name_plural),
        }
        models_list.append(model_info)
    return models_list
