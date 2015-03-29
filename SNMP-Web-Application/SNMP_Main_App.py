#!/usr/bin/env python
# -*- coding: utf-8 -*-



# This script requires installation of a python module called Bottle - a fast, simple and lightweight WSGI micro web-framework for Python
# Its documentation is available at http://bottlepy.org/docs/dev/index.html



# Initializing and running the SNMP based web application - RESTful web services

print '\n\n\n***Welcome to the SNMP based Web Application - RESTful Web Services***\n\n'



# Importing Python modules

from bottle import route, run, abort, response, request, static_file # Bottle is a fast, simple and lightweight WSGI micro web-framework for Python
import json # Python module for JSON - a lightweight data-interchange format



# SNMP based web application - RESTful web services


@route('/')
def welcome_app(filename = 'API_Info.html'):
    return static_file(filename, root='Config/API_Info/')


@route('/snmp')
def welcome_snmp():
    return '***Welcome to the SNMP based Web Application (RESTful Web Services) - SNMP Directory***'


@route('/snmp/config')
def welcome_snmp_config():
    return '***Welcome to the SNMP based Web Application (RESTful Web Services) - SNMP Config Directory***'


@route('/snmp/config/agents/json', method='GET')
def agents_list(filename = 'Agents_List.json'):
    return static_file(filename, root='Config/Agents/')


@route('/snmp/config/interfaces/Face/json', method='GET')
def agents_list(filename = 'Face_Interface_List.json'):
    return static_file(filename, root='Config/Device_Interfaces/')


@route('/snmp/config/interfaces/Hannibal/json', method='GET')
def agents_list(filename = 'Hannibal_Interface_List.json'):
    return static_file(filename, root='Config/Device_Interfaces/')


@route('/snmp/config/interfaces/BA/json', method='GET')
def agents_list(filename = 'BA_Interface_List.json'):
    return static_file(filename, root='Config/Device_Interfaces/')


@route('/snmp/config/interfaces/Murdock/json', method='GET')
def agents_list(filename = 'Murdock_Interface_List.json'):
    return static_file(filename, root='Config/Device_Interfaces/')


@route('/snmp/config/interfaces/139.63.246.113/json', method='GET')
def agents_list(filename = 'Face_Interface_List.json'):
    return static_file(filename, root='Config/Device_Interfaces/')


@route('/snmp/config/interfaces/139.63.246.114/json', method='GET')
def agents_list(filename = 'Hannibal_Interface_List.json'):

    return static_file(filename, root='Config/Device_Interfaces/')


@route('/snmp/config/interfaces/139.63.246.115/json', method='GET')
def agents_list(filename = 'BA_Interface_List.json'):
    return static_file(filename, root='Config/Device_Interfaces/')


@route('/snmp/config/interfaces/139.63.246.111/json', method='GET')
def agents_list(filename = 'Murdock_Interface_List.json'):
    return static_file(filename, root='Config/Device_Interfaces/')


@route('/snmp/config/interfaces/mac/Face/json', method='GET')
def agents_list(filename = 'Face_Interface_MAC.json'):
    return static_file(filename, root='Config/Interface_MAC_Addresses/')


@route('/snmp/config/interfaces/mac/Hannibal/json', method='GET')
def agents_list(filename = 'Hannibal_Interface_MAC.json'):
    return static_file(filename, root='Config/Interface_MAC_Addresses/')


@route('/snmp/config/interfaces/mac/BA/json', method='GET')
def agents_list(filename = 'BA_Interface_MAC.json'):
    return static_file(filename, root='Config/Interface_MAC_Addresses/')


@route('/snmp/config/interfaces/mac/Murdock/json', method='GET')
def agents_list(filename = 'Murdock_Interface_MAC.json'):
    return static_file(filename, root='Config/Interface_MAC_Addresses/')


@route('/snmp/config/interfaces/mac/139.63.246.113/json', method='GET')
def agents_list(filename = 'Face_Interface_MAC.json'):
    return static_file(filename, root='Config/Interface_MAC_Addresses/')


@route('/snmp/config/interfaces/mac/139.63.246.114/json', method='GET')
def agents_list(filename = 'Hannibal_Interface_MAC.json'):
    return static_file(filename, root='Config/Interface_MAC_Addresses/')


@route('/snmp/config/interfaces/mac/139.63.246.115/json', method='GET')
def agents_list(filename = 'BA_Interface_MAC.json'):
    return static_file(filename, root='Config/Interface_MAC_Addresses/')


@route('/snmp/config/interfaces/mac/139.63.246.111/json', method='GET')
def agents_list(filename = 'Murdock_Interface_MAC.json'):
    return static_file(filename, root='Config/Interface_MAC_Addresses/')


@route('/snmp/config/thresholds/utilization/json', method='PUT')
def put_document():
    data = request.body.readline()
    print(data)
    if not data:
        abort(400, 'No data received')
    thresholds = json.loads(data)
    try:
        with open("Config/Thresholds/Utilization_Thresholds.json", "w") as json_file:
            json.dump(thresholds, json_file)
    except:
        return '***ERROR***'
    


@route('/snmp/config/thresholds/utilization/json', method='GET')
def agents_list(filename = 'Utilization_Thresholds.json'):
    return static_file(filename, root='Config/Thresholds/')


@route('/snmp/events')
def welcome_snmp_events():
    return '***Welcome to the SNMP based Web Application (RESTful Web Services) - SNMP Events Directory***'


@route('/snmp/events/interface/status/Face/json', method='GET')
def interface_status(filename = 'Face_Operational_Status.json'):
    return static_file(filename, root='Events/Interface/')


@route('/snmp/events/interface/status/BA/json', method='GET')
def interface_status(filename = 'BA_Operational_Status.json'):
    return static_file(filename, root='Events/Interface/')


@route('/snmp/events/interface/status/Murdock/json', method='GET')
def interface_status(filename = 'Murdock_Operational_Status.json'):
    return static_file(filename, root='Events/Interface/')


@route('/snmp/events/interface/status/Hannibal/json', method='GET')
def interface_status(filename = 'Hannibal_Operational_Status.json'):
    return static_file(filename, root='Events/Interface/')


@route('/snmp/events/interface/status/139.63.246.113/json', method='GET')
def interface_status(filename = 'Face_Operational_Status.json'):
    return static_file(filename, root='Events/Interface/')


@route('/snmp/events/interface/status/139.63.246.115/json', method='GET')
def interface_status(filename = 'BA_Operational_Status.json'):
    return static_file(filename, root='Events/Interface/')


@route('/snmp/events/interface/status/139.63.246.111/json', method='GET')
def interface_status(filename = 'Murdock_Operational_Status.json'):
    return static_file(filename, root='Events/Interface/')


@route('/snmp/events/interface/status/139.63.246.114/json', method='GET')
def interface_status(filename = 'Hannibal_Operational_Status.json'):
    return static_file(filename, root='Events/Interface/')


@route('/snmp/events/interface/utilization/Face/json', method='GET')
def interface_status(filename = 'Face_Utilizations.json'):
    return static_file(filename, root='Events/Interface/')


@route('/snmp/events/interface/utilization/BA/json', method='GET')
def interface_status(filename = 'BA_Utilizations.json'):
    return static_file(filename, root='Events/Interface/')


@route('/snmp/events/interface/utilization/Murdock/json', method='GET')
def interface_status(filename = 'Murdock_Utilizations.json'):
    return static_file(filename, root='Events/Interface/')


@route('/snmp/events/interface/utilization/Hannibal/json', method='GET')
def interface_status(filename = 'Hannibal_Utilizations.json'):
    return static_file(filename, root='Events/Interface/')


@route('/snmp/events/interface/utilization/139.63.246.113/json', method='GET')
def interface_status(filename = 'Face_Utilizations.json'):
    return static_file(filename, root='Events/Interface/')


@route('/snmp/events/interface/utilization/139.63.246.115/json', method='GET')
def interface_status(filename = 'BA_Utilizations.json'):
    return static_file(filename, root='Events/Interface/')


@route('/snmp/events/interface/utilization/139.63.246.111/json', method='GET')
def interface_status(filename = 'Murdock_Utilizations.json'):
    return static_file(filename, root='Events/Interface/')


@route('/snmp/events/interface/utilization/139.63.246.114/json', method='GET')
def interface_status(filename = 'Hannibal_Utilizations.json'):
    return static_file(filename, root='Events/Interface/')



# SNMP based web service configuration

run(host='localhost', port=8090, debug=True)




