#!/usr/bin/python
# -*- coding: utf-8 -*-

# using Windows named pipes
# Copyright © 2001-2023 Python Software Foundation; All Rights Reserved

import multiprocessing.connection as mc
from multiprocessing import util
import sys
import socket
import time

try:
    import _winapi
except ImportError:
    _winapi = None

class ConnectClient:
    def __init__(self, address):
        self.__address = address

    def _address_type(self):
        if type(self.__address) == tuple:
            return 'AF_INET'
        elif type(self.__address) is str and self.__address.startswith('\\\\'):
            return 'AF_PIPE'
        elif type(self.__address) is str or util.is_abstract_socket_namespace(self.__address):
            return 'AF_UNIX'
        else:
            raise ValueError('address type of %r unrecognized' % self.__address)
        
    def _validate_family(self, family):
        if sys.platform != 'win32' and family == 'AF_PIPE':
            raise ValueError('Family %s is not recognized.' % family)

        if sys.platform == 'win32' and family == 'AF_UNIX':
            if not hasattr(socket, family):
                raise ValueError('Family %s is not recognized.' % family)
            
    def _init_timeout(self, timeout=20.):
        return time.monotonic() + timeout
    
    def _check_timeout(self, t):
        return time.monotonic() > t 
            
    def _pipe_client(self):
        t = self._init_timeout()
        while 1:
            try:
                _winapi.WaitNamedPipe(self.__address, 1000)
                h = _winapi.CreateFile(
                    self.__address, _winapi.GENERIC_READ | _winapi.GENERIC_WRITE,
                    0, _winapi.NULL, _winapi.OPEN_EXISTING,
                    _winapi.FILE_FLAG_OVERLAPPED, _winapi.NULL
                    )
            except OSError as e:
                if e.winerror not in (_winapi.ERROR_SEM_TIMEOUT,
                                      _winapi.ERROR_PIPE_BUSY) or mc._check_timeout(t):
                    raise
            else:
                break
        else:
            raise
        return mc.PipeConnection(h)
    
    def _socket_client(self):
        family = self._address_type()
        with socket.socket( getattr(socket, family) ) as s:
            s.setblocking(True)
            s.connect(self.__address)
            return mc.Connection(s.detach())

    def client(self):
        """创建管道客户端.

        利用multiprocessing模块创建命名管道客户端.

        Returns:
            任意文件描述符的连接类(Unix), 
            或套接字句柄(Windows).

        Raises:
            OSError: 创建管道失败.
        """
        family = self._address_type()
        self._validate_family(family)
        if family == 'AF_PIPE':
            client = self._pipe_client()
        else:
            client = self._socket_client()
        return client