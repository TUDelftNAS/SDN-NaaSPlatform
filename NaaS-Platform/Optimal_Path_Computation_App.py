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



# This script requires installation of NetworkX, matplotlib, and NumPy Python modules
# NetworkX is a Python language software package for the creation, manipulation, and study of the structure, dynamics, and functions of complex networks
# Its documentation is available at https://networkx.github.io/
# matplotlib is a python 2D plotting library
# Its documentation is available at http://matplotlib.org/
# NumPy is the fundamental package for scientific computing with Python
# Its documentation is available at http://www.numpy.org/



# Network-as-a-Service (NaaS) platform's optimal path selection application



# Importing Python modules

import sys # Python module for system (i.e. interpreter) specific parameters and functions
import select # Python module for I/O completion waiting
import os # Python module for using OS dependent functionality



# Importing NetworkX Python module
# NetworkX is a Python language software package for the creation, manipulation, and study of the structure, dynamics, and functions of complex networks

import networkx as nx



# Importing matplotlib Python module
# matplotlib is a python 2D plotting library

import matplotlib.pyplot as plt



#Importing NumPy Python module
# NumPy is the fundamental package for scientific computing with Python

import numpy as np



# Importing NaaS platform's main application for performing NaaS related operations and functions

from Main_App import *




class optimal_testbed_network_1():


    # Computing optimal paths based on network core interface bandwidth utilization and operating status metrics in a network (i.e. edge + core) of open (i.e. OF/OVS) switches



    def optimal_path(self, delete_links, update_link_weights):
            try:
                npl="Path_Computation_Plots/Testbed_1/network.png"
                sppr="Path_Computation_Plots/Testbed_1/short_path_right.png"
                sppl="Path_Computation_Plots/Testbed_1/short_path_left.png"
                oppr="Path_Computation_Plots/Testbed_1/optimal_path_right.png"
                oppl="Path_Computation_Plots/Testbed_1/optimal_path_left.png"
                if os.path.isfile(npl):
                        os.remove(npl)
                else:
                    print("Error: %s file not found" % npl)
                if os.path.isfile(sppr):
                        os.remove(sppr)
                else:
                    print("Error: %s file not found" % sppr)
                if os.path.isfile(sppl):
                    os.remove(sppl)
                else:
                    print("Error: %s file not found" % sppl)
                if os.path.isfile(oppr):
                        os.remove(oppr)
                else:
                    print("Error: %s file not found" % oppr)
                if os.path.isfile(oppl):
                        os.remove(oppl)
                else:
                    print("Error: %s file not found" % oppl)
                edge_sflow_agents = naas_arch().edge_sflow_agents()
                core_sflow_agents = naas_arch().core_sflow_agents()
                testbed_1_topo = naas_arch().testbed_1_topology()
                print '\n\nStarting the optimal path computation algorithm...\n\n'
                print '\n\nThis optimal path computational algorithm uses network core interface bandwidth utilization and operating status metrics...\n\n' 
                G = nx.DiGraph()
                for key in testbed_1_topo:
                    G.add_node(key)
                for node in testbed_1_topo:
                    for key in testbed_1_topo[node]:
                        if_id = key
                        neighbor = testbed_1_topo[node][key]
                        G.add_edge(node, neighbor, key=if_id, weight=1.0)
                node_list = G.nodes()
                edge_switch_list = []
                for key in edge_sflow_agents:
                    edge_switch_list.append(edge_sflow_agents[key])
                esl = edge_switch_list
                nl = node_list
                esl[0], esl[1] = esl[1], esl[0]
                a = nl.index(esl[0])
                nl[a], nl[0] = nl[0], nl[a]
                b = nl.index(esl[1])
                ln = len(node_list)
                ln = ln - 1
                nl[b], nl[ln] = nl[ln], nl[b]
                edge_switch_list = esl
                node_list = nl
                print '\nNetwork edge switches (i.e. IP Addresses) :\n'
                i = 0
                for switch in edge_switch_list:
                    i += 1
                    print i, '.', switch
                print '\n'
                print '\nList of all the switches (i.e. edge + core) in the network (i.e. IP Addresses) :\n'
                i = 0
                for node in node_list:
                    i += 1
                    print i, '.', node
                print '\n'
                print '\nInitializing the network traffic matrix (i.e. adjacency matrix) as per the above node/switch list: \n'
                adj = nx.to_numpy_matrix(G, nodelist=node_list)
                print adj
                print '\n'
                print '\nUpdating the operational status of the links/interfaces :\n\n'
                for dl in delete_links:
                    node = ''
                    neighbor = ''
                    if_id = ''
                    node = dl
                    links = delete_links[node]
                    for link in links:
                        if_id = link
                        neighbors = G[node]
                        for ng in neighbors:
                            if neighbors[ng]['key'] == if_id:
                                neighbor = ng
                        if (node != '' and neighbor != ''):
                            print '***One of the links/intefaces in the network was reported as down/failed***'
                            print '\nLink/interface details (i.e. source - destination):'
                            print node, '-', neighbor
                            print neighbor, '-', node
                            G.remove_edge(node,neighbor)
                            G.remove_edge(neighbor,node)
                            print '\n***Interface/link Deleted From the traffic matrix***'
                            print '\n\n'
                print '\nUpdated network traffic matrix (i.e. adjacency matrix): \n'
                adj = nx.to_numpy_matrix(G, nodelist=node_list)
                print adj
                print '\n\n'
                labels = {}
                for n in G.nodes():
                    labels[n] = n
                pos = nx.spring_layout(G)
                nx.draw(G,pos,node_color='y', node_size=1000)
                nx.draw_networkx_labels(G,pos,labels)
                plt.suptitle('Network Graph', fontsize=14, fontweight='bold')
                plt.savefig("Path_Computation_Plots/Testbed_1/network.png")
                #plt.show()
                print '\nComputing the new shortest paths between the network edges based on the above updated traffic matrix...\n'
                print '\nStarting the Dijkstra\'s algorithm for computing shortest paths between the network edges...\n' 
                sp_right = nx.dijkstra_path(G,source=edge_switch_list[0],target=edge_switch_list[1])
                sp_left = nx.dijkstra_path(G,source=edge_switch_list[1],target=edge_switch_list[0])
                labels = {}
                for n in G.nodes():
                    labels[n] = n
                pos = nx.spring_layout(G)
                nx.draw(G,pos,node_color='y', node_size=1000)
                nx.draw_networkx_labels(G,pos,labels)
                spr_edges = zip(sp_right,sp_right[1:])
                nx.draw_networkx_nodes(G,pos,nodelist=sp_right,node_color='r')
                nx.draw_networkx_edges(G,pos,edgelist=spr_edges,edge_color='r',width=5)
                plt.suptitle('Computed End-to-End Shortest Path 1', fontsize=14, fontweight='bold')
                plt.savefig("Path_Computation_Plots/Testbed_1/short_path_right.png")
                plt.axis('equal')
                #plt.show()
                labels = {}
                for n in G.nodes():
                    labels[n] = n
                pos = nx.spring_layout(G)
                nx.draw(G,pos,node_color='y', node_size=1000)
                nx.draw_networkx_labels(G,pos,labels)
                spl_edges = zip(sp_left,sp_left[1:])
                nx.draw_networkx_nodes(G,pos,nodelist=sp_left,node_color='r')
                nx.draw_networkx_edges(G,pos,edgelist=spl_edges,edge_color='r',width=5)
                nx.draw_networkx_labels(G,pos, labels)
                plt.suptitle('Computed End-to-End Shortest Path 2', fontsize=14, fontweight='bold')
                plt.savefig("Path_Computation_Plots/Testbed_1/short_path_left.png")
                plt.axis('equal')
                #plt.show()
                print '\nComputed shortest paths between the edge switches: \n'
                for spr in sp_right:
                    print '|'
                    print spr
                    print '|'
                print '\n\n'
                for spl in sp_left:
                    print '|'
                    print spl
                    print '|'
                all_paths_right = []
                all_paths_left = []
                i = 0
                for asp in nx.all_simple_paths(G, source=edge_switch_list[0], target=edge_switch_list[1]):
                    i += 1
                    all_paths_right.append(asp)
                i = 0
                for asp in nx.all_simple_paths(G, source=edge_switch_list[1], target=edge_switch_list[0]):
                    i += 1
                    all_paths_left.append(asp)
                print '\n\n\nUpdating the utilizations (i.e. bandwidth consumptions) of the links/interfaces :\n\n'
                for ulw in update_link_weights:
                    node = ''
                    neighbor = ''
                    weight = ''
                    node = ulw
                    links = update_link_weights[node]
                    for l in links:
                        neighbor = l
                        weight = links[l]
                        print '***One of the links/intefaces in the network was reported with high bandwidth utilization***'
                        print '\nLink/interface details (i.e. source - destination):'
                        print node, '-', neighbor
                        G[node][neighbor]['weight'] = float(weight)
                        print '\n***Interface/link utilization (i.e. bandwidth consumption) updated in the traffic matrix***'
                        print '\n\n'
                print '\nUpdated network traffic matrix (i.e. adjacency matrix): \n'
                adj = nx.to_numpy_matrix(G, nodelist=node_list)
                print adj
                print '\n\n'
                print '\nComputing the new optimal paths between the network edges based on the above updated traffic matrix...\n'
                print '\nStarting the Dijkstra\'s algorithm for computing optimal paths between the network edges...\n' 
                op_right = nx.dijkstra_path(G,source=edge_switch_list[0],target=edge_switch_list[1])
                op_left = nx.dijkstra_path(G,source=edge_switch_list[1],target=edge_switch_list[0])
                labels = {}
                for n in G.nodes():
                    labels[n] = n
                pos = nx.spring_layout(G)
                nx.draw(G,pos,node_color='y', node_size=1000)
                nx.draw_networkx_labels(G,pos,labels)
                opr_edges = zip(op_right,op_right[1:])
                nx.draw_networkx_nodes(G,pos,nodelist=op_right,node_color='r')
                nx.draw_networkx_edges(G,pos,edgelist=opr_edges,edge_color='r',width=5)
                plt.suptitle('Computed End-to-End Optimal Path 1', fontsize=14, fontweight='bold')
                plt.savefig("Path_Computation_Plots/Testbed_1/optimal_path_right.png")
                plt.axis('equal')
                #plt.show()
                labels = {}
                for n in G.nodes():
                    labels[n] = n
                pos = nx.spring_layout(G)
                nx.draw(G,pos,node_color='y', node_size=1000)
                nx.draw_networkx_labels(G,pos,labels)
                opl_edges = zip(op_left,op_left[1:])
                nx.draw_networkx_nodes(G,pos,nodelist=op_left,node_color='r')
                nx.draw_networkx_edges(G,pos,edgelist=opl_edges,edge_color='r',width=5)
                plt.suptitle('Computed End-to-End Optimal Path 2', fontsize=14, fontweight='bold')
                plt.savefig("Path_Computation_Plots/Testbed_1/optimal_path_left.png")
                plt.axis('equal')
                #plt.show()
                print '\nComputed optimal paths between the edge switches: \n'
                for opr in op_right:
                    print '|'
                    print opr
                    print '|'
                print '\n\n'
                for opl in op_left:
                    print '|'
                    print opl
                    print '|'
                return {'All Paths Right' : all_paths_right, 'All Paths Left' : all_paths_left, 'Shortest Path Right' : sp_right, 'Shortest Path Left' : sp_left, 'Optimal Path Right' : op_right, 'Optimal Path Left' : op_left}
            except KeyboardInterrupt:
                print '\n\n\nSaving all the changes...'
                print '\nYou are now exiting the NaaS sFlow based edge flow monitoring application...\n'
                sys.exit(0)
            except:
                print '\n\n\n***ERROR***: Network edges are not reachabel\n'
                return {}



class optimal_testbed_network_2():


    # Computing optimal paths based on network core interface bandwidth utilization and operating status metrics in a network with legacy (i.e.vendor-specific) switches as the core network devices



    def optimal_path(self, delete_links, update_link_weights):
            try:
                npl="Path_Computation_Plots/Testbed_2/network.png"
                sppr="Path_Computation_Plots/Testbed_2/short_path_right.png"
                sppl="Path_Computation_Plots/Testbed_2/short_path_left.png"
                oppr="Path_Computation_Plots/Testbed_2/optimal_path_right.png"
                oppl="Path_Computation_Plots/Testbed_2/optimal_path_left.png"
                if os.path.isfile(npl):
                        os.remove(npl)
                else:
                    print("Error: %s file not found" % npl)
                if os.path.isfile(sppr):
                        os.remove(sppr)
                else:
                    print("Error: %s file not found" % sppr)
                if os.path.isfile(sppl):
                    os.remove(sppl)
                else:
                    print("Error: %s file not found" % sppl)
                if os.path.isfile(oppr):
                        os.remove(oppr)
                else:
                    print("Error: %s file not found" % oppr)
                if os.path.isfile(oppl):
                        os.remove(oppl)
                else:
                    print("Error: %s file not found" % oppl)
                edge_sflow_agents = naas_arch().edge_sflow_agents()
                core_snmp_agents = naas_arch().core_snmp_agents()
                testbed_2_topo = naas_arch().testbed_2_topology()
                print '\n\nStarting the optimal path computation algorithm...\n\n'
                print '\n\nThis optimal path computational algorithm uses network core interface bandwidth utilization and operating status metrics...\n\n' 
                G = nx.DiGraph()
                for key in testbed_2_topo:
                    G.add_node(key)
                for node in testbed_2_topo:
                    for key in testbed_2_topo[node]:
                        if_id = key
                        neighbor = testbed_2_topo[node][key]
                        G.add_edge(node, neighbor, key=if_id, weight=1.0)
                node_list = G.nodes()
                edge_switch_list = []
                for key in edge_sflow_agents:
                    edge_switch_list.append(edge_sflow_agents[key])
                esl = edge_switch_list
                nl = node_list
                esl[0], esl[1] = esl[1], esl[0]
                a = nl.index(esl[0])
                nl[a], nl[0] = nl[0], nl[a]
                b = nl.index(esl[1])
                ln = len(node_list)
                ln = ln - 1
                nl[b], nl[ln] = nl[ln], nl[b]
                c = nl.index('139.63.246.113')
                nl[c], nl[1] = nl[1], nl[c]
                d = nl.index('139.63.246.114')
                ln = len(node_list)
                ln = ln - 2
                nl[d], nl[ln] = nl[ln], nl[d]
                edge_switch_list = esl
                node_list = nl
                print '\nNetwork edge switches (i.e. IP Addresses) :\n'
                i = 0
                for switch in edge_switch_list:
                    i += 1
                    print i, '.', switch
                print '\n'
                print '\nList of all the switches (i.e. edge + core) in the network (i.e. IP Addresses) :\n'
                i = 0
                for node in node_list:
                    i += 1
                    print i, '.', node
                print '\n'
                print '\nInitializing the network traffic matrix (i.e. adjacency matrix) as per the above node/switch list: \n'
                adj = nx.to_numpy_matrix(G, nodelist=node_list)
                print adj
                print '\n'
                print '\nUpdating the operational status of the links/interfaces :\n\n'
                for dl in delete_links:
                    node = ''
                    neighbor = ''
                    if_id = ''
                    node = dl
                    links = delete_links[node]
                    for link in links:
                        if_id = link
                        neighbors = G[node]
                        for ng in neighbors:
                            if neighbors[ng]['key'] == if_id:
                                neighbor = ng
                        if (node != '' and neighbor != ''):
                            print '***One of the links/intefaces in the network was reported as down/failed***'
                            print '\nLink/interface details (i.e. source - destination):'
                            print node, '-', neighbor
                            print neighbor, '-', node
                            G.remove_edge(node,neighbor)
                            G.remove_edge(neighbor,node)
                            print '\n***Interface/link Deleted From the traffic matrix***'
                            print '\n\n'
                print '\nUpdated network traffic matrix (i.e. adjacency matrix): \n'
                adj = nx.to_numpy_matrix(G, nodelist=node_list)
                print adj
                print '\n\n'
                labels = {}
                for n in G.nodes():
                    labels[n] = n
                pos = nx.spring_layout(G)
                nx.draw(G,pos,node_color='y', node_size=1000)
                nx.draw_networkx_labels(G,pos,labels)
                plt.suptitle('Network Graph', fontsize=14, fontweight='bold')
                plt.savefig("Path_Computation_Plots/Testbed_2/network.png")
                #plt.show()
                print '\nComputing the new shortest paths between the network edges based on the above updated traffic matrix...\n'
                print '\nStarting the Dijkstra\'s algorithm for computing shortest paths between the network edges...\n' 
                sp_right = nx.dijkstra_path(G,source=edge_switch_list[0],target=edge_switch_list[1])
                sp_left = nx.dijkstra_path(G,source=edge_switch_list[1],target=edge_switch_list[0])
                labels = {}
                for n in G.nodes():
                    labels[n] = n
                pos = nx.spring_layout(G)
                nx.draw(G,pos,node_color='y', node_size=1000)
                nx.draw_networkx_labels(G,pos,labels)
                spr_edges = zip(sp_right,sp_right[1:])
                nx.draw_networkx_nodes(G,pos,nodelist=sp_right,node_color='r')
                nx.draw_networkx_edges(G,pos,edgelist=spr_edges,edge_color='r',width=5)
                plt.suptitle('Computed End-to-End Shortest Path 1', fontsize=14, fontweight='bold')
                plt.savefig("Path_Computation_Plots/Testbed_2/short_path_right.png")
                plt.axis('equal')
                #plt.show()
                labels = {}
                for n in G.nodes():
                    labels[n] = n
                pos = nx.spring_layout(G)
                nx.draw(G,pos,node_color='y', node_size=1000)
                nx.draw_networkx_labels(G,pos,labels)
                spl_edges = zip(sp_left,sp_left[1:])
                nx.draw_networkx_nodes(G,pos,nodelist=sp_left,node_color='r')
                nx.draw_networkx_edges(G,pos,edgelist=spl_edges,edge_color='r',width=5)
                nx.draw_networkx_labels(G,pos, labels)
                plt.suptitle('Computed End-to-End Shortest Path 2', fontsize=14, fontweight='bold')
                plt.savefig("Path_Computation_Plots/Testbed_2/short_path_left.png")
                plt.axis('equal')
                #plt.show()
                print '\nComputed shortest paths between the edge switches: \n'
                for spr in sp_right:
                    print '|'
                    print spr
                    print '|'
                print '\n\n'
                for spl in sp_left:
                    print '|'
                    print spl
                    print '|'
                all_paths_right = []
                all_paths_left = []
                i = 0
                for asp in nx.all_simple_paths(G, source=edge_switch_list[0], target=edge_switch_list[1]):
                    i += 1
                    all_paths_right.append(asp)
                i = 0
                for asp in nx.all_simple_paths(G, source=edge_switch_list[1], target=edge_switch_list[0]):
                    i += 1
                    all_paths_left.append(asp)
                print '\n\n\nUpdating the utilizations (i.e. bandwidth consumptions) of the links/interfaces :\n\n'
                for ulw in update_link_weights:
                    node = ''
                    neighbor = ''
                    weight = ''
                    node = ulw
                    links = update_link_weights[node]
                    for l in links:
                        neighbor = l
                        weight = links[l]
                        print '***One of the links/intefaces in the network was reported with high bandwidth utilization***'
                        print '\nLink/interface details (i.e. source - destination):'
                        print node, '-', neighbor
                        G[node][neighbor]['weight'] = float(weight)
                        print '\n***Interface/link utilization (i.e. bandwidth consumption) updated in the traffic matrix***'
                        print '\n\n'
                print '\nUpdated network traffic matrix (i.e. adjacency matrix): \n'
                adj = nx.to_numpy_matrix(G, nodelist=node_list)
                print adj
                print '\n\n'
                print '\nComputing the new optimal paths between the network edges based on the above updated traffic matrix...\n'
                print '\nStarting the Dijkstra\'s algorithm for computing optimal paths between the network edges...\n' 
                op_right = nx.dijkstra_path(G,source=edge_switch_list[0],target=edge_switch_list[1])
                op_left = nx.dijkstra_path(G,source=edge_switch_list[1],target=edge_switch_list[0])
                labels = {}
                for n in G.nodes():
                    labels[n] = n
                pos = nx.spring_layout(G)
                nx.draw(G,pos,node_color='y', node_size=1000)
                nx.draw_networkx_labels(G,pos,labels)
                opr_edges = zip(op_right,op_right[1:])
                nx.draw_networkx_nodes(G,pos,nodelist=op_right,node_color='r')
                nx.draw_networkx_edges(G,pos,edgelist=opr_edges,edge_color='r',width=5)
                plt.suptitle('Computed End-to-End Optimal Path 1', fontsize=14, fontweight='bold')
                plt.savefig("Path_Computation_Plots/Testbed_2/optimal_path_right.png")
                plt.axis('equal')
                #plt.show()
                labels = {}
                for n in G.nodes():
                    labels[n] = n
                pos = nx.spring_layout(G)
                nx.draw(G,pos,node_color='y', node_size=1000)
                nx.draw_networkx_labels(G,pos,labels)
                opl_edges = zip(op_left,op_left[1:])
                nx.draw_networkx_nodes(G,pos,nodelist=op_left,node_color='r')
                nx.draw_networkx_edges(G,pos,edgelist=opl_edges,edge_color='r',width=5)
                plt.suptitle('Computed End-to-End Optimal Path 2', fontsize=14, fontweight='bold')
                plt.savefig("Path_Computation_Plots/Testbed_2/optimal_path_left.png")
                plt.axis('equal')
                #plt.show()
                print '\nComputed optimal paths between the edge switches: \n'
                for opr in op_right:
                    print '|'
                    print opr
                    print '|'
                print '\n\n'
                for opl in op_left:
                    print '|'
                    print opl
                    print '|'
                return {'All Paths Right' : all_paths_right, 'All Paths Left' : all_paths_left, 'Shortest Path Right' : sp_right, 'Shortest Path Left' : sp_left, 'Optimal Path Right' : op_right, 'Optimal Path Left' : op_left}
            except KeyboardInterrupt:
                print '\n\n\nSaving all the changes...'
                print '\nYou are now exiting the NaaS sFlow based edge flow monitoring application...\n'
                sys.exit(0)
            except:
                print '\n\n\n***ERROR***: Network edges are not reachabel\n'
                return {}

