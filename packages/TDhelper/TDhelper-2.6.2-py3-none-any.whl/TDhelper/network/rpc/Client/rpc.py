import logging
import json
import time
from TDhelper.network.http.REST_HTTP import GET
from TDhelper.generic.dynamic.base.Meta import dynamic_creator
from TDhelper.network.rpc.Core.struct import RPC_SERVICE
from TDhelper.Decorators.log import logging, logging_setup
from TDhelper.Decorators.performance import performance

performance.on_off(True)

class client():
    __TOKEN_KEY__ = "api-token"
    __TOKEN__ = ""
    __LOGGER__ = logging
    __service_exists__= lambda o,k: True if k in o.__dict__ else False
    __get_service__= lambda o,k: getattr(o,k) if o.__service_exists__(k) else None
    
    @performance.performance_testing
    def __init__(self, uri, path: list = [], token: str = "", sniffer: list = ["sniffer"], services: list = [], token_key=None, logger: dict = None, try_count:int=5, try_sleep:int=3)->None:
        '''rpc client.
        
        params:
        
            uri - <class: string>: rpc gateway;
            
            path - <class: list>: rpc init url path;
            
            token - <class: string>: it's no use;
            
            sniffer - <class: list>: rpc service sniffer path, get it with operator;
            
            services - <class: list>: get rpc service by service list, default all, default all; 
            
            token_key - <class: string>: key field  for rpc authorized. it is request headers field; validate in SAAS-CLI framework core.filter.access.py;
            
            logger - <class: dict>: logger configure dict;
            
            try_count - <class:int>: max count for service available sniffer, default 5;
            
            try_sleep -<class: int>: service available sniffer retry sleep time, default 3 second;
        '''
        if logger:
            self.__LOGGER__.basicConfig(level=logging.INFO)
            self.__LOGGER__.config.dictConfig(logger)
        self.__TOKEN_KEY__ = token_key if token_key else self.__TOKEN_KEY__
        self.__TOKEN__ = token
        header = {
            "access-source":"rpc"
        }
        if self.__TOKEN__:
            header.update({self.__TOKEN_KEY__:self.__TOKEN__})
        else:
            raise ValueError("not found access token.")
        uri = uri.rstrip("/")
        rpc_uri = uri+"/"+"/".join(path)
        if services:
            rpc_uri += "?key="+",".join(services)
        rpc_server_state = False
        for v in range(0, try_count):
            body = self.__get_conf__(uri+"/"+"/".join(sniffer), header)
            if body:
                if body['state'] == 200:
                    rpc_server_state = True
                    break
            time.sleep(try_sleep)
        if not rpc_server_state:
            raise Exception("can not connect rpc server(%s)." %
                            (uri+"/"+"/".join(sniffer)))
        self.__context__ = self.__get_conf__(rpc_uri, header)
        if self.__context__:
            if self.__context__["msg"]:
                self.__dict__["__srv_struct__"] = {}
                for k, v in self.__context__["msg"].items():
                    self.__dict__["__srv_struct__"][k] = type(
                        k, (RPC_SERVICE,), {}).create_by_cnf(v, self.__TOKEN_KEY__)
                    methods = [kv for kv in v['methods'].keys()]
                    self.__dict__[k] = type(k, (dynamic_creator,), {
                                            "__dynamic_methods__": methods, "__hook_method__": self.__call__})()
            else:
                self.__LOGGER__.error("not found rpc method.%s"%self.__context__["msg"])
                raise Exception("not found rpc method.%s"%self.__context__["msg"])
        else:
            raise Exception("not found rpc instance config.")
        super(client, self).__init__()

    @performance.performance_testing
    def __call__(self, service_name, fun_name, *args, **kwargs):
        remote_func_name = ("".join([service_name, '.', fun_name]))
        if service_name in self.__srv_struct__:
            if hasattr(self.__srv_struct__[service_name], 'methods'):
                if fun_name in self.__srv_struct__[service_name].methods:
                    try:
                        start = time.clock_gettime(0)
                        result = self.__srv_struct__[service_name].__remote_call__(
                            fun_name, *args, **kwargs)
                        end = time.clock_gettime(0)
                        self.__LOGGER__.info("call %s, time consuming %f(s)" % (
                            remote_func_name, (end-start)))
                        return result
                    except Exception as e:
                        self.__LOGGER__.error(e)
                else:
                    self.__LOGGER__.error(
                        "in service(%s) not found method(%s)", (service_name, fun_name))
            else:
                self.__LOGGER__.error("service obj not found key(methods).")
        else:
            self.__LOGGER__.error('not found service(%s).' % service_name)
        return {"state": -1, "msg": {}}

    def __get_conf__(self, uri, header={}):
        state, body = GET(uri, http_headers=header,
                          time_out=5, charset="utf-8")
        if state == 200:
            body = json.loads(body)
            if body["state"] == 200:
                return body
            else:
                return {}
        return {}
    
    def reload(self):
        pass
    
    def monitor(self,speed=None):
        '''
            start monitor service health.
            
            Args:
            
                speed: <cls,int>, monitor speed. seconds.
        '''
        if self.__srv_struct__:
            for o in self.__srv_struct__:
                self.__srv_struct__[o].monitor(speed)
                
    def stop_monitor(self):
        '''
            stop monitor service health.
        '''
        if self.__srv_struct__:
            for o in self.__srv_struct__:
                self.__srv_struct__[o].stop_monitor()