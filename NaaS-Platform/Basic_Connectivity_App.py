#!/usr/bin/env python
# -*- coding: utf-8 -*-



# Network-as-a-Service (NaaS) platform's basic connectivity application



# Importing Python modules

import sys # Python module for system (i.e. interpreter) specific parameters and functions
import select # Python module for I/O completion waiting
import time # Python module for various time related functions



# Importing NaaS platform's main application for performing NaaS related operations and functions

from Main_App import *



# Importing NaaS platform's optimal path computation application for optimal path computations and selections

from Optimal_Path_Computation_App import *



class testbed_network_1():


    # Starting a basic connectivity application in a network (i.e. edge + core) of open (i.e. OF/OVS) switches

    def __init__(self):
            try:
                odl_base = naas_arch().odl_base_url()
                url_odl = odl_base['URL']
                ip_odl = odl_base['Host IP']
                odl_header = naas_arch().odl_api_header()
                cred = naas_arch().odl_user_cred()
                name = cred['User Name']
                password = cred['Password']
                odl_switches = naas_arch().odl_switches()
                odl_switches_ip = naas_arch().odl_switches_ip()
                testbed_1_topo = naas_arch().testbed_1_topology()
                testbed_1_lsps = naas_arch().testbed_1_path_bindings()
                sflow_if_map = naas_arch().sflow_interface_mapping()
                flow = odl_api_json_formats()
                stat = odl_api_flow_stat()
                odl = odl_api_calls()
                delete_links = {}
                update_link_weights = {}
                print '\n\nStarting the basic connectivity application...\n\n'
                print '\n\nInitializing and setting up the basic connectivity across the network...\n\n'
                print '\n\nEnter the end-user hosts query timeout/interval (i.e. in seconds)...\n\n'
                timeout = raw_input('End-User Hosts Query Timeout/Interval (Default Value: 10): ')
                if timeout == '':
                    timeout = 10
                timeout = int(timeout)
                print '\n\n\n'
                while True:
                    print 'Accessing the list of end-hosts that are connected to the network edge switches (i.e. OF/OVS switches)...\n\n'
                    list_hosts = odl.odl_list_hosts(url_odl, name, password)
                    i = 0
                    for hostConfig in list_hosts['hostConfig']:
                        i += 1
                        odl_switch_ip = ''
                        dst_add = hostConfig['networkAddress']
                        host_switch_id = hostConfig['nodeId']
                        for key in odl_switches:
                            if odl_switches[key] != host_switch_id:
                                switch_id = odl_switches[key]
                        print '\n\n\n'
                        print 'Detected an end-user host...'
                        print '\n'
                        print 'End-user Host - ', i
                        print 'End-user Host - Network (IP) Address: ' , hostConfig['networkAddress']
                        print 'End-user Host - Data Layer (MAC) Address: ' , hostConfig['dataLayerAddress']
                        print 'Connected to the Switch (ID): ' , hostConfig['nodeId']
                        print 'Connected to the Switch Edge (ID): ' , hostConfig['nodeConnectorId']
                        for key in odl_switches_ip:
                            if odl_switches_ip[key] == hostConfig['nodeId']:
                                odl_switch_ip = key   
                        print 'Connected to the Switch (IP) Address: ', odl_switch_ip
                        basic_connectivity_flow_stats = {}
                        installed = ''
                        with open("Statistics_Logs/Testbed_1_Basic_Connectivity_Flow_Stats.json") as json_file:
                                basic_connectivity_flow_stats = json.load(json_file)
                        for key in basic_connectivity_flow_stats:
                            if (basic_connectivity_flow_stats[key]['Switch ID'] == switch_id and basic_connectivity_flow_stats[key]['IP Destination'] == dst_add):
                                installed = 'yes'
                                print '\n\n\n***Already installed a MPLS LSP for the above end-user host through the ODL controller\'s REST API***\n\n'
                        if not installed == 'yes':
                            mpls_push_stats = {}
                            mpls_push_flow_stats = {}
                            mpls_push_flow = flow.odl_mpls_push_json()
                            mpls_push_stats = stat.odl_mpls_push_stat()
                            mpls_push_flow_stats = mpls_push_stats['stat']
                            mpls_push_flow_counter = mpls_push_stats['counter']
                            src_add = ''
                            in_port = ''
                            dl_dst = ''
                            dl_src = ''
                            protocol = ''
                            tcp_src_port = ''
                            tcp_dst_port = ''
                            udp_src_port = ''
                            udp_dst_port = ''
                            vlan_id = ''
                            vlan_priority = ''
                            table_id = '0'
                            priority = '10'
                            paths = optimal_testbed_network_1().optimal_path(delete_links, update_link_weights)
                            shortest_path_right = paths['Shortest Path Right']
                            shortest_path_left = paths['Shortest Path Left']
                            shortest_path_right_label = ''
                            shortest_path_left_label = ''
                            for key in testbed_1_lsps:
                                if testbed_1_lsps[key] == shortest_path_right:
                                    shortest_path_right_label = key
                                if testbed_1_lsps[key] == shortest_path_left:
                                    shortest_path_left_label = key
                            for key in odl_switches_ip:
                                    if odl_switches_ip[key] == switch_id:
                                        switch_ip = key
                            if switch_ip == shortest_path_right[0]:
                                label = shortest_path_right_label
                            if switch_ip == shortest_path_left[0]:
                                label = shortest_path_left_label  
                            action_mpls_label = label
                            con_switch = testbed_1_lsps[label][1]
                            for key in testbed_1_topo[switch_ip]:
                                if testbed_1_topo[switch_ip][key] == con_switch:
                                    con_port = key
                            for key in sflow_if_map:
                                if sflow_if_map[key] == con_port:
                                    port = key
                            action_out_port = port
                            flow_stat = {}
                            flow_stat = odl.odl_mpls_push_flow_inst(url_odl, name, password, odl_header, mpls_push_flow, mpls_push_flow_counter, switch_id, dst_add, src_add, in_port, dl_dst, dl_src, protocol, tcp_src_port, tcp_dst_port, udp_src_port, udp_dst_port, vlan_id, vlan_priority, action_mpls_label, action_out_port, table_id, priority)
                            if flow_stat:
                                flow_name = flow_stat['Flow ID']
                                mpls_push_flow_stats[flow_name] = flow_stat
                                basic_connectivity_flow_stats[flow_name] = {'Switch ID': switch_id, 'IP Destination' : dst_add, 'MPLS Label' : label}
                                with open("Statistics_Logs/MPLS_Push_Flow_Stats.json", "w") as json_file:
                                    json.dump(mpls_push_flow_stats, json_file)
                                with open("Statistics_Logs/Testbed_1_Basic_Connectivity_Flow_Stats.json", "w") as json_file:
                                    json.dump(basic_connectivity_flow_stats, json_file)
                    time.sleep(timeout)
            except KeyboardInterrupt:
                print '\n\n\nSaving all the changes...'
                print '\nYou are now exiting the NaaS basic connectivity application...\n'
                sys.exit(0)
            except:
                print '\n\n\nSaving all the changes...'
                print '\nYou are now exiting the NaaS platform\'s basic connectivity application...\n'
                sys.exit(0)
            



class testbed_network_2():


    # Starting a basic connectivity application in a network with legacy switches at network core and open (i.e. OF/OVS) switches at the network edge

    def __init__(self):
            try:
                odl_base = naas_arch().odl_base_url()
                url_odl = odl_base['URL']
                ip_odl = odl_base['Host IP']
                odl_header = naas_arch().odl_api_header()
                cred = naas_arch().odl_user_cred()
                name = cred['User Name']
                password = cred['Password']
                odl_switches = naas_arch().odl_switches()
                odl_switches_ip = naas_arch().odl_switches_ip()
                testbed_2_topo = naas_arch().testbed_2_topology()
                testbed_2_lsps = naas_arch().testbed_2_path_bindings()
                sflow_if_map = naas_arch().sflow_interface_mapping()
                flow = odl_api_json_formats()
                stat = odl_api_flow_stat()
                odl = odl_api_calls()
                delete_links = {}
                update_link_weights = {}
                print '\n\nStarting the basic connectivity application...\n\n'
                print '\n\nInitializing and setting up the basic connectivity across the network...\n\n'
                print '\n\nEnter the next-hop network core legacy switch interface MAC addresses to the edge OF/OVS switches...'
                print 'Note: Default values are as per the configured testbed for my graduation project...\n\n'
                next_hop_mac = {}
                for key in odl_switches:
                    mac_add = ''
                    id_switch = odl_switches[key]
                    alias_switch = key
                    print 'Switch ID: ', id_switch
                    print 'Switch Alias Name: ', alias_switch
                    for key in odl_switches_ip:
                        ip_switch = key
                        if odl_switches_ip[key] == id_switch:
                            print 'Switch Management IP Address: ', ip_switch
                    mac_add = raw_input('Next-hop Legacy Switch Interface MAC Address to the above edge OF/OVS switch: ')
                    if mac_add == '':
                        if id_switch == 'openflow:5578350727664762986':
                            mac_add = '00:14:f6:83:30:00'
                        if id_switch == 'openflow:5578350727664762989':
                            mac_add = '00:14:f6:82:80:00'
                    next_hop_mac[id_switch] = mac_add
                    print '\n\n'
                print '\n\nEnter the end-user hosts query timeout/interval (i.e. in seconds)...\n\n'
                timeout = raw_input('End-User Hosts Query Timeout/Interval (Default Value: 10): ')
                if timeout == '':
                    timeout = 10
                timeout = int(timeout)
                print '\n\n\n'
                while True:
                    print 'Accessing the list of end-hosts that are connected to the network edge switches (i.e. OF/OVS switches)...\n\n'
                    list_hosts = odl.odl_list_hosts(url_odl, name, password)
                    i = 0
                    for hostConfig in list_hosts['hostConfig']:
                        i += 1
                        odl_switch_ip = ''
                        dst_add = hostConfig['networkAddress']
                        host_switch_id = hostConfig['nodeId']
                        for key in odl_switches:
                            if odl_switches[key] != host_switch_id:
                                switch_id = odl_switches[key]
                        print '\n\n\n'
                        print 'Detected an end-user host...'
                        print '\n'
                        print 'End-user Host - ', i
                        print 'End-user Host - Network (IP) Address: ' , hostConfig['networkAddress']
                        print 'End-user Host - Data Layer (MAC) Address: ' , hostConfig['dataLayerAddress']
                        print 'Connected to the Switch (ID): ' , hostConfig['nodeId']
                        print 'Connected to the Switch Edge (ID): ' , hostConfig['nodeConnectorId']
                        for key in odl_switches_ip:
                            if odl_switches_ip[key] == hostConfig['nodeId']:
                                odl_switch_ip = key   
                        print 'Connected to the Switch (IP) Address: ', odl_switch_ip
                        basic_connectivity_flow_stats = {}
                        installed = ''
                        with open("Statistics_Logs/Testbed_2_Basic_Connectivity_Flow_Stats.json") as json_file:
                                basic_connectivity_flow_stats = json.load(json_file)
                        for key in basic_connectivity_flow_stats:
                            if (basic_connectivity_flow_stats[key]['Switch ID'] == switch_id and basic_connectivity_flow_stats[key]['IP Destination'] == dst_add):
                                installed = 'yes'
                                print '\n\n\n***Already installed a MPLS LSP for the above end-user host through the ODL controller\'s REST API***\n\n'
                        if not installed == 'yes':
                            mpls_push_stats = {}
                            mpls_push_flow_stats = {}
                            hyb_mpls_push_flow = flow.odl_hyb_mpls_push_json()
                            mpls_push_stats = stat.odl_mpls_push_stat()
                            mpls_push_flow_stats = mpls_push_stats['stat']
                            mpls_push_flow_counter = mpls_push_stats['counter']
                            src_add = ''
                            in_port = ''
                            dl_dst = ''
                            dl_src = ''
                            protocol = ''
                            tcp_src_port = ''
                            tcp_dst_port = ''
                            udp_src_port = ''
                            udp_dst_port = ''
                            vlan_id = ''
                            vlan_priority = ''
                            table_id = '0'
                            priority = '20'
                            action_dl_dst = next_hop_mac[switch_id]
                            paths = optimal_testbed_network_2().optimal_path(delete_links, update_link_weights)
                            shortest_path_right = paths['Shortest Path Right']
                            shortest_path_left = paths['Shortest Path Left']
                            shortest_path_right_label = ''
                            shortest_path_left_label = ''
                            for key in testbed_2_lsps:
                                if testbed_2_lsps[key] == shortest_path_right:
                                    shortest_path_right_label = key
                                if testbed_2_lsps[key] == shortest_path_left:
                                    shortest_path_left_label = key
                            for key in odl_switches_ip:
                                    if odl_switches_ip[key] == switch_id:
                                        switch_ip = key
                            if switch_ip == shortest_path_right[0]:
                                label = shortest_path_right_label
                            if switch_ip == shortest_path_left[0]:
                                label = shortest_path_left_label 
                            action_mpls_label = label
                            con_switch = testbed_2_lsps[label][1]
                            for key in testbed_2_topo[switch_ip]:
                                if testbed_2_topo[switch_ip][key] == con_switch:
                                    con_port = key
                            for key in sflow_if_map:
                                if sflow_if_map[key] == con_port:
                                    port = key
                            action_out_port = port
                            flow_stat = {}
                            flow_stat = odl.odl_hyb_mpls_push_flow_inst(url_odl, name, password, odl_header, hyb_mpls_push_flow, mpls_push_flow_counter, switch_id, dst_add, src_add, in_port, dl_dst, dl_src, protocol, tcp_src_port, tcp_dst_port, udp_src_port, udp_dst_port, vlan_id, vlan_priority, action_mpls_label, action_out_port, action_dl_dst, table_id, priority)
                            if flow_stat:
                                flow_name = flow_stat['Flow ID']
                                mpls_push_flow_stats[flow_name] = flow_stat
                                basic_connectivity_flow_stats[flow_name] = {'Switch ID': switch_id, 'IP Destination' : dst_add, 'MPLS Label' : label}
                                with open("Statistics_Logs/MPLS_Push_Flow_Stats.json", "w") as json_file:
                                    json.dump(mpls_push_flow_stats, json_file)
                                with open("Statistics_Logs/Testbed_2_Basic_Connectivity_Flow_Stats.json", "w") as json_file:
                                    json.dump(basic_connectivity_flow_stats, json_file)
                    time.sleep(timeout)
            except KeyboardInterrupt:
                print '\n\n\nSaving all the changes...'
                print '\nYou are now exiting the NaaS basic connectivity application...\n'
                sys.exit(0)
            except:
                print '\n\n\nSaving all the changes...'
                print '\nYou are now exiting the NaaS platform\'s basic connectivity application...\n'
                sys.exit(0)
           





