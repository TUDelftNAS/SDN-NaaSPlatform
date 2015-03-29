#!/usr/bin/env python
# -*- coding: utf-8 -*-



# Network-as-a-Service (NaaS) platform's load balancing application



# Importing Python modules

import sys # Python module for system (i.e. interpreter) specific parameters and functions
import select # Python module for I/O completion waiting
import time # Python module to perform various time related functions



# Importing NaaS platform's main application for performing NaaS related operations and functions

from Main_App import *



# Importing NaaS platform's sFlow based edge flow monitoring application for monitoring and detecting large traffic flows at the network edge 

from sFlow_Edge_Flow_Monitoring_App import *



# Importing NaaS platform's sFlow based Core interface monitoring application for monitoring and detecting high bandwidth interface utilizations and failures in the network core of Testbed network 1 (i.e. network (i.e. edge + core) with sFlow enabled open (i.e. OF/OVS) switches)

from sFlow_Core_Interface_Monitoring_App import *



# Importing NaaS platform's SNMP based Core interface monitoring application for monitoring and detecting high bandwidth interface utilizations and failures in the network core of Testbed network 2 (i.e. network core with legacy (i.e. vendor-specific) switches)

from SNMP_Core_Interface_Monitoring_App import *



# Importing NaaS platform's optimal path computation application for optimal path computations and selections

from Optimal_Path_Computation_App import *




class load_balance_testbed_network_1():


    # Starting a load balancing application for a network (i.e. edge + core) of open (i.e. OF/OVS) switches



    def __init__(self):
            try:
                odl_base = naas_arch().odl_base_url()
                url_odl = odl_base['URL']
                ip_odl = odl_base['Host IP']
                odl_header = naas_arch().odl_api_header()
                cred = naas_arch().odl_user_cred()
                name = cred['User Name']
                password = cred['Password']
                edge_sflow_base = naas_arch().edge_sflow_base_url()
                url_edge_sflow = edge_sflow_base['URL']
                ip_edge_sflow = edge_sflow_base['Host IP']
                core_sflow_base = naas_arch().core_sflow_base_url()
                url_core_sflow = core_sflow_base['URL']
                ip_core_sflow = core_sflow_base['Host IP']
                sflow_header = naas_arch().sflow_api_header()
                odl_switches = naas_arch().odl_switches()
                odl_switches_ip = naas_arch().odl_switches_ip()
                edge_sflow_agents = naas_arch().edge_sflow_agents()
                core_sflow_agents = naas_arch().core_sflow_agents()
                testbed_1_topo = naas_arch().testbed_1_topology()
                testbed_1_lsps = naas_arch().testbed_1_path_bindings()
                sflow_if_map = naas_arch().sflow_interface_mapping()
                flow = odl_api_json_formats()
                stat = odl_api_flow_stat()
                odl = odl_api_calls()
                sflow = sflow_api_calls()
                print '\n\n\n'
                edge_flow = network_edge_flow_monitoring()
                print '\n\n\n'
                core_mon = sflow_network_core_interface_monitoring()
                while True:
                    print '\n\n\n\nEnter the above configured sFlow based edge flow monitoring application name...\n\n'
                    flow_name = raw_input('sFlow based Edge Flow Monitoring Application Name (Required): ')
                    url_sflow = url_edge_sflow
                    flow_def = sflow.sflow_flow_def(url_sflow, flow_name)
                    if flow_def == {}:
                        print '\n\nThere is no such sFlow based edge flow monitoring application that is currently running in the NaaS platform...\n\n'
                        print '\n\nRe-configure and Re-enter the sFlow based edge flow monitoring application name...\n\n'
                    else:
                        break
                flow_keys = flow_def['keys']
                keys = re.sub(r'\s', '', flow_keys).split(',')
                source_key = keys[0]
                destination_key = keys[1]
                print '\n\n\n\nEnter the priority value for this load balancing application and its corresponding actions...\n\n'
                priority_load_balance = raw_input('Load Balancing Priority Value (Default Value = 100): ')
                if priority_load_balance == '':
                    priority_load_balance = '100'
                print '\n\n\n\nEnter the load balancing query timeout/interval (i.e. in seconds)...\n\n'
                timeout = raw_input('Load Balancing Query Timeout/Interval (Default Value: 20): ')
                if timeout == '':
                    timeout = 10
                timeout = int(timeout)
                print '\n\nStarting the load balancing application...\n\n'
                while True:
                    print '\n\nQuerying for network core interface monitoring triggered events...\n\n'
                    print '\n\nChecking for Interface/Link Failures in the Network Core..\n\n'
                    delete_links = {}
                    update_link_weights = {}
                    int_failures = {}
                    high_utis = {}
                    int_failures = core_mon.int_fail_events()
                    if int_failures != {}:
                        for key in int_failures:
                            agent_node = int_failures[key]['Agent']
                            agent_interface_id = int_failures[key]['Interface ID']
                            agent_interface = sflow_if_map[agent_interface_id]
                            if delete_links != {}:
                                m = 0
                                for key in delete_links:
                                    if key == agent_node:
                                        m += 1
                                if m != 0:
                                    old_link_list = delete_links[agent_node]
                                    old_link_list.append(agent_interface)
                                    delete_links[agent_node] = old_link_list
                                else:
                                    new_link_list = []
                                    new_link_list.append(agent_interface)
                                    delete_links[agent_node] = new_link_list
                            else:
                                new_link_list = []
                                new_link_list.append(agent_interface)
                                delete_links[agent_node] = new_link_list
                        paths = optimal_testbed_network_1().optimal_path(delete_links, update_link_weights)
                        if paths != {}:
                            all_paths_right = paths['All Paths Right']
                            all_paths_left = paths['All Paths Left']
                            shortest_path_right = paths['Shortest Path Right']
                            shortest_path_left = paths['Shortest Path Left']
                            no_path_labels = []
                            shortest_path_right_label = ''
                            shortest_path_left_label = ''
                            for key in testbed_1_lsps:
                                if testbed_1_lsps[key] == shortest_path_right:
                                    shortest_path_right_label = key
                                if testbed_1_lsps[key] == shortest_path_left:
                                    shortest_path_left_label = key
                            for key in testbed_1_lsps:
                                m = 0
                                for apr in all_paths_right:
                                    if testbed_1_lsps[key] == apr:
                                        m += 1
                                for apl in all_paths_left:
                                    if testbed_1_lsps[key] == apl:
                                        m += 1
                                if m == 0:
                                    no_path_labels.append(key)
                            with open("Statistics_Logs/Testbed_1_Basic_Connectivity_Flow_Stats.json") as json_file:
                                        basic_connectivity_flow_stats = json.load(json_file)
                            installed_path_labels = []
                            deleted_path_labels = []
                            for key in basic_connectivity_flow_stats:
                                installed_path_labels.append(basic_connectivity_flow_stats[key]['MPLS Label'])
                            deleted_path_labels = set(installed_path_labels).intersection(no_path_labels)
                            deleted_flows = {}
                            for dpl in deleted_path_labels:
                                for key in basic_connectivity_flow_stats:
                                    if basic_connectivity_flow_stats[key]['MPLS Label'] == dpl:
                                        deleted_flows[key] = basic_connectivity_flow_stats[key]
                            for key in deleted_flows:
                                flow_id = key
                                mpls_push_stats = {}
                                mpls_push_flow_stats = {}
                                mpls_push_flow = flow.odl_mpls_push_json()
                                mpls_push_stats = stat.odl_mpls_push_stat()
                                mpls_push_flow_stats = mpls_push_stats['stat']
                                mpls_push_flow_counter = mpls_push_stats['counter']
                                switch_id = deleted_flows[key]['Switch ID']
                                dst_add = deleted_flows[key]['IP Destination']
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
                                    if mpls_push_flow_stats:
                                        del(mpls_push_flow_stats[flow_id])
                                        del(basic_connectivity_flow_stats[flow_id])
                                        with open("Statistics_Logs/MPLS_Push_Flow_Stats.json", "w") as json_file:
                                            json.dump(mpls_push_flow_stats, json_file)
                                        with open("Statistics_Logs/Testbed_1_Basic_Connectivity_Flow_Stats.json", "w") as json_file:
                                            json.dump(basic_connectivity_flow_stats, json_file)
                            with open("Statistics_Logs/Testbed_1_Load_Balancing_Flow_Stats.json") as json_file:
                                load_balancing_flow_stats = json.load(json_file)
                            installed_path_labels = []
                            deleted_path_labels = []
                            for key in load_balancing_flow_stats:
                                installed_path_labels.append(load_balancing_flow_stats[key]['MPLS Label'])
                            deleted_path_labels = set(installed_path_labels).intersection(no_path_labels)
                            deleted_flows = {}
                            for dpl in deleted_path_labels:
                                for key in load_balancing_flow_stats:
                                    if load_balancing_flow_stats[key]['MPLS Label'] == dpl:
                                        deleted_flows[key] = load_balancing_flow_stats[key]
                            for key in deleted_flows:
                                flow_id = key
                                mpls_push_stats = {}
                                mpls_push_flow_stats = {}
                                mpls_push_flow = flow.odl_mpls_push_json()
                                mpls_push_stats = stat.odl_mpls_push_stat()
                                mpls_push_flow_stats = mpls_push_stats['stat']
                                mpls_push_flow_counter = mpls_push_stats['counter']
                                switch_id = deleted_flows[key]['Switch ID']
                                add_src = deleted_flows[key]['Source Add']
                                add_dst = deleted_flows[key]['Destination Add']
                                priority = deleted_flows[key]['Priority']
                                with open("sFlow_ODL_Flowkeys_Bindings/Load_Balancing_Flowkeys_Bindings.json") as json_file:
                                                    load_balancing_flow_keys = json.load(json_file)
                                for key in load_balancing_flow_keys:
                                    if key == source_key:
                                        src_match_rule = load_balancing_flow_keys[key]
                                for key in load_balancing_flow_keys:
                                    if key == destination_key:
                                        dst_match_rule = load_balancing_flow_keys[key]
                                dst_add = ''
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
                                if src_match_rule == 'src_add':
                                    src_add = add_src
                                if src_match_rule == 'dl_src':
                                    dl_src = add_src
                                if src_match_rule == 'tcp_src_port':
                                    tcp_src_port = add_src
                                if src_match_rule == 'udp_src_port':
                                    udp_src_port = add_src
                                if dst_match_rule == 'dst_add':
                                    dst_add = add_dst
                                if dst_match_rule == 'dl_dst':
                                    dl_dst = add_dst
                                if dst_match_rule == 'tcp_dst_port':
                                    tcp_dst_port = add_dst
                                if dst_match_rule == 'udp_dst_port':
                                    udp_dst_port = add_dst
                                if src_match_rule == 'vlan_id':
                                    vlan_id = add_src
                                if src_match_rule == 'vlan_priority':
                                    vlan_pirority = add_src
                                if dst_match_rule == 'vlan_id':
                                    vlan_id = add_dst
                                if dst_match_rule == 'vlan_priority':
                                    vlan_pirority = add_dst
                                table_id = '0'
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
                                    load_balancing_flow_stats[flow_name] = {'Switch ID': switch_id, 'Source Add' : add_src, 'Destination Add' : add_dst, 'MPLS Label' : label, 'Priority' : priority}
                                    with open("Statistics_Logs/MPLS_Push_Flow_Stats.json", "w") as json_file:
                                        json.dump(mpls_push_flow_stats, json_file)
                                    with open("Statistics_Logs/Testbed_1_Load_Balancing_Flow_Stats.json", "w") as json_file:
                                        json.dump(load_balancing_flow_stats, json_file)
                                    if mpls_push_flow_stats:
                                        del(mpls_push_flow_stats[flow_id])
                                        del(load_balancing_flow_stats[flow_id])
                                        with open("Statistics_Logs/MPLS_Push_Flow_Stats.json", "w") as json_file:
                                            json.dump(mpls_push_flow_stats, json_file)
                                        with open("Statistics_Logs/Testbed_1_Load_Balancing_Flow_Stats.json", "w") as json_file:
                                            json.dump(load_balancing_flow_stats, json_file)
                    high_utis = core_mon.int_high_uti_events()
                    if high_utis != {}:
                        for key in high_utis:
                            agent_node = high_utis[key]['Agent']
                            agent_interface_id = high_utis[key]['Interface ID']
                            direction = high_utis[key]['Metric']
                            agent_interface = sflow_if_map[agent_interface_id]
                            links = testbed_1_topo[agent_node]
                            neighbor_node = links[agent_interface]
                            if direction == 'ifinutilization':
                                test = agent_node
                                agent_node = neighbor_node
                                neighbor_node = test
                            if update_link_weights != {}:
                                m = 0
                                for key in update_link_weights:
                                    if key == agent_node:
                                        m += 1
                                if m != 0:
                                    old_links = {}
                                    old_links = update_link_weights[agent_node]
                                    k = 0
                                    for key in old_links:
                                        if neighbor_node == key:
                                            k += 1
                                    if k == 0:
                                        old_links[neighbor_node] = 10
                                    update_link_weights[agent_node] = old_links
                                else:
                                    new_links = {}
                                    new_links[neighbor_node] = 10
                                    update_link_weights[agent_node] = new_links
                            else:
                                new_links = {}
                                new_links[neighbor_node] = 10
                                update_link_weights[agent_node] = new_links
                        paths = optimal_testbed_network_1().optimal_path(delete_links, update_link_weights)
                        if paths != {}:
                            optimal_path_right = paths['Optimal Path Right']
                            optimal_path_left = paths['Optimal Path Left']
                            optimal_path_right_label = ''
                            optimal_path_left_label = ''
                            for key in testbed_1_lsps:
                                if testbed_1_lsps[key] == optimal_path_right:
                                    optimal_path_right_label = key
                                if testbed_1_lsps[key] == optimal_path_left:
                                    optimal_path_left_label = key
                            large_flow_events = edge_flow.network_edge_large_flow_events(flow_name)
                            print large_flow_events
                            for key in large_flow_events:
                                with open("Statistics_Logs/Testbed_1_Load_Balancing_Flow_Stats.json") as json_file:
                                    load_balancing_flow_stats = json.load(json_file)
                                mpls_push_stats = {}
                                mpls_push_flow_stats = {}
                                mpls_push_flow = flow.odl_mpls_push_json()
                                mpls_push_stats = stat.odl_mpls_push_stat()
                                mpls_push_flow_stats = mpls_push_stats['stat']
                                mpls_push_flow_counter = mpls_push_stats['counter']
                                switch_ip = large_flow_events[key]['Agent']
                                add_src = large_flow_events[key]['Source Add']
                                add_dst = large_flow_events[key]['Destination Add']
                                with open("sFlow_ODL_Flowkeys_Bindings/Load_Balancing_Flowkeys_Bindings.json") as json_file:
                                                    load_balancing_flow_keys = json.load(json_file)
                                for key in load_balancing_flow_keys:
                                    if key == source_key:
                                        src_match_rule = load_balancing_flow_keys[key]
                                for key in load_balancing_flow_keys:
                                    if key == destination_key:
                                        dst_match_rule = load_balancing_flow_keys[key]
                                for key in odl_switches_ip:
                                    if key == switch_ip:
                                        switch_id = odl_switches_ip[key]
                                dst_add = ''
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
                                if src_match_rule == 'src_add':
                                    src_add = add_src
                                if src_match_rule == 'dl_src':
                                    dl_src = add_src
                                if src_match_rule == 'tcp_src_port':
                                    tcp_src_port = add_src
                                if src_match_rule == 'udp_src_port':
                                    udp_src_port = add_src
                                if dst_match_rule == 'dst_add':
                                    dst_add = add_dst
                                if dst_match_rule == 'dl_dst':
                                    dl_dst = add_dst
                                if dst_match_rule == 'tcp_dst_port':
                                    tcp_dst_port = add_dst
                                if dst_match_rule == 'udp_dst_port':
                                    udp_dst_port = add_dst
                                if src_match_rule == 'vlan_id':
                                    vlan_id = add_src
                                if src_match_rule == 'vlan_priority':
                                    vlan_pirority = add_src
                                if dst_match_rule == 'vlan_id':
                                    vlan_id = add_dst
                                if dst_match_rule == 'vlan_priority':
                                    vlan_pirority = add_dst
                                table_id = '0'
                                priority = priority_load_balance
                                for key in odl_switches_ip:
                                    if odl_switches_ip[key] == switch_id:
                                        switch_ip = key
                                if switch_ip == optimal_path_right[0]:
                                    label = optimal_path_right_label
                                if switch_ip == optimal_path_left[0]:
                                    label = optimal_path_left_label
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
                                    load_balancing_flow_stats[flow_name] = {'Switch ID': switch_id, 'Source Add' : add_src, 'Destination Add' : add_dst, 'MPLS Label' : label, 'Priority' : priority}
                                    with open("Statistics_Logs/MPLS_Push_Flow_Stats.json", "w") as json_file:
                                        json.dump(mpls_push_flow_stats, json_file)
                                    with open("Statistics_Logs/Testbed_1_Load_Balancing_Flow_Stats.json", "w") as json_file:
                                        json.dump(load_balancing_flow_stats, json_file)   
                    time.sleep(timeout)
            except KeyboardInterrupt:
                print '\n\n\nSaving all the changes...'
                print '\nYou are now exiting the NaaS sFlow based edge flow monitoring application...\n'
                sys.exit(0)
            except:
                print '\n\n\nSaving all the changes...'
                print '\nYou are now exiting the NaaS platform\'s load balancing application...\n'
                sys.exit(0)



class load_balance_testbed_network_2():


    # Starting a load balancing application for a network with legacy (i.e. vendor-specific) switches at network core and open (i.e. OF/OVS) switches at the network edge


    def __init__(self):
            try:
                odl_base = naas_arch().odl_base_url()
                url_odl = odl_base['URL']
                ip_odl = odl_base['Host IP']
                odl_header = naas_arch().odl_api_header()
                cred = naas_arch().odl_user_cred()
                name = cred['User Name']
                password = cred['Password']
                edge_sflow_base = naas_arch().edge_sflow_base_url()
                url_edge_sflow = edge_sflow_base['URL']
                ip_edge_sflow = edge_sflow_base['Host IP']
                sflow_header = naas_arch().sflow_api_header()
                core_snmp_base = naas_arch().core_snmp_base_url()
                url_core_snmp = core_snmp_base['URL']
                ip_core_snmp = core_snmp_base['Host IP']
                odl_switches = naas_arch().odl_switches()
                odl_switches_ip = naas_arch().odl_switches_ip()
                edge_sflow_agents = naas_arch().edge_sflow_agents()
                core_snmp_agents = naas_arch().core_snmp_agents()
                testbed_2_topo = naas_arch().testbed_2_topology()
                testbed_2_lsps = naas_arch().testbed_2_path_bindings()
                sflow_if_map = naas_arch().sflow_interface_mapping()
                flow = odl_api_json_formats()
                stat = odl_api_flow_stat()
                odl = odl_api_calls()
                sflow = sflow_api_calls()
                snmp = snmp_api_calls()
                print '\n\n\n'
                edge_flow = network_edge_flow_monitoring()
                print '\n\n\n'
                core_mon = snmp_network_core_interface_monitoring()
                while True:
                    print '\n\n\n\nEnter the above configured sFlow based edge flow monitoring application name...\n\n'
                    flow_name = raw_input('sFlow based Edge Flow Monitoring Application Name (Required): ')
                    url_sflow = url_edge_sflow
                    flow_def = sflow.sflow_flow_def(url_sflow, flow_name)
                    if flow_def == {}:
                        print '\n\nThere is no such sFlow based edge flow monitoring application that is currently running in the NaaS platform...\n\n'
                        print '\n\nRe-configure and Re-enter the sFlow based edge flow monitoring application name...\n\n'
                    else:
                        break
                flow_keys = flow_def['keys']
                keys = re.sub(r'\s', '', flow_keys).split(',')
                source_key = keys[0]
                destination_key = keys[1]
                print '\n\n\n\nEnter the priority value for this load balancing application and its corresponding actions...\n\n'
                priority_load_balance = raw_input('Load Balancing Priority Value (Default Value = 200): ')
                if priority_load_balance == '':
                    priority_load_balance = '200'
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
                print '\n\n\n\nEnter the load balancing query timeout/interval (i.e. in seconds)...\n\n'
                timeout = raw_input('Load Balancing Query Timeout/Interval (Default Value: 20): ')
                if timeout == '':
                    timeout = 10
                timeout = int(timeout)
                print '\n\nStarting the load balancing application...\n\n'
                while True:
                    print '\n\nQuerying for network core interface monitoring triggered events...\n\n'
                    print '\n\nChecking for Interface/Link Failures in the Network Core..\n\n'
                    delete_links = {}
                    update_link_weights = {}
                    int_failures = {}
                    high_utis = {}
                    int_failures = core_mon.int_fail_events()
                    if int_failures != {}:
                        for key in int_failures:
                            agent_node = int_failures[key]['Agent']
                            agent_interface_id = int_failures[key]['Interface ID']
                            for key in sflow_if_map:
                                if agent_interface_id == key:
                                    agent_interface = sflow_if_map[key]
                            else:
                                url_snmp = url_core_snmp
                                agent = agent_node
                                snmp_agent_interfaces = snmp.snmp_agent_interfaces(url_snmp, agent)
                                agent_interface = snmp_agent_interfaces[agent_interface_id]
                            if delete_links != {}:
                                m = 0
                                for key in delete_links:
                                    if key == agent_node:
                                        m += 1
                                if m != 0:
                                    old_link_list = delete_links[agent_node]
                                    old_link_list.append(agent_interface)
                                    delete_links[agent_node] = old_link_list
                                else:
                                    new_link_list = []
                                    new_link_list.append(agent_interface)
                                    delete_links[agent_node] = new_link_list
                            else:
                                new_link_list = []
                                new_link_list.append(agent_interface)
                                delete_links[agent_node] = new_link_list
                        paths = optimal_testbed_network_2().optimal_path(delete_links, update_link_weights)
                        if paths != {}:
                            all_paths_right = paths['All Paths Right']
                            all_paths_left = paths['All Paths Left']
                            shortest_path_right = paths['Shortest Path Right']
                            shortest_path_left = paths['Shortest Path Left']
                            no_path_labels = []
                            shortest_path_right_label = ''
                            shortest_path_left_label = ''
                            for key in testbed_2_lsps:
                                if testbed_2_lsps[key] == shortest_path_right:
                                    shortest_path_right_label = key
                                if testbed_2_lsps[key] == shortest_path_left:
                                    shortest_path_left_label = key
                            for key in testbed_2_lsps:
                                m = 0
                                for apr in all_paths_right:
                                    if testbed_2_lsps[key] == apr:
                                        m += 1
                                for apl in all_paths_left:
                                    if testbed_2_lsps[key] == apl:
                                        m += 1
                                if m == 0:
                                    no_path_labels.append(key)
                            with open("Statistics_Logs/Testbed_2_Basic_Connectivity_Flow_Stats.json") as json_file:
                                        basic_connectivity_flow_stats = json.load(json_file)
                            installed_path_labels = []
                            deleted_path_labels = []
                            for key in basic_connectivity_flow_stats:
                                installed_path_labels.append(basic_connectivity_flow_stats[key]['MPLS Label'])
                            deleted_path_labels = set(installed_path_labels).intersection(no_path_labels)
                            deleted_flows = {}
                            for dpl in deleted_path_labels:
                                for key in basic_connectivity_flow_stats:
                                    if basic_connectivity_flow_stats[key]['MPLS Label'] == dpl:
                                        deleted_flows[key] = basic_connectivity_flow_stats[key]
                            for key in deleted_flows:
                                flow_id = key
                                mpls_push_stats = {}
                                mpls_push_flow_stats = {}
                                hyb_mpls_push_flow = flow.odl_hyb_mpls_push_json()
                                mpls_push_stats = stat.odl_mpls_push_stat()
                                mpls_push_flow_stats = mpls_push_stats['stat']
                                mpls_push_flow_counter = mpls_push_stats['counter']
                                switch_id = deleted_flows[key]['Switch ID']
                                dst_add = deleted_flows[key]['IP Destination']
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
                                action_dl_dst = next_hop_mac[switch_id]
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
                                    if mpls_push_flow_stats:
                                        del(mpls_push_flow_stats[flow_id])
                                        del(basic_connectivity_flow_stats[flow_id])
                                        with open("Statistics_Logs/MPLS_Push_Flow_Stats.json", "w") as json_file:
                                            json.dump(mpls_push_flow_stats, json_file)
                                        with open("Statistics_Logs/Testbed_2_Basic_Connectivity_Flow_Stats.json", "w") as json_file:
                                            json.dump(basic_connectivity_flow_stats, json_file)
                            with open("Statistics_Logs/Testbed_2_Load_Balancing_Flow_Stats.json") as json_file:
                                load_balancing_flow_stats = json.load(json_file)
                            installed_path_labels = []
                            deleted_path_labels = []
                            for key in load_balancing_flow_stats:
                                installed_path_labels.append(load_balancing_flow_stats[key]['MPLS Label'])
                            deleted_path_labels = set(installed_path_labels).intersection(no_path_labels)
                            deleted_flows = {}
                            for dpl in deleted_path_labels:
                                for key in load_balancing_flow_stats:
                                    if load_balancing_flow_stats[key]['MPLS Label'] == dpl:
                                        deleted_flows[key] = load_balancing_flow_stats[key]
                            for key in deleted_flows:
                                flow_id = key
                                mpls_push_stats = {}
                                mpls_push_flow_stats = {}
                                hyb_mpls_push_flow = flow.odl_hyb_mpls_push_json()
                                mpls_push_stats = stat.odl_mpls_push_stat()
                                mpls_push_flow_stats = mpls_push_stats['stat']
                                mpls_push_flow_counter = mpls_push_stats['counter']
                                switch_id = deleted_flows[key]['Switch ID']
                                add_src = deleted_flows[key]['Source Add']
                                add_dst = deleted_flows[key]['Destination Add']
                                priority = deleted_flows[key]['Priority']
                                with open("sFlow_ODL_Flowkeys_Bindings/Load_Balancing_Flowkeys_Bindings.json") as json_file:
                                                    load_balancing_flow_keys = json.load(json_file)
                                for key in load_balancing_flow_keys:
                                    if key == source_key:
                                        src_match_rule = load_balancing_flow_keys[key]
                                for key in load_balancing_flow_keys:
                                    if key == destination_key:
                                        dst_match_rule = load_balancing_flow_keys[key]
                                dst_add = ''
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
                                if src_match_rule == 'src_add':
                                    src_add = add_src
                                if src_match_rule == 'dl_src':
                                    dl_src = add_src
                                if src_match_rule == 'tcp_src_port':
                                    tcp_src_port = add_src
                                if src_match_rule == 'udp_src_port':
                                    udp_src_port = add_src
                                if dst_match_rule == 'dst_add':
                                    dst_add = add_dst
                                if dst_match_rule == 'dl_dst':
                                    dl_dst = add_dst
                                if dst_match_rule == 'tcp_dst_port':
                                    tcp_dst_port = add_dst
                                if dst_match_rule == 'udp_dst_port':
                                    udp_dst_port = add_dst
                                if src_match_rule == 'vlan_id':
                                    vlan_id = add_src
                                if src_match_rule == 'vlan_priority':
                                    vlan_pirority = add_src
                                if dst_match_rule == 'vlan_id':
                                    vlan_id = add_dst
                                if dst_match_rule == 'vlan_priority':
                                    vlan_pirority = add_dst
                                table_id = '0'
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
                                action_dl_dst = next_hop_mac[switch_id]
                                flow_stat = {}
                                flow_stat = odl.odl_hyb_mpls_push_flow_inst(url_odl, name, password, odl_header, hyb_mpls_push_flow, mpls_push_flow_counter, switch_id, dst_add, src_add, in_port, dl_dst, dl_src, protocol, tcp_src_port, tcp_dst_port, udp_src_port, udp_dst_port, vlan_id, vlan_priority, action_mpls_label, action_out_port, action_dl_dst, table_id, priority)
                                if flow_stat:
                                    flow_name = flow_stat['Flow ID']
                                    mpls_push_flow_stats[flow_name] = flow_stat
                                    load_balancing_flow_stats[flow_name] = {'Switch ID': switch_id, 'Source Add' : add_src, 'Destination Add' : add_dst, 'MPLS Label' : label, 'Priority' : priority}
                                    with open("Statistics_Logs/MPLS_Push_Flow_Stats.json", "w") as json_file:
                                        json.dump(mpls_push_flow_stats, json_file)
                                    with open("Statistics_Logs/Testbed_2_Load_Balancing_Flow_Stats.json", "w") as json_file:
                                        json.dump(load_balancing_flow_stats, json_file)
                                    if mpls_push_flow_stats:
                                        del(mpls_push_flow_stats[flow_id])
                                        del(load_balancing_flow_stats[flow_id])
                                        with open("Statistics_Logs/MPLS_Push_Flow_Stats.json", "w") as json_file:
                                            json.dump(mpls_push_flow_stats, json_file)
                                        with open("Statistics_Logs/Testbed_2_Load_Balancing_Flow_Stats.json", "w") as json_file:
                                            json.dump(load_balancing_flow_stats, json_file)
                    high_utis = core_mon.int_high_uti_events()
                    if high_utis != {}:
                        for key in high_utis:
                            agent_node = high_utis[key]['Agent']
                            agent_interface_id = high_utis[key]['Interface ID']
                            direction = high_utis[key]['Metric']
                            for key in sflow_if_map:
                                if agent_interface_id == key:
                                    agent_interface = sflow_if_map[key]
                            else:
                                url_snmp = url_core_snmp
                                agent = agent_node
                                snmp_agent_interfaces = snmp.snmp_agent_interfaces(url_snmp, agent)
                                agent_interface = snmp_agent_interfaces[agent_interface_id]
                            links = testbed_2_topo[agent_node]
                            neighbor_node = links[agent_interface]
                            if direction == 'ifinutilization':
                                test = agent_node
                                agent_node = neighbor_node
                                neighbor_node = test
                            if update_link_weights != {}:
                                m = 0
                                for key in update_link_weights:
                                    if key == agent_node:
                                        m += 1
                                if m != 0:
                                    old_links = {}
                                    old_links = update_link_weights[agent_node]
                                    k = 0
                                    for key in old_links:
                                        if neighbor_node == key:
                                            k += 1
                                    if k == 0:
                                        old_links[neighbor_node] = 10
                                    update_link_weights[agent_node] = old_links
                                else:
                                    new_links = {}
                                    new_links[neighbor_node] = 10
                                    update_link_weights[agent_node] = new_links
                            else:
                                new_links = {}
                                new_links[neighbor_node] = 10
                                update_link_weights[agent_node] = new_links
                        paths = optimal_testbed_network_2().optimal_path(delete_links, update_link_weights)
                        if paths != {}:
                            optimal_path_right = paths['Optimal Path Right']
                            optimal_path_left = paths['Optimal Path Left']
                            optimal_path_right_label = ''
                            optimal_path_left_label = ''
                            for key in testbed_2_lsps:
                                if testbed_2_lsps[key] == optimal_path_right:
                                    optimal_path_right_label = key
                                if testbed_2_lsps[key] == optimal_path_left:
                                    optimal_path_left_label = key
                            large_flow_events = edge_flow.network_edge_large_flow_events(flow_name)
                            for key in large_flow_events:
                                with open("Statistics_Logs/Testbed_2_Load_Balancing_Flow_Stats.json") as json_file:
                                    load_balancing_flow_stats = json.load(json_file)
                                mpls_push_stats = {}
                                mpls_push_flow_stats = {}
                                hyb_mpls_push_flow = flow.odl_hyb_mpls_push_json()
                                mpls_push_stats = stat.odl_mpls_push_stat()
                                mpls_push_flow_stats = mpls_push_stats['stat']
                                mpls_push_flow_counter = mpls_push_stats['counter']
                                switch_ip = large_flow_events[key]['Agent']
                                add_src = large_flow_events[key]['Source Add']
                                add_dst = large_flow_events[key]['Destination Add']
                                with open("sFlow_ODL_Flowkeys_Bindings/Load_Balancing_Flowkeys_Bindings.json") as json_file:
                                                    load_balancing_flow_keys = json.load(json_file)
                                for key in load_balancing_flow_keys:
                                    if key == source_key:
                                        src_match_rule = load_balancing_flow_keys[key]
                                for key in load_balancing_flow_keys:
                                    if key == destination_key:
                                        dst_match_rule = load_balancing_flow_keys[key]
                                for key in odl_switches_ip:
                                    if key == switch_ip:
                                        switch_id = odl_switches_ip[key]
                                dst_add = ''
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
                                if src_match_rule == 'src_add':
                                    src_add = add_src
                                if src_match_rule == 'dl_src':
                                    dl_src = add_src
                                if src_match_rule == 'tcp_src_port':
                                    tcp_src_port = add_src
                                if src_match_rule == 'udp_src_port':
                                    udp_src_port = add_src
                                if dst_match_rule == 'dst_add':
                                    dst_add = add_dst
                                if dst_match_rule == 'dl_dst':
                                    dl_dst = add_dst
                                if dst_match_rule == 'tcp_dst_port':
                                    tcp_dst_port = add_dst
                                if dst_match_rule == 'udp_dst_port':
                                    udp_dst_port = add_dst
                                if src_match_rule == 'vlan_id':
                                    vlan_id = add_src
                                if src_match_rule == 'vlan_priority':
                                    vlan_pirority = add_src
                                if dst_match_rule == 'vlan_id':
                                    vlan_id = add_dst
                                if dst_match_rule == 'vlan_priority':
                                    vlan_pirority = add_dst
                                table_id = '0'
                                priority = priority_load_balance
                                for key in odl_switches_ip:
                                    if odl_switches_ip[key] == switch_id:
                                        switch_ip = key
                                if switch_ip == optimal_path_right[0]:
                                    label = optimal_path_right_label
                                if switch_ip == optimal_path_left[0]:
                                    label = optimal_path_left_label
                                action_mpls_label = label
                                con_switch = testbed_2_lsps[label][1]
                                for key in testbed_2_topo[switch_ip]:
                                    if testbed_2_topo[switch_ip][key] == con_switch:
                                        con_port = key
                                for key in sflow_if_map:
                                    if sflow_if_map[key] == con_port:
                                        port = key
                                action_out_port = port
                                action_dl_dst = next_hop_mac[switch_id]
                                flow_stat = {}
                                flow_stat = odl.odl_hyb_mpls_push_flow_inst(url_odl, name, password, odl_header, hyb_mpls_push_flow, mpls_push_flow_counter, switch_id, dst_add, src_add, in_port, dl_dst, dl_src, protocol, tcp_src_port, tcp_dst_port, udp_src_port, udp_dst_port, vlan_id, vlan_priority, action_mpls_label, action_out_port, action_dl_dst, table_id, priority)
                                if flow_stat:
                                    flow_name = flow_stat['Flow ID']
                                    mpls_push_flow_stats[flow_name] = flow_stat
                                    load_balancing_flow_stats[flow_name] = {'Switch ID': switch_id, 'Source Add' : add_src, 'Destination Add' : add_dst, 'MPLS Label' : label, 'Priority' : priority}
                                    with open("Statistics_Logs/MPLS_Push_Flow_Stats.json", "w") as json_file:
                                        json.dump(mpls_push_flow_stats, json_file)
                                    with open("Statistics_Logs/Testbed_2_Load_Balancing_Flow_Stats.json", "w") as json_file:
                                        json.dump(load_balancing_flow_stats, json_file)   
                    time.sleep(timeout)
            except KeyboardInterrupt:
                print '\n\n\nSaving all the changes...'
                print '\nYou are now exiting the NaaS sFlow based edge flow monitoring application...\n'
                sys.exit(0)
            except:
                print '\n\n\nSaving all the changes...'
                print '\nYou are now exiting the NaaS platform\'s load balancing application...\n'
                sys.exit(0)









