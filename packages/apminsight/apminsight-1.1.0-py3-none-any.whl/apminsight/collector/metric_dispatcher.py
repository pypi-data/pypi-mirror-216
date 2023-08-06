import json
import random
import string
import socket
import threading
import platform
from queue import Queue
from apminsight import constants
from apminsight import get_agent
from apminsight.logger import agentlogger
from apminsight.util import current_milli_time, is_non_empty_string, convert_tobase64, remove_null_keys


class MetricDispatcher():
    def __init__(self, config):   
        self.__dispatcher_queue = Queue()
        self.__started = False
        self.__agent_last_communicated = None
        self.__event = threading.Event()
        self.__agent_threshold_config = None
        self.__connection_payload = self.create_connection_payload(config)
        
    def push_to_dispatcher_queue(self, txn):
        self.__dispatcher_queue.put(txn)
    
    def started(self):
        return self.__started
    
    def set_event(self):
        self.__event.set()
        
    def clear_event(self):
        self.__event.clear()
        
    def get_agent_last_communicated(self):
        return self.__agent_last_communicated
        
    def update_app_port(self, app_port):
        if get_agent().get_config().is_using_exporter():
            self.__connection_payload['connect_info']['agent_info']['port'] = int(app_port)
        else:
            self.__connection_payload['agent_info']['port'] = int(app_port)
            
    def get_connection_payload(self, wsgi_environ=None):
        conn_payload = self.__connection_payload
        if wsgi_environ is not None:
            txn_name = wsgi_environ.get(constants.path_info_str, '')
            conn_payload["misc_info"]["txn.name"] = txn_name
        if get_agent().get_config().is_using_exporter():
            conn_payload = json.dumps(conn_payload)
            conn_payload+="\n"
        return conn_payload
    
    def start_dispatching(self):
        try:
            if self.__started is True:
                return
            metric_dispatcher_thread = threading.Thread(target=self.background_task, args=(60,), kwargs={})
            metric_dispatcher_thread.setDaemon(True)
            metric_dispatcher_thread.start()
            self.__started = True
        except Exception :
            agentlogger.exception('Error while starting background task')

    def background_task(self, timeout):
        while True:
            try:   
                if not self.__dispatcher_queue.empty():
                    txn = self.__dispatcher_queue.get(block = False)
                    self.send_txn_data(txn)
                else:
                    event_set = self.__event.wait(timeout)
                    if event_set:
                        continue
                    else:
                        self.get_connection_payload()
            except:
                agentlogger.exception('in background task')
        
    def send_txn_data(self, txn):
        if txn:
            config = get_agent().get_config()
            try:
                json_to_exporter = self.create_json_to_send(txn)
                HOST = config.get_exporter_host()  # The server's hostname or IP address
                PORT = int(config.get_exporter_data_port())  # The port used by the server
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.connect((HOST, PORT))
                    s.sendall(bytes(json_to_exporter, encoding="utf-8"))
                    s.close()
                    self.__agent_last_communicated = current_milli_time()
                    self.__event.clear()
                    agentlogger.info("Successfully sent transaction data to S247DataExporter")
            except ConnectionRefusedError:
                agentlogger.info('Error while sending transaction data to S247DataExporter, please check if the exporter is running')
            except:
                agentlogger.exception('while sending transaction data')

    def send_connect_data(self, payload):
        try:
            config = get_agent().get_config()
            HOST = config.get_exporter_host()  # The server's hostname or IP address
            PORT = int(config.get_exporter_status_port())  # The port used by the server
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((HOST, PORT))
                s.sendall(bytes(payload, encoding="utf-8"))
                data = s.recv(1024)
                s.close()
                self.__agent_last_communicated = current_milli_time()
            return data
        except ConnectionRefusedError:
            agentlogger.info('Error while Connecting to S247DataExporter, please check if the exporter is running')
        except:
            agentlogger.exception('while getting transaction data')
    
    def update_threshold_config(self, wsgi_environ=None):
        try:
            agent = get_agent()
            payload_to_exporter = self.get_connection_payload(wsgi_environ)
            response = self.send_connect_data(payload_to_exporter)
            if response:
                response = json.loads(response.decode("utf-8"))
                agent.get_threshold().update_sql_trace_threshold(response.get("transaction.trace.sql.stacktrace.threshold"))
                agent_threshold_config = {key:val for key, val in response.items() if not 'transaction' in key}
                if agent_threshold_config != self.__agent_threshold_config:
                    agent.get_ins_info().set_status(response.get("instance.status"))
                    agent.get_ins_info().set_instanceid(response.get("instance.id"))
                    agent.get_config().set_license_key(response.get('license.key', ''))    
                    agent.get_ins_info().write_conf_info(self.get_info_for_conf_file(agent_threshold_config))
                    self.__agent_threshold_config = agent_threshold_config
                agentlogger.info("Recieved the instance and threshold info from S247DataExporter successfully")
            else:
                agentlogger.info("No response from S247DataExporter")
        except:
            agentlogger.exception("while getting instance and threshold info from S247DataExporter")
    
    def get_info_for_conf_file(self, response):
        if response:
            response.pop('license.key')
            info_for_conf_file = {
                constants.SETUP_CONFIG: get_agent().get_config().get_user_setup_config(),
                constants.THRESHOLD_CONFIG : response
            }
            return info_for_conf_file
        return response
    
    def create_connection_payload(self, config):
        conn_payload = {
                "agent_info" : { 
                "application.type": constants.python_str, 
                "agent.version": config.get_agent_version(), 
                "application.name": config.get_app_name(), 
                "port": config.get_app_port(), 
                "host.type": config.get_host_type(),
                "hostname": config.get_host_name(),
                "fqdn" : config.get_fqdn()
            }, "environment" : { 
                #"UserName": process.env.USER, 
                "OSVersion": platform.release(), 
                "MachineName": platform.node(), 
                'AgentInstallPath': config.get_installed_dir(), 
                "Python version": platform.python_version(), 
                "OSArch": platform.machine(), 
                "OS": platform.system(),
                "Python implementation" : platform.python_implementation()
            }
        }
        if config.is_using_exporter():
            conn_payload = { 
            "connect_info" : conn_payload,
            "misc_info" : {}
        }
        
        return conn_payload
    
    def create_json_to_send(self, txn):
        transaction_info = {}
        method_info = []
        from apminsight import get_agent
        config = get_agent().get_config()
        transaction_info[constants.exporter_param_key_http_host] = config.get_host_name()
        transaction_info[constants.exporter_param_key_request_url] = txn.get_url()
        transaction_info[constants.exporter_param_key_query_string] = txn.get_query_param()
        transaction_info[constants.exporter_param_key_transaction_duration] = txn.get_rt()
        transaction_info[constants.exporter_param_key_request_method] = txn.get_method()
        transaction_info[constants.exporter_param_key_bytes_in] = None
        transaction_info[constants.exporter_param_key_bytes_out] = None
        transaction_info[constants.exporter_param_key_transaction_type] = 1      #1 for WEB txn/ 0 for BG txn
        transaction_info[constants.exporter_param_key_distributed_count] = 0 #Distributed trace count
        transaction_info[constants.exporter_param_key_thread_id] = None
        transaction_info[constants.exporter_param_key_response_code] = txn.get_status_code()
        transaction_info[constants.exporter_param_key_collection_time] = txn.get_start_time()
        transaction_info[constants.exporter_param_key_collection_end_time] = txn.get_end_time()
        transaction_info[constants.exporter_param_key_cpu_time] = txn.get_cpu_time()
        transaction_info[constants.exporter_param_key_memory_usage] = None
        transaction_info[constants.exporter_param_key_trace_id] = ''.join(random.choices(string.ascii_letters, k=7)) #sending a random string for now
        transaction_info[constants.exporter_param_key_custom_params] = None
        transaction_info[constants.exporter_param_key_trace_id] = txn.get_trace_id()
        remove_null_keys(transaction_info)
        method_info =  txn.add_trackers(txn.get_root_tracker(), method_info)
        json_to_exporter = {
                            "apm" : {constants.data_str : True,
                                    "application_info": {	
                                                        constants.exporter_param_key_application_type : constants.python_comp,
                                                        constants.exporter_param_key_application_name : get_agent().get_config().get_app_name(),
                                                        constants.exporter_param_key_instance_id : get_agent().get_ins_info().get_instance_id(),
                                                        },
                                    constants.transaction_info_str : transaction_info,
                                    constants.method_info_str : {"span_info": method_info}
                                    }
                            }
        json_to_exporter = convert_tobase64(json.dumps(json_to_exporter))
        if is_non_empty_string(json_to_exporter):
            json_to_exporter+="\n"
        return json_to_exporter
    
