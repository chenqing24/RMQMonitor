#!/usr/bin/env python
# -*- coding: utf-8 -*-

from influxdb import client as influxdb

class DBWriter():

    def __init__(self,
                 host,
                 port,
                 username,
                 password,
                 database):
        self.host = host
        self.port = port
        self.username= username
        self.password = password
        self.database = database
        self.influxdb = influxdb.InfluxDBClient(host,port,username,password,database)

    def writ(self,data):
        self.influxdb.write_points(data)
