#!/usr/bin/env python
# -*- coding: utf-8 -*-

# #Copyright (C) 2015, Delft University of Technology, Faculty of Electrical Engineering, Mathematics and Computer Science, Network Architectures and Services and TNO, ICT - Service Enabling and Management, Mani Prashanth Varma Manthena, Niels van Adrichem, Casper van den Broek and F. A. Kuipers
#
# This file is part of NaaSPlatform.
#
# NaaSPlatform is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# NaaSPlatform is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with NaaSPlatform. If not, see <http://www.gnu.org/licenses/>.



# Network-as-a-Service (NaaS) platform's SNMP based core interface monitoring application



# Importing Python modules

import sys # Python module for system (i.e. interpreter) specific parameters and functions
import select # Python module for I/O completion waiting



# Importing NaaS platform's main application for performing NaaS related operations and functions

from Main_App import *




class snmp_network_core_interface_monitoring():


    # SNMP based network core interface monitoring application for detecting high bandwidth link utilizations and failures in the network's core

    global url_snmp, ip_snmp, snmp_agents, snmp, ifin_metric_name, ifout_metric_name, thresh_data
    core_snmp_base = naas_arch().core_snmp_base_url()
    url_snmp = core_snmp_base['URL']
    ip_snmp = core_snmp_base['Host IP']
    snmp_agents = naas_arch().core_snmp_agents()
    snmp = snmp_api_calls()
    thresh_data = {}
    ifin_metric_name = 'ifinutilization'
    ifout_metric_name = 'ifoututilization'



    # Initializing the core SNMP based interface monitoring application for detecting high bandwidth link utilizations and failures in the network's core

    def __init__(self):
        try:
            print '\n\nStarting a SNMP based core interface monitoring application...\n\n'
            print '\n\nFor detecting high bandwidth link utilizations and link failures in the network\'s core...\n\n'
            print '\n\nEnter the following details in order to start the SNMP based core interface monitoring application...'
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
            thresh_data['ifinutilization'] = ifin_thresh_value
            thresh_data['ifoututilization'] = ifout_thresh_value
            print '\n'
            snmp_uti_thresholds = snmp.snmp_uti_thresh_add(url_snmp, thresh_data)
            print '\n\n'
        except KeyboardInterrupt:
            print '\n\n\nSaving all the changes...'
            print '\nYou are now exiting the NaaS SNMP based core interface monitoring application...\n'
            sys.exit(0)
        except:
            print '\n\n\n***ERROR***: Found an exception, restart the application in order to check and debug the errors/exceptions...\n'
            print '\n\n\nSaving all the changes...'
            print '\nYou are now exiting the NaaS SNMP based core interface monitoring application...\n'
            sys.exit(0)
       
        


    # For retrieving high bandwidth utilization events as per the above initialized core SNMP interface monitoring application

    def int_high_uti_events(self):
            try:
                d = 0
                high_uti_events = {}
                snmp_uti_thresholds = snmp.snmp_uti_thresh_def(url_snmp)
                threshold = snmp_uti_thresholds['ifinutilization']
                print '\n\n\nQuerying for high bandwidth link utilization events...\n'
                snmp_agents = snmp.snmp_agents(url_snmp)
                for key in snmp_agents:
                    agent = snmp_agents[key]
                    metric = 'utilization'
                    snmp_events = snmp.snmp_agent_interface_events(url_snmp, agent, metric)
                    if snmp_events == {}:
                        print '\n\n***No Detected/Triggered High Bandwidth Link Utilization Events***\n\n'
                    else:   
                        for key in snmp_events:
                            e = snmp_events[key]
                            if (ifin_metric_name == e['Metric'] or ifout_metric_name == e['Metric']):
                                d += 1
                                event_id = str(d)
                                high_uti_info = {}
                                print '\n\n\n***Detected a High Bandwidth Utilization Event***\n\n'
                                print '***The Detected High Bandwidth Utilization Event is Active***\n\n'
                                print 'High Bandwidth Utilization Event Number: ', event_id
                                print 'High Bandwidth Utilization Event Type: ', e['Metric']
                                print 'High Bandwidth Utilization Event Threshold Value in bytes per second: ', threshold 
                                print 'High Bandwidth Utilization Event Actual Value in % of Total Available Link Bandwidth: ', e['Value']
                                print 'Agent :', e['Agent']
                                print 'Interface ID :', e['Interface ID']
                                print 'Time Stamp: ', e['Last Updated']
                                high_uti_info = { 'Agent' : e['Agent'], 'Interface ID' : e['Interface ID'], 'Metric' : e['Metric'], 'Value' : e['Value'], 'Time Stamp' : e['Last Updated']}           
                                high_uti_events[event_id] = high_uti_info       
                return high_uti_events
            except KeyboardInterrupt:
                print '\n\n\nSaving all the changes...'
                print '\nYou are now exiting the NaaS SNMP based core interface monitoring application...\n'
                sys.exit(0)
            except:
                print '\n\n\n***ERROR***: Found an exception, restart the application in order to check and debug the errors/exceptions...\n'
                print '\n\n\nSaving all the changes...'
                print '\nYou are now exiting the NaaS sFlow based core interface monitoring application...\n'
                sys.exit(0)
            
            
            


    # For retrieving link/interface failure events in the network core

    def int_fail_events(self):
            try:
                d = 0
                int_fail_events = {}
                print '\n\n\nQuerying for link/interface failure events...\n'
                snmp_agents = snmp.snmp_agents(url_snmp)
                for key in snmp_agents:
                    agent = snmp_agents[key]
                    metric = 'status'
                    snmp_events = snmp.snmp_agent_interface_events(url_snmp, agent, metric)
                    if snmp_events == {}:
                        print '\n\n***No Detected/Triggered Link Failure Events***\n\n'
                    else:
                        for key in snmp_events:
                            e = snmp_events[key]
                            if (e['Value'] == 'down'):
                                d += 1
                                event_id = str(d)
                                int_fail_info = {}
                                print '\n\n\n***Detected a Link/Interface Failure Event***...\n\n'
                                print 'Link/Interface Failure Event Number: ', event_id
                                print 'Link/Interface Failure Type: ', e['Metric']
                                print 'Link/Interface Failure Status: ', e['Value']
                                print 'Agent :', e['Agent']
                                print 'Interface ID :', e['Interface ID']
                                print 'Last Updated: ', e['Last Updated']
                                int_fail_info = { 'Agent' : e['Agent'], 'Interface ID' : e['Interface ID'], 'Metric' : e['Metric'], 'Value' : e['Value'], 'Last Updated' : e['Last Updated']}
                                int_fail_events[event_id] = int_fail_info
                return int_fail_events
            except KeyboardInterrupt:
                print '\n\n\nSaving all the changes...'
                print '\nYou are now exiting the NaaS SNMP based core interface monitoring application...\n'
                sys.exit(0)
            except:
                print '\n\n\n***ERROR***: Found an exception, restart the application in order to check and debug the errors/exceptions...\n'
                print '\n\n\nSaving all the changes...'
                print '\nYou are now exiting the NaaS sFlow based core interface monitoring application...\n'
                sys.exit(0)
            


