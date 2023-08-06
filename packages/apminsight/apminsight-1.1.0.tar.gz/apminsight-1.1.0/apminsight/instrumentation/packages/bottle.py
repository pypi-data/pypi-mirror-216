from apminsight import constants
from apminsight.instrumentation.wrapper import wsgi_wrapper, args_wrapper
from apminsight.context import get_cur_txn, is_no_active_txn
from apminsight.logger import agentlogger

def get_status_code(original, module_name, method_info):
    def wrapper(*args, **kwargs):
        if is_no_active_txn():
            return original(*args, **kwargs)
        try:
            cur_txn = get_cur_txn()
            status_code = 500
            if isinstance(args,tuple) and len(args) >= 3 :
                status_code =  int(args[2])
            cur_txn.set_status_code(status_code)
        except:
            agentlogger.exception('Exception occured while getting Status Code')
        return original(*args, **kwargs)
    return wrapper

module_info = {
    'bottle' : [
        {
            constants.class_str : 'Bottle',
            constants.method_str : 'wsgi',
            constants.wrapper_str : wsgi_wrapper,
            constants.component_str : constants.bottle_comp
        },
        {
            constants.class_str : 'Route',
            constants.method_str : '__init__',
            constants.wrap_args_str : 4,
            constants.component_str : constants.bottle_comp,
        },
        {
            constants.class_str : 'MakoTemplate',
            constants.method_str : 'render',
            constants.component_str : 'MAKOTEMPLATE'
        },
        {
            constants.class_str : 'CheetahTemplate',
            constants.method_str : 'render',
            constants.component_str : 'CheetahTemplate'
        },
        {
            constants.class_str : 'Jinja2Template',
            constants.method_str : 'render',
            constants.component_str : 'Jinja2Template'
        },
        {
            constants.class_str : 'SimpleTemplate',
            constants.method_str : 'render',
            constants.component_str : 'SimpleTemplate'
        },
         {
            constants.class_str : 'BaseResponse',
            constants.method_str : '__init__',
            constants.component_str : constants.bottle_comp,
            constants.wrapper_str : get_status_code
        }
    ],
}
