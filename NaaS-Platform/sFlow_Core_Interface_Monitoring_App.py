#!/usr/bin/env python
# -*- coding: utf-8 -*-

# #Copyright (C) 2015, Delft University of Technology, Faculty of Electrical Engineering, Mathematics and Computer Science, Network Architectures and Services and TNO, ICT - Service Enabling and Management, Mani Prashanth Varma Manthena, Niels van Adrichem, Casper van den Broek and F. A. Kuipers
#
# This file is part of NaaSPlatform.
#
# NDNFlow is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# NDNFlow is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with NaaSPlatform. If not, see <http://www.gnu.org/licenses/>.



# Network-as-a-Service (NaaS) platform's sFlow based core interface monitoring application



# Importing Python modules

import sys # Python module for system (i.e. interpreter) specific parameters and functions
import select # Python module for I/O completion waiting



# Importing NaaS platform's main application for performing NaaS related operations and functions

from Main_App import *




class sflow_network_core_interface_monitoring():


    # sFlow based network core interface monitoring application for detecting high bandwidth link utilizations and failures in the network's core

    global url_sflow, ip_sflow, sflow_header, sflow_agents, sflow, ifin_metric_name, ifout_metric_name, ifin_thresh_name, ifout_thresh_name, ifin_thresh_data, ifout_thresh_data
    core_sflow_base = naas_arch().core_sflow_base_url()
    url_sflow = core_sflow_base['URL']
    ip_sflow = core_sflow_base['Host IP']
    sflow_header = naas_arch().sflow_api_header()
    sflow_agents = naas_arch().core_sflow_agents()
    sflow = sflow_api_calls()
    ifin_metric_name = 'ifinutilization'
    ifout_metric_name = 'ifoututilization'
    ifin_thresh_name = 'ifinuti'
    ifout_thresh_name = 'ifoututi'
    ifin_thresh_data = {}
    ifout_thresh_data = {}


    # Initializing the core network sFlow based interface monitoring application for detecting high bandwidth link utilizations in the network's core

    def __init__(self):
        try:
            print '\n\nStarting a sFlow based core network interface monitoring application...\n\n'
            print '\n\nFor detecting high bandwidth link utilizations and link failures in the network\'s core...\n\n'
            print '\n\nEnter the following details in order to start the sFlow based core interface monitoring application...'
            print '\nNote: If you want to skip an entry, press the enter key\n\n'
            print '\n\nIncoming traffic monitoring metric name: ', ifin_metric_name
            print '\n\nOutgoing traffic monitoring metric name: ', ifout_metric_name
            print '\n\nSet the threshold limits/values (i.e. in % of total available link bandwidth) for the interface\'s incoming and outgoing traffic...\n\n'
            ifin_thresh_value = raw_input('Enter the Incoming Traffic Link Utilization Threshold Limit/Value (Default value = 10): ')
            ifout_thresh_value = raw_input('Enter the Outgoing Traffic Link Utilization Threshold Limit/Value (Default value = 10): ')
            if ifin_thresh_value == '':
                ifin_thresh_value = '10'
            if ifout_thresh_value == '':
                ifout_thresh_value = '10'
            print '\n\nIncoming traffic link utilization threshold limit/value in % of total available link bandwidth: ', ifin_thresh_value
            print '\n\nOutgoing traffic link utilization threshold limit/value in % of total available link bandwidth: ', ifout_thresh_value
            ifin_thresh_data['metric'] = ifin_metric_name
            ifin_thresh_data['value'] = ifin_thresh_value
            print '\n\n\nAdding a sFlow threshold (i.e. in % of total available link bandwidth) to detect a high bandwidth link utilization by the incoming traffic of an interface...\n'
            sflow.sflow_thresh_add(url_sflow, sflow_header, ifin_thresh_name, ifin_thresh_data)
            ifout_thresh_data['metric'] = ifout_metric_name
            ifout_thresh_data['value'] = ifout_thresh_value
            print '\n\n\nAdding a sFlow threshold (i.e. in % of total available link bandwidth) to detect a high bandwidth link utilization by the outgoing traffic of an interface...\n'
            sflow.sflow_thresh_add(url_sflow, sflow_header, ifout_thresh_name, ifout_thresh_data)
        except KeyboardInterrupt:
            print '\n\n\nSaving all the changes...'
            print '\nYou are now exiting the NaaS sFlow based core interface monitoring application...\n'
            sys.exit(0)
        except:
            print '\n\n\n***ERROR***: Found an exception, restart the application in order to check and debug the errors/exceptions...\n'
            print '\n\n\nSaving all the changes...'
            print '\nYou are now exiting the NaaS sFlow based core interface monitoring application...\n'
            sys.exit(0)


    # For retrieving high bandwidth utilization events as per the above initialized simple core sflow interface monitoring application

    def int_high_uti_events(self):
            try:
                high_uti_events = {}
                events_filter = ''
                eventID = -1
                print '\n\n\nQuerying for High Bandwidth Link Utilization Events...\n'
                events_filter = 'eventID='
                events_filter += str(eventID)
                response = sflow.sflow_events(url_sflow, events_filter)
                if response.status_code == 200:
                    events = response.json()
                    if len(events) == 0:
                        print '\n\n***No Detected/Triggered High Bandwidth Link Utilization Events***\n\n'
                    else:
                        d = 0
                        for e in events:
                            if (ifin_metric_name == e['metric'] or ifout_metric_name == e['metric']):
                                d += 1
                                high_uti_info = {}
                                print '\n\n\n***Detected a High Bandwidth Utilization Event***\n\n'
                                print 'High Bandwidth Utilization Event Number: ', e['eventID']
                                print 'High Bandwidth Utilization Event Type: ', e['metric']
                                print 'High Bandwidth Utilization Event Threshold Value in bytes per second: ', e['threshold']
                                print 'High Bandwidth Utilization Event Actual Value in % of Total Available Link Bandwidth: ', e['value']
                                print 'Checking the Status of the Detected High Bandwidth Utilization Event...'
                                agent = e['agent']
                                interface = e['dataSource']
                                metric = e['metric']
                                response = sflow.sflow_interface_metric_value(url_sflow, agent, interface, metric)
                                metric_val = response.json()
                                print '\n\n\n'
                                print 'Large Flow Event Current Status: '
                                print '\n\n\n'
                                if len(metric_val) > 0:
                                    status = 'inactive'
                                    for key in metric_val[0]:
                                        if key == 'metricValue':
                                            if metric_val[0]['metricValue'] >= int(e['threshold']):
                                                status = 'active'
                                                print '***The Detected High Bandwidth Utilization Event is Active***\n\n'
                                                print 'Agent :', e['agent']
                                                print 'Interface ID :', e['dataSource']
                                                print  e['metric'], ': ', e['value']
                                                print 'Time Stamp: ', e['timestamp']
                                                high_uti_info = { 'Agent' : e['agent'], 'Interface ID' : e['dataSource'], 'Metric' : e['metric'], 'Value' : e['value'], 'Time Stamp' : e['timestamp']}
                                                m = 0
                                                for hui in high_uti_events:
                                                    if (high_uti_events[hui]['Agent'] == e['agent'] and high_uti_events[hui]['Interface ID'] == e['dataSource'] and high_uti_events[hui]['Metric'] == e['metric']):
                                                        m += 1
                                                if m == 0:
                                                    print '***Note: This Active High Bandwidth Utilization Event is the Latest/Unique Instance***\n\n'
                                                    high_uti_events[e['eventID']] = high_uti_info
                                                else:
                                                    print '\n\n***Note: This Active High Bandwidth Utilization Event is Not the Latest/Unique Instance***\n\n' 
                                    if status == 'inactive':
                                        print '\n\n***The Detected High Bandwidth Utilization Event is no Longer Active***\n\n'
                        if d == 0:
                            print '\n\n***No Detected/Triggered High Bandwidth Link Utilization Events***\n\n'
                return high_uti_events
            except KeyboardInterrupt:
                print '\n\n\nSaving all the changes...'
                print '\nYou are now exiting the NaaS sFlow based core interface monitoring application...\n'
                sys.exit(0)
            except:
                print '\n\n\n***ERROR***: Found an exception, restart the application in order to check and debug the errors/exceptions...\n'
                print '\n\n\nSaving all the changes...'
                print '\nYou are now exiting the NaaS sFlow based edge flow monitoring application...\n'
                sys.exit(0)
            


    # For retrieving link/interface failure events in the network core

    def int_fail_events(self):
            try:
                int_fail_events = {}
                print '\n\n\nQuerying for link/interface failure events...\n'
                agent = 'ALL'
                metric = 'ifoperstatus'
                response = sflow.sflow_metric_values(url_sflow, agent, metric)
                if response.status_code == 200:
                    events = response.json()
                    if len(events) == 0:
                        print '\n\n***No Detected/Triggered Link/Interface Failure Events***\n\n'
                    i = 0
                    d = 0
                    for e in events:
                        if (e['metricValue'] == 'down'):
                            d += 1
                            i += 1
                            event_id = str(i)
                            int_fail_info = {}
                            print '\n\n\n***Detected a Link/Interface Failure Event***...\n\n'
                            print 'Link/Interface Failure Event Number: ', event_id
                            print 'Link/Interface Failure Type: ', e['metricName']
                            print 'Link/Interface Failure Status: ', e['metricValue']
                            print '\n\n\n'
                            print '\n\n\nPrinting the Link/Interface Failure Event information/details...\n\n'
                            print 'Agent :', e['agent']
                            print 'Interface ID :', e['dataSource']
                            print  e['metricName'], ': ', e['metricValue']
                            print 'Last Updated: ', e['lastUpdate']
                            int_fail_info = { 'Agent' : e['agent'], 'Interface ID' : e['dataSource'], 'Metric' : e['metricName'], 'Value' : e['metricValue'], 'Last Updated' : e['lastUpdate']}
                            int_fail_events[event_id] = int_fail_info
                    if d == 0:
                        print '\n\n***No Detected/Triggered Link/Interface Failure Events***\n\n'
                return int_fail_events
            except KeyboardInterrupt:
                print '\n\n\nSaving all the changes...'
                print '\nYou are now exiting the NaaS sFlow based core interface monitoring application...\n'
                sys.exit(0)
            except:
                print '\n\n\n***ERROR***: Found an exception, restart the application in order to check and debug the errors/exceptions...\n'
                print '\n\n\nSaving all the changes...'
                print '\nYou are now exiting the NaaS sFlow based core interface monitoring application...\n'
                sys.exit(0)
