
import os
import json
import time
import threading
import requests

from .instrumentation import check_and_instrument,module_info


__version__ = "1.0.0"

name = "site24x7_openai_observability"

site24x7_apikey = os.getenv("SITE24X7_LICENSE_KEY", None)
payload_print = os.getenv("SITE24X7_PRINT_PAYLOAD","false").lower in ("true","on","yes","1")

COLLECTOR_HOSTS ={"us":"plusinsight.site24x7.com",
                 "eu":"plusinsight.site24x7.eu",
                 "cn":"plusinsight.site24x7.cn",
                 "in":"plusinsight.site24x7.in",
                 "au":"plusinsight.site24x7.net.au",
                 "jp":"plusinsight.site24x7.jp",
                 "aa":"plusinsight.localsite24x7.com"
                 }
COLLECTOR_PORT = os.getenv("APM_OPENAI_COLLECTOR_PORT","443")

REQUEST_PATH = "/airh/usage"
DEFAULT_SAMPLING = 10

check_and_instrument(module_info)

class OpenaAICallTracker():
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls, *args, **kwargs):
        if not isinstance(cls._instance, cls):
            cls._instance = object.__new__(cls)
        return cls._instance
    
    def __init__(self):
        self.appkey = os.getenv("SITE24X7_LICENSE_KEY",None)
        self.endpoint = self.construct_endpoint_url()
        self.request_queue = []
        self.thread_interval = os.getenv("SITE24X7_POLLING_INTERVAL",30) #seconds
        self.task_sheduled = False
        self.stop_thread = False
        self.flush_data()
        self.schedule_background_task()
        self.openai_call_count = 0
        self.capture_openai_text = os.getenv("SITE24X7_CAPTURE_OPENAI_TEXT","true").lower in ("true","on","yes","1")
        self.sampling_factor = self.set_sampling_factor()
     
    def increment_call(self):
        with self._lock:
            self.openai_call_count += 1

    def get_count(self):
        with self._lock:
            return self.openai_call_count
        
    def reset_sampling(self):
        with self._lock:
            self.openai_call_count = 0

    def set_sampling_factor(self,value = DEFAULT_SAMPLING):
        try:
            env_value = os.getenv("SITE24X7_SAMPLING_FACTOR")
            if env_value is not None:
                return int(env_value)
        except (ValueError, TypeError):
            pass
        return value

    def set_config(self,config={}):
        self.appkey = config.get("appkey",site24x7_apikey)
        self.sampling_factor = self.set_sampling_factor(config.get("sampling_factor",DEFAULT_SAMPLING))
        collector_url = config.get("collector_url",None)
        self.capture_openai_text = config.get("capture_openai_text",os.getenv("SITE24X7_CAPTURE_OPENAI_TEXT","true").lower in ("true","on","yes","1"))
        self.endpoint = self.construct_endpoint_url(collector_url)

    def _get_host(self):
        if self.appkey:
            host = os.getenv("SITE24X7_APM_HOST",None)
            data_center = self.appkey[:2]
            return host if host and len(host) else COLLECTOR_HOSTS.get(data_center,"")
        return None
    
    def _get_port(self):
        port = os.getenv("SITE24X7_APM_PORT","")
        if isinstance(port, str) and len(port):
            return port
        return COLLECTOR_PORT
        
    def construct_endpoint_url(self, collector_url=None):
        endpoint_url = os.getenv("APM_OPEANI_COLLECTOR_URL", collector_url)
        if self.appkey is not None and endpoint_url is None:
            host = self._get_host()
            port = self._get_port()
            return  host + ':' + port
        return endpoint_url
    
    def record_message(self):
        count = self.get_count()
        return True if self.capture_openai_text and count%self.sampling_factor == 0 else False

    def record_request(self, info):
        with OpenaAICallTracker._lock:
            if self.appkey:
                self.request_queue.append(info)
                
    def flush_data(self):
        if 'request_queue' in self.__dict__:
            with self._lock:
                data = self.request_queue
                self.request_queue = []
            return data
        return []
    
    def stop(self):
        self.stop_thread = True
        if self.task_sheduled:
            self._task.join()
    
    def push_data(self):
        while True:
            try:
                self.reset_sampling()
                data = self.flush_data()
                if len(data) and self.appkey is not None and self.endpoint is not None:
                    url = 'https://' + self.endpoint+ REQUEST_PATH
                    query_param = 'license.key='+ self.appkey
                    complete_url = url + '?' + query_param
                    response = requests.post(complete_url, data = json.dumps(data))
            except Exception as exc:
                print('Error while sending OpenAI data to APM collector'+ str(exc))
            finally:
                time.sleep(self.thread_interval)
    
    def schedule_background_task(self):
        try:
            if self.task_sheduled is True:
                return
            
            import threading
            self._task = threading.Thread(target=self.push_data, args=(), kwargs={})
            self._task.setDaemon(True)
            self._task.start()
            self.task_sheduled = True

        except Exception as exc:
            print('Error while scheduleing task for openai collector',exc)


openai_tracker = OpenaAICallTracker()

'''
    config = {
        "appkey" : "site24x7 license key",
        "sampling_factor : Value #default=10

    }
'''
def initalize(appkey=None, capture_openai_text=True, sampling_factor=10, collector_url = None):
    config = {
        "appkey":appkey,
        "capture_openai_text": capture_openai_text,
        "sampling_factor": sampling_factor,
        "collector_url" : collector_url
    } 
    openai_tracker.set_config(config)

