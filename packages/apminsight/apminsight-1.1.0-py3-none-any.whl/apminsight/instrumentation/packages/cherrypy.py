from apminsight import constants
from apminsight.instrumentation.wrapper import copy_attributes, wsgi_wrapper, default_wrapper
from apminsight.context import get_cur_txn, is_no_active_txn
from apminsight.util import is_callable
from apminsight.logger import agentlogger

def view_wrapper(original, module, method_info):
    def wrapper(*args, **kwargs):
        if is_no_active_txn():
            return original(*args, **kwargs)
        try:
            res = original(*args, **kwargs)
        except Exception as exc:
            raise exc
        if isinstance(res,tuple) and len(res) == 2 :
            view = res[0]
            if is_callable(view):
                try:
                    module = view.__module__
                    method_info =  {'method' : view.__name__}
                    new_method = default_wrapper(view, module, method_info)
                    copy_attributes(view, new_method)
                    new_result = list(res)
                    new_result[0] = new_method
                    res = tuple(new_result)

                except:
                    agentlogger.exception("Error in CherryPy view wrapper")
        return res
    return wrapper

def get_status_code(original, module, method_info):
    def wrapper(*args, **kwargs):

        if is_no_active_txn():
            return original(*args, **kwargs)
    
        cur_txn = get_cur_txn()
        try:
            res = original(*args, **kwargs)
        except Exception as exc:
            raise exc
        try:
            if res :
                status_code = res.status
                cur_txn.set_status_code(int(status_code.split(' ')[0]))
        except:
            agentlogger.exception("while getting Status Code in CherryPy application")
        return res
    return wrapper
    
module_info = {
    'cherrypy._cpwsgi' : [
        {
            constants.class_str : 'CPWSGIApp',
            constants.method_str : '__call__',
            constants.component_str : 'CHERRYPY',
            constants.wrapper_str : wsgi_wrapper
        },
    ],

    'cherrypy._cprequest' : [
        {
            constants.class_str : 'Request',
            constants.method_str : 'run',
            constants.component_str : 'CHERRYPY',
            constants.wrapper_str : get_status_code
        }
    ],
    'cherrypy._cpdispatch' : [
        {
            constants.class_str : 'Dispatcher',
            constants.method_str : 'find_handler',
            constants.component_str : 'CHERRYPY',
            constants.wrapper_str : view_wrapper
        }
    ],
 }
