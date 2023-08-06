
import copy
from apminsight.collector.connhandler import init_connection
from apminsight.metric.txn import Transaction
from apminsight.metric.tracker import Tracker
from apminsight.metric.dbtracker import DbTracker
from apminsight.metric.metricstore import Metricstore
from apminsight.config.configuration import Configuration
from apminsight.collector.ins_info import Instanceinfo
from apminsight.config.threshold import Threshold
from apminsight import context
from apminsight import constants
from apminsight.logger import agentlogger
from apminsight.util import check_and_create_base_dir
from apminsight import agentfactory
from apminsight.context import get_cur_txn
from apminsight.collector.metric_dispatcher import MetricDispatcher
from apminsight.collector.rescodes import res_codes_info


def initalize(options={}):
    options['agentbasedir'] = check_and_create_base_dir()
    agentfactory.agent_instance = Agent(options)
    agent_instance = agentfactory.agent_instance
    if not agent_instance.get_config().is_using_exporter():
        if not agent_instance.get_config().is_configured_properly():
            raise RuntimeError('Configure license key properly')
        init_connection()
    return agent_instance

class Agent:
    def __init__(self, info):
        self.config = Configuration(info)
        self.ins_info = Instanceinfo(info)
        self.threshold = Threshold()
        self.metricstore = Metricstore() if not self.config.is_using_exporter() else None
        self.txn_queue = [] if not self.config.is_using_exporter() else None
        self.metric_dispatcher = MetricDispatcher(self.config) if self.config.is_using_exporter() else None
        
    def update_app_port(self, app_port):
        self.config.set_app_port(app_port)
        self.metric_dispatcher.update_app_port(app_port)
        
    def push_to_queue(self, txn):
        self.txn_queue.append(txn)

    def get_txn_queue_for_metrics_processing(self):
        txn_list = copy.copy(self.txn_queue)
        self.txn_queue = []
        return txn_list

    def is_data_collection_allowed(self):
        cur_status = self.ins_info.get_status()
        if cur_status in [constants.manage_agent, constants.agent_config_updated]:
            return True
        
        return False

    def check_and_create_txn(self, wsgi_environ, root_tracker_info):
        try:
            if not self.get_config().app_port_set():
                if not wsgi_environ.get(constants.server_port_str).isnumeric():
                    agentlogger.info('Auto detection of port failed due to absense of SERVER PORT details in environ')
                    return
                self.update_app_port(wsgi_environ[constants.server_port_str])
                    
            if self.get_config().is_using_exporter():
                self.metric_dispatcher.update_threshold_config(wsgi_environ)
                if not self.metric_dispatcher.started():
                    self.metric_dispatcher.start_dispatching()

            context.clear_cur_context()
            if not self.is_data_collection_allowed():
                if not self.get_ins_info().get_status():
                    agentlogger.info('data collection stopped due to no response code')
                else:
                    agentlogger.info('data collection stopped due to response code %s %s', str(self.get_ins_info().get_status()), res_codes_info.get(self.get_ins_info().get_status()).get('name'))
                return

            if type(wsgi_environ) is not dict:
                return

            if type(root_tracker_info) is not dict:
                return

            uri = wsgi_environ.get(constants.path_info_str, '')
            if not self.threshold.is_txn_allowed(uri):
                agentlogger.info(uri + ' txn skipped')
                return

            txn = Transaction(wsgi_environ, root_tracker_info)
            context.ser_cur_context(txn, txn.get_root_tracker())
            # handle cross app response
            return txn
        except Exception:
            agentlogger.exception("while creating txn obj")
        return Transaction(wsgi_environ, root_tracker_info)

    def check_and_create_tracker(self, tracker_info):
        track = None
        cur_txn = get_cur_txn()
        try:
            if type(tracker_info) is not dict:
                return None

            if context.is_txn_active() is not True:
                return None

            if 'parent' not in tracker_info:
                tracker_info['parent'] = context.get_cur_tracker()

            if constants.is_db_tracker_str in tracker_info:
                track = DbTracker(tracker_info)
            else:
                track = Tracker(tracker_info)

            cur_txn.increment_method_count(1)

            context.set_cur_tracker(track)
        except:
            agentlogger.exception("While creating Tracker")
        
        return track

    
    def end_txn(self, txn, res=None, err=None):
        try:
            if txn is None:
                return

            if isinstance(txn, Transaction):
                txn.end_txn(res, err)
        except Exception:
            agentlogger.exception("tracking end txn")


    def end_tracker(self, tracker, err=None):
        if isinstance(tracker, Tracker) is not True:
            return

        txn=context.get_cur_txn()
        if isinstance(txn, Transaction):
            tracker.end_tracker(err)
            cur_txn = context.get_cur_txn()
            cur_txn.handle_end_tracker(tracker)


    def get_config(self):
        return self.config

    def get_threshold(self):
        return self.threshold

    def get_ins_info(self):
        return self.ins_info

    def get_metric_store(self):
        for txn in self.get_txn_queue_for_metrics_processing():
            self.metricstore.add_web_txn(txn)
        return self.metricstore
    
