#!/usr/bin/env python
# -*- coding: utf-8 -*-
from NotifySenderInfo import NotifySenderInfo
import httplib

class OpsAlerm():

    def __init__(self,senderinfo,notifytype='sms'):
        self.__sender = senderinfo
        self.__sender.Load(notifytype)


    def Send(self,message,mobile):
        # 把空格替换成url 空格 %20
        msg = message.replace(' ', '%20')

        httpClient = None
        url = self.__sender.Url.replace('${account}',self.__sender.Account).replace('${password}',self.__sender.Password).replace('${mobile}',mobile).replace('${message}',msg)

        try:
            #httpClient = httplib.HTTPConnection('tccommon.17usoft.com', 80, timeout=60)
            #httpClient.request('GET', '/smstemplate/service/SendMessage?account=TCWeb.Bank&password=TCWeb.Bank9633&mobile=18616805733,13761786363&message=this_is_20test!')

            httpClient = httplib.HTTPConnection(self.__sender.Host, int(self.__sender.Port), timeout=60)
            httpClient.request('GET', url)
            #response是HTTPResponse对象
            response = httpClient.getresponse()
            print response.status
            print response.reason
            print response.read()
        except Exception, e:
            print e
        finally:
            if httpClient:
                httpClient.close()