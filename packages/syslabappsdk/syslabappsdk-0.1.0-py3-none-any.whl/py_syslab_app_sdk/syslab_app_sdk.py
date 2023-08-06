#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import logging
import random
import json
from . import connect_client
from . import variable_info

RPC_RUNCODE = "repl/runcode"
RPC_GETVALUE = "repl/getvalue"
RPC_GETVARIABLES = "repl/getvariables"
RPC_CLOSEAPP = "repl/closeapp"

# 获取的工作区变量信息列表
list_variable_info = []

# 获取的工作区变量值
str_variable_value = ""

def make_dir_if_not_exist(dir):
    if not os.path.exists(dir):
        os.mkdir(dir)

def init_log():
    log_dir = os.path.join(os.getcwd(), 'log')
    make_dir_if_not_exist(log_dir)
    logging.basicConfig(filename=log_dir + os.path.sep + 'log_file.log',
                        format='%(asctime)s - %(name)s - %(levelname)s -%(module)s:  %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S %p',
                        level=logging.INFO)

class SyslabAppSdk():
    def __init__(self, app_name, pipe_name):
        self.__app_name = app_name
        self.__pipe_name = pipe_name

        init_log()
        
        try:
            conn_client = connect_client.ConnectClient(self.__pipe_name)
            self.__conn = conn_client.client()
        except ConnectionRefusedError as e:
            logging.info("Could not open pipe.")
            self.__conn = None

    def _generate_uuid_v4(self):
            hex_digits = ""
            for i in range(8):
                hex_digits += '{0:x}'.format(random.randint(0, 15))
            hex_digits += "-"
            for i in range(4):
                hex_digits += '{0:x}'.format(random.randint(0, 15))
            hex_digits += "-4"
            for i in range(3):
                hex_digits += '{0:x}'.format(random.randint(0, 15))
            hex_digits += "-{0:x}".format(random.randint(8, 11))
            for i in range(3):
                hex_digits += '{0:x}'.format(random.randint(0, 15))
            hex_digits += "-"
            for i in range(12):
                hex_digits += '{0:x}'.format(random.randint(0, 15))
            return hex_digits

    def _gen_request_text(self, method, params, req_id):
        request_json = f'{{"method": "{method}", "id": "{req_id}", "params": {params}, "jsonrpc": "2.0"}}'
        request = f'Content-Length: {len(request_json)}\r\n\r\n{request_json}'
        return request

    def _send_request(self, request):
        if self.__conn == None:
            return False
        return self.__conn.send_bytes(request.encode("utf-8"))

    def _consume_respond_msg(self):
        respond = ""
        respond_length = 0
        while True:
            temp_respond = self.__conn.recv_bytes()
            temp_respond = temp_respond.decode("utf-8")
            if temp_respond.find("Content-Length: ") == 0:
                cl_str = "Content-Length: "
                rn_place = temp_respond.find("\r\n")
                sub_str = temp_respond[len(cl_str):rn_place]
                respond_length = int(sub_str) + 4 + rn_place
            respond += temp_respond
            if len(respond) >= respond_length:
                return respond

    def _unpack_json_get_variables(self, text, request_id):
        start_pos = text.find('{')
        if start_pos == -1:
            return False

        json_text = text[start_pos:]
        doc = json.loads(json_text)

        if 'id' not in doc:
            return False
        if doc['id'] != request_id:
            return False
        if 'result' not in doc:
            return False

        result = doc['result']
        if isinstance(result, list):
            list_variable_info.clear()
            for var_info in result:
                temp_type = var_info['type']
                if temp_type and str(temp_type) != 'Nothing':
                    var_name = var_info['head']
                    var_type = var_info['type']
                    var = variable_info.VariableInfo(var_name, var_type)
                    list_variable_info.append(var)
        return list_variable_info
    
    def _unpack_json_get_value(self, text, var_name, request_id):
        logging.info("_unpack_json_get_value:function begin.")
        key = "\"value\":"
        first = text.find(key) + len(key)
        last = text.find('}', first)
        value = text[first:last]
        logging.info("_unpack_json_get_value:complete function.")
        return value
 
    def mw_get_variables(self, show_modules):
        """获取 Syslab 工作区变量列表.

        发送请求, 获取 Syslab 工作区变量列表.

        参数:
            show_modules: 是否显示模块列表, 一般为False.

        返回:
            成功时返回变量列表, 失败时返回False. 
        """
        uuid = self._generate_uuid_v4()
        req_id = self.__app_name + "-" + uuid
        params = '{"modules":' + ('true' if show_modules else 'false') + '}'
        result = self._send_request(self._gen_request_text(RPC_GETVARIABLES, params, req_id))

        if result is not None:
            logging.info("mw_get_variables failure!")
            return False
        respond = self._consume_respond_msg()

        return self._unpack_json_get_variables(respond, req_id)

    def mw_get_value(self, var_name):
        """获取 Syslab 工作区变量值.

        发送请求, 获取 Syslab 工作区变量值.

        参数:
            var_name: 变量名, 可以为子变量a.b.

        返回:
            成功时返回变量值, 失败时返回False. 
        """
        uuid = self._generate_uuid_v4()
        req_id = self.__app_name + "-" + uuid
        logging.info("mw_get_value:begin send request.")
        params = '{\"var\":\"%s\"}' % str(var_name)
        result = self._send_request(self._gen_request_text(RPC_GETVALUE, params, req_id))
        if result is not None:
            logging.info("mw_get_value failure!")
            return False
        logging.info("mw_get_value:begin send complete.")

        logging.info("mw_get_value:begin get respond.")
        respond = self._consume_respond_msg()
        return self._unpack_json_get_value(respond, var_name, req_id)

    def mw_run_script(self, code, show_code_in_repl, show_result_in_repl):
        """在 Syslab 工作区执行 Julia 脚本代码.

        发送请求, 在 Syslab 工作区执行 Julia 脚本代码.

        参数:
            code: 要运行的 Julia 脚本.
            show_code_in_repl: 是否在 Syslab REPL 中显示代码.
            show_result_in_repl: 是否在 Syslab REPL 中显示结果.

        返回:
            成功时返回脚本运行后的JSON格式的字符串结果, 失败时返回False. 
        """
        str_show_code_in_repl = 'true' if show_code_in_repl else 'false'
        str_show_result_in_repl = 'true' if show_result_in_repl else 'false'
        params = '{"softscope":false, "line":0, "column":0, "mod":"Main", "showCodeInREPL":%s, "showResultInREPL":%s, "showErrorInREPL":true, "filename":"", "code":"%s"}' % (
            str_show_code_in_repl, str_show_result_in_repl, code)

        uuid = self._generate_uuid_v4()
        req_id = self.__app_name + "-" + uuid
        result = self._send_request(self._gen_request_text(RPC_RUNCODE, params, req_id))
        if result is not None:
            logging.info("mw_run_script failure!")
            return False

        return self._consume_respond_msg()

    def close_pipe(self):
        """关闭命名管道.

        发送请求, 关闭命名管道.
        """
        if self.__conn:
            notice_json = f'{{"method": "{RPC_CLOSEAPP}", "params": "null", "jsonrpc": "2.0"}}'
            notice = f'Content-Length: {len(notice_json)}\r\n\r\n{notice_json}'
            self._send_request(notice)
            self.__conn.close()