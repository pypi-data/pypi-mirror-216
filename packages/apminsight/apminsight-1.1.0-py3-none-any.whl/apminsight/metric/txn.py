
import os
import random
import string
from apminsight import constants
from apminsight.util import current_milli_time,is_empty_string
from apminsight.metric.tracker import Tracker
from apminsight.metric.dbtracker import DbTracker
from apminsight.agentfactory import get_agent
from apminsight.metric.component import Component
from apminsight.constants import webtxn_prefix

class Transaction:

    def __init__(self, wsgi_environ={}, root_tracker_info={}):
        self._url = wsgi_environ.get(constants.path_info_str, str())
        self._query = wsgi_environ.get(constants.query_string_str, str())
        self._request_method = wsgi_environ.get(constants.request_method_str, str())
        self._root_trakcer = Tracker(root_tracker_info)
        self._start_time = current_milli_time()
        self._end_time = None
        self._rt = 0
        self._completed = False
        self._status_code = 200
        self._exceptions_info = {}
        self._exceptions_count = 0
        self._external_comps = {}
        self._internal_comps = {}
        self._extcall_count = 0
        self._db_calls = []
        self._method_count = 1
        self._trace_id = ''.join(random.choices(string.ascii_letters+string.digits, k=32))
        self._custom_params = None
        self._cpu_start_time = int(round(os.times()[0] * 1000))
        self._cpu_end_time = None

    def end_txn(self, res=None, err=None):
        agent = get_agent()
        if agent.is_data_collection_allowed() is False:
            return

        self._root_trakcer.end_tracker(err)
        self._end_time = current_milli_time()
        if res is not None and hasattr(res, constants.status_code_str):
            self._status_code = res.status_code
        if err is not None:
            self._status_code = 500 
        self._rt = self._end_time-self._start_time
        self._completed = True
        self._cpu_end_time = int(round(os.times()[0] * 1000))
        if agent.get_config().is_using_exporter():
            agent.metric_dispatcher.push_to_dispatcher_queue(self)
            agent.metric_dispatcher.set_event()
        else:
            agent.push_to_queue(self)

    def handle_end_tracker(self, tracker):
        self.aggregate_component(tracker)
        self.check_and_add_db_call(tracker)
        self.check_and_add_error(tracker)


    def aggregate_component(self, tracker):
        if is_empty_string(tracker.get_component()):
            return

        component = Component(tracker)
        if component.is_ext():
            component.aggregate_to_global(self._external_comps)
            self._extcall_count += component.get_count() + component.get_error_count()
        else:
            component.aggregate_to_global(self._internal_comps)
         

    def check_and_add_db_call(self, db_tracker):
        if isinstance(db_tracker, DbTracker):
            self._db_calls.append(db_tracker)


    def check_and_add_error(self, tracker):
        if not tracker.is_error():
            return

        err_name = tracker.get_error_name()
        if is_empty_string(err_name):
            return

        err_count = self._exceptions_info.get(err_name, 0)
        self._exceptions_info[err_name] = err_count+1
        self._exceptions_count += 1 


    @staticmethod
    def comp_details_for_trace(allcompinfo):
        comp_details = {'success' : {}, 'fail' : {}}
        for eachcomp in allcompinfo.keys():
            compinfo = allcompinfo[eachcomp]
            if compinfo.get_name() in comp_details['success'].keys():
                comp_details['success'][compinfo.get_name()] += compinfo.get_count()
                comp_details['fail'][compinfo.get_name()] += compinfo.get_error_count()
            else:
                comp_details['success'][compinfo.get_name()] = compinfo.get_count()
                comp_details['fail'][compinfo.get_name()] = compinfo.get_error_count()


        return comp_details
        
    def add_trackers(self, tracker, method_info):
        tracker_data= tracker.add_tracker_data()
        method_info.append(tracker_data)
        for child_tracker in tracker.get_child_trackers():
            method_info = self.add_trackers(child_tracker, method_info)
        return method_info

    def get_trace_info(self):
        trace_info = {}
        trace_info['t_name'] = webtxn_prefix + self.get_url()
        trace_info['http_method_name'] = self.get_method()
        trace_info['s_time'] = self.get_start_time()
        trace_info['r_time'] = self.get_rt()
        trace_info['http_query_str'] = self.get_query_param()
        trace_info['trace_reason'] = 4
        trace_info['db_opn'] = []
        trace_info['loginfo'] = []
        trace_info['method_count'] = self.get_method_count()
        trace_info['dt_count'] = 0 
        trace_info['ext_components'] = Transaction.comp_details_for_trace(self._external_comps)
        trace_info['int_components'] = Transaction.comp_details_for_trace(self._internal_comps)
        if self.get_status_code() is not None:
            trace_info['httpcode'] = self.get_status_code()

        return trace_info

    def get_trace_data(self):
        trace_info = self.get_trace_info()
        trace_data = self._root_trakcer.get_tracker_data_for_trace(trace_info)
        return [trace_info, trace_data]

    def get_status_code(self):
        return self._status_code

    def set_status_code(self, code):
        if isinstance(code, int):
            self._status_code = code
            
    def get_method_count(self):
        return self._method_count

    def increment_method_count(self, count):
        if isinstance(count, int):
            self._method_count+=count
            
    def get_root_tracker(self):
        return self._root_trakcer

    def get_url(self):
        return self._url

    def get_method(self):
        return self._request_method

    def get_rt(self):
        return self._rt
    
    def set_rt(self, rt):
        if isinstance(rt, int):
            self._rt = rt

    def get_start_time(self):
        return self._start_time

    def get_end_time(self):
        return self._end_time
    
    def get_query_param(self):
        return self._query

    def get_exceptions_info(self):
        return self._exceptions_info

    def get_exceptions_count(self):
        return self._exceptions_count

    def set_exceptions_count(self, count):
        if isinstance(count, int):
            self._exceptions_count = count
            
    def get_status_code(self):
        return self._status_code

    def clear_db_calls(self):
        self._db_calls = []

    def get_db_calls(self):
        return self._db_calls
    
    def update_db_calls(self, db_calls):
        if isinstance(db_calls, list):
            self._db_calls+=db_calls

    def get_internal_comps(self):
        return self._internal_comps

    def get_external_comps(self):
        return self._external_comps

    def get_ext_call_count(self):
        return self._extcall_count

    def is_completed(self):
        return self._completed

    def get_trace_id(self):
        return self._trace_id
    
    def get_cpu_time(self):
        if self._cpu_end_time:
            return self._cpu_end_time - self._cpu_start_time
        else :
            return None
    
    def is_error_txn(self):
        if isinstance(self._status_code, int) and self._status_code >= 400:
            return True
        
        return self._root_trakcer.is_error()

    def set_custom_params(self, key, value):
        
        if self._custom_params is None:
            self._custom_params = {key:[value]}
        elif len(self._custom_params)>10:
            return
        elif self._custom_params.get(key):
            if len(self._custom_params[key])<10:
                self._custom_params[key].append(value)
        else:
            self._custom_params[key] = [value]
      
    def get_custom_params(self):
        return self._custom_params
        
    def aggregate_trackers(self, tracker):
        for child_tracker in tracker.get_child_trackers():
            self.aggregate_trackers(child_tracker)
        self.handle_end_tracker(tracker)
