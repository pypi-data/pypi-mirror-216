from apminsight import constants
from apminsight.logger import agentlogger

def extract_req(tracker, args=(), kwargs={}, return_value=None, error=None):
    try:
        if args:
            request = args[1]
            method = request.method
            url = request.url
            url_str = str(url)
            host = url.host
            port = url.port
            status = ''
            if return_value:
                status = str(return_value.status_code)
            if status:
                tracker.set_tracker_name( tracker.get_tracker_name() + " : " + method + ' - ' + status + ' - ' + url_str)
                tracker.set_as_http_err() if int(status) >= 400 else 0
            else:
                tracker.set_tracker_name( tracker.get_tracker_name() + " : " + method + ' - ' + url_str)
            info = {constants.HTTP_METHOD: method, constants.HTTP: host, constants.PORT: port, constants.URL: url_str, constants.STATUS: status}
            tracker.set_info(info)

    except Exception as exc:
        agentlogger.exception("while extracting HTTPX request")

module_info = {
    'httpx._client' : [
        {   constants.class_str : 'Client',
            constants.method_str : 'send',
            constants.component_str : constants.http_comp,
            constants.extract_info_str : extract_req,
        },
    ],
}
