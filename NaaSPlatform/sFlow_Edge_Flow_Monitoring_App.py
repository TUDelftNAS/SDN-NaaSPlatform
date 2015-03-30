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



# Network-as-a-Service (NaaS) platform's sFlow based edge flow monitoring application



# Importing Python modules

import sys # Python module for system (i.e. interpreter) specific parameters and functions
import select # Python module for I/O completion waiting



# Importing NaaS platform's main application for performing NaaS related operations and functions

from Main_App import *




class network_edge_flow_monitoring():


    # Network edge flow monitoring application for detecting large traffic flows at the network's edge

    
    # Initializing the network edge flow monitoring application for detecting large traffic flows at the network's edge

    def __init__(self):
        try:
            edge_sflow_base = naas_arch().edge_sflow_base_url()
            url_sflow = edge_sflow_base['URL']
            ip_sflow = edge_sflow_base['Host IP']
            sflow_header = naas_arch().sflow_api_header()
            sflow_agents = naas_arch().edge_sflow_agents()
            sflow = sflow_api_calls()
            group_data = {}
            flow_data = {}
            thresh_data = {}
            int_add = []
            ext_add = []
            print '\n\nStarting a network edge flow monitoring application for detecting large traffic flows at the network\'s edge...\n\n'
            print '\n\nEnter the following details in order to start the network\'s edge traffic flow monitoring application...'
            print '\nNote: If you want to skip an entry, press the enter key\n\n'
            print '\nAssign a name to the network edge  flow monitoring application...\n\n'
            flow_monitoring_name = raw_input('Enter a Name for this Network Edge Flow Monitoring Instance (Required): ')
            group_name = flow_monitoring_name
            sflow_name = flow_monitoring_name
            thresh_name = flow_monitoring_name
            print '\n\n\n\nEnter the following details in order to categorize the network\'s edge traffic...\n\n'
            add_int = raw_input('Enter the List of Addresses you want to group as ¨internal¨: ')
            int_add.append(add_int)
            group_data['internal'] = int_add
            add_ext = raw_input('Enter the List of Addresses you want to group as ¨external¨: ')
            ext_add.append(add_ext)
            group_data['external'] = ext_add
            if (add_int != '' or add_ext != ''):
                print '\n\n\nAdding a sFlow address group to categorize the network\'s edge traffic as defined above...\n'
                sflow.sflow_group_add(url_sflow, sflow_header, group_name, group_data)
            sflow.sflow_flowkeys(url_sflow)
            print '\n\nEnter the flowkeys (source flowkey followed by destination flowkey which are seperated by ¨,¨) you want to add to the flow definition\n\n'
            flow_keys = raw_input('Enter the Flowkeys (Default value: ¨ipsource,ipdestination¨): ')
            if flow_keys == '':
                flow_keys = 'ipsource,ipdestination'
            print '\n\nEnter the flow value (e.g. ¨bytes¨, ¨frames¨, etc.) you want to add to the flow definition...\n'
            flow_value = raw_input('Enter the Flow value (Default value: ¨bytes¨): ')
            if flow_value == '':
                flow_value = 'bytes'
            keys = re.sub(r'\s', '', flow_keys).split(',')
            source_key = keys[0]
            destination_key = keys[1]
            flow_data['keys'] = flow_keys
            flow_data['value'] = flow_value
            if (add_int != '' or add_ext != ''):
                print '\n\nAssign the above defined address groups to categorize network\'s edge traffic (i.e. based on traffic source and destination addresses)\n\n'
                source_group = raw_input('Traffic Source Address Group Name (¨internal¨/¨external¨): ')
                destination_group = raw_input('Traffic Destination Address Group Name (¨internal¨/¨external¨): ')
                flow_filter = 'group:'+source_key+':'+group_name+'='+source_group+'&group:'+destination_key+':'+group_name+'='+destination_group
                flow_data['filter'] = flow_filter
            print '\n\nAdding a sFlow flow to monitor network\'s edge traffic for large traffic flows..\n'
            sflow.sflow_flow_add(url_sflow, sflow_header, sflow_name, flow_data)
            print '\n\nSet the threshold limit/value (i.e. in Mbps) for detecting large traffic flows in the above defined sFlow flow\n\n'
            thresh_value = raw_input('Enter the Threshold Limit/Value (Default value = 100 Mbps): ')
            if thresh_value == '':
                thresh_value = '100'
            thresh_value = int(thresh_value)
            thresh_value = thresh_value * 125000
            print '\n\nThreshold limit/value in bytes per second: ', thresh_value
            thresh_value = str(thresh_value)
            thresh_data['metric'] = sflow_name
            thresh_data['value'] = thresh_value
            print '\n\n\nAdding a sFlow threshold (i.e. bytes per second) to detect a large flow in the above defined sFlow flow...\n'
            sflow.sflow_thresh_add(url_sflow, sflow_header, thresh_name, thresh_data)
        except KeyboardInterrupt:
            print '\n\n\nSaving all the changes...'
            print '\nYou are now exiting the NaaS sFlow based edge flow monitoring application...\n'
            sys.exit(0)
        except:
            print '\n\n\nSaving all the changes...'
            print '\nYou are now exiting the NaaS sFlow based edge flow monitoring application...\n'
            sys.exit(0)
        



    # For retrieving large flow events as per the above initialized network edge flow monitoring application

    def network_edge_large_flow_events(self, flow_monitoring_name):
            try:
                edge_sflow_base = naas_arch().edge_sflow_base_url()
                url_sflow = edge_sflow_base['URL']
                ip_sflow = edge_sflow_base['Host IP']
                sflow_header = naas_arch().sflow_api_header()
                sflow_agents = naas_arch().edge_sflow_agents()
                sflow = sflow_api_calls()
                group_name = flow_monitoring_name
                sflow_name = flow_monitoring_name
                thresh_name = flow_monitoring_name
                large_flow_events = {}
                events_filter = ''
                eventID = -1
                print '\n\n\nQuerying for Large Flow Events...\n'
                events_filter = 'eventID='
                events_filter += str(eventID)
                response = sflow.sflow_events(url_sflow, events_filter)
                if response.status_code == 200:
                    events = response.json()
                    if len(events) == 0:
                        print '\n\n***No Detected/Triggered Large Flow Events***\n\n'
                    else:
                        d = 0
                        for e in events:
                            if sflow_name == e['metric']:
                                d += 1
                                large_flow_info = {}
                                print '\n\n\n***Detected a Large Flow Event***\n\n'
                                print 'Large Flow Event ID: ', e['eventID']
                                print 'Large Flow Event Threshold Value in bytes per second: ', e['threshold']
                                thresh_value = int(e['threshold'])
                                thresh_value = thresh_value/125000
                                thresh_value = str(thresh_value)
                                print 'Large Flow Event Threshold Value in Mbps: ', thresh_value
                                print 'Large Flow Event Actaul Value in bytes per second: ', e['value']
                                flow_value = int(e['value'])
                                flow_value = flow_value/125000
                                flow_value = str(flow_value)
                                print 'Large Flow Event Value in Mbps: ', flow_value
                                print '\n\n\n'
                                print 'Checking the Status of the Detected Large Flow Event...' 
                                agent = e['agent']
                                interface = e['dataSource']
                                metric = e['metric']
                                response = sflow.sflow_interface_metric_value(url_sflow, agent, interface, metric)
                                metric_val = response.json()
                                print '\n\n\n'
                                print 'Large Flow Event Current Status: '
                                print '\n\n\n'
                                if len(metric_val) > 0:
                                    large_flow_list = []
                                    status = 'inactive'
                                    for key in metric_val[0]:
                                        if key == 'topKeys':
                                            if metric_val[0]['metricValue'] >= int(e['threshold']):
                                                status = 'active'
                                                print '***The Detected Large Flow Event is Active***\n\n'
                                                print '\n\n\nPrinting the Large Flow Event Information/Details...\n\n'
                                                large_flow = metric_val[0]['topKeys'][0]['key']
                                                large_flow_list = large_flow.split(",")
                                                print 'Large Flow Source Address: ', large_flow_list[0]
                                                print 'Large Flow Destination Address: ', large_flow_list[1]
                                                print 'Large Flow Detected Agent IP Address: ', e['agent']
                                                print 'Large Flow Incoming Interface ID : ', e['dataSource']
                                                print 'Large Flow Event Time Stamp: ', e['timestamp']
                                                large_flow_info = { 'Agent' : e['agent'], 'Interface ID' : e['dataSource'], 'Metric' : e['metric'], 'Value' : e['value'], 'Time Stamp' : e['timestamp'], 'Source Add' : large_flow_list[0], 'Destination Add' : large_flow_list[1]}
                                                m = 0
                                                for lfe in large_flow_events:
                                                    if (large_flow_events[lfe]['Source Add'] == large_flow_list[0] and large_flow_events[lfe]['Destination Add'] == large_flow_list[1]):
                                                        m += 1
                                                if m == 0:
                                                    print '***Note: This Active Large Flow Event is the Latest/Unique Instance***\n\n'
                                                    large_flow_events[e['eventID']] = large_flow_info
                                                else:
                                                    print '\n\n***Note: This Active Large Flow Event is Not the Latest/Unique Instance***\n\n' 
                                    if status == 'inactive':
                                        print '\n\n***The Detected Large Flow Event is no Longer Active***\n\n'
                        if d == 0:
                            print '\n\n***No Detected/Triggered Large Flow Events***\n\n'
                return large_flow_events                        
            except KeyboardInterrupt:
                print '\n\n\nSaving all the changes...'
                print '\nYou are now exiting the NaaS sFlow based edge flow monitoring application...\n'
                sys.exit(0)
            except:
                print '\n\n\nSaving all the changes...'
                print '\nYou are now exiting the NaaS sFlow based edge flow monitoring application...\n'
                sys.exit(0)
