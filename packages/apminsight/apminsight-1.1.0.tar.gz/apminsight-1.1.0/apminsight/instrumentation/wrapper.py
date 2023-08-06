
from apminsight.agentfactory import get_agent
from apminsight.logger import agentlogger
from apminsight.constants import wrap_args_str, CUSTOMPARAMS
from apminsight.util import is_callable, is_empty_string
from apminsight.context import clear_cur_context
from apminsight.metric.tracker import Tracker
from apminsight.constants import extract_info_str
from apminsight.instrumentation.util import create_tracker_info
from apminsight.context import is_no_active_txn, get_cur_tracker, set_cur_tracker,get_cur_txn


def wsgi_wrapper(original, module, method_info):
    def wrapper(*args, **kwargs):
        cur_txn = None 
        res = None
        agent = get_agent()
        try:
            wsgi_environ = args[1]
            tracker_info = create_tracker_info(module, method_info)
            cur_txn = agent.check_and_create_txn(wsgi_environ, tracker_info)
            res = original(*args, **kwargs)
            agent.end_txn(cur_txn, res)
        except Exception as exc:
            agent.end_txn(cur_txn, err=exc)
            raise exc
        finally:
            clear_cur_context()
                 
        return res

    return wrapper


def default_wrapper(original, module, method_info):
    def wrapper(*args, **kwargs):
        if is_no_active_txn():
            return original(*args, **kwargs)
       
        res = None 
        err = None
        agent = get_agent()
        parent_tracker = get_cur_tracker()
        tracker_info = create_tracker_info(module, method_info, parent_tracker)
        cur_tracker = agent.check_and_create_tracker(tracker_info)
        try:
            res = original(*args, **kwargs)
        except Exception as exc:
            err = exc
            raise exc
        finally:
            handle_tracker_end(cur_tracker, method_info, args, kwargs, res, err)
            set_cur_tracker(parent_tracker)

        return res

    # special handling for flask route decorator
    wrapper.__name__ = original.__name__
    return wrapper


def handle_tracker_end(tracker, method_info, args, kwargs, res, err):
    try:
        if isinstance(tracker, Tracker) is not True:
            return

        if type(method_info) is dict and extract_info_str in method_info:
            extractor = method_info[extract_info_str]
            extractor(tracker, args=args, kwargs=kwargs, return_value=res, error=err )

        tracker.end_tracker(err= err)
    except Exception:
        agentlogger.exception("While handling tracker end")


def copy_attributes(source, dest):
    try:
        for att in source.__dict__:
            setattr(dest, att, getattr(source, att))
        
    except Exception:
        agentlogger.exception('copying attribute')



def args_wrapper(original, module, method_info):
    def wrapper(*args, **kwargs): 
        if wrap_args_str in method_info:
            args_index = method_info[wrap_args_str]
            if isinstance(args, (list, tuple)) and len(args)> args_index and is_callable(args[args_index]):
                try:
                    act_method = args[args_index]
                    temp = list(args)
                    module_name = act_method.__module__
                    args_method_info = { 'method' : act_method.__name__ }
                    #Special case for flask where two different routes have same view function
                    view_wrapper = getattr(act_method, "apm_view_wrapper", None)
                    if view_wrapper is None:
                        view_wrapper = default_wrapper(act_method, module_name, args_method_info)
                        try:
                            setattr(act_method, "apm_view_wrapper", view_wrapper)
                        except AttributeError:
                            agentlogger.exception('in args_wrapper function')
                    copy_attributes(act_method, view_wrapper)
                    temp[args_index] = view_wrapper
                    args = temp
                except Exception:
                    agentlogger.exception('error in args wrapper')

        return original(*args, **kwargs)
    
    return wrapper

def add_custom_param(key, value):
    if is_no_active_txn():
        return
    
    if not (is_empty_string(key) or value in [None, '']):  
        agent = get_agent()
        if not type(value).__module__=='builtins':
            try:
                value = value.__dict__
            except TypeError:
                agentlogger.exception('while setting custom params, please provide a valied type as Value for custom params')
                return
            except:
                agentlogger.exception('while setting custom params')
        tracker_info = {'name':CUSTOMPARAMS +'(Key='+str(key)+', Value='+str(value), 'parent' : get_cur_tracker()}
        parent_tracker = get_cur_tracker()
        cur_tracker = agent.check_and_create_tracker(tracker_info)
        get_cur_txn().set_custom_params(key, value)        
        cur_tracker.end_tracker()
        set_cur_tracker(parent_tracker)
