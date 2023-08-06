from apminsight import constants
from apminsight.instrumentation.wrapper import wsgi_wrapper
from apminsight.context import get_cur_txn, is_no_active_txn
from apminsight.logger import agentlogger


def get_status_code(original, module, method_info):
    def wrapper(*args, **kwargs):
        if is_no_active_txn():
            return original(*args, **kwargs)
        try:
            res = original(*args, **kwargs)
        except Exception as exc:
            raise exc
        try:
            if hasattr(args[0], 'status'):
                cur_txn = get_cur_txn()
                status = args[0].status
                if isinstance(status, str):
                    status_code = int(status.split()[0])
                cur_txn.set_status_code(status_code)
        except:
            agentlogger.exception('while getting status code')
        return res
    return wrapper

module_info = {
    'pyramid.router' : [
        {
            constants.class_str : 'Router',
            constants.method_str : '__call__',
            constants.wrapper_str : wsgi_wrapper,
            constants.component_str : constants.pyramid_comp
        },
    ],
    'pyramid.config.views': [
        {
            constants.class_str : 'ViewsConfiguratorMixin',
            constants.method_str : '_derive_view',
            constants.component_str : constants.pyramid_comp,
            constants.wrap_args_str : 1
        }
    ],
    'pyramid.renderers' : [
        {
            constants.class_str : 'RendererHelper',
            constants.method_str : 'render',
            constants.component_str : constants.template,
        }
    
    ],
    'pyramid.response' : [
        {
            constants.class_str : 'Response',
            constants.method_str : '__init__',
            constants.wrapper_str : get_status_code,
            constants.component_str : constants.pyramid_comp,
        }
    ]
}
