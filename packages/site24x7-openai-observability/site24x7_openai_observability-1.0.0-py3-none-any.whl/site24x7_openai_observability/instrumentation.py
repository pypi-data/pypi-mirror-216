import time
import platform
from importlib import import_module 

def check_module():
    global apm_module_status
    if apm_module_status is not None:
        return apm_module_status
    try:
        module_status = import_module("apminsight")
        if module_status is not None:
            apm_module_status = True
    except Exception as exc:
        # print("Failed to load apminsight module",str(exc))
        apm_module_status = False
    return apm_module_status

apm_module_status = None
check_module()

def get_message(return_value):
    if return_value :
        if "text" in return_value['choices'][0]:
            return return_value['choices'][0]['text']
        elif "message" in return_value['choices'][0]:
            return return_value['choices'][0]['message']['content']
    return ""

def get_prompt(kwargs):
    if "prompt" in kwargs:
        return kwargs['prompt']
    elif "messages" in kwargs:
        return kwargs['messages'][-1]['content']
         

def get_system_message(kwargs):
    content = ""
    if "messages" in kwargs:
        for messages in kwargs['messages']:
            if messages.role == 'system':
                content.appned(messages.content)
    
    return content

def get_error_details(err):
    if err :
        try:
            import openai 
            if isinstance(err,openai.error.OpenAIError):
                return {"error":err._message, "response_code": err.http_status}
        except Exception:
            pass
        return {"error":str(err),"response_code":500}
    else:
        return {"error":"-","response_code":200}
    
def get_openai_key():
    import openai
    try:
        api_key = openai.api_key or openai.util.default_api_key()
        if api_key :
            return api_key[:3]+"..."+api_key[-4:]
    except :
        pass
    return None

def extract_info(tracker, args=(), kwargs={}, return_value=None, error=None,starttime=None):
    try:  
        from site24x7_openai_observability import openai_tracker, payload_print
        api_info = ({'starttime':starttime, #tracker.get_start_time(),
                        'model': kwargs.get('model',kwargs.get('engine',"")),
                        'requesttime':int(round(time.time() * 1000))-starttime,#tracker.get_start_time(),
                        'total_token':return_value.usage.total_tokens if return_value else 0,
                        "prompt_token":return_value.usage.prompt_tokens if return_value else 0,
                        "response_token":return_value.usage.completion_tokens if return_value else 0,
                        'api_key':get_openai_key(),
                        'host':platform.node()
                        })
        
        api_info.update(get_error_details(error))
        
        if openai_tracker.record_message():
            api_info.update({
                'prompt': get_prompt(kwargs),
                #"system_content":get_system_message(kwargs),
                'message': get_message(return_value), 
            })
        # if tracker:
        #     api_info.update({'spanid':tracker.get_span_id()
        #                     #,'traceid':tracker.get_trace_id()
        #                     })
        if payload_print:
            print("openai call info",api_info)
        openai_tracker.increment_call()                 
        openai_tracker.record_request(api_info) 
    except Exception as exc:
        print("Exception in openai instumentation",str(exc))


def create_apm_tracker(module, method_info):
    try:
        if apm_module_status:
            from apminsight import get_agent
            from apminsight.context import get_cur_tracker
            from apminsight.instrumentation.util import create_tracker_info
            
            parent_tracker = get_cur_tracker()
            if parent_tracker:
                agent = get_agent()
                tracker_info = create_tracker_info(module, method_info, parent_tracker)
                return agent.check_and_create_tracker(tracker_info)
    except Exception as exc:
        pass
    return None

def close_apm_tracker(tracker, method_info,args,kwargs,res,err,starttime):
    if apm_module_status and tracker :
        from apminsight.context import set_cur_tracker
        from apminsight.instrumentation.wrapper import handle_tracker_end
        handle_tracker_end(tracker, method_info, args, kwargs, res, err)
        set_cur_tracker(tracker.get_parent())

def default_openai_wrapper(original, module, method_info):
    def wrapper(*args, **kwargs):
        res = None 
        err = None
        try:
            cur_tracker = create_apm_tracker(module, method_info)
            starttime = int(round(time.time() * 1000))
            res = original(*args, **kwargs)
        except Exception as exc:
            err = exc
            raise exc
        finally:
            close_apm_tracker(cur_tracker, method_info,args,kwargs,res,err,starttime)
            extract_info(cur_tracker,args,kwargs,res,err,starttime) 
        return res

    wrapper.__name__ = original.__name__
    return wrapper

def check_and_instrument(module_info):
    for module_name in module_info:
        try:
            act_module = import_module(module_name)
            if hasattr(act_module, 'apminsight_instrumented'):
                return 
            for method_info in module_info.get(module_name):
                instrument_method(module_name, act_module, method_info)
                setattr(act_module, 'apminsight_instrumented', True)
        except Exception:
            print(module_name + " not presnt")
            #agentlogger.info(each_mod +' is not present')

def instrument_method(module_name, act_module, method_info):
    parent_ref = act_module
    class_name = ''

    if type(method_info) is not dict:
        return
    
    if "class" in method_info:
        class_name = method_info.get("class")
        if hasattr(act_module, class_name):
            parent_ref = getattr(act_module, class_name)
            module_name = module_name+'.'+class_name
            

    method_name = method_info.get("method", '')
    if hasattr(parent_ref, method_name):
        original = getattr(parent_ref, method_name)
        # use default wrapper if there is no wrapper attribute
        wrapper_factory = method_info.get("wrapper") if "wrapper" in method_info else default_openai_wrapper
        wrapper = wrapper_factory(original, module_name, method_info)
        setattr(parent_ref,  method_name, wrapper)

module_info = {
    'openai.api_resources.completion' : [
        {
            "class" : 'Completion',
            "method" : 'create',
            "component" : "OPENAI",
            "wrapper" : default_openai_wrapper,
        }
    ],
    'openai.api_resources.chat_completion' : [
        {     
            "class" : 'ChatCompletion',
            "method" : 'create',
            "component" : "OPENAI",
            "wrapper" : default_openai_wrapper,
        }
    ],
}
