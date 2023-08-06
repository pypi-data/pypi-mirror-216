
from apminsight import constants
from apminsight.instrumentation.wrapper import wsgi_wrapper

def wrap_get_wsgi_application(original, module, method_info):
    def wrapper(*args, **kwargs):
        from apminsight.instrumentation import instrument_django_middlewares
        instrument_django_middlewares()
        return original(*args, **kwargs)
    return wrapper

module_info = {
    'django.core.handlers.wsgi' : [
        {
            constants.class_str : 'WSGIHandler',
            constants.method_str : '__call__',
            constants.wrapper_str : wsgi_wrapper,
            constants.component_str : constants.django_comp
        }
    ],
    'django.conf.urls' : [
        {
            constants.method_str : 'url',
            constants.wrap_args_str : 1,
            constants.component_str : constants.django_comp
        }
    ],
    'django.urls' : [
        {
            constants.method_str : 'path',
            constants.wrap_args_str : 1,
            constants.component_str : constants.django_comp
        }
    ],
    'django.template' : [
        {
            constants.class_str : 'Template',
            constants.method_str : 'render',
            constants.component_str : constants.template
        }
    ],
    'django.core.wsgi' : [
        {
            constants.method_str : 'get_wsgi_application',
            constants.wrapper_str : wrap_get_wsgi_application,
            constants.component_str : constants.django_comp
        }
    ],
}