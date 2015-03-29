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



# Network-as-a-Service (NaaS) platform's edge firewall application



# Importing Python modules

import sys # Python module for system (i.e. interpreter) specific parameters and functions
import select # Python module for I/O completion waiting



# Importing NaaS platform's main application for performing NaaS related operations and functions

from Main_App import *



class network_edge_firewall():


    # Network edge firewall application for mitigating DDoS (i.e. distributed denial of service) attacks, by categorizing network's edge traffic based on user defined address groups

    def __init__(self):
        try:
            print '\n\nStarting a network edge firewall application for mitigating DDoS (i.e. distributed denial of service) attacks...\n\n'
            odl_base = naas_arch().odl_base_url()
            url_odl = odl_base['URL']
            ip_odl = odl_base['Host IP']
            odl_header = naas_arch().odl_api_header()
            cred = naas_arch().odl_user_cred()
            name = cred['User Name']
            password = cred['Password']
            edge_sflow_base = naas_arch().edge_sflow_base_url()
            url_sflow = edge_sflow_base['URL']
            ip_sflow = edge_sflow_base['Host IP']
            sflow_header = naas_arch().sflow_api_header()
            odl_switches = naas_arch().odl_switches()
            odl_switches_ip = naas_arch().odl_switches_ip()
            sflow_agents = naas_arch().edge_sflow_agents()
            flow = odl_api_json_formats()
            stat = odl_api_flow_stat()
            odl = odl_api_calls()
            sflow = sflow_api_calls()
            int_add = []
            ext_add = []
            group_data = {}
            flow_data = {}
            thresh_data = {}
            print '\n\nEnter the following details in order to start the network edge firewall application...'
            print '\nNote: If you want to skip an entry, press the enter key\n\n'
            print '\nAssign a name to the network edge firewall application...\n\n'
            firewall_name = raw_input('Enter a Name for this Network Edge Firewall Instance (Required): ')
            group_name = firewall_name
            sflow_name = firewall_name
            thresh_name = firewall_name
            print '\n\n\n\nEnter the following details in order to categorize the network\'s edge traffic...\n\n'
            add = raw_input('Enter the List of Addresses you want to group as ¨trusted/internal¨ (Default value: 10.8.1.0/24): ')
            if add == '':
                add = '10.8.1.0/24'
            int_add.append(add)
            group_data['internal'] = int_add
            add = raw_input('Enter the List of Addresses you want to group as ¨un-trusted/external¨ (Default value: 0.0.0.0/0): ')
            if add == '':
                add = '0.0.0.0/0'
            ext_add.append(add)
            group_data['external'] = ext_add
            print '\n\n\nAdding a sFlow address group to categorize the incoming network\'s edge traffic as defined above...\n'
            sflow.sflow_group_add(url_sflow, sflow_header, group_name, group_data)
            sflow.sflow_flowkeys(url_sflow)
            print '\n\nEnter the flowkeys (source flowkey followed by destination flowkey which are seperated by ¨,¨) you want to add to the flow definition\n\n'
            flow_keys = raw_input('Enter the Flowkeys (Default value: ¨ipsource,ipdestination¨): ')
            if flow_keys == '':
                flow_keys = 'ipsource,ipdestination'
            print '\n\nEnter the flow value (e.g. ¨bytes¨, ¨frames¨, etc.) you want to add to the flow definition...\n'
            flow_value = raw_input('Enter the Flow value (Default value: ¨frames¨): ')
            if flow_value == '':
                flow_value = 'frames'
            keys = re.sub(r'\s', '', flow_keys).split(',')
            source_key = keys[0]
            destination_key = keys[1]
            flow_filter = 'group:'+source_key+':'+group_name+'=external&group:'+destination_key+':'+group_name+'=internal'
            flow_data['keys'] = flow_keys
            flow_data['value'] = flow_value
            flow_data['filter'] = flow_filter
            print '\n\nAdding a sFlow flow to monitor network\'s edge traffic as per the above defined sFlow address group for DDoS attacks..\n'
            sflow.sflow_flow_add(url_sflow, sflow_header, sflow_name, flow_data)
            print '\n\nSet the threshold limit/value for detecting DDoS attacks in the above defined sFlow flow\n\n'
            thresh_value = raw_input('Enter the Threshold Limit/Value (Default value = 1000): ')
            if thresh_value == '':
                thresh_value = '1000'
            thresh_data['metric'] = sflow_name
            thresh_data['value'] = thresh_value
            print '\n\n\nAdding a sFlow threshold (i.e. frames per second) to detect/trigger DDoS attacks/events in the above defined sFlow flow...\n'
            sflow.sflow_thresh_add(url_sflow, sflow_header, thresh_name, thresh_data)
            print '\n\nSet the DDoS attack events query filter...\n\n'
            max_events = raw_input('Enter the Maximum Number of DDoS Attack Events to Query at any given time (Default value = 10): ')
            if max_events == '':
                max_events = '10'
            timeout_events = raw_input('Enter the Timeout (i.e. in seconds) between DDoS Attack Events Queries(Default value = 60): ')
            if timeout_events == '':
                timeout_events = '60'
            print '\n\n\nSet the minimum timeout (i.e. in minutes) for releasing the installed firewall actions and restarting the firewall application...\n\n'
            release_time = raw_input('Enter the Minimum Timeout (i.e. in minutes) for releasing the installed firewall actions (Default value = 10): ')
            if release_time == '':
                release_time = '10'
            release_counter = (int(release_time)*60)/(int(timeout_events))
            q = 0
            eventID = -1
            while 1 == 1:
                q += 1
                print '\n\n\nQuerying for DDoS Attack Events...\n'
                print 'Query Number: ', q
                events_filter = ''
                events_filter = 'maxEvents='
                events_filter += max_events
                events_filter += '&'
                events_filter += 'timeout='
                events_filter += timeout_events
                events_filter += '&eventID='
                events_filter += str(eventID)
                response = sflow.sflow_events(url_sflow, events_filter)
                if response.status_code != 200: break
                events = response.json()
                if len(events) == 0:
                    release_counter -= 1
                    if release_counter == 0:
                        print '\n\n\n***Restarting the Simple Network Edge Firewall Application***\n\n'
                        with open("Statistics_Logs/Edge_Firewall_Flow_Stats.json") as json_file:
                            firewall_flow_stats = json.load(json_file)
                        if firewall_flow_stats:
                            print '\n\n\nReleasing the edge firewall actions installed in the network\'s edge OF/OVS switches....\n\n'
                            for key in firewall_flow_stats:
                                static_stats = {}
                                static_flow_stats = {}
                                firewall_flow_stats = {}
                                static_flow = flow.odl_static_json()
                                static_stats = stat.odl_static_stat()
                                static_flow_stats = static_stats['stat']
                                with open("Statistics_Logs/Edge_Firewall_Flow_Stats.json") as json_file:
                                    firewall_flow_stats = json.load(json_file)
                                flow_name = key
                                switch_id = firewall_flow_stats[key]['Switch ID']
                                print '\n\nReleasing the edge firewall action...\n\n'
                                deleted_flow = odl.odl_static_flow_del(url_odl, name, password, switch_id, flow_name)
                                if deleted_flow:
                                    if firewall_flow_stats:
                                        print '\n\n***Succesfully released the Firewall action***\n\n'
                                        del(static_flow_stats[deleted_flow])
                                        del(firewall_flow_stats[deleted_flow])
                                        with open("Statistics_Logs/Static_Flow_Stats.json", "w") as json_file:
                                            json.dump(static_flow_stats, json_file)
                                        with open("Statistics_Logs/Edge_Firewall_Flow_Stats.json", "w") as json_file:
                                            json.dump(firewall_flow_stats, json_file)
                        else:
                            print '\n\n\nNo installed firewall actions in the network\'s edge OF/OVS switches...\n\n'
                        print '\n\n\nContinuing with the simple network edge firewall...\n\n'
                        release_counter = (int(release_time)*60)/(int(timeout_events))
                        eventID = -1
                        continue
                    else:
                        print '\n\n\nContinuing with the simple network edge firewall...\n\n'
                        continue
                else:
                    eventID = events[0]['eventID']
                    for e in events:
                        if sflow_name == e['metric']:
                            print '\n\n\n***Detected a DDoS Attack Event***\n\n'
                            print 'DDoS Attack Event ID: ', e['eventID']
                            print 'DDoS Attack Event Threshold Value in frames per second: ', e['threshold']
                            print 'DDoS Attack Event Actual Value in frames per second: ', e['value']
                            print '\n\n\n'
                            print 'Checking the Status of the Detected DDoS Attack Event...' 
                            agent = e['agent']
                            interface = e['dataSource']
                            metric = e['metric']
                            response = sflow.sflow_interface_metric_value(url_sflow, agent, interface, metric)
                            metric_val = response.json()
                            print '\n\n\n'
                            print 'DDoS Attack Event Current Status: '
                            print '\n\n\n'
                            if len(metric_val) > 0:
                                attack_list = []
                                status = 'inactive'
                                for key in metric_val[0]:
                                    if key == 'topKeys':
                                            status = 'active'
                                            print '***The Detected DDoS Attack Event is Active***\n\n'
                                            print '\n\n\nPrinting the DDoS Attack Information/Details...\n\n'
                                            attack = metric_val[0]['topKeys'][0]['key']
                                            attack_list = attack.split(",")
                                            print 'DDoS Attacker/Source Address: ', attack_list[0]
                                            print 'DDoS Attack Target/Destination Address: ', attack_list[1]
                                            print 'DDoS Attack Detected sFlow Agent IP Address: ', agent
                                            print 'DDoS Attack Incoming Interface ID: ', interface
                                            print '\n\n\nBlocking DDoS attacker\'s incoming traffic through the ODL controller\'s REST API...\n\n'
                                            odl_switches = naas_arch().odl_switches()
                                            sflow_agents = naas_arch().edge_sflow_agents()
                                            static_stats = {}
                                            static_flow_stats = {}
                                            firewall_flow_stats = {}
                                            static_flow = flow.odl_static_json()
                                            static_stats = stat.odl_static_stat()
                                            static_flow_stats = static_stats['stat']
                                            static_flow_counter = static_stats['counter']
                                            with open("Statistics_Logs/Edge_Firewall_Flow_Stats.json") as json_file:
                                                firewall_flow_stats = json.load(json_file)
                                            switch_name = ''
                                            switch_id = ''
                                            blocked = ''
                                            for key in odl_switches_ip:
                                                if key == e['agent']:
                                                    switch_id = odl_switches_ip[key]
                                            for key in firewall_flow_stats:
                                                if (firewall_flow_stats[key]['Switch ID'] == switch_id and firewall_flow_stats[key]['Source Add'] == attack_list[0] and firewall_flow_stats[key]['In Port ID'] == interface):
                                                    blocked = 'yes'
                                                    print '\n\n\n***Already Blocked attacker\'s incoming traffic through the ODL controller\'s REST API***\n\n'
                                            if not blocked == 'yes':
                                                with open("sFlow_ODL_Flowkeys_Bindings/Edge_Firewall_Flowkeys_Bindings.json") as json_file:
                                                    firewall_flow_keys = json.load(json_file)
                                                for key in firewall_flow_keys:
                                                    if key == source_key:
                                                        match_rule = firewall_flow_keys[key]
                                                in_port = interface
                                                src_add = ''
                                                dst_add = ''
                                                dl_dst = ''
                                                dl_src = ''
                                                protocol = ''
                                                src_port = ''
                                                dst_port = ''
                                                vlan_id = ''
                                                vlan_priority = ''
                                                if match_rule == 'src_add':
                                                    src_add = attack_list[0]
                                                if match_rule == 'dl_src':
                                                    dl_src = attack_list[0]
                                                if match_rule == 'src_port':
                                                    src_port = attack_list[0]
                                                priority = '1000'
                                                action = []
                                                action_input = 'DROP'
                                                action.append(action_input)
                                                flow_stat = {}
                                                flow_stat = odl.odl_static_flow_inst(url_odl, name, password, odl_header, static_flow, static_flow_counter, switch_id, dst_add, src_add, in_port, dl_dst, dl_src, protocol, src_port, dst_port, vlan_id, vlan_priority, action, priority)
                                                if flow_stat:
                                                    print '\n\n\n***Succesfully Blocked attacker\'s incoming traffic through the ODL controller\'s REST API***\n\n'
                                                    flow_name = flow_stat['Flow Name']
                                                    static_flow_stats[flow_name] = flow_stat
                                                    firewall_flow_stats[flow_name] = {'Switch ID': switch_id, 'Source Add' : attack_list[0], 'In Port ID' : interface}
                                                    with open("Statistics_Logs/Static_Flow_Stats.json", "w") as json_file:
                                                        json.dump(static_flow_stats, json_file)
                                                    with open("Statistics_Logs/Edge_Firewall_Flow_Stats.json", "w") as json_file:
                                                        json.dump(firewall_flow_stats, json_file)
                                if status == 'inactive':
                                    print '***The Detected DDoS Attack Event is no Longer Active***\n\n'
        except KeyboardInterrupt:
            print '\n\n\nSaving all the changes...'
            print '\nYou are now exiting the NaaS edge firewall application...\n'
            sys.exit(0)
        except:
            print '\n\n\nSaving all the changes...'
            print '\nYou are now exiting the NaaS edge firewall application...\n'
            sys.exit(0)

