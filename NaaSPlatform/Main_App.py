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



# This script requires installation of a python module called Requests - It is a simple and elegant HTTP library for Python
# Its documentation is available at http://docs.python-requests.org/en/latest/



# Network-as-a-Service (NaaS) platform's main application



# Importing Python modules

import requests # Python module for oppening URLs (mostly HTTP) - It is a simple and elegant HTTP library for Python
from requests.auth import HTTPBasicAuth # For basic HTTP authentication using Python requests
import json # Python module for JSON - a lightweight data-interchange format
import re # Python module for parsing strings
import sys # Python module for system (i.e. interpreter) specific parameters and functions
import os # Python module for operating system dependent functionality
import subprocess # Python module to spawn new processes, connect to their input/output/error pipes, and obtain their return codes



class naas_config():


    # Configuring the NaaS platform and its architecture


    # Building OpenDaylight (ODL) controller's (i.e. OpenFlow based SDN controller) REST/RESTCONF API base URL

    def odl_base_url(self):
        print '\nEnter the IP address of the system/VM hosting the OpenDaylight (ODL) controller...\n'
        print 'If it is the same system/VM as this, ODL Controller IP Address = "localhost", just press the enter key\n'
        ip_odl = raw_input('ODL Controller IP Address: ')
        ip_odl = ip_odl.lower()
        if ip_odl == '':
            ip_odl = 'localhost'
        url_odl = 'http://'
        url_odl += ip_odl
        url_odl += ':8080/'
        print '\nODL controller\'s REST/RESTCONF API base URL: ' + url_odl
        print '\n'
        return {'URL' : url_odl, 'Host IP' : ip_odl}


    # Accepting user login credentials for the ODL controller

    def odl_user_cred(self):
        print '\nEnter your login credentials for the ODL controller...\n'
        print 'Default Settings: User Name = "admin", Password = "admin"\n'
        print 'Press the enter key twice, in order to use the above default values as your login credentials for the ODL controller\n'
        name = raw_input('User Name: ')
        name = name.lower()
        password = raw_input('Password: ')
        password = password.lower()
        if name == '':
            name = 'admin'
        if password == '':
            password = 'admin'
        print '\nLogged in as: ' + name
        print '\n'
        return {'User Name' : name, 'Password' : password}


    # Building network edge - sFlow-RT network analyzer's (i.e. sFlow based edge monitoring) REST API base URL

    def edge_sflow_base_url(self):
        print '\nEnter the IP address of the system/VM hosting the edge - sFlow-RT network analyzer (i.e. sFlow based network monitoring)...\n'
        print 'If it is the same system/VM as this, Edge - sFlow-RT Network Analyzer IP Address = "localhost", just press the enter key\n'
        ip_edge_sflow = raw_input('Edge - sFlow-RT Network Analyzer IP Address: ')
        ip_edge_sflow = ip_edge_sflow.lower()
        if ip_edge_sflow == '':
            ip_edge_sflow = 'localhost'
        url_edge_sflow = 'http://'
        url_edge_sflow += ip_edge_sflow
        url_edge_sflow += ':8008/'
        print '\nEdge - sFlow-RT network analyzer\'s REST API base URL: ' + url_edge_sflow
        print '\n'
        return {'URL' : url_edge_sflow, 'Host IP' : ip_edge_sflow}


    # Building network core - sFlow-RT network analyzer's (i.e. sFlow based core monitoring) REST API base URL

    def core_sflow_base_url(self):
        print '\nEnter the IP address of the system/VM hosting the core - sFlow-RT network analyzer (i.e. sFlow based network monitoring)...\n'
        print 'If it is the same system/VM as this, Core - sFlow-RT Network Analyzer IP Address = "localhost", just press the enter key\n'
        ip_core_sflow = raw_input('Core - sFlow-RT Network Analyzer IP Address: ')
        ip_core_sflow = ip_core_sflow.lower()
        if ip_core_sflow == '':
            ip_core_sflow = 'localhost'
        url_core_sflow = 'http://'
        url_core_sflow += ip_core_sflow
        url_core_sflow += ':8008/'
        print '\nCore - sFlow-RT network analyzer\'s REST API base URL: ' + url_core_sflow
        print '\n'
        return {'URL' : url_core_sflow, 'Host IP' : ip_core_sflow}


    # Building network core - SNMP network monitoring application's REST API base URL

    def core_snmp_base_url(self):
        print '\nEnter the IP address of the system/VM hosting the core - SNMP network monitoring application...\n'
        print 'If it is the same system/VM as this, Core - SNMP Network Monitoring Application IP Address = "localhost", just press the enter key\n'
        ip_core_snmp = raw_input('Core - SNMP Network Monitoring Application IP Address: ')
        ip_core_snmp = ip_core_snmp.lower()
        if ip_core_snmp == '':
            ip_core_snmp = 'localhost'
        url_core_snmp = 'http://'
        url_core_snmp += ip_core_snmp
        url_core_snmp += ':8090/'
        print '\nCore - SNMP network monitoring application\'s REST API base URL: ' + url_core_snmp
        print '\n'
        return {'URL' : url_core_snmp, 'Host IP' : ip_core_snmp}



class naas_initialize():


    # Initializing the NaaS platform and its architecture


    # Retrieving, testing, and debugging ODL controller's REST/RESTCONF API base url and the corresponding user login credentials
    
    def odl_config(self):
        try:
            base_odl = naas_config().odl_base_url() 
            url_odl = base_odl['URL']
            ip_odl = base_odl['Host IP']
            login_odl = naas_config().odl_user_cred() 
            name = login_odl['User Name']
            password = login_odl['Password']
        except KeyboardInterrupt:
            print '\n\n\nSaving all the changes...'
            print '\nYou are now exiting the NaaS main application...\n'
            sys.exit(0)
        except:
            print '\n\n\n***ERROR***: Found an exception, restart the application in order to check and debug the errors/exceptions...\n'
            print '\n\n\nSaving all the changes...'
            print '\nYou are now exiting the NaaS main application...\n'
            sys.exit(0)
        while True:
            try:
                url = url_odl
                url += 'controller/nb/v2/connectionmanager/nodes'
                response = requests.get(url, auth = (name, password))
                if response.status_code == 200:
                    print '\nCan succesfully reach the ODL controller running in the above configured host system/vm (IP:' , ip_odl ,')\n'
                    print '\n'
                    break
                elif response.status_code != 200:
                    print '\n***ERROR***: Invalid user login credentials for the ODL controller...\n'
                    print 'Re-enter the user login credentials for the ODL controller...\n'
                    login_odl = naas_config().odl_user_cred() 
                    name = login_odl['User Name']
                    password = login_odl['Password']
                    print '\n'
            except KeyboardInterrupt:
                print '\n\n\nSaving all the changes...'
                print '\nYou are now exiting the NaaS main application...\n'
                sys.exit(0)
            except:
                print '\n***ERROR***: Can not reach the ODL controller running in the above configured host system/vm (IP:' , ip_odl ,'), check if the ODL controller is running and configured properly...\n'
                print 'Re-enter the ODL controller\'s configuration details...\n'
                try:
                    base_odl = naas_config().odl_base_url() 
                    url_odl = base_odl['URL']
                    ip_odl = base_odl['Host IP']
                    print '\n'
                except KeyboardInterrupt:
                    print '\n\n\nSaving all the changes...'
                    print '\nYou are now exiting the NaaS main application...\n'
                    sys.exit(0)
                except:
                    print '\n\n\n***ERROR***: Found an exception, restart the application in order to check and debug the errors/exceptions...\n'
                    print '\n\n\nSaving all the changes...'
                    print '\nYou are now exiting the NaaS main application...\n'
                    sys.exit(0)
            try:
                print 'Do you wish to try re-connecting to the ODL controller or exit the application ?\n'
                while True:
                    print 'Default value = ¨yes¨\n'
                    choice = raw_input('Reconnect (¨yes¨/¨no¨): ')
                    choice = choice.lower()
                    if (choice == 'yes' or choice == '' or choice == 'y'):
                        break
                    elif (choice == 'no' or choice == 'n'):
                        sys.exit(0)
                    else:
                        print '\nInvalid entry!!\n'
            except KeyboardInterrupt:
                print '\n\n\nSaving all the changes...'
                print '\nYou are now exiting the NaaS main application...\n'
                sys.exit(0)
            except:
                print '\n\n\nSaving all the changes...'
                print '\nYou are now exiting the NaaS main application...\n'
                sys.exit(0)
            print'\n'
        odl_config = {}
        odl_config = {'URL' : url_odl, 'Host IP' : ip_odl, 'User Name' : name, 'Password' : password}
        with open("Statistics_Logs/ODL_Config.json", "w") as json_file:
            json.dump(odl_config, json_file)


    # Retrieving, testing, and debugging edge - sFlow-RT network analyzer's REST API base url
    
    def edge_sflow_config(self):
        try:
            base_edge_sflow = naas_config().edge_sflow_base_url() 
            url_edge_sflow = base_edge_sflow['URL']
            ip_edge_sflow = base_edge_sflow['Host IP']
        except KeyboardInterrupt:
            print '\n\n\nSaving all the changes...'
            print '\nYou are now exiting the NaaS main application...\n'
            sys.exit(0)
        except:
            print '\n\n\n***ERROR***: Found an exception, restart the application in order to check and debug the errors/exceptions...\n'
            print '\n\n\nSaving all the changes...'
            print '\nYou are now exiting the NaaS main application...\n'
            sys.exit(0)
        while True:
            try:
                response = requests.get(url_edge_sflow)
                if response.status_code == 200:
                    print '\nCan succesfully reach the edge - sFlow-RT network analyzer running in the above configured host system/vm (IP:' , ip_edge_sflow ,')\n'
                    print '\n'
                    break
            except KeyboardInterrupt:
                print '\n\n\nSaving all the changes...'
                print '\nYou are now exiting the NaaS main application...\n'
                sys.exit(0)
            except:
                print '\n***ERROR***: Can not reach the edge - sFlow-RT network analyzer running in the above configured host system/vm (IP:' , ip_edge_sflow ,'), check if the sFlow-RT network analyzer is running and configured properly...\n'
                print 'Re-enter the edge - sFlow-RT network analyzer\'s configuration details...\n'
                try:
                    base_edge_sflow = naas_config().edge_sflow_base_url() 
                    url_edge_sflow = base_edge_sflow['URL']
                    ip_edge_sflow = base_edge_sflow['Host IP']
                    print '\n'
                except KeyboardInterrupt:
                    print '\n\nSaving all the changes...'
                    print '\nYou are now exiting the NaaS main application...\n'
                    sys.exit(0)
                except:
                    print '\n\n\n***ERROR***: Found an exception, restart the application in order to check and debug the errors/exceptions...\n'
                    print '\n\n\nSaving all the changes...'
                    print '\nYou are now exiting the NaaS main application...\n'
                    sys.exit(0)
            try:
                print 'Do you wish to try re-connecting to the edge - sFlow-RT network analyzer or exit the application ?\n'
                while True:
                    print 'Default value = ¨yes¨\n'
                    choice = raw_input('Reconnect (¨yes¨/¨no¨): ')
                    choice = choice.lower()
                    if (choice == 'yes' or choice == '' or choice == 'y'):
                        break
                    elif (choice == 'no' or choice == 'n'):
                        sys.exit(0)
                    else:
                        print '\nInvalid entry!!\n'
            except KeyboardInterrupt:
                print '\n\n\nSaving all the changes...'
                print '\nYou are now exiting the NaaS main application...\n'
                sys.exit(0)
            except:
                print '\n\n\nSaving all the changes...'
                print '\nYou are now exiting the NaaS main application...\n'
                sys.exit(0)
            print'\n'
        edge_sflow_config = {}
        edge_sflow_config = {'URL' : url_edge_sflow, 'Host IP' : ip_edge_sflow}
        with open("Statistics_Logs/Edge_sFlow_Config.json", "w") as json_file:
            json.dump(edge_sflow_config, json_file)


    # Retrieving, testing, and debugging core - sFlow-RT network analyzer's REST API base url
    
    def core_sflow_config(self):
        try:
            base_core_sflow = naas_config().core_sflow_base_url() 
            url_core_sflow = base_core_sflow['URL']
            ip_core_sflow = base_core_sflow['Host IP']
        except KeyboardInterrupt:
            print '\n\n\nSaving all the changes...'
            print '\nYou are now exiting the NaaS main application...\n'
            sys.exit(0)
        except:
            print '\n\n\n***ERROR***: Found an exception, restart the application in order to check and debug the errors/exceptions...\n'
            print '\n\n\nSaving all the changes...'
            print '\nYou are now exiting the NaaS main application...\n'
            sys.exit(0)
        while True:
            try:
                response = requests.get(url_core_sflow)
                if response.status_code == 200:
                    print '\nCan succesfully reach the core - sFlow-RT network analyzer running in the above configured host system/vm (IP:' , ip_core_sflow ,')\n'
                    print '\n'
                    break
            except KeyboardInterrupt:
                print '\n\n\nSaving all the changes...'
                print '\nYou are now exiting the NaaS main application...\n'
                sys.exit(0)
            except:
                print '\n***ERROR***: Can not reach the core - sFlow-RT network analyzer running in the above configured host system/vm (IP:' , ip_core_sflow ,'), check if the sFlow-RT network analyzer is running and configured properly...\n'
                print 'Re-enter the core - sFlow-RT network analyzer\'s configuration details...\n'
                try:
                    base_core_sflow = naas_config().core_sflow_base_url() 
                    url_core_sflow = base_core_sflow['URL']
                    ip_core_sflow = base_core_sflow['Host IP']
                    print '\n'
                except KeyboardInterrupt:
                    print '\n\nSaving all the changes...'
                    print '\nYou are now exiting the NaaS main application...\n'
                    sys.exit(0)
                except:
                    print '\n\n\n***ERROR***: Found an exception, restart the application in order to check and debug the errors/exceptions...\n'
                    print '\n\n\nSaving all the changes...'
                    print '\nYou are now exiting the NaaS main application...\n'
                    sys.exit(0)
            try:
                print 'Do you wish to try re-connecting to the core - sFlow-RT network analyzer or exit the application ?\n'
                while True:
                    print 'Default value = ¨yes¨\n'
                    choice = raw_input('Reconnect (¨yes¨/¨no¨): ')
                    choice = choice.lower()
                    if (choice == 'yes' or choice == '' or choice == 'y'):
                        break
                    elif (choice == 'no' or choice == 'n'):
                        sys.exit(0)
                    else:
                        print '\nInvalid entry!!\n'
            except KeyboardInterrupt:
                print '\n\n\nSaving all the changes...'
                print '\nYou are now exiting the NaaS main application...\n'
                sys.exit(0)
            except:
                print '\n\n\nSaving all the changes...'
                print '\nYou are now exiting the NaaS main application...\n'
                sys.exit(0)
            print'\n'
        core_sflow_config = {}
        core_sflow_config = {'URL' : url_core_sflow, 'Host IP' : ip_core_sflow}
        with open("Statistics_Logs/Core_sFlow_Config.json", "w") as json_file:
            json.dump(core_sflow_config, json_file)


    # Retrieving, testing, and debugging core - SNMP network monitoring application's REST API base url
    
    def core_snmp_config(self):
        try:
            base_core_snmp = naas_config().core_snmp_base_url() 
            url_core_snmp = base_core_snmp['URL']
            ip_core_snmp = base_core_snmp['Host IP']
        except KeyboardInterrupt:
            print '\n\n\nSaving all the changes...'
            print '\nYou are now exiting the NaaS main application...\n'
            sys.exit(0)
        except:
            print '\n\n\n***ERROR***: Found an exception, restart the application in order to check and debug the errors/exceptions...\n'
            print '\n\n\nSaving all the changes...'
            print '\nYou are now exiting the NaaS main application...\n'
            sys.exit(0)
        while True:
            try:
                response = requests.get(url_core_snmp)
                if response.status_code == 200:
                    print '\nCan succesfully reach the core - SNMP network monitoring application running in the above configured host system/vm (IP Address:' , ip_core_snmp ,')\n'
                    print '\n'
                    break
            except KeyboardInterrupt:
                print '\n\n\nSaving all the changes...'
                print '\nYou are now exiting the NaaS main application...\n'
                sys.exit(0)
            except:
                print '\n***ERROR***: Can not reach the core - SNMP network monitoring application running in the above configured host system/vm (IP:' , ip_core_snmp ,'), check if the SNMP network monitoring application is running and configured properly...\n'
                print 'Re-enter the core - SNMP network monitoring application\'s configuration details...\n'
                try:
                    base_core_snmp = naas_config().core_snmp_base_url() 
                    url_core_snmp = base_core_snmp['URL']
                    ip_core_snmp = base_core_snmp['Host IP']
                    print '\n'
                except KeyboardInterrupt:
                    print '\n\nSaving all the changes...'
                    print '\nYou are now exiting the NaaS main application...\n'
                    sys.exit(0)
                except:
                    print '\n\n\n***ERROR***: Found an exception, restart the application in order to check and debug the errors/exceptions...\n'
                    print '\n\n\nSaving all the changes...'
                    print '\nYou are now exiting the NaaS main application...\n'
                    sys.exit(0)
            try:
                print 'Do you wish to try re-connecting to the core - SNMP network monitoring application or exit the application ?\n'
                while True:
                    print 'Default value = ¨yes¨\n'
                    choice = raw_input('Reconnect (¨yes¨/¨no¨): ')
                    choice = choice.lower()
                    if (choice == 'yes' or choice == '' or choice == 'y'):
                        break
                    elif (choice == 'no' or choice == 'n'):
                        sys.exit(0)
                    else:
                        print '\nInvalid entry!!\n'
            except KeyboardInterrupt:
                print '\n\n\nSaving all the changes...'
                print '\nYou are now exiting the NaaS main application...\n'
                sys.exit(0)
            except:
                print '\n\n\nSaving all the changes...'
                print '\nYou are now exiting the NaaS main application...\n'
                sys.exit(0)
            print'\n'
        core_snmp_config = {}
        core_snmp_config = {'URL' : url_core_snmp, 'Host IP' : ip_core_snmp}
        with open("Statistics_Logs/Core_SNMP_Config.json", "w") as json_file:
            json.dump(core_snmp_config, json_file)



class naas_arch():


    # Retrieving the key configured NaaS platform and architectural information - for the following JSON files, go to the folder NaaS_Platform/Statistics_Logs/


    # ODL controller's REST/RESTCONF API base url with its host system/VM's IP address 
    
    def odl_base_url(self):
        with open("Statistics_Logs/ODL_Config.json") as json_file:
            odl_config = {}
            odl_config = json.load(json_file)
            url_odl = odl_config['URL']
            ip_odl = odl_config['Host IP']
            return {'URL' : url_odl, 'Host IP' : ip_odl}


    # For assigning JSON related ODL controller's REST/RESTCONF API header information

    def odl_api_header(self):
        odl_header = {'content-type':'application/json', 'accept':'application/json'}
        return odl_header


    # User login credentials for the ODL controller
    
    def odl_user_cred(self):
        with open("Statistics_Logs/ODL_Config.json") as json_file:
            odl_config = {}
            odl_config = json.load(json_file)
            name = odl_config['User Name']
            password = odl_config['Password']
            return {'User Name' : name, 'Password' : password}


    # Edge - sFlow-RT network analyzer's REST API base url with its host system/VM's IP address 

    def edge_sflow_base_url(self):
        with open("Statistics_Logs/Edge_sFlow_Config.json") as json_file:
            edge_sflow_config = {}
            edge_sflow_config = json.load(json_file)
            url_edge_sflow = edge_sflow_config['URL']
            ip_edge_sflow = edge_sflow_config['Host IP']
            return {'URL' : url_edge_sflow, 'Host IP' : ip_edge_sflow}


    # Core - sFlow-RT network analyzer's REST API base url with its host system/VM's IP address 

    def core_sflow_base_url(self):
        with open("Statistics_Logs/Core_sFlow_Config.json") as json_file:
            core_sflow_config = {}
            core_sflow_config = json.load(json_file)
            url_core_sflow = core_sflow_config['URL']
            ip_core_sflow = core_sflow_config['Host IP']
            return {'URL' : url_core_sflow, 'Host IP' : ip_core_sflow}


    # For assigning JSON related sFlow-RT network analyzer's REST API header information

    def sflow_api_header(self):
        sflow_header = {'content-type':'application/json'}
        return sflow_header


    # Core - SNMP network monitoring application's REST API base url with its host system/VM's IP address 

    def core_snmp_base_url(self):
        with open("Statistics_Logs/Core_SNMP_Config.json") as json_file:
            core_snmp_config = {}
            core_snmp_config = json.load(json_file)
            url_core_snmp = core_snmp_config['URL']
            ip_core_snmp = core_snmp_config['Host IP']
            return {'URL' : url_core_snmp, 'Host IP' : ip_core_snmp}


    # List of connected OF/OVS (i.e. OpenFlow/Open vSwitch) switches to the ODL controller, along with their configured alias names

    def odl_switches(self):
        with open("Statistics_Logs/ODL_Switches_List.json") as json_file:
            odl_switches = {}
            odl_switches = json.load(json_file)
            return odl_switches

    
    # Configured management IP addresses of the underlying OF/OVS (i.e. OpenFlow/Open vSwitch) switches that are connected to the ODL controller

    def odl_switches_ip(self):
        with open("Statistics_Logs/ODL_Switches_IP.json") as json_file:
            odl_switches_ip = {}
            odl_switches_ip = json.load(json_file)
            return odl_switches_ip


    # List of connected network edge sFlow agents (i.e. switches with sFlow support in their hardware, e.g most of the currently available OF/OVS physical switches) to the edge - sFlow-RT network analyzer, along with their configured alias names

    def edge_sflow_agents(self):
        with open("Statistics_Logs/Edge_sFlow_Agents_List.json") as json_file:
            edge_sflow_agents = {}
            edge_sflow_agents = json.load(json_file)
            return edge_sflow_agents


    # List of connected network core sFlow agents (i.e. switches with sFlow support in their hardware, e.g most of the currently available OF/OVS physical switches) to the core - sFlow-RT network analyzer, along with their configured alias names

    def core_sflow_agents(self):
        with open("Statistics_Logs/Core_sFlow_Agents_List.json") as json_file:
            core_sflow_agents = {}
            core_sflow_agents = json.load(json_file)
            return core_sflow_agents


    # List of connected network core SNMP agents (i.e. legacy switches) to the core - SNMP network monitoring application, along with their configured alias names

    def core_snmp_agents(self):
        with open("Statistics_Logs/Core_SNMP_Agents_List.json") as json_file:
            core_snmp_agents = {}
            core_snmp_agents = json.load(json_file)
            return core_snmp_agents


    # Network topology of testbed network - 1 (i.e. network (i.e. core + edge) with open (i.e. OF/OVS) switches)

    def testbed_1_topology(self):
        with open("Network_Topology/Testbed_1.json") as json_file:
            testbed_1_topo = {}
            testbed_1_topo = json.load(json_file)
            return testbed_1_topo


    # Network topology of testbed network - 2 (i.e. network core with legacy (i.e. vendor-specific) switches and network edge with open (i.e. OF/OVS) switches)

    def testbed_2_topology(self):
        with open("Network_Topology/Testbed_2.json") as json_file:
            testbed_2_topo = {}
            testbed_2_topo = json.load(json_file)
            return testbed_2_topo


    # Ingress MPLS push label (i.e. at network edge) to path bindings (i.e. static network core LSPs) of testbed network - 1 (i.e. network (i.e. core + edge) with open (i.e. OF/OVS) switches)

    def testbed_1_path_bindings(self):
        with open("MPLS_Push_Label_Path_Bindings/Testbed_1.json") as json_file:
            testbed_1_lsps = {}
            testbed_1_lsps = json.load(json_file)
            return testbed_1_lsps


    # Ingress MPLS push label (i.e. at network edge) to path bindings (i.e. static network core LSPs) of testbed network - 2 (i.e. network core with legacy (i.e. vendor-specific) switches and network edge with open (i.e. OF/OVS) switches)

    def testbed_2_path_bindings(self):
        with open("MPLS_Push_Label_Path_Bindings/Testbed_2.json") as json_file:
            testbed_2_lsps = {}
            testbed_2_lsps = json.load(json_file)
            return testbed_2_lsps


    # sFlow interface index to physical interface name mapping in open (i.e. OF/OVS) switches

    def sflow_interface_mapping(self):
        with open("Network_Topology/sFlow_Interface_Index_Mapping.json") as json_file:
            sflow_if_map = {}
            sflow_if_map = json.load(json_file)
            return sflow_if_map



class odl_api_json_formats():


    # Retrieving the JSON formats for flow insertions/installations through the ODL controller's REST/RESTCONF APIs - for the following JSON files, go to the folder NaaS_Platform/JSON_Files_for_Flow_Installations/


    # JSON format for installing static flows in the underlying OF/OVS switch flow tables

    def odl_static_json(self):
        with open("JSON_Files_for_Flow_Installations/Static_Flow.json") as json_file: 
            static_flow = json.load(json_file)
        return static_flow


    # JSON format for installing MPLS push flows in the underlying OF/OVS switch flow tables

    def odl_mpls_push_json(self):
        with open("JSON_Files_for_Flow_Installations/MPLS_Push_Flow.json") as json_file: 
            mpls_push_flow = json.load(json_file)
        return mpls_push_flow


    # JSON format for installing MPLS push flows in the underlying OF/OVS switch flow tables in the case of a hybrid MPLS network with legacy (i.e. vendor-specific) switches/routers as the MPLS LSRs

    def odl_hyb_mpls_push_json(self):
        with open("JSON_Files_for_Flow_Installations/Hybrid_MPLS_Push_Flow.json") as json_file: 
            hybrid_mpls_push_flow = json.load(json_file)
        return hybrid_mpls_push_flow



class odl_api_flow_stat():


    # Retrieving the statistics of the flows that are installed through the ODL controller's REST/RESTCONF APIs - for the following JSON files, go to the folder NaaS_Platform/Statistics_Logs/


    # For retrieving the statistics of the installed static flows in the underlying OF/OVS switch flow tables

    def odl_static_stat(self):
        with open("Statistics_Logs/Static_Flow_Stats.json") as json_file: 
            static_flow_stats = {}
            static_flow_stats = json.load(json_file)
            if static_flow_stats:
                count = []
                for key in static_flow_stats:
                    c = map(int, re.findall('\d+', key))
                    count += c
                static_flow_counter = max(count)
                static_flow_counter += 1
            else:
                static_flow_counter = 1
        return {'stat' : static_flow_stats, 'counter' : static_flow_counter}


    # For retrieving the statistics of the installed MPLS push flows in the underlying OF/OVS switch flow tables

    def odl_mpls_push_stat(self):
        with open("Statistics_Logs/MPLS_Push_Flow_Stats.json") as json_file:
            mpls_push_flow_stats = {}
            mpls_push_flow_stats = json.load(json_file)
            if mpls_push_flow_stats:
                count = []
                for key in mpls_push_flow_stats:
                    c = map(int, re.findall('\d+', key))
                    count += c
                mpls_push_flow_counter = max(count)
                mpls_push_flow_counter += 1
            else:
                mpls_push_flow_counter = 100
        return {'stat' : mpls_push_flow_stats, 'counter' : mpls_push_flow_counter}



class odl_api_calls():


    # ODL controller's REST/RESTCONF API calls:


    # For the list of connected OF/OVS switches to the ODL controller

    def odl_list_conn(self, url_odl, name, password):
        print '\n\nConnecting to the ODL controller through its REST API...\n'
        url = url_odl
        url += 'controller/nb/v2/connectionmanager/nodes'
        print 'URL:', url
        print '\n'
        response = requests.get(url, auth = (name, password))
        if response.status_code != 200:
            print '\n***ERROR***: Unable to communicate with the ODL controller through its REST API, check if the ODL controller is running and configured properly\n'
            print '\nError response from the ODL controller:', response
            print '\n'
            print response.headers
            print '\n'        
        else:
            print '\nCan succesfully communicate with the ODL controller through its REST API...\n'
            print '\nList of connected switches to the ODL controller:\n'
            list_conn = response.json()
            if list_conn == {}:
                print '\n\n***ERROR***: There are no connected OF/OVS switches to the ODL controller \n'
                print 'Check and debug the connections between the OF/OVS switches and the ODL controller\n'
                print '\n\nDo you wish to continue or exit the application ?\n'
                while True:
                    print 'Default value = ¨yes¨\n'
                    choice = raw_input('Continue (¨yes¨/¨no¨): ')
                    choice = choice.lower()
                    if (choice == 'yes' or choice == '' or choice == 'y'):
                        break
                    elif (choice == 'no' or choice == 'n'):
                        sys.exit(0)
                    else:
                        print '\nInvalid entry!!\n'
                print '\n\n'
            else:
                odl_switches = []
                for node in list_conn['node']:
                    print 'Switch ID: ' + node['id']
                    print 'Connection Type: ' + node['type']
                    odl_switches.append(node['id'])
                    print '\n'
                print '\n'
                return odl_switches


    # For showing the underlying OF/OVS switch topology

    def odl_topo(self, url_odl, name, password):
        print '\n\nConnecting to the ODL controller through its REST API...\n'
        url = url_odl
        url += 'controller/nb/v2/topology/default'
        print 'URL:', url
        print '\n'
        response = requests.get(url, auth = (name, password))
        if response.status_code != 200:
            print '\n***ERROR***: Unable to communicate with the ODL controller through its REST API, check if the ODL controller is running and configured properly...\n'
            print '\nError response from the ODL controller:', response
            print '\n'
            print response.headers
            print '\n'
        else:
            print '\nCan succesfully communicate with the ODL controller through its REST API...\n'
            print '\nUnderlying OF/OVS topology:\n'
            topo = response.json()
            if topo['edgeProperties'] == []:
                print '\n\n***EMPTY***\n'
            else:
                try:
                    i = 1
                    for edgeProperties in topo['edgeProperties']:
                        print 'Edge - ', i
                        print 'Switch ID: ' + edgeProperties['edge']['tailNodeConnector']['node']['id']
                        print 'Edge ID: ' + edgeProperties['edge']['tailNodeConnector']['id']
                        print 'Connected to Switch (ID): ' + edgeProperties['edge']['headNodeConnector']['node']['id']
                        print 'Connected to Switch Edge (ID): ' + edgeProperties['edge']['headNodeConnector']['id']
                        #print 'Edge Bandwidth: ' , edgeProperties['properties']['bandwidth']['value']
                        print 'Edge Time Stamp: ' , edgeProperties['properties']['timeStamp']['value']
                        i += 1
                        print '\n'
                except:
                    print '\n\n***ERROR***: Problem retrieving the remaining details, check and debug this REST API call\n'


    # For listing all the connected OF/OVS switches and their properties

    def odl_switch_prop(self, url_odl, name, password):
        print '\n\nConnecting to the ODL controller through its REST API...\n'
        url = url_odl
        url += 'controller/nb/v2/switchmanager/default/nodes'
        print 'URL:', url
        print '\n'
        response = requests.get(url, auth = (name, password))
        if response.status_code != 200:
            print '\n***ERROR***: Unable to communicate with the ODL controller through its REST API, check if the ODL controller is running and configured properly...\n'
            print '\nError response from the ODL controller:', response
            print '\n'
            print response.headers
            print '\n'
        else:
            print '\nCan succesfully communicate with the ODL controller through its REST API...\n'
            print '\nList of all underlying OF/OVS switches and their properties:\n'
            switch_prop = response.json()
            if switch_prop['nodeProperties'] == []:
                print '\n\n***EMPTY***\n'
            else:
                try:
                    for nodeProperties in switch_prop['nodeProperties']:
                        print 'Switch ID: ' , nodeProperties['node']['id']
                        print 'Switch MAC Address: ' , nodeProperties['properties']['macAddress']['value']
                        print 'Switch Tables: ' , nodeProperties['properties']['tables']['value']
                        print 'Switch Forwarding: ' , nodeProperties['properties']['forwarding']['value']
                        print 'Switch Time Stamp: ' , nodeProperties['properties']['timeStamp']['value']
                        print 'Switch Buffers: ' , nodeProperties['properties']['buffers']['value']
                        print 'Switch Capabilities: ' , nodeProperties['properties']['capabilities']['value']
                        print '\n'
                except:
                    print '\n\n***ERROR***: Problem retrieving the remaining details, check and debug this REST API call\n'


    # For listing all the connected end-user hosts to the underlying OF/OVS switches along with their configurations

    def odl_list_hosts(self, url_odl, name, password):
        print '\n\nConnecting to the ODL controller through its REST API...\n'
        url = url_odl
        url += 'controller/nb/v2/hosttracker/default/hosts/active'
        print 'URL:', url
        print '\n'
        response = requests.get(url, auth = (name, password))
        if response.status_code != 200:
            print '\n***ERROR***: Unable to communicate with the ODL controller through its REST API, check if the ODL controller is running and configured properly...\n'
            print '\nError response from the ODL controller:', response
            print '\n'
            print response.headers
            print '\n'
        else:
            print '\nCan succesfully communicate with the ODL controller through its REST API...\n'
            print '\nList of all the connected end-user hosts to the underlying OF/OVS switches along with their configurations:\n'
            list_hosts = response.json()
            if list_hosts['hostConfig'] == []:
                print '\n\n***EMPTY***\n'
            else:
                i = 1
                for hostConfig in list_hosts['hostConfig']:
                    print 'End-user Host - ', i
                    print 'End-user Host - Network (IP) Address: ' , hostConfig['networkAddress']
                    print 'End-user Host - Data Layer (MAC) Address: ' , hostConfig['dataLayerAddress']
                    print 'Connected to the Switch (ID): ' , hostConfig['nodeId']
                    print 'Connected to the Switch Edge (ID): ' , hostConfig['nodeConnectorId']
                    print 'VLAN ID: ' , hostConfig['vlan']
                    print 'Host Type - Static Host: ' , hostConfig['staticHost']
                    i += 1
                    print '\n'
            return list_hosts


    # For listing all the installed flows in the underlying OF/OVS switches along with their statistics

    def odl_flow_stat(self, url_odl, name, password):
        print '\n\nConnecting to the ODL controller through its REST API...\n'
        url = url_odl
        url += 'controller/nb/v2/statistics/default/flow'
        print 'URL:', url
        print '\n'
        response = requests.get(url, auth = (name, password))
        if response.status_code != 200:
            print '\n***ERROR***: Unable to communicate with the ODL controller through its REST API, check if the ODL controller is running and configured properly...\n'
            print '\nError response from the ODL controller:', response
            print '\n'
            print response.headers
            print '\n'
        else:
            print '\nCan succesfully communicate with the ODL controller through its REST API...\n'
            print '\nList of all the installed flows along with their statistics:\n'
            flow_stat = response.json()
            if flow_stat['flowStatistics'] == []:
                print '\n\n***EMPTY***\n'
            else:
                for flowStatistics in flow_stat['flowStatistics']:
                    print '\nSwitch ID: ' , flowStatistics['node']['id']
                    print '\n'
                    i = 1
                    if not flowStatistics['flowStatistic']:
                        print '\n\n***EMPTY***\n\n'
                    else:
                        for flowStatistic in flowStatistics['flowStatistic']:
                            print 'Flow - ', i
                            j = 1
                            k = 1
                            print 'Table ID: ' , flowStatistic['tableId']
                            print 'Duration in Seconds: ' , flowStatistic['durationSeconds']
                            print 'Packet Count: ' , flowStatistic['packetCount']
                            print 'Byte Count: ' , flowStatistic['byteCount']
                            for matchField in flowStatistic['flow']['match']['matchField']:
                                print 'Match Field - ', j
                                print 'Match Field Type: ' , matchField['type']
                                print 'Match Field value: ' , matchField['value']
                                j += 1
                            for actions in flowStatistic['flow']['actions']:
                                print 'Action - ', k
                                print 'Action Type: ' , actions['type']
                                print 'Action Value: ' , actions['port']['id']
                                k += 1
                            print 'Priority: ' , flowStatistic['flow']['priority']
                            print 'Idle Timeout: ' , flowStatistic['flow']['idleTimeout']
                            print 'Hard Timeout: ' , flowStatistic['flow']['hardTimeout']
                            i += 1
                            print '\n'
                        print '\n'
                        print '\n'


    # For listing all the available ports in the underlying OF/OVS switches along with their statistics

    def odl_port_stat(self, url_odl, name, password):
        print '\n\nConnecting to the ODL controller through its REST API...\n'
        url = url_odl
        url += 'controller/nb/v2/statistics/default/port'
        print 'URL:', url
        print '\n'
        response = requests.get(url, auth = (name, password))
        if response.status_code != 200:
            print '\n***ERROR***: Unable to communicate with the ODL controller through its REST API, check if the ODL controller is running and configured properly...\n'
            print '\nError response from the ODL controller:', response
            print '\n'
            print response.headers
            print '\n' 
        else:
            print '\nCan succesfully communicate with the ODL controller through its REST API...\n'
            print '\nList of all the available ports in the underlying OF/OVS switches along with their statistics\n'
            port_stat = response.json()
            if port_stat['portStatistics'] == []:
                print '\n\n***EMPTY***\n'
            else:
                for portStatistics in port_stat['portStatistics']:
                    print '\nSwitch ID: ' , portStatistics['node']['id']
                    print '\n'
                    if not portStatistics['portStatistic']:
                        print '\n\n***EMPTY***\n\n'
                    else:
                        for portStatistic in portStatistics['portStatistic']:
                            print 'Port ID: ' , portStatistic['nodeConnector']['id']
                            print 'Recieved Packets: ' , portStatistic['receivePackets']
                            print 'Transmitted Packets: ' , portStatistic['transmitPackets']
                            print 'Recieved Bytes: ' , portStatistic['receiveBytes']
                            print 'Transmitted Bytes: ' , portStatistic['transmitBytes']
                            print 'Received Packet Drops: ' , portStatistic['receiveDrops']
                            print 'Transmitted Packet Drops' , portStatistic['transmitDrops']
                            print 'Received Packet Errors' , portStatistic['receiveErrors']
                            print 'Transmitted Packet Errors' , portStatistic['transmitErrors']
                            print 'Received Frame Error' , portStatistic['receiveFrameError']
                            print 'Received OverRun Error' , portStatistic['receiveOverRunError']
                            print 'Received Crc Error' , portStatistic['receiveCrcError']
                            print 'Collision Count' , portStatistic['collisionCount']
                            print '\n'
                        print '\n'
                        print '\n'


    # For listing all the available flow tables in the underlying OF/OVS switches along with their statistics

    def odl_table_stat(self, url_odl, name, password):
        print '\n\nConnecting to the ODL controller through its REST API...\n'
        url = url_odl
        url += 'controller/nb/v2/statistics/default/table'
        print 'URL:', url
        print '\n'
        response = requests.get(url, auth = (name, password))
        if response.status_code != 200:
            print '\n***ERROR***: Unable to communicate with the ODL controller through its REST API, check if the ODL controller is running and configured properly...\n'
            print '\nError response from the ODL controller:', response
            print '\n'
            print response.headers
            print '\n'
        else:
            print '\nCan succesfully communicate with the ODL controller through its REST API...\n'
            print '\nList of all the available flow tables in the underlying OF/OVS switches along with their statistics\n'
            table_stat = response.json()
            if table_stat['tableStatistics'] == []:
                print '\n\n***EMPTY***\n'
            else:
                for tableStatistics in table_stat['tableStatistics']:
                    print '\nSwitch ID: ' , tableStatistics['node']['id']
                    print '\n'
                    if not tableStatistics['tableStatistic']:
                        print '\n\n***EMPTY***\n\n'
                    else:
                        for tableStatistic in tableStatistics['tableStatistic']:
                            print 'Active Count: ' , tableStatistic['activeCount']
                            print 'Lookup Count: ' , tableStatistic['lookupCount']
                            print 'Matched Count: ' , tableStatistic['matchedCount']
                            print 'Maximum Entries: ' , tableStatistic['maximumEntries']
                            print '\n'
                        print '\n'
                        print '\n'


    # For installing static flows in the underlying OF/OVS switch flow tables through the ODL controller's REST API

    def odl_static_flow_inst(self, url_odl, name, password, odl_header, static_flow, static_flow_counter, switch_id, dst_add, src_add, in_port, dl_dst, dl_src, protocol, src_port, dst_port, vlan_id, vlan_priority, action, priority):
        print '\n\nConnecting to the ODL controller through its REST API...\n'
        url = url_odl
        url += 'controller/nb/v2/flowprogrammer/default/node/MD_SAL/'
        url += switch_id
        url += '/staticFlow/'
        flow_name = 'flow'
        flow_name += `static_flow_counter`
        url += flow_name
        sf = static_flow
        sf['name'] = flow_name
        sf['node']['id'] = switch_id
        if dst_add == '':
            del(sf['nwDst'])
        else:
            sf['nwDst'] = dst_add
        if src_add == '':
            del(sf['nwSrc'])
        else:
            sf['nwSrc'] = src_add
        if in_port == '':
            del(sf['ingressPort'])
        else:
            port = switch_id
            port += ':'
            port += in_port
            in_port = port
            sf['ingressPort'] = in_port
        if dl_dst == '':
            del(sf['dlDst'])
        else:
            sf['dlDst'] = dl_dst
        if dl_src == '':
            del(sf['dlSrc'])
        else:
            sf['dlSrc'] = dl_src
        if src_port == '':
            del(sf['tpSrc'])
        else:
            sf['tpSrc'] = src_port
        if dst_port == '':
            del(sf['tpDst'])
        else:
            sf['tpDst'] = dst_port
        if protocol == '':
            del(sf['protocol'])
        else:
            sf['protocol'] = protocol
        if vlan_id == '':
            del(sf['vlanId'])
        else:
            sf['vlanId'] = vlan_id
        if vlan_priority == '':
            del(sf['vlanPriority'])
        else:
            sf['vlanPriority'] = vlan_priority
        sf['actions'] = action
        sf['priority'] = priority
        print 'URL:', url
        print '\n'
        response = requests.put(url, data = json.dumps(sf), headers = odl_header, auth = (name, password))
        if (response.status_code != 201 and response.status_code != 200):
            print '\n***ERROR***: verify the flow instalation details and re-enter them...\n'
            print '\nError response from the ODL controller:', response
            print '\n'
            print response.headers
            print '\n'
        else:
            act = action.pop()
            match = []
            match.extend((dst_add, src_add, in_port, dl_dst, dl_src, protocol, src_port, dst_port, vlan_id, vlan_priority))
            print '\nSuccesfully installed the flow...\n'
            print '\nFlow Installation Detalis: \n'
            print 'Match fields Notation/order: ' + '(1.Dst IP Add, 2.Src IP Add, 3.In Port ID, 4. Dst MAC Add, 5. Src MAC Add, 6.Protocol, 7.Src Port, 8.Dst Port, 9.VLAN ID, 10.VLAN Prio)\n'
            print 'Switch ID: ' + switch_id
            print 'Flow Name: ' + flow_name
            print 'Priority: ' + priority
            print 'Action Field: ' + act
            print 'Match fields: '
            i = 1
            for mf in match:
                print i , '.', '%s' %mf
                i += 1
            print '\n'
            return {'Switch ID' : switch_id, 'Flow Name' : flow_name, 'Match Fields' : match, 'Action Field' : act, 'Priority' : priority}


    # For deleting/un-installing static flows in the underlying OF/OVS switch flow tables through the ODL controller's REST API

    def odl_static_flow_del(self, url_odl, name, password, switch_id, flow_name):
        print '\n\nConnecting to the ODL controller through its REST API...\n'
        url = url_odl
        url += 'controller/nb/v2/flowprogrammer/default/node/MD_SAL/'
        url += switch_id
        url += '/staticFlow/'
        url += flow_name
        print 'URL:', url
        print '\n'
        response = requests.delete(url, auth = (name, password))
        if (response.status_code != 204 and response.status_code != 200):
            print '\n***ERROR***: verify the flow deletion/un-installation details and re-enter them...\n'
            print '\nError response from the ODL controller:', response
            print '\n'
            print response.headers
            print '\n'
        else:
            print '\nSuccesfully uninstalled the flow...\n'
            print '\nFlow deletion/un-Installation Detalis: \n'
            print 'Switch ID: ' + switch_id
            print 'Flow name: ' + flow_name
            print '\n'
            return flow_name


    # For installing MPLS push flows in the underlying OF/OVS switch flow tables through the ODL controller's RESTCONF API

    def odl_mpls_push_flow_inst(self, url_odl, name, password, odl_header, mpls_push_flow, mpls_push_flow_counter, switch_id, dst_add, src_add, in_port, dl_dst, dl_src, protocol, tcp_src_port, tcp_dst_port, udp_src_port, udp_dst_port, vlan_id, vlan_priority, action_mpls_label, action_out_port, table_id, priority):
        print '\n\nConnecting to the ODL controller through its REST/RESTCONF API...\n'
        url = url_odl
        url += 'restconf/config/opendaylight-inventory:nodes/node/'
        url += switch_id
        url += '/table/'
        url += table_id
        url += '/flow/'
        flow_id = mpls_push_flow_counter
        url += `flow_id`
        pmf = mpls_push_flow
        pmf['flow']['id'] = mpls_push_flow_counter
        pmf['flow']['priority'] = priority
        if dst_add == '':
            del(pmf['flow']['match']['ipv4-destination'])
        else:
            pmf['flow']['match']['ipv4-destination'] = dst_add
        if src_add == '':
            del(pmf['flow']['match']['ipv4-source'])
        else:
            pmf['flow']['match']['ipv4-source'] = src_add
        if in_port == '':
            del(pmf['flow']['match']['in-port'])
        else:
            pmf['flow']['match']['in-port'] = in_port
        if dl_dst == '':
            del(pmf['flow']['match']['ethernet-match']['ethernet-destination'])
        else:
            pmf['flow']['match']['ethernet-match']['ethernet-destination']['address'] = dl_dst
        if dl_src == '':
            del(pmf['flow']['match']['ethernet-match']['ethernet-source'])
        else:
            pmf['flow']['match']['ethernet-match']['ethernet-source']['address'] = dl_src
        if protocol == '':
            del(pmf['flow']['match']['ip-match'])
        else:
            pmf['flow']['match']['ip-match']['ip-protocol'] = protocol
        if tcp_src_port == '':
            del(pmf['flow']['match']['tcp-source-port'])
        else:
            pmf['flow']['match']['tcp-source-port'] = tcp_src_port
        if tcp_dst_port == '':
            del(pmf['flow']['match']['tcp-destination-port'])
        else:
            pmf['flow']['match']['tcp-destination-port'] = tcp_dst_port
        if udp_src_port == '':
            del(pmf['flow']['match']['udp-source-port'])
        else:
            pmf['flow']['match']['udp-source-port'] = udp_src_port
        if udp_dst_port == '':
            del(pmf['flow']['match']['udp-destination-port'])
        else:
            pmf['flow']['match']['udp-destination-port'] = udp_dst_port
        if vlan_id == '':
            del(pmf['flow']['match']['vlan-match'])
        else:
            pmf['flow']['match']['vlan-match']['vlan-id']['vlan-id'] = vlan_id
            if vlan_priority == '':
                del(pmf['flow']['match']['vlan-match']['vlan-pcp'])
            else:
                pmf['flow']['match']['vlan-match']['vlan-pcp'] = vlan_priority
        for act in pmf['flow']['instructions']['instruction']['apply-actions']['action']:
            if act['order'] == '0':
                act['push-mpls-action']['ethernet-type'] = '34887'
            if act['order'] == '1':
                act['set-field']['protocol-match-fields']['mpls-label'] = action_mpls_label
            if act['order'] == '2':
                act['output-action']['output-node-connector'] = action_out_port
        print 'URL:', url
        print '\n'
        response = requests.put(url, data = json.dumps(pmf), headers = odl_header, auth = (name, password))
        if (response.status_code != 201 and response.status_code != 200):
            print '\n***ERROR***: verify the flow instalation details and re-enter them...\n'
            print '\nError response from the ODL controller:', response
            print '\n'
            print response.headers
            print '\n'
        else:
            print '\nSuccesfully installed the flow...\n'
            print '\nFlow Installation Detalis: \n'
            print 'Switch ID: ' + switch_id
            print 'Flow ID: ' , flow_id
            print 'Priority: ' + priority
            print 'Action Fields: '
            print '1', '.', 'Push MPLS Label = ' , action_mpls_label
            print '2', '.', 'Output/Egress Switch Port = ' , action_out_port
            print 'Match fields: '
            print '1', '.', 'Destination IP Address = ' , dst_add
            print '2', '.', 'Source IP Address = ' , src_add
            print '3', '.', 'Ingress/Input Switch Port = ' , in_port
            print '4', '.', 'Destination MAC Address = ' , dl_dst
            print '5', '.', 'Source MAC Address = ' , dl_src
            print '6', '.', 'Protocol Number = ' , protocol
            print '7', '.', 'TCP Source Port = ' , tcp_src_port
            print '8', '.', 'TCP Destination Port = ' , tcp_dst_port
            print '9', '.', 'UDP Source Port = ' , udp_src_port
            print '10', '.', 'UDP Destination Port = ' , udp_dst_port
            print '11', '.', 'VLAN ID = ' , vlan_id
            print '12', '.', 'VLAN Priority = ' , vlan_priority
            flow_id = str(flow_id)
            return {'Switch ID' : switch_id, 'Flow ID' : flow_id, 'MPLS Label' : action_mpls_label, 'Out Port' : action_out_port, 'Dst IP Add' : dst_add, 'Src IP Add' : src_add, 'In Port' : in_port, 'Dl Dst Add' : dl_dst, 'Dl Src Add' : dl_src, 'Protocol' : protocol, 'TCP Src Port' : tcp_src_port, 'TCP Dst Port' : tcp_dst_port, 'UDP Src Port' : udp_src_port, 'UDP Dst Port' : udp_dst_port, 'VLAN ID' : vlan_id, 'VLAN Priority' : vlan_priority, 'Table ID' : table_id, 'Priority' : priority}


    # For installing above MPLS push flows in the case of a hybrid MPLS network with legacy (i.e. vendor-specific) switches/routers as its LSRs

    def odl_hyb_mpls_push_flow_inst(self, url_odl, name, password, odl_header, hyb_mpls_push_flow, mpls_push_flow_counter, switch_id, dst_add, src_add, in_port, dl_dst, dl_src, protocol, tcp_src_port, tcp_dst_port, udp_src_port, udp_dst_port, vlan_id, vlan_priority, action_mpls_label, action_out_port, action_dl_dst, table_id, priority):
        print '\n\nConnecting to the ODL controller through its REST/RESTCONF API...\n'
        url = url_odl
        url += 'restconf/config/opendaylight-inventory:nodes/node/'
        url += switch_id
        url += '/table/'
        url += table_id
        url += '/flow/'
        flow_id = mpls_push_flow_counter
        url += `flow_id`
        hpmf = hyb_mpls_push_flow
        hpmf['flow']['id'] = mpls_push_flow_counter
        hpmf['flow']['priority'] = priority
        if dst_add == '':
            del(hpmf['flow']['match']['ipv4-destination'])
        else:
            hpmf['flow']['match']['ipv4-destination'] = dst_add
        if src_add == '':
            del(hpmf['flow']['match']['ipv4-source'])
        else:
            hpmf['flow']['match']['ipv4-source'] = src_add
        if in_port == '':
            del(hpmf['flow']['match']['in-port'])
        else:
            hpmf['flow']['match']['in-port'] = in_port
        if dl_dst == '':
            del(hpmf['flow']['match']['ethernet-match']['ethernet-destination'])
        else:
            hpmf['flow']['match']['ethernet-match']['ethernet-destination']['address'] = dl_dst
        if dl_src == '':
            del(hpmf['flow']['match']['ethernet-match']['ethernet-source'])
        else:
            hpmf['flow']['match']['ethernet-match']['ethernet-source']['address'] = dl_src
        if protocol == '':
            del(hpmf['flow']['match']['ip-match'])
        else:
            hpmf['flow']['match']['ip-match']['ip-protocol'] = protocol
        if tcp_src_port == '':
            del(hpmf['flow']['match']['tcp-source-port'])
        else:
            hpmf['flow']['match']['tcp-source-port'] = tcp_src_port
        if tcp_dst_port == '':
            del(hpmf['flow']['match']['tcp-destination-port'])
        else:
            hpmf['flow']['match']['tcp-destination-port'] = tcp_dst_port
        if udp_src_port == '':
            del(hpmf['flow']['match']['udp-source-port'])
        else:
            hpmf['flow']['match']['udp-source-port'] = udp_src_port
        if udp_dst_port == '':
            del(hpmf['flow']['match']['udp-destination-port'])
        else:
            hpmf['flow']['match']['udp-destination-port'] = udp_dst_port
        if vlan_id == '':
            del(hpmf['flow']['match']['vlan-match'])
        else:
            hpmf['flow']['match']['vlan-match']['vlan-id']['vlan-id'] = vlan_id
            if vlan_priority == '':
                del(hpmf['flow']['match']['vlan-match']['vlan-pcp'])
            else:
                hpmf['flow']['match']['vlan-match']['vlan-pcp'] = vlan_priority
        for act in hpmf['flow']['instructions']['instruction']['apply-actions']['action']:
            if act['order'] == '0':
                act['push-mpls-action']['ethernet-type'] = '34887'
            if act['order'] == '1':
                act['set-field']['protocol-match-fields']['mpls-label'] = action_mpls_label
            if act['order'] == '2':
                act['set-field']['ethernet-match']['ethernet-destination']['address'] = action_dl_dst
            if act['order'] == '3':
                act['output-action']['output-node-connector'] = action_out_port
        print 'URL:', url
        print '\n'
        response = requests.put(url, data = json.dumps(hpmf), headers = odl_header, auth = (name, password))
        if (response.status_code != 201 and response.status_code != 200):
            print '\n***ERROR***: verify the flow instalation details and re-enter them...\n'
            print '\nError response from the ODL controller:', response
            print '\n'
            print response.headers
            print '\n'
        else:
            print '\nSuccesfully installed the flow...\n'
            print '\nFlow Installation Detalis: \n'
            print 'Switch ID: ' + switch_id
            print 'Flow ID: ' , flow_id
            print 'Priority: ' + priority
            print 'Action Fields: '
            print '1', '.', 'Push MPLS Label = ' , action_mpls_label
            print '2', '.', 'Output/Egress Switch Port = ' , action_out_port
            print 'Match fields: '
            print '1', '.', 'Destination IP Address = ' , dst_add
            print '2', '.', 'Source IP Address = ' , src_add
            print '3', '.', 'Ingress/Input Switch Port = ' , in_port
            print '4', '.', 'Destination MAC Address = ' , dl_dst
            print '5', '.', 'Source MAC Address = ' , dl_src
            print '6', '.', 'Protocol Number = ' , protocol
            print '7', '.', 'TCP Source Port = ' , tcp_src_port
            print '8', '.', 'TCP Destination Port = ' , tcp_dst_port
            print '9', '.', 'UDP Source Port = ' , udp_src_port
            print '10', '.', 'UDP Destination Port = ' , udp_dst_port
            print '11', '.', 'VLAN ID = ' , vlan_id
            print '12', '.', 'VLAN Priority = ' , vlan_priority
            flow_id = str(flow_id)
            return {'Switch ID' : switch_id, 'Flow ID' : flow_id, 'MPLS Label' : action_mpls_label, 'Out Port' : action_out_port, 'Dst IP Add' : dst_add, 'Src IP Add' : src_add, 'In Port' : in_port, 'Dl Dst Add' : dl_dst, 'Dl Src Add' : dl_src, 'Protocol' : protocol, 'TCP Src Port' : tcp_src_port, 'TCP Dst Port' : tcp_dst_port, 'UDP Src Port' : udp_src_port, 'UDP Dst Port' : udp_dst_port, 'VLAN ID' : vlan_id, 'VLAN Priority' : vlan_priority, 'Table ID' : table_id, 'Priority' : priority}


    # For deleting/un-installing MPLS push flows in the underlying OF/OVS switch flow tables through the ODL controller's RESTCONF API

    def odl_mpls_push_flow_del(self, url_odl, name, password, switch_id, flow_id, table_id):
        print '\n\nConnecting to the ODL controller through its REST/RESTCONF API...\n'
        url = url_odl
        url += 'restconf/config/opendaylight-inventory:nodes/node/'
        url += switch_id
        url += '/table/'
        url += table_id
        url += '/flow/'
        url += flow_id
        print 'URL:', url
        print '\n'
        response = requests.delete(url, auth = (name, password))
        if (response.status_code != 204 and response.status_code != 200):
            print '\n***ERROR***: verify the flow deletion/un-installation details and re-enter them...\n'
            print '\nError response from the ODL controller:', response
            print '\n'
            print response.headers
            print '\n'
        else:
            print '\nSuccesfully uninstalled the flow...\n'
            print '\nFlow deletion/un-Installation Detalis: \n'
            print 'Switch ID: ' + switch_id
            print 'Flow ID: ' , flow_id
            print 'Table ID: ' + table_id
            print '\n'
            return flow_id



class sflow_api_calls():


    # sFlow-RT network analyzer's REST API calls (i.e. for both edge and cores - sFlow-RT network analyzers):


    # For the list of statistics describing sFlow-RT network analyzer's performance

    def sflow_perform(self, url_sflow):
        print '\n\nConnecting to the sFlow-RT network analyzer through its REST API...\n'
        url = url_sflow
        url += 'analyzer/json'
        print 'URL:', url
        print '\n'
        response = requests.get(url)
        if response.status_code != 200:
            print '\n***ERROR***: Unable to communicate with the sFlow-RT network analyzer through its REST API, check if the sFlow-RT network analyzer is running and configured properly...\n'
            print '\nError response from the sFlow-RT network analyzer:', response
            print '\n'
            print response.headers
            print '\n'
        else:
            print '\nCan succesfully communicate with the sFlow-RT network analyzer through its REST API...\n'
            print '\nstatistics describing sFlow-RT network analyzer performance:\n'
            sflow_stat = response.json()
            print 'Uptime:', sflow_stat['uptime']
            print 'sFlow Agents:', sflow_stat['sFlowAgents']
            print 'sFlow Bytes Received:', sflow_stat['sFlowBytesReceived']
            print 'sFlow Datagrams Received:', sflow_stat['sFlowDatagramsReceived']
            print 'sFlow Datagrams Discarded:', sflow_stat['sFlowDatagramsDiscarded']
            print 'sFlow Parse Errors:', sflow_stat['sFlowParseErrors']
            print 'Generated Events:', sflow_stat['eventsGenerated']
            print 'Lost Events:', sflow_stat['eventsLost']
            print 'Generated Flows:', sflow_stat['flowsGenerated']
            print 'Lost Flows:', sflow_stat['flowsLost']
            print '\n'


    # For the list of connected sFlow agents to the sFlow-RT network analyzer, along with their statistics

    def sflow_agents(self, url_sflow):
        print '\n\nConnecting to the sFlow-RT network analyzer through its REST API...\n'
        url = url_sflow
        url += 'agents/json'
        print 'URL:', url
        print '\n'
        response = requests.get(url)
        if response.status_code != 200:
            print '\n***ERROR***: Unable to communicate with the sFlow-RT network analyzer through its REST API, check if the sFlow-RT network analyzer is running and configured properly...\n'
            print '\nError response from the sFlow-RT network analyzer:', response
            print '\n'
            print response.headers
            print '\n'
        else:
            print '\nCan succesfully communicate with the sFlow-RT network analyzer through its REST API...\n'
            print '\nList of sFlow agents that are connected to the sFlow-RT network analyzer, along with their statistics:\n'
            agents = response.json()
            if agents == {}:
                print '\n\n***ERROR***: There are no connected sFlow agents (i.e. OF/OVS switches) to the sFlow-RT network analyzer\n'
                print 'Check and debug the connections between the sFlow agents (i.e. OF/OVS switches) and the sFlow-RT network analyzer\n'
                print '\n\nDo you wish to continue or exit the application ?\n'
                while True:
                    print 'Default value = ¨yes¨\n'
                    choice = raw_input('Continue (¨yes¨/¨no¨): ')
                    choice = choice.lower()
                    if (choice == 'yes' or choice == '' or choice == 'y'):
                        break
                    elif (choice == 'no' or choice == 'n'):
                        sys.exit(0)
                    else:
                        print '\nInvalid entry !!\n'
                print '\n\n'
            else:
                i = 1
                sflow_agents = []
                for a in agents:
                    print 'Agent ', i, ':\n'
                    print 'IP Address: ', a
                    print 'Uptime:', agents[a]['uptime']
                    print 'sFlow Datagrams Received:', agents[a]['sFlowDatagramsReceived']
                    print 'sFlow Datagrams Lost:', agents[a]['sFlowDatagramsLost']
                    print 'sFlow Datagrams Out of Order:', agents[a]['sFlowDatagramsOutOfOrder']
                    print 'sFlow Datagrams Duplicates:', agents[a]['sFlowDatagramsDuplicates']
                    sflow_agents.append(a)
                    i += 1
                    print '\n'
                print '\n'
                return sflow_agents


    # For the list of currently active sFlow metrics in the sflow agents

    def sflow_metrics(self, url_sflow):
        print '\n\nConnecting to the sFlow-RT network analyzer through its REST API...\n'
        url = url_sflow
        url += 'metrics/json'
        print 'URL:', url
        print '\n'
        response = requests.get(url)
        if response.status_code != 200:
            print '\n***ERROR***: Unable to communicate with the sFlow-RT network analyzer through its REST API, check if the sFlow-RT network analyzer is running and configured properly...\n'
            print '\nError response from the sFlow-RT network analyzer:', response
            print '\n'
            print response.headers
            print '\n'
        else:
            print '\nCan succesfully communicate with the sFlow-RT network analyzer through its REST API...\n'
            print '\nList of currently active sFlow metrics :\n'
            metrics = response.json()
            if metrics == {}:
                print '\n\n***EMPTY***\n'
            else:
                i = 1
                for m in metrics:
                    print 'Metric ', i, ':', m
                    i += 1
                print '\n'


    # For the sFlow metric values of a sFlow agent(s)

    def sflow_metric_values(self, url_sflow, agent, metric):
        print '\n\nConnecting to the sFlow-RT network analyzer through its REST API...\n'
        url = url_sflow
        url += 'dump/'
        url += agent
        url += '/'
        url += metric
        url += '/json'
        print 'URL:', url
        print '\n'
        response = requests.get(url)
        if response.status_code != 200:
            print '\n***ERROR***: verify the input details and re-enter them...\n'
            print '\nError response from the sFlow-RT network analyzer:', response
            print '\n'
            print response.headers
            print '\n'
        else:
            print '\nCan succesfully communicate with the sFlow-RT network analyzer through its REST API...\n'
            print '\nsFlow metric values of a sFlow agent(s):\n'
            metric_values = response.json()
            if metric_values == []:
                print '\n\n***EMPTY***\n'
            else:
                for mvs in metric_values:
                    print 'Metric Name: ', mvs['metricName']
                    print 'Metric Value: ', mvs['metricValue']
                    print 'Interface ID: ', mvs['dataSource']
                    print 'Agent IP Address: ', mvs['agent']
                    print '\n'
                print '\n'
        return response


    # For the list of interfaces of a sFlow agent(s)

    def sflow_interfaces(self, url_sflow, agent):
        print '\n\nConnecting to the sFlow-RT network analyzer through its REST API...\n'
        url = url_sflow
        url += 'dump/'
        url += agent
        url += '/ifindex/json'
        print 'URL:', url
        print '\n'
        response = requests.get(url)
        if response.status_code != 200:
            print '\n***ERROR***: verify the input details and re-enter them...\n'
            print '\nError response from the sFlow-RT network analyzer:', response
            print '\n'
            print response.headers
            print '\n'
        else:
            print '\nCan succesfully communicate with the sFlow-RT network analyzer through its REST API...\n'
            print '\nList of interfaces of a sFlow agent(s):\n'
            interface = response.json()
            if interface == []:
                print '\n\n***EMPTY***\n'
            else:
                for i in interface:
                    print 'Interface ID: ', i['dataSource']
                    print 'Agent IP Address: ', i['agent']
                    print '\n'
                print '\n'
            return interface


    # For the sFlow metric value of a sFlow agent's interface

    def sflow_interface_metric_value(self, url_sflow, agent, interface, metric):
        print '\n\nConnecting to the sFlow-RT network analyzer through its REST API...\n'
        url = url_sflow
        url += 'metric/'
        url += agent
        url += '/'
        url += interface
        url += '.'
        url += metric
        url += '/json'
        print 'URL:', url
        print '\n'
        response = requests.get(url)
        if response.status_code != 200:
            print '\n***ERROR***: verify the input details and re-enter them...\n'
            print '\nError response from the sFlow-RT network analyzer:', response
            print '\n'
            print response.headers
            print '\n'
        else:
            print '\nCan succesfully communicate with the sFlow-RT network analyzer through its REST API...\n'
            print '\nsFlow metric value of a sFlow agent\'s interface:\n'
            metric_value = response.json()
            if metric_value == []:
                print '\n\n***EMPTY***\n'
            else:
                try:
                    for mv in metric_value:
                        print 'Metric Name: ', mv['metricName']
                        print 'Metric Value: ', mv['metricValue']
                        print 'Interface ID: ', mv['dataSource']
                        print 'Agent IP Address: ', mv['agent']
                        print '\n'
                except:
                    print 'None'
        return response


    # For the list of currently active sFlow flow keys

    def sflow_flowkeys(self, url_sflow):
        print '\n\nConnecting to the sFlow-RT network analyzer through its REST API...\n'
        url = url_sflow
        url += 'flowkeys/json'
        print 'URL:', url
        print '\n'
        response = requests.get(url)
        if response.status_code != 200:
            print '\n***ERROR***: Unable to communicate with the sFlow-RT network analyzer through its REST API, check if the sFlow-RT network analyzer is running and configured properly...\n'
            print '\nError response from the sFlow-RT network analyzer:', response
            print '\n'
            print response.headers
            print '\n'
        else:
            print '\nCan succesfully communicate with the sFlow-RT network analyzer through its REST API...\n'
            print '\nList of currently active sFlow flow keys :\n'
            flowkeys = response.json()
            if flowkeys == {}:
                print '\n\n***EMPTY***\n'
            else:
                i = 1
                for fk in flowkeys:
                    print 'Flow Key ', i, ':', fk
                    i += 1
                print '\n'


    # For the list of configured sFlow flow definitions 

    def sflow_flows(self, url_sflow):
        print '\n\nConnecting to the sFlow-RT network analyzer through its REST API...\n'
        url = url_sflow
        url += 'flow/json'
        print 'URL:', url
        print '\n'
        response = requests.get(url)
        if response.status_code != 200:
            print '\n***ERROR***: Unable to communicate with the sFlow-RT network analyzer through its REST API, check if the sFlow-RT network analyzer is running and configured properly...\n'
            print '\nError response from the sFlow-RT network analyzer:', response
            print '\n'
            print response.headers
            print '\n'
        else:
            print '\nCan succesfully communicate with the sFlow-RT network analyzer through its REST API...\n'
            print '\nList of configured sFlow flow definitions :\n'
            flows = response.json()
            if flows == {}:
                print '\n\n***EMPTY***\n'
            else:
                for fs in flows:
                    print 'Flow Name: ', fs
                    print 'Flow Keys: ', flows[fs]['keys']
                    print 'Flow Value: ', flows[fs]['value']
                    try:
                        print 'Flow Filter: ', flows[fs]['filter']
                    except:
                        print 'None'
                    print '\n'
                print '\n'


    # For a sFlow flow definition/details

    def sflow_flow_def(self, url_sflow, flow_name):
        print '\n\nConnecting to the sFlow-RT network analyzer through its REST API...\n'
        url = url_sflow
        url += 'flow/'
        url += flow_name
        url += '/json'
        print 'URL:', url
        print '\n'
        response = requests.get(url)
        if (response.status_code != 200):
            print '\n***ERROR***: verify the input details and re-enter them...\n'
            print '\nError response from the sFlow-RT network analyzer:', response
            print '\n'
            print response.headers
            print '\n'
        else:
            print '\nCan succesfully communicate with the sFlow-RT network analyzer through its REST API...\n'
            print '\nsFlow flow definition :\n'
            flow_def = response.json()
            if flow_def == {}:
                print '\n\n***EMPTY***\n'
            else:
                print 'Flow Name: ', flow_name
                print '\n'
                print 'Flow Keys: ', flow_def['keys']
                print 'Flow Value: ', flow_def['value']
                try:
                    print 'Flow Filter: ', flow_def['filter']
                except:
                    print 'None'
                print 'Flow Active Timeout: ', flow_def['activeTimeout']
                try:
                    print 'Flow Log: ', flow_def['log']
                except:
                    print 'None'
                print 'Number of Largest Flows to Maintain: ', flow_def['n']
                print 'Flow Smoothing Factor: ', flow_def['t']
                print '\n'
        return flow_def


    # For defining/adding a sFlow flow

    def sflow_flow_add(self, url_sflow, sflow_header, flow_name, flow_data):
        print '\n\nConnecting to the sFlow-RT network analyzer through its REST API...\n'
        url = url_sflow
        url += 'flow/'
        url += flow_name
        url += '/json'
        print 'URL:', url
        print '\n'
        response = requests.put(url, data = json.dumps(flow_data), headers = sflow_header)
        if (response.status_code != 200 and response.status_code != 204):
            print '\n***ERROR***: verify the input details and re-enter them...\n'
            print '\nError response from the sFlow-RT network analyzer:', response
            print '\n'
            print response.headers
            print '\n'
        else:
            print '\nCan succesfully communicate with the sFlow-RT network analyzer through its REST API...\n'
            print '\nAdded sFlow flow :\n'
            print 'Flow Name: ', flow_name
            print '\n'
            for key in flow_data:
                print key, ': ',  flow_data[key]
            print '\n'


    # For deleting a sFlow flow

    def sflow_flow_del(self, url_sflow, flow_name):
        print '\n\nConnecting to the sFlow-RT network analyzer through its REST API...\n'
        url = url_sflow
        url += 'flow/'
        url += flow_name
        url += '/json'
        print 'URL:', url
        print '\n'
        response = requests.delete(url)
        if (response.status_code != 200 and response.status_code != 204):
            print '\n***ERROR***: verify the input details and re-enter them...\n'
            print '\nError response from the sFlow-RT network analyzer:', response
            print '\n'
            print response.headers
            print '\n'
        else:
            print '\nCan succesfully communicate with the sFlow-RT network analyzer through its REST API...\n'
            print '\nDeleted sFlow flow :\n'
            print 'Flow Name: ', flow_name
            print '\n'


    # For the list of top active sFlow flows

    def sflow_active_flows(self, url_sflow, agent, flow_name):
        print '\n\nConnecting to the sFlow-RT network analyzer through its REST API...\n'
        url = url_sflow
        url += 'activeflows/'
        url += agent
        url += '/'
        url += flow_name
        url += '/json'
        print 'URL:', url
        print '\n'
        response = requests.get(url)
        if response.status_code != 200:
            print '\n***ERROR***: verify the input details and re-enter them...\n'
            print '\nError response from the sFlow-RT network analyzer:', response
            print '\n'
            print response.headers
            print '\n'
        else:
            print '\nCan succesfully communicate with the sFlow-RT network analyzer through its REST API...\n'
            print '\nList of top active sFlow flows :\n'
            active_flows = response.json()
            if active_flows == []:
                print '\n\n***EMPTY***\n'
            else:
                for af in active_flows:
                    print 'Flow Name: ', flow_name
                    print 'Flow Key: ', af['key']
                    print 'Flow Value: ', af['value']
                    print 'Flow ID: ', af['flowN']
                    print 'Interface ID: ', af['dataSource']
                    print 'Agent IP Address: ', af['agent']
                    try:
                        print 'Flow Filter: ', af['filter']
                    except:
                        print 'None'
                    print '\n'
                print '\n'


    # For the list of completed sFlow flows

    def sflow_comp_flows(self, url_sflow):
        print '\n\nConnecting to the sFlow-RT network analyzer through its REST API...\n'
        url = url_sflow
        url += 'flows/json'
        print 'URL:', url
        print '\n'
        response = requests.get(url)
        if response.status_code != 200:
            print '\n***ERROR***: Unable to communicate with the sFlow-RT network analyzer through its REST API, check if the sFlow-RT network analyzer is running and configured properly...\n'
            print '\nError response from the sFlow-RT network analyzer:', response
            print '\n'
            print response.headers
            print '\n'
        else:
            print '\nCan succesfully communicate with the sFlow-RT network analyzer through its REST API...\n'
            print '\nList of top active sFlow flows :\n'
            comp_flows = response.json()
            if comp_flows == []:
                print '\n\n***EMPTY***\n'
            else:
                for cf in comp_flows:
                    print 'Flow Name: ', cf['name']
                    print 'Flow Key: ', cf['flowKeys']
                    print 'Flow Value: ', cf['value']
                    print 'Flow ID: ', cf['flowID']
                    print 'Interface ID: ', cf['dataSource']
                    print 'Agent IP Address: ', cf['agent']
                    try:
                        print 'Flow Filter: ', cf['filter']
                    except:
                        print 'None'
                    print '\n'
                print '\n'


    # For the list of names of all the defined/added sFlow address groups

    def sflow_groups(self, url_sflow):
        print '\n\nConnecting to the sFlow-RT network analyzer through its REST API...\n'
        url = url_sflow
        url += 'groups/json'
        print 'URL:', url
        print '\n'
        response = requests.get(url)
        if (response.status_code != 200):
            print '\n***ERROR***: Unable to communicate with the sFlow-RT network analyzer through its REST API, check if the sFlow-RT network analyzer is running and configured properly...\n'
            print '\nError response from the sFlow-RT network analyzer:', response
            print '\n'
            print response.headers
            print '\n'
        else:
            print '\nCan succesfully communicate with the sFlow-RT network analyzer through its REST API...\n'
            print '\nList of names of all the defined/added sFlow address groups :\n'
            groups = response.json()
            if groups == {}:
                print '\n\n***EMPTY***\n'
            else:
                i = 1
                for gs in groups:
                    print i, '.', gs
                    i += 1
                print '\n'


    # For a sFlow address group definition/details

    def sflow_group_def(self, url_sflow, group_name):
        print '\n\nConnecting to the sFlow-RT network analyzer through its REST API...\n'
        url = url_sflow
        url += 'group/'
        url += group_name
        url += '/json'
        print 'URL:', url
        print '\n'
        response = requests.get(url)
        if (response.status_code != 200):
            print '\n***ERROR***: verify the input details and re-enter them...\n'
            print '\nError response from the sFlow-RT network analyzer:', response
            print '\n'
            print response.headers
            print '\n'
        else:
            print '\nCan succesfully communicate with the sFlow-RT network analyzer through its REST API...\n'
            print '\nsFlow address group definition :\n'
            group_def = response.json()
            if group_def == {}:
                print '\n\n***EMPTY***\n'
            else:
                print 'Group Name: ', group_name
                print '\n'
                for key in group_def:
                    print key, ': '
                    i = 1
                    for gd in group_def[key]:
                        print i, '.', gd
                        i += 1
                    print '\n'
                print '\n'
            
                


    # For defining/adding a sFlow address group to categorize network traffic

    def sflow_group_add(self, url_sflow, sflow_header, group_name, group_data):
        print '\n\nConnecting to the sFlow-RT network analyzer through its REST API...\n'
        url = url_sflow
        url += 'group/'
        url += group_name
        url += '/json'
        print 'URL:', url
        print '\n'
        response = requests.put(url, data = json.dumps(group_data), headers = sflow_header)
        if (response.status_code != 200 and response.status_code != 204):
            print '\n***ERROR***: verify the input details and re-enter them...\n'
            print '\nError response from the sFlow-RT network analyzer:', response
            print '\n'
            print response.headers
            print '\n'
        else:
            print '\nCan succesfully communicate with the sFlow-RT network analyzer through its REST API...\n'
            print '\nAdded sFlow address group :\n'
            print 'Group Name: ', group_name
            print '\n'
            for key in group_data:
                print key, ':'
                i = 1
                for add in group_data[key]:
                    print i, '.', add
                    i += 1
                print '\n'
            print '\n'


    # For deleting a sFlow address group

    def sflow_group_del(self, url_sflow, group_name):
        print '\n\nConnecting to the sFlow-RT network analyzer through its REST API...\n'
        url = url_sflow
        url += 'group/'
        url += group_name
        url += '/json'
        print 'URL:', url
        print '\n'
        response = requests.delete(url)
        if (response.status_code != 200 and response.status_code != 204):
            print '\n***ERROR***: verify the input details and re-enter them...\n'
            print '\nError response from the sFlow-RT network analyzer:', response
            print '\n'
            print response.headers
            print '\n'
        else:
            print '\nCan succesfully communicate with the sFlow-RT network analyzer through its REST API...\n'
            print '\nDeleted sFlow address group :\n'
            print 'Group Name: ', group_name
            print '\n'


    # For the list of configured sFlow thresholds

    def sflow_thresholds(self, url_sflow):
        print '\n\nConnecting to the sFlow-RT network analyzer through its REST API...\n'
        url = url_sflow
        url += 'threshold/json'
        print 'URL:', url
        print '\n'
        response = requests.get(url)
        if response.status_code != 200:
            print '\n***ERROR***: Unable to communicate with the sFlow-RT network analyzer through its REST API, check if the sFlow-RT network analyzer is running and configured properly...\n'
            print '\nError response from the sFlow-RT network analyzer:', response
            print '\n'
            print response.headers
            print '\n'
        else:
            print '\nCan succesfully communicate with the sFlow-RT network analyzer through its REST API...\n'
            print '\nList of configured sFlow thresholds :\n'
            thresholds = response.json()
            if thresholds == {}:
                print '\n\n***EMPTY***\n'
            else:
                for th in thresholds:
                    print 'Threshold Name: ', th
                    print 'Threshold Metric: ', thresholds[th]['metric']
                    print 'Threshold Value: ', thresholds[th]['value']
                    try:
                        print 'Threshold Filter: ', thresholds[th]['filter']
                    except:
                        print 'None'
                    print '\n'
                print '\n'


    # For a sFlow threshold definition/details

    def sflow_thresh_def(self, url_sflow, thresh_name):
        print '\n\nConnecting to the sFlow-RT network analyzer through its REST API...\n'
        url = url_sflow
        url += 'threshold/'
        url += thresh_name
        url += '/json'
        print 'URL:', url
        print '\n'
        response = requests.get(url)
        if (response.status_code != 200):
            print '\n***ERROR***: verify the input details and re-enter them...\n'
            print '\nError response from the sFlow-RT network analyzer:', response
            print '\n'
            print response.headers
            print '\n'
        else:
            print '\nCan succesfully communicate with the sFlow-RT network analyzer through its REST API...\n'
            print '\nsFlow threshold definition :\n'
            thresh_def = response.json()
            if thresh_def == {}:
                print '\n\n***EMPTY***\n'
            else:
                print 'Threshold Name: ', thresh_name
                print '\n'
                print 'Threshold Metric: ', thresh_def['metric']
                print 'Threshold Value: ', thresh_def['value']
                try:
                    print 'Threshold Filter: ', thresh_def['filter']
                except:
                    print 'None'
                print 'Threshold Timeout: ', thresh_def['timeout']
                print '\n'


    # For defining/adding a sFlow threshold

    def sflow_thresh_add(self, url_sflow, sflow_header, thresh_name, thresh_data):
        print '\n\nConnecting to the sFlow-RT network analyzer through its REST API...\n'
        url = url_sflow
        url += 'threshold/'
        url += thresh_name
        url += '/json'
        print 'URL:', url
        print '\n'
        response = requests.put(url, data = json.dumps(thresh_data), headers = sflow_header)
        if (response.status_code != 200 and response.status_code != 204):
            print '\n***ERROR***: verify the input details and re-enter them...\n'
            print '\nError response from the sFlow-RT network analyzer:', response
            print '\n'
            print response.headers
            print '\n'
        else:
            print '\nCan succesfully communicate with the sFlow-RT network analyzer through its REST API...\n'
            print '\nAdded sFlow threshold :\n'
            print 'Threshold Name: ', thresh_name
            print '\n'
            for key in thresh_data:
                print key, ': ',  thresh_data[key]
            print '\n'


    # For deleting a sFlow threshold

    def sflow_thresh_del(self, url_sflow, thresh_name):
        print '\n\nConnecting to the sFlow-RT network analyzer through its REST API...\n'
        url = url_sflow
        url += 'threshold/'
        url += thresh_name
        url += '/json'
        print 'URL:', url
        print '\n'
        response = requests.delete(url)
        if (response.status_code != 200 and response.status_code != 204):
            print '\n***ERROR***: verify the input details and re-enter them...\n'
            print '\nError response from the sFlow-RT network analyzer:', response
            print '\n'
            print response.headers
            print '\n'
        else:
            print '\nCan succesfully communicate with the sFlow-RT network analyzer through its REST API...\n'
            print '\nDeleted sFlow threshold :\n'
            print 'Threshold Name: ', thresh_name
            print '\n'


    # For the list of sFlow events

    def sflow_events(self, url_sflow, events_filter):
        print '\n\nConnecting to the sFlow-RT network analyzer through its REST API...\n'
        url = url_sflow
        url += 'events/json'
        if events_filter:
            url += '?'
            url += events_filter
        print 'URL:', url
        print '\n'
        response = requests.get(url)
        if response.status_code != 200:
            print '\n***ERROR***: Unable to communicate with the sFlow-RT network analyzer through its REST API, check if the sFlow-RT network analyzer is running and configured properly...\n'
            print '\nError response from the sFlow-RT network analyzer:', response
            print '\n'
            print response.headers
            print '\n'
        else:
            print '\nCan succesfully communicate with the sFlow-RT network analyzer through its REST API...\n'
            print '\nList of sFlow events :\n'
            events = response.json()
            if events == []:
                print '\n\n***EMPTY***\n'
            else:
                for e in events:
                    print 'Event ID: ', e['eventID']
                    print 'Event Value: ', e['value']
                    print 'Metric Name: ', e['metric']
                    print 'Threshold Name: ', e['thresholdID']
                    print 'Threshold Value: ', e['threshold']
                    print 'Interface ID: ', e['dataSource']
                    print 'Agent IP Address: ', e['agent']
                    try:
                        print 'Flow Filter: ', e['filter']
                    except:
                        print 'None'
                    print '\n'
                print '\n'
        return response



class snmp_api_calls():


    # Core - SNMP network monitoring application's REST API calls:


    # For the list of connected SNMP agents to the SNMP network monitoring application, along with their confgured alias names

    def snmp_agents(self, url_snmp):
        print '\n\nConnecting to the SNMP network monitoring application through its REST API...\n'
        url = url_snmp
        url += 'snmp/config/agents/json'
        print 'URL:', url
        print '\n'
        response = requests.get(url)
        if response.status_code != 200:
            print '\n***ERROR***: Unable to communicate with the SNMP network monitoring application through its REST API, check if the SNMP network monitoring application is running and configured properly...\n'
            print '\nError response from the SNMP network monitoring application:', response
            print '\n'
            print response.headers
            print '\n'
        else:
            print '\nCan succesfully communicate with the SNMP network monitoring application through its REST API...\n'
            print '\nList of SNMP agents that are connected to the SNMP network monitoring application:\n'
            snmp_agents = response.json()
            if snmp_agents == {}:
                print '\n\n***ERROR***: There are no connected SNMP agents (i.e. legacy switches) to the SNMP network monitoring application\n'
                print 'Check and debug the connections between the SNMP agents (i.e. legacy switches) and the SNMP network monitoring application\n'
                print '\n\nDo you wish to continue or exit the application ?\n'
                while True:
                    print 'Default value = ¨yes¨\n'
                    choice = raw_input('Continue (¨yes¨/¨no¨): ')
                    choice = choice.lower()
                    if (choice == 'yes' or choice == '' or choice == 'y'):
                        break
                    elif (choice == 'no' or choice == 'n'):
                        sys.exit(0)
                    else:
                        print '\nInvalid entry !!\n'
                print '\n\n'
            else:
                i = 1
                for key in snmp_agents:
                    print 'Agent ', i, ':\n'
                    print 'Agent Name: ', key
                    print 'IP Address: ', snmp_agents[key]
                    i += 1
                    print '\n'
                print '\n'
            return snmp_agents


    # For the list of interfaces of an SNMP agent along with mappings between SNMP interface index (i.e. ifindex) and physical interface name 

    def snmp_agent_interfaces(self, url_snmp, agent):
        print '\n\nConnecting to the SNMP network monitoring application through its REST API...\n'
        url = url_snmp
        url += 'snmp/config/interfaces/'
        url += agent
        url += '/json'
        print 'URL:', url
        print '\n'
        response = requests.get(url)
        if response.status_code != 200:
            print '\n***ERROR***: Unable to communicate with the SNMP network monitoring application through its REST API, check if the SNMP network monitoring application is running and configured properly...\n'
            print '\nError response from the SNMP network monitoring application:', response
            print '\n'
            print response.headers
            print '\n'
        else:
            print '\nCan succesfully communicate with the SNMP network monitoring application through its REST API...\n'
            print '\nlist of Interfaces of an SNMP Agent along with Mappings between SNMP Interface ID (i.e. ifindex) and Physical Interface Name:\n'
            snmp_agent_interfaces = response.json()
            if snmp_agent_interfaces == {}:
                print '\n\n***ERROR***: There are no connected interfaces to the SNMP agent (i.e. legacy switch)\n'
                print 'Check and debug the interfaces of the SNMP agent (i.e. legacy switch)\n'
            else:
                i = 1
                for key in snmp_agent_interfaces:
                    print 'Interface ', i, ':\n'
                    print 'Interface ID (i.e. SNMP ifindex): ', key
                    print 'Interface Physical Name: ', snmp_agent_interfaces[key]
                    print 'Agent IP Address: ', agent
                    i += 1
                    print '\n'
                print '\n'
            return snmp_agent_interfaces


    # For the MAC (i.e. physical) addresses of the SNMP agent interfaces

    def snmp_agent_interfaces_mac(self, url_snmp, agent):
        print '\n\nConnecting to the SNMP network monitoring application through its REST API...\n'
        url = url_snmp
        url += 'snmp/config/interfaces/mac/'
        url += agent
        url += '/json'
        print 'URL:', url
        print '\n'
        response = requests.get(url)
        if response.status_code != 200:
            print '\n***ERROR***: Unable to communicate with the SNMP network monitoring application through its REST API, check if the SNMP network monitoring application is running and configured properly...\n'
            print '\nError response from the SNMP network monitoring application:', response
            print '\n'
            print response.headers
            print '\n'
        else:
            print '\nCan succesfully communicate with the SNMP network monitoring application through its REST API...\n'
            print '\nMAC (i.e. physical) addresses of the SNMP agent interfaces :\n'
            snmp_interface_mac = response.json()
            if snmp_interface_mac == {}:
                print '\n\n***ERROR***: There are no connected interfaces to the SNMP agent (i.e. legacy switch)\n'
                print 'Check and debug the interfaces of the SNMP agent (i.e. legacy switch)\n'
            else:
                i = 1
                for key in snmp_interface_mac:
                    print 'Interface ', i, ':\n'
                    print 'Interface ID (i.e. SNMP ifindex): ', key
                    print 'Interface MAC Address: ', snmp_interface_mac[key]
                    print 'Agent IP Address: ', agent
                    i += 1
                    print '\n'
                print '\n'
            return snmp_interface_mac


    # For the definition/details of SNMP based interface utilization thresholds

    def snmp_uti_thresh_def(self, url_snmp):
        print '\n\nConnecting to the SNMP network monitoring application through its REST API...\n'
        url = url_snmp
        url += 'snmp/config/thresholds/utilization/json'
        print 'URL:', url
        print '\n'
        response = requests.get(url)
        if  response.status_code != 200:
            print '\n***ERROR***: verify the input details and re-enter them...\n'
            print '\nError response from the SNMP network monitoring application:', response
            print '\n'
            print response.headers
            print '\n'
        else:
            print '\nCan succesfully communicate with the SNMP network monitoring application through its REST API...\n'
            snmp_uti_thresholds = response.json()
            if snmp_uti_thresholds == {}:
                print '\n\n***EMPTY***\n'
            else:
                print '\nConfigured SNMP based interface utilization thresholds for incoming and outgoing traffic in % of total available bandwidth :'
                print '\n'
                for key in snmp_uti_thresholds:
                    print key, ': ',  snmp_uti_thresholds[key]
                    print '\n'
            print '\n'
            return snmp_uti_thresholds


    # For adding/changing SNMP based interface utilization thresholds

    def snmp_uti_thresh_add(self, url_snmp, thresh_data):
        print '\n\nConnecting to the SNMP network monitoring application through its REST API...\n'
        url = url_snmp
        url += 'snmp/config/thresholds/utilization/json'
        print 'URL:', url
        print '\n'
        response = requests.put(url, data = json.dumps(thresh_data))
        if  response.status_code != 200:
            print '\n***ERROR***: verify the input details and re-enter them...\n'
            print '\nError response from the SNMP network monitoring application:', response
            print '\n'
            print response.headers
            print '\n'
        else:
            print '\nCan succesfully communicate with the SNMP network monitoring application through its REST API...\n'
            print '\nAdded/changed SNMP based interface utilization thresholds for incoming and outgoing traffic in % of total available bandwidth :'
            print '\n'
            for key in thresh_data:
                print key, ': ',  thresh_data[key]
                print '\n'
            print '\n'


    # For the list of triggered network core - SNMP interface monitoring events that are configured by the SNMP network monitoring application (i.e. interface high bandwidth utilizations and failures)

    def snmp_agent_interface_events(self, url_snmp, agent, metric):
        print '\n\nConnecting to the SNMP network monitoring application through its REST API...\n'
        url = url_snmp
        url += 'snmp/events/interface/'
        url += metric
        url += '/'
        url += agent
        url += '/json'
        print 'URL:', url
        print '\n'
        response = requests.get(url)
        if response.status_code != 200:
            print '\n***ERROR***: Unable to communicate with the SNMP network monitoring application through its REST API, check if the SNMP network monitoring application is running and configured properly...\n'
            print '\nError response from the SNMP network monitoring application:', response
            print '\n'
            print response.headers
            print '\n'
        else:
            print '\nCan succesfully communicate with the SNMP network monitoring application through its REST API...\n'
            print '\nList of triggered network core - SNMP interface monitoring events that are configured by the SNMP network monitoring application:\n'
            snmp_events = response.json()
            if snmp_events == {}:
                print '\n\n***EMPTY***\n'
            else:
                for key in snmp_events:
                    print 'Event ID: ', key
                    info = snmp_events[key]
                    for key in info:
                        print key, ':', info[key]
                    print '\n'
                print '\n'
            return snmp_events



class odl_ip():


    # Accepting the configured management IP addresses of the underlying OF/OVS (i.e. OpenFlow/Open vSwitch) switches that are connected to the ODL controller

    global odl_base, cred
    odl_base = naas_arch().odl_base_url()
    cred = naas_arch().odl_user_cred()


    def __init__(self):
        url_odl = odl_base['URL']
        name = cred['User Name']
        password = cred['Password']
        print 'List of all the connected OF/OVS switches to the ODL controller:'
        try:
            odl_switches = odl_api_calls().odl_list_conn(url_odl, name, password)
        except KeyboardInterrupt:
            print '\n\nSaving all the changes...'
            print '\nYou are now exiting the NaaS main application...\n'
            sys.exit(0)
        except:
            print '\n\n\n***ERROR***: Found an exception, restart the application in order to check and debug the errors/exceptions...\n'
            print '\n\n\nSaving all the changes...'
            print '\nYou are now exiting the NaaS main application...\n'
            sys.exit(0)
        try:
            if odl_switches:
                odl_switches_ip = {}
                print '\nEnter the configured management IP addresses of the underlying OF/OVS switches that are connected to the ODL controller \n'
                while True:
                    i = 0
                    for switch in odl_switches:
                        i += 1
                        print '\nSwitch ID: ', switch
                        print '\n'
                        ip = raw_input('Management IP Address (Required): ')
                        if ip == '':
                            ip = str(i)
                        odl_switches_ip[ip] = switch
                        print '\n\n'
                    print '\n'
                    print '\nDo you want to confirm the above entered management IP addresses of the underlying OF/OVS switches ?\n'    
                    print 'Default value = ¨yes¨\n\n'
                    choice = raw_input('Confirm (¨yes¨): ')
                    choice = choice.lower()
                    if (choice == 'yes' or choice == '' or choice == 'y'):
                        print '\n\nThe above entries have been confirmed and accepted\n'
                        break                        
                    else:
                        print '\n\nThe above entries have not been confirmed\n'
                        print '\nRe-enter the configured management IP addresses of the underlying OF/OVS switches that are connected to the ODL controller \n'
                with open("Statistics_Logs/ODL_Switches_IP.json", "w") as json_file:
                    json.dump(odl_switches_ip, json_file)
                print '\n\n'
            else:
                odl_switches_ip = {}
                with open("Statistics_Logs/ODL_Switches_IP.json", "w") as json_file:
                    json.dump(odl_switches_ip, json_file)
                    print '\n\n'
        except KeyboardInterrupt:
            print '\n\nSaving all the changes...'
            print '\nYou are now exiting the NaaS main application...\n'
            sys.exit(0)
        except:
            print '\n\n\n***ERROR***: Found an exception, restart the application in order to check and debug the errors/exceptions...\n'
            print '\n\n\nSaving all the changes...'
            print '\nYou are now exiting the NaaS main application...\n'
            sys.exit(0)



class odl_alias():


    # Assigning alias names to the OF/OVS switches that are connected to the ODL controller

    global odl_base, cred
    odl_base = naas_arch().odl_base_url()
    cred = naas_arch().odl_user_cred()


    def __init__(self):
        url_odl = odl_base['URL']
        name = cred['User Name']
        password = cred['Password']
        print 'List of all the connected OF/OVS switches to the ODL controller:'
        try:
            odl_switches = odl_api_calls().odl_list_conn(url_odl, name, password)
        except KeyboardInterrupt:
            print '\n\nSaving all the changes...'
            print '\nYou are now exiting the NaaS main application...\n'
            sys.exit(0)
        except:
            print '\n\n\n***ERROR***: Found an exception, restart the application in order to check and debug the errors/exceptions...\n'
            print '\n\n\nSaving all the changes...'
            print '\nYou are now exiting the NaaS main application...\n'
            sys.exit(0)
        try:
            if odl_switches:
                print '\nDo you want to assign specific alias names to the OF/OVS switches that are connected to the ODL controller ?\n'
                while True:
                    alias_odl_switches = {}
                    print 'Default value = ¨yes¨\n\n'
                    choice = raw_input('Assign Alias Names (¨yes¨/¨no¨): ')
                    choice = choice.lower()
                    if (choice == 'yes' or choice == '' or choice == 'y'):
                        print '\n\nEnter the alias name you want to assign to the following OF/OVS switches...\n'
                        for switch in odl_switches:
                            print '\nSwitch ID: ', switch
                            print '\n'
                            alias = raw_input('Alias Name: ')
                            alias_odl_switches[alias] = switch
                            print '\n\n'
                        print '\n'
                        break
                    elif (choice == 'no' or choice == 'n'):
                        i = 1
                        for switch in odl_switches:
                            alias = 's'
                            alias += str(i)
                            alias_odl_switches[alias] = switch
                            i += 1
                        print '\n'
                        break
                    else:
                        print '\nInvalid entry!!\n'
                with open("Statistics_Logs/ODL_Switches_List.json", "w") as json_file:
                    json.dump(alias_odl_switches, json_file)
                print '\n\n'
            else:
                alias_odl_switches = {}
                with open("Statistics_Logs/ODL_Switches_List.json", "w") as json_file:
                    json.dump(alias_odl_switches, json_file)
                    print '\n\n'
        except KeyboardInterrupt:
            print '\n\nSaving all the changes...'
            print '\nYou are now exiting the NaaS main application...\n'
            sys.exit(0)
        except:
            print '\n\n\n***ERROR***: Found an exception, restart the application in order to check and debug the errors/exceptions...\n'
            print '\n\n\nSaving all the changes...'
            print '\nYou are now exiting the NaaS main application...\n'
            sys.exit(0)



class edge_sflow_alias():


    # Assigning alias names to the network edge sFlow agents that are connected to the edge - sFlow-RT network analyzer

    global edge_sflow_base
    edge_sflow_base = naas_arch().edge_sflow_base_url()


    def __init__(self):
        url_sflow = edge_sflow_base['URL']
        print 'List of all the connected network edge sFlow agents to the edge - sFlow-RT network analyzer:'
        try:
            sflow_agents = sflow_api_calls().sflow_agents(url_sflow)
        except KeyboardInterrupt:
            print '\n\nSaving all the changes...'
            print '\nYou are now exiting the NaaS main application...\n'
            sys.exit(0)
        except:
            print '\n\n\n***ERROR***: Found an exception, restart the application in order to check and debug the errors/exceptions...\n'
            print '\n\n\nSaving all the changes...'
            print '\nYou are now exiting the NaaS main application...\n'
            sys.exit(0)
        try:
            if sflow_agents:
                print '\nDo you want to assign specific alias names to the above network edge sFlow agents ?\n'
                while True:
                    alias_sflow_agents = {}
                    print 'Default value = ¨yes¨\n\n'
                    choice = raw_input('Assign Alias Names (¨yes¨/¨no¨): ')
                    choice = choice.lower()
                    if (choice == 'yes' or choice == '' or choice == 'y'):
                        print '\n\nEnter the alias name you want to assign to the following sFlow agents...\n'
                        for agent in sflow_agents:
                            print '\nAgent IP Address: ', agent
                            print '\n'
                            alias = raw_input('Alias Name: ')
                            alias_sflow_agents[alias] = agent
                            print '\n\n'
                        print '\n'
                        break
                    elif (choice == 'no' or choice == 'n'):
                        i = 1
                        for agent in sflow_agents:
                            alias = 's'
                            alias += str(i)
                            alias_sflow_agents[alias] = agent
                            i += 1
                        print '\n'
                        break
                    else:
                        print '\nInvalid entry!!\n'
                with open("Statistics_Logs/Edge_sFlow_Agents_List.json", "w") as json_file:
                    json.dump(alias_sflow_agents, json_file)
                print '\n\n'
            else:
                alias_sflow_agents = {}
                with open("Statistics_Logs/Edge_sFlow_Agents_List.json", "w") as json_file:
                    json.dump(alias_sflow_agents, json_file)
                    print '\n\n'
        except KeyboardInterrupt:
            print '\n\nSaving all the changes...'
            print '\nYou are now exiting the NaaS main application...\n'
            sys.exit(0)
        except:
            print '\n\n\n***ERROR***: Found an exception, restart the application in order to check and debug the errors/exceptions...\n'
            print '\n\n\nSaving all the changes...'
            print '\nYou are now exiting the NaaS main application...\n'
            sys.exit(0)



class core_sflow_alias():


    # Assigning alias names to the network core sFlow agents that are connected to the core - sFlow-RT network analyzer

    global core_sflow_base
    core_sflow_base = naas_arch().core_sflow_base_url()


    def __init__(self):
        url_sflow = core_sflow_base['URL']
        print 'List of all the connected network core sFlow agents to the core - sFlow-RT network analyzer:'
        try:
            sflow_agents = sflow_api_calls().sflow_agents(url_sflow)
        except KeyboardInterrupt:
            print '\n\nSaving all the changes...'
            print '\nYou are now exiting the NaaS main application...\n'
            sys.exit(0)
        except:
            print '\n\n\n***ERROR***: Found an exception, restart the application in order to check and debug the errors/exceptions...\n'
            print '\n\n\nSaving all the changes...'
            print '\nYou are now exiting the NaaS main application...\n'
            sys.exit(0)
        try:
            if sflow_agents:
                print '\nDo you want to assign specific alias names to the above network core sFlow agents ?\n'
                while True:
                    alias_sflow_agents = {}
                    print 'Default value = ¨yes¨\n\n'
                    choice = raw_input('Assign Alias Names (¨yes¨/¨no¨): ')
                    choice = choice.lower()
                    if (choice == 'yes' or choice == '' or choice == 'y'):
                        print '\n\nEnter the alias name you want to assign to the following sFlow agents...\n'
                        for agent in sflow_agents:
                            print '\nAgent IP Address: ', agent
                            print '\n'
                            alias = raw_input('Alias Name: ')
                            alias_sflow_agents[alias] = agent
                            print '\n\n'
                        print '\n'
                        break
                    elif (choice == 'no' or choice == 'n'):
                        i = 3
                        for agent in sflow_agents:
                            alias = 's'
                            alias += str(i)
                            alias_sflow_agents[alias] = agent
                            i += 1
                        print '\n'
                        break
                    else:
                        print '\nInvalid entry!!\n'
                with open("Statistics_Logs/Core_sFlow_Agents_List.json", "w") as json_file:
                    json.dump(alias_sflow_agents, json_file)
                print '\n\n'
            else:
                alias_sflow_agents = {}
                with open("Statistics_Logs/Core_sFlow_Agents_List.json", "w") as json_file:
                    json.dump(alias_sflow_agents, json_file)
                    print '\n\n'
        except KeyboardInterrupt:
            print '\n\nSaving all the changes...'
            print '\nYou are now exiting the NaaS main application...\n'
            sys.exit(0)
        except:
            print '\n\n\n***ERROR***: Found an exception, restart the application in order to check and debug the errors/exceptions...\n'
            print '\n\n\nSaving all the changes...'
            print '\nYou are now exiting the NaaS main application...\n'
            sys.exit(0)



class core_snmp_alias():


    # Printing the alias names of the network core SNMP agents (i.e. legacy switches) that are connected to the core - SNMP network monitoring application

    global core_snmp_base
    core_snmp_base = naas_arch().core_snmp_base_url()


    def __init__(self):
        url_snmp = core_snmp_base['URL']
        print 'List of all the connected network core SNMP agents to the core - SNMP network monitoring application, along with their confgured alias names:'
        try:
            snmp_agents = snmp_api_calls().snmp_agents(url_snmp)
        except KeyboardInterrupt:
            print '\n\nSaving all the changes...'
            print '\nYou are now exiting the NaaS main application...\n'
            sys.exit(0)
        except:
            print '\n\n\n***ERROR***: Found an exception, restart the application in order to check and debug the errors/exceptions...\n'
            print '\n\n\nSaving all the changes...'
            print '\nYou are now exiting the NaaS main application...\n'
            sys.exit(0)



class naas_manual():


    # Accepting user commands to manually perform NaaS related operations and functions (i.e. ODL controller and sFlow-RT network analyzer related REST/RESTCONF API calls)

    def __init__(self):
        print '\nEnter a command to perform a manual NaaS operation...\n'
        print 'For the list of available commands, enter: Command = ¨list¨ or ¨help¨ or ¨?¨\n'
        print 'At anytime, if you want to close this NaaS application, enter: command = ¨exit¨ (or) ¨close¨\n'
        while True:
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
            core_snmp_base = naas_arch().core_snmp_base_url()
            url_core_snmp = core_snmp_base['URL']
            ip_core_snmp = core_snmp_base['Host IP']
            odl_switches = naas_arch().odl_switches()
            odl_switches_ip = naas_arch().odl_switches_ip()
            edge_sflow_agents = naas_arch().edge_sflow_agents()
            core_sflow_agents = naas_arch().core_sflow_agents()
            core_snmp_agents = naas_arch().core_snmp_agents()
            testbed_1_topo = naas_arch().testbed_1_topology()
            testbed_2_topo = naas_arch().testbed_2_topology()
            testbed_1_lsps = naas_arch().testbed_1_path_bindings()
            testbed_2_lsps = naas_arch().testbed_2_path_bindings()
            sflow_if_map = naas_arch().sflow_interface_mapping()
            flow = odl_api_json_formats()
            stat = odl_api_flow_stat()
            odl = odl_api_calls()
            sflow = sflow_api_calls()
            snmp = snmp_api_calls()
            print '\n'
            try:
                cmd = raw_input('Command: ')
                cmd = cmd.lower()
                if (cmd.strip() == 'exit' or cmd.strip() == 'close'):
                    print '\n\nSaving all the changes...'
                    print '\nYou are now exiting the NaaS main application...\n'
                    static_flow_stats = {}
                    with open("Statistics_Logs/Static_Flow_Stats.json", "w") as json_file:
                                    json.dump(static_flow_stats, json_file)
                    firewall_flow_stats = {}
                    with open("Statistics_Logs/Edge_Firewall_Flow_Stats.json", "w") as json_file:
                        json.dump(firewall_flow_stats, json_file)
                    mpls_push_flow_stats = {}
                    with open("Statistics_Logs/MPLS_Push_Flow_Stats.json", "w") as json_file:
                        json.dump(mpls_push_flow_stats, json_file)
                    basic_connectivity_flow_stats = {}
                    with open("Statistics_Logs/Testbed_1_Basic_Connectivity_Flow_Stats.json", "w") as json_file:
                        json.dump(basic_connectivity_flow_stats, json_file)
                    with open("Statistics_Logs/Testbed_2_Basic_Connectivity_Flow_Stats.json", "w") as json_file:
                        json.dump(basic_connectivity_flow_stats, json_file)
                    load_balancing_flow_stats = {}
                    with open("Statistics_Logs/Testbed_1_Load_Balancing_Flow_Stats.json", "w") as json_file:
                        json.dump(load_balancing_flow_stats, json_file)
                    with open("Statistics_Logs/Testbed_2_Load_Balancing_Flow_Stats.json", "w") as json_file:
                        json.dump(load_balancing_flow_stats, json_file)
                    break
                elif (cmd == 'clear' or cmd == 'clear all'):
                    os.system('clear')
                elif (cmd == 'list' or cmd == 'help' or cmd == '?'):
                    print '\n\nHere is the list of available commands to perform NaaS operations:\n'
                    print '¨odl list conn¨     -- For the list of connected OF/OVS switches to the ODL controller'
                    print '¨odl switch ip¨     -- For the configured management IP addresses of the OF/OVS switches that are connected to the ODL controller'
                    print '¨edit switch ip¨    -- For editing/changing above entries of the configured management IP addresses of the underlying OF/OVS switches'
                    print '¨odl switch alias¨  -- For the assigned alias names of the OF/OVS switches that are connected to the ODL controller'
                    print '¨edit switch alias¨ -- For editing/changing above entries of the alias names of the underlying OF/OVS switches'
                    print '¨odl topo¨          -- For the underlying OF/OVS topology with the list of interfaces and their properties'
                    print '¨odl switch prop¨   -- For the list of all the underlying OF/OVS switches along with their properties'
                    print '¨odl list hosts¨    -- For the list of all the connected end-user hosts along with their configurations'
                    print '¨odl flow stat¨     -- For the list of all the installed flows in the underlying OF/OVS switches along with their statistics'
                    print '¨odl port stat¨     -- For the list of all the available ports in the underlying OF/OVS switches along with their statistics'
                    print '¨odl table stat¨    -- For the list of all the available flow tables in the underlying OF/OVS switches along with their statistics'
                    print '¨static flow inst¨  -- For installing static flows in the underlying OF/OVS switch flow tables through the ODL controller\'s REST API'
                    print '¨static flow stat¨  -- For the list of all the installed static flows in the underlying OF/OVS switch flow tables'
                    print '¨static flow del¨   -- For deleting static flows in the underlying OF/OVS switch flow tables through the ODL controller\'s REST API'
                    print '¨mpls push inst¨    -- For installing MPLS push flows in the OF/OVS switch flow tables through the ODL controller\'s RESTCONF API'
                    print '¨hyb mpls push¨     -- For installing above MPLS push flows in the case of a hybrid MPLS network with legacy switches as its LSRs'
                    print '¨mpls push stat¨    -- For the list of all the installed MPLS push flows in the underlying OF/OVS switch flow tables'
                    print '¨mpls push del¨     -- For deleting MPLS push flows in the OF/OVS switch flow tables through the ODL controller\'s RESTCONF API'
                    print '¨sflow perform¨     -- For the statistics describing sFlow-RT analyzer performance'
                    print '¨sflow agents¨      -- For the list of connected sFlow agents to the sFlow-RT network analyzer, along with their statistics'
                    print '¨edge sflow alias¨  -- For the assigned alias names of the edge sFlow agents that are connected to the edge sFlow-RT network analyzer'
                    print '¨edit edge alias¨   -- For editing/changing above entries of the alias names of the underlying network edge sFlow agents'
                    print '¨core sflow alias¨  -- For the assigned alias names of the core sFlow agents that are connected to the core sFlow-RT network analyzer'
                    print '¨edit core alias¨   -- For editing/changing above entries of the alias names of the underlying network core sFlow agents'
                    print '¨sflow metrics¨     -- For the list of currently active sFlow metrics'
                    print '¨sflow met val¨     -- For the list of currently active sFlow metrics'
                    print '¨sflow ifs¨         -- For the list of interfaces of an sFlow agent(s)'
                    print '¨sflow if met val¨  -- For a sFlow metric value of a sFlow agent\'s interface'
                    print '¨sflow flowkeys¨    -- For the list of currently active sFlow flow keys'
                    print '¨sflow flows¨       -- For the list of sFlow flow definitions'
                    print '¨sflow flow def¨    -- For a sFlow flow definition/details'
                    print '¨sflow flow add¨    -- For defining/adding a sFlow flow'
                    print '¨sflow flow del¨    -- For deleting a sFlow flow'
                    print '¨sflow activeflows¨ -- For the list of top active sFlow flows'
                    print '¨sflow comp flows¨  -- For the list of completed sFlow flows'
                    print '¨sflow groups¨      -- For the list of names of the defined/added sFlow address groups'
                    print '¨sflow group def¨   -- For a sFlow address group definition/details'
                    print '¨sflow group add¨   -- For defining/adding a sFlow address group to categorize network traffic'
                    print '¨sflow group del¨   -- For deleting a sFlow address group'
                    print '¨sflow thresholds¨  -- For the list of sFlow thresholds'
                    print '¨sflow thresh def¨  -- For a sFlow threshold definition/details'
                    print '¨sflow thresh add¨  -- For defining/adding a sFlow threshold'
                    print '¨sflow thresh del¨  -- For deleting a sFlow threshold'
                    print '¨sflow events¨      -- For the list of sFlow events'
                    print '¨core snmp agents¨  -- For the list of connected SNMP agents (i.e. network core legacy switches) to the SNMP monitoring application'
                    print '¨snmp agent int¨    -- For the list of interfaces of an SNMP agent along with mappings between SNMP ifindex and physical name'
                    print '¨snmp int mac¨      -- For the MAC (i.e. physical) addresses of the SNMP agent interfaces'
                    print '¨uti thresh def¨    -- For the SNMP based interface utilization thresholds definition/details'
                    print '¨uti thresh add¨    -- For adding/changing SNMP based interface utilization thresholds'
                    print '¨snmp int events¨   -- For the list of triggered network core - SNMP interface monitoring events (i.e. high utilizations and failures)'
                    print '¨test 1 topo¨       -- For the topology of testbed network 1 (i.e. network with open (i.e. OF/OVS) switches)'
                    print '¨test 2 topo¨       -- For the topology of testbed network 2 (i.e. network core with legacy (i.e. vendor-specific) switches)'
                    print '¨test 1 lsps¨       -- For the ingress MPLS push label to path bindings (i.e. static network core LSPs) of testbed network 1'
                    print '¨test 2 lsps¨       -- For the ingress MPLS push label to path bindings (i.e. static network core LSPs) of testbed network 2'
                    print '¨load balancing¨    -- For running a new instance of Network-as-a-Service (NaaS) platform\'s load balancing application'
                    print '¨edge firewall¨     -- For running a new instance of Network-as-a-Service (NaaS) platform\'s edge firewall application'
                    print '¨basic connectivity¨-- For running a new instance of Network-as-a-Service (NaaS) platform\'s basic connectivity application'
                    print '¨clear¨             -- For clearing the  NaaS application CLI/terminal at any time'
                    print '¨clear all¨         -- For clearing the  NaaS application CLI/terminal at any time'
                    print '¨exit¨ (or) ¨close¨ -- For closing this NaaS application at any time'
                elif cmd == 'odl list conn':
                    odl_switch = odl.odl_list_conn(url_odl, name, password)
                elif cmd == 'odl switch ip':
                    print '\n\nConfigured management IP addresses of the OF/OVS switches that are connected to the ODL controller :\n'
                    if odl_switches_ip == {}:
                        print '\n\n***EMPTY***\n'
                    else:
                        for key in odl_switches_ip:
                            print 'Switch ID: ', odl_switches_ip[key]
                            print 'Management IP Address: ', key
                            print '\n'
                        print '\n'
                elif cmd == 'edit switch ip':
                    print '\n\n'
                    switch_ip = odl_ip()
                elif cmd == 'odl switch alias':
                    print '\n\nAlias names of the OF/OVS switches that are connected to the ODL controller :\n'
                    if odl_switches == {}:
                        print '\n\n***EMPTY***\n'
                    else:
                        for key in odl_switches:
                            print 'Switch ID: ', odl_switches[key]
                            print 'Alias Name: ', key
                            print '\n'
                        print '\n'
                elif cmd == 'edit switch alias':
                    print '\n\n'
                    switch_alias = odl_alias()
                elif cmd == 'odl topo':
                    odl.odl_topo(url_odl, name, password)
                elif cmd == 'odl switch prop':
                    odl.odl_switch_prop(url_odl, name, password)
                elif cmd == 'odl list hosts':
                    list_hosts = odl.odl_list_hosts(url_odl, name, password)
                elif cmd == 'odl flow stat':
                    odl.odl_flow_stat(url_odl, name, password)
                elif cmd == 'odl port stat':
                    odl.odl_port_stat(url_odl, name, password)
                elif cmd == 'odl table stat':
                    odl.odl_table_stat(url_odl, name, password)
                elif cmd == 'static flow inst':
                    static_stats = {}
                    static_flow_stats = {}
                    static_flow = flow.odl_static_json()
                    static_stats = stat.odl_static_stat()
                    static_flow_stats = static_stats['stat']
                    static_flow_counter = static_stats['counter']
                    print '\n\nEnter the following details for the flow you want to install...'
                    print '\nNote: If you want to skip an match field entry, press the enter key\n\n'
                    switch_id = raw_input('Enter the Switch ID/Alias Name/Management IP Address (Required): ')
                    if switch_id in odl_switches:
                        switch_id = odl_switches[switch_id]
                    if switch_id in odl_switches_ip:
                        switch_id = odl_switches_ip[switch_id]
                    print '\n'
                    dst_add = raw_input('Enter the Match Field - Destination IP Address: ')
                    src_add = raw_input('Enter the Match Field - Source IP Address: ')
                    in_port = raw_input('Enter the Match Field - Input/Ingress Switch Edge/Port Number: ')
                    dl_dst = raw_input('Enter the Match Field - Destination MAC Address: ')
                    dl_src = raw_input('Enter the Match Field - Source MAC Address: ')
                    protocol = raw_input('Enter the Match Field - Protocol Number (E.g. 6 for TCP): ')
                    src_port = raw_input('Enter the Match Field - Source Port Number (Range: 0 - 65535): ')
                    dst_port = raw_input('Enter the Match Field - Destination Port Number (Range: 0 - 65535): ')
                    vlan_id = raw_input('Enter the Match Field - VLAN ID: ')
                    vlan_priority = raw_input('Enter the Match Field - VLAN Priority (Range: 0 - 7): ')
                    priority = raw_input('Enter the Priority Field (Default value = 1000): ')
                    if priority == '':
                        priority = '1000'
                    print '\n'
                    action = []
                    action_input = raw_input('Enter the Action Field  - ¨drop¨ or Output/Egress Switch Edge/Port Number (Required): ')
                    action_input = action_input.lower()
                    if action_input == 'drop':
                        action_input = 'DROP'
                    else:
                        act = 'OUTPUT='
                        act += switch_id
                        act += ':'
                        act += action_input
                        action_input = act
                    action.append(action_input)
                    flow_stat = {}
                    flow_stat = odl.odl_static_flow_inst(url_odl, name, password, odl_header, static_flow, static_flow_counter, switch_id, dst_add, src_add, in_port, dl_dst, dl_src, protocol, src_port, dst_port, vlan_id, vlan_priority, action, priority)
                    if flow_stat:
                        flow_name = flow_stat['Flow Name']
                        static_flow_stats[flow_name] = flow_stat
                        with open("Statistics_Logs/Static_Flow_Stats.json", "w") as json_file:
                            json.dump(static_flow_stats, json_file)
                elif cmd == 'static flow stat':
                    static_stats = {}
                    static_flow_stats = {}
                    static_stats = stat.odl_static_stat()
                    static_flow_stats = static_stats['stat']
                    print '\n\nlist of all the installed static flows in the underlying switch flow tables...'
                    print '\n'
                    if static_flow_stats == {}:
                        print '\n***EMPTY***\n'
                    else:
                        for key in static_flow_stats:
                            print 'Match fields Notation/order: ' + '(1.Dst IP Add, 2.Src IP Add, 3.In Port ID, 4. Dst MAC Add, 5. Src MAC Add, 6.Protocol, 7.Src Port, 8.Dst Port, 9.VLAN ID, 10.VLAN Prio)\n'
                            print 'Flow name: ' , static_flow_stats[key]['Flow Name']
                            print 'Switch ID: ' , static_flow_stats[key]['Switch ID']
                            print 'Action Field: ' , static_flow_stats[key]['Action Field']
                            print 'Priority: ' , static_flow_stats[key]['Priority']
                            print 'Match Fields: '
                            i = 1
                            for mf in static_flow_stats[key]['Match Fields']:
                                print i , '.', '%s' %mf
                                i += 1
                            print '\n'
                elif cmd == 'static flow del':
                    static_stats = {}
                    static_flow_stats = {}
                    static_stats = stat.odl_static_stat()
                    static_flow_stats = static_stats['stat']
                    print '\n\nEnter the following details for the static flow you want to delete/un-install...\n\n'
                    switch_id = raw_input('Enter the Switch ID/Alias Name/Management IP Address (Required): ')
                    if switch_id in odl_switches:
                        switch_id = odl_switches[switch_id]
                    if switch_id in odl_switches_ip:
                        switch_id = odl_switches_ip[switch_id]
                    print '\n'
                    flow_name = raw_input('Enter the Flow Name (Required): ')
                    flow_name = flow_name.lower()
                    f = 'flow'
                    if f not in flow_name:
                        flow_name = f + flow_name
                    deleted_flow = odl.odl_static_flow_del(url_odl, name, password, switch_id, flow_name)
                    if deleted_flow:
                        if static_flow_stats:
                            del(static_flow_stats[deleted_flow])
                            with open("Statistics_Logs/Static_Flow_Stats.json", "w") as json_file:
                                json.dump(static_flow_stats, json_file)
                elif cmd == 'mpls push inst':
                    mpls_push_stats = {}
                    mpls_push_flow_stats = {}
                    mpls_push_flow = flow.odl_mpls_push_json()
                    mpls_push_stats = stat.odl_mpls_push_stat()
                    mpls_push_flow_stats = mpls_push_stats['stat']
                    mpls_push_flow_counter = mpls_push_stats['counter']
                    print '\n\nEnter the following details for the MPLS push flow you want to install...'
                    print '\nNote: If you want to skip an match field entry, press the enter key\n\n'
                    switch_id = raw_input('Enter the Switch ID/Alias Name/Management IP Address (Required): ')
                    if switch_id in odl_switches:
                        switch_id = odl_switches[switch_id]
                    if switch_id in odl_switches_ip:
                        switch_id = odl_switches_ip[switch_id]
                    print '\n'
                    dst_add = raw_input('Enter the Match Field - Destination IP Address: ')
                    src_add = raw_input('Enter the Match Field - Source IP Address: ')
                    in_port = raw_input('Enter the Match Field - Input/Ingress Switch Edge/Port Number: ')
                    dl_dst = raw_input('Enter the Match Field - Destination MAC Address: ')
                    dl_src = raw_input('Enter the Match Field - Source MAC Address: ')
                    protocol = raw_input('Enter the Match Field - Protocol Number (E.g. 6 for TCP and 17 for UDP): ')
                    tcp_src_port = raw_input('Enter the Match Field - TCP Source Port Number: ')
                    tcp_dst_port = raw_input('Enter the Match Field - TCP Destination Port Number: ')
                    udp_src_port = raw_input('Enter the Match Field - UDP Source Port Number: ')
                    udp_dst_port = raw_input('Enter the Match Field - UDP Destination Port Number: ')
                    vlan_id = raw_input('Enter the Match Field - VLAN ID: ')
                    vlan_priority = raw_input('Enter the Match Field - VLAN Priority (Range: 0 - 7): ')
                    table_id = raw_input('Enter the Table ID for Flow Installation (Default value = 0): ')
                    if table_id == '':
                        table_id = '0'
                    priority = raw_input('Enter the Priority Field (Default value = 100): ')
                    if priority == '':
                        priority = '100'
                    print '\n'
                    action_mpls_label = raw_input('Enter the Action Field  - MPLS Label to Push for the Flow (Required): ')
                    action_out_port = raw_input('Enter the Action Field  - Output/Egress Switch Edge/Port Number (Required): ')
                    flow_stat = {}
                    flow_stat = odl.odl_mpls_push_flow_inst(url_odl, name, password, odl_header, mpls_push_flow, mpls_push_flow_counter, switch_id, dst_add, src_add, in_port, dl_dst, dl_src, protocol, tcp_src_port, tcp_dst_port, udp_src_port, udp_dst_port, vlan_id, vlan_priority, action_mpls_label, action_out_port, table_id, priority)
                    if flow_stat:
                        flow_name = flow_stat['Flow ID']
                        mpls_push_flow_stats[flow_name] = flow_stat
                        with open("Statistics_Logs/MPLS_Push_Flow_Stats.json", "w") as json_file:
                            json.dump(mpls_push_flow_stats, json_file)
                elif cmd == 'hyb mpls push':
                    mpls_push_stats = {}
                    mpls_push_flow_stats = {}
                    hyb_mpls_push_flow = flow.odl_hyb_mpls_push_json()
                    mpls_push_stats = stat.odl_mpls_push_stat()
                    mpls_push_flow_stats = mpls_push_stats['stat']
                    mpls_push_flow_counter = mpls_push_stats['counter']
                    print '\n\nEnter the following details for the MPLS push flow you want to install...'
                    print '\nNote: If you want to skip an match field entry, press the enter key\n\n'
                    switch_id = raw_input('Enter the Switch ID/Alias Name/Management IP Address (Required): ')
                    if switch_id in odl_switches:
                        switch_id = odl_switches[switch_id]
                    if switch_id in odl_switches_ip:
                        switch_id = odl_switches_ip[switch_id]
                    print '\n'
                    dst_add = raw_input('Enter the Match Field - Destination IP Address: ')
                    src_add = raw_input('Enter the Match Field - Source IP Address: ')
                    in_port = raw_input('Enter the Match Field - Input/Ingress Switch Edge/Port Number: ')
                    dl_dst = raw_input('Enter the Match Field - Destination MAC Address: ')
                    dl_src = raw_input('Enter the Match Field - Source MAC Address: ')
                    protocol = raw_input('Enter the Match Field - Protocol Number (E.g. 6 for TCP and 17 for UDP): ')
                    tcp_src_port = raw_input('Enter the Match Field - TCP Source Port Number: ')
                    tcp_dst_port = raw_input('Enter the Match Field - TCP Destination Port Number: ')
                    udp_src_port = raw_input('Enter the Match Field - UDP Source Port Number: ')
                    udp_dst_port = raw_input('Enter the Match Field - UDP Destination Port Number: ')
                    vlan_id = raw_input('Enter the Match Field - VLAN ID: ')
                    vlan_priority = raw_input('Enter the Match Field - VLAN Priority (Range: 0 - 7): ')
                    table_id = raw_input('Enter the Table ID for Flow Installation (Default value = 0): ')
                    if table_id == '':
                        table_id = '0'
                    priority = raw_input('Enter the Priority Field (Default value = 100): ')
                    if priority == '':
                        priority = '100'
                    print '\n'
                    action_dl_dst = raw_input('Enter the Action Field  - Next-hop Legacy Switch MAC Address (Default value as per the configured testbed for my graduation project): ')
                    if action_dl_dst == '':
                        if switch_id == 'openflow:5578350727664762986':
                            action_dl_dst = '00:14:f6:83:30:00'
                        if switch_id == 'openflow:5578350727664762989':
                            action_dl_dst = '00:14:f6:82:80:00'
                    print '\n'
                    action_mpls_label = raw_input('Enter the Action Field  - MPLS Label to Push for the Flow (Required): ')
                    action_out_port = raw_input('Enter the Action Field  - Output/Egress Switch Edge/Port Number (Required): ')
                    flow_stat = {}
                    flow_stat = odl.odl_hyb_mpls_push_flow_inst(url_odl, name, password, odl_header, hyb_mpls_push_flow, mpls_push_flow_counter, switch_id, dst_add, src_add, in_port, dl_dst, dl_src, protocol, tcp_src_port, tcp_dst_port, udp_src_port, udp_dst_port, vlan_id, vlan_priority, action_mpls_label, action_out_port, action_dl_dst, table_id, priority)
                    if flow_stat:
                        flow_name = flow_stat['Flow ID']
                        mpls_push_flow_stats[flow_name] = flow_stat
                        with open("Statistics_Logs/MPLS_Push_Flow_Stats.json", "w") as json_file:
                            json.dump(mpls_push_flow_stats, json_file)
                elif cmd == 'mpls push stat':
                    mpls_push_stats = {}
                    mpls_push_flow_stats = {}
                    mpls_push_stats = stat.odl_mpls_push_stat()
                    mpls_push_flow_stats = mpls_push_stats['stat']
                    print '\n\nlist of all the installed MPLS push flows in the underlying switch flow tables...'
                    print '\n'
                    if mpls_push_flow_stats == {}:
                        print '\n***EMPTY***\n'
                    else:
                        for key in mpls_push_flow_stats:
                            print 'Flow ID: ' , mpls_push_flow_stats[key]['Flow ID']
                            print 'Switch ID: ' , mpls_push_flow_stats[key]['Switch ID']
                            print 'Table ID: ' , mpls_push_flow_stats[key]['Table ID']
                            print 'Priority: ' , mpls_push_flow_stats[key]['Priority']
                            print 'Action Fields: '
                            print '1', '.', 'Push MPLS Label = ' , mpls_push_flow_stats[key]['MPLS Label']
                            print '2', '.', 'Output/Egress Switch Port = ' , mpls_push_flow_stats[key]['Out Port']
                            print 'Match Fields: '
                            print '1', '.', 'Destination IP Address = ' , mpls_push_flow_stats[key]['Dst IP Add']
                            print '2', '.', 'Source IP Address = ' , mpls_push_flow_stats[key]['Src IP Add']
                            print '3', '.', 'Ingress/Input Switch Port = ' , mpls_push_flow_stats[key]['In Port']
                            print '4', '.', 'Destination MAC Address = ' , mpls_push_flow_stats[key]['Dl Dst Add']
                            print '5', '.', 'Source MAC Address = ' , mpls_push_flow_stats[key]['Dl Src Add']
                            print '6', '.', 'Protocol Number = ' , mpls_push_flow_stats[key]['Protocol']
                            print '7', '.', 'TCP Source Port = ' , mpls_push_flow_stats[key]['TCP Src Port']
                            print '8', '.', 'TCP Destination Port = ' , mpls_push_flow_stats[key]['TCP Dst Port']
                            print '9', '.', 'UDP Source Port = ' , mpls_push_flow_stats[key]['UDP Src Port']
                            print '10', '.', 'UDP Destination Port = ' , mpls_push_flow_stats[key]['UDP Dst Port']
                            print '11', '.', 'VLAN ID = ' , mpls_push_flow_stats[key]['VLAN ID']
                            print '11', '.', 'VLAN Priority = ' , mpls_push_flow_stats[key]['VLAN Priority']
                            print '\n'
                elif cmd == 'mpls push del':
                    mpls_push_stats = {}
                    mpls_push_flow_stats = {}
                    mpls_push_stats = stat.odl_mpls_push_stat()
                    mpls_push_flow_stats = mpls_push_stats['stat']
                    print '\n\nEnter the following details for the MPLS push flow you want to delete/un-install...\n'
                    switch_id = raw_input('\nEnter the Switch ID/Alias Name/Management IP Address (Required): ')
                    if switch_id in odl_switches:
                        switch_id = odl_switches[switch_id]
                    if switch_id in odl_switches_ip:
                        switch_id = odl_switches_ip[switch_id]
                    print '\n'
                    flow_id = raw_input('Enter the Flow ID (Required): ')
                    print '\n'
                    table_id = raw_input('Enter the Table ID (Default Value = 0): ')
                    if table_id == '':
                        table_id = '0'
                    deleted_flow = odl.odl_mpls_push_flow_del(url_odl, name, password, switch_id, flow_id, table_id)
                    if deleted_flow:
                        if mpls_push_flow_stats:
                            del(mpls_push_flow_stats[deleted_flow])
                            with open("Statistics_Logs/MPLS_Push_Flow_Stats.json", "w") as json_file:
                                json.dump(mpls_push_flow_stats, json_file)
                elif cmd == 'sflow perform':
                    print '\n\nEnter the part of the network (i.e. edge or core) you want to monitor ?\n'
                    print 'Default value = ¨edge¨\n'
                    choice = raw_input('Network Part (¨edge¨/¨core¨): ')
                    choice = choice.lower()
                    if (choice == 'core' or choice == 'c'):
                        url_sflow = url_core_sflow
                    else:
                        url_sflow = url_edge_sflow
                    sflow.sflow_perform(url_sflow)
                elif cmd == 'sflow agents':
                    print '\n\nEnter the part of the network (i.e. edge or core) you want to monitor ?\n'
                    print 'Default value = ¨edge¨\n'
                    choice = raw_input('Network Part (¨edge¨/¨core¨): ')
                    choice = choice.lower()
                    if (choice == 'core' or choice == 'c'):
                        url_sflow = url_core_sflow
                    else:
                        url_sflow = url_edge_sflow
                    sflow_agent = sflow.sflow_agents(url_sflow)
                elif cmd == 'edge sflow alias':
                    print '\n\nAlias names of the network edge sFlow agents that are connected to the edge - sFlow-RT network analyzer :\n'
                    if edge_sflow_agents == {}:
                        print '\n\n***EMPTY***\n'
                    else:
                        for key in edge_sflow_agents:
                            print 'Agent IP Address: ', edge_sflow_agents[key]
                            print 'Alias Name: ', key
                            print '\n'
                        print '\n'
                elif cmd == 'edit edge alias':
                    print '\n\n'
                    edge_agent_alias = edge_sflow_alias()
                elif cmd == 'core sflow alias':
                    print '\n\nAlias names of the network core sFlow agents that are connected to the core - sFlow-RT network analyzer :\n'
                    if core_sflow_agents == {}:
                        print '\n\n***EMPTY***\n'
                    else:
                        for key in core_sflow_agents:
                            print 'Agent IP Address: ', core_sflow_agents[key]
                            print 'Alias Name: ', key
                            print '\n'
                        print '\n'
                elif cmd == 'edit core alias':
                    print '\n\n'
                    core_agent_alias = core_sflow_alias()
                elif cmd == 'sflow metrics':
                    print '\n\nEnter the part of the network (i.e. edge or core) you want to monitor ?\n'
                    print 'Default value = ¨edge¨\n'
                    choice = raw_input('Network Part (¨edge¨/¨core¨): ')
                    choice = choice.lower()
                    if (choice == 'core' or choice == 'c'):
                        url_sflow = url_core_sflow
                    else:
                        url_sflow = url_edge_sflow
                    sflow.sflow_metrics(url_sflow)
                elif cmd == 'sflow met val':
                    print '\n\nEnter the following details for printing the SFlow metric values of an sFlow agent(s)...'
                    print '\nNote: If you want to skip an entry, press the enter key\n\n'
                    print 'Enter the part of the network (i.e. edge or core) you want to monitor ?\n'
                    print 'Default value = ¨edge¨\n'
                    choice = raw_input('Network Part (¨edge¨/¨core¨): ')
                    choice = choice.lower()
                    if (choice == 'core' or choice == 'c'):
                        url_sflow = url_core_sflow
                    else:
                        url_sflow = url_edge_sflow
                    print '\n\n'
                    agent = raw_input('Enter the sFlow Agent\'s IP Address (or) the Agent\'s Alias Name (Default value = ¨ALL¨): ')
                    if agent in edge_sflow_agents:
                        agent = edge_sflow_agents[agent]
                    if agent in core_sflow_agents:
                        agent = core_sflow_agents[agent]
                    if agent == '':
                        agent = 'ALL'
                    print '\n'
                    metric = raw_input('Enter the sFlow Metric Name (Default value = ¨ALL¨): ')
                    if metric == '':
                        metric= 'ALL'
                    response = sflow.sflow_metric_values(url_sflow, agent, metric)
                elif cmd == 'sflow ifs':
                    print '\n\nEnter the following details for printing the list of interfaces of an sFlow agent(s)...'
                    print '\nNote: If you want to skip an entry, press the enter key\n\n'
                    print 'Enter the part of the network (i.e. edge or core) you want to monitor ?\n'
                    print 'Default value = ¨edge¨\n'
                    choice = raw_input('Network Part (¨edge¨/¨core¨): ')
                    choice = choice.lower()
                    if (choice == 'core' or choice == 'c'):
                        url_sflow = url_core_sflow
                    else:
                        url_sflow = url_edge_sflow
                    print '\n\n'
                    agent = raw_input('Enter the sFlow Agent\'s IP Address (or) the Agent\'s Alias Name (Default value = ¨ALL¨): ')
                    if agent in edge_sflow_agents:
                        agent = edge_sflow_agents[agent]
                    if agent in core_sflow_agents:
                        agent = core_sflow_agents[agent]
                    if agent == '':
                        agent = 'ALL'
                    core_interfaces = sflow.sflow_interfaces(url_sflow, agent)
                elif cmd == 'sflow if met val':
                    print '\n\nEnter the following details for printing an sFlow metric value of an sFlow agent\'s interface...'
                    print '\nNote: If you want to skip an entry, press the enter key\n\n'
                    print 'Enter the part of the network (i.e. edge or core) you want to monitor ?\n'
                    print 'Default value = ¨edge¨\n'
                    choice = raw_input('Network Part (¨edge¨/¨core¨): ')
                    choice = choice.lower()
                    if (choice == 'core' or choice == 'c'):
                        url_sflow = url_core_sflow
                    else:
                        url_sflow = url_edge_sflow
                    print '\n\n'
                    agent = raw_input('Enter the sFlow Agent\'s IP Address (or) the Agent\'s Alias Name (Default value = ¨ALL¨): ')
                    if agent in edge_sflow_agents:
                        agent = edge_sflow_agents[agent]
                    if agent in core_sflow_agents:
                        agent = core_sflow_agents[agent]
                    if agent == '':
                        agent = 'ALL'
                    print '\n'
                    metric = raw_input('Enter the sFlow Metric Name (Required): ')
                    interface = raw_input('Enter the sFlow Interface ID (Required): ')
                    response = sflow.sflow_interface_metric_value(url_sflow, agent, interface, metric)
                elif cmd == 'sflow flowkeys':
                    print '\n\nEnter the part of the network (i.e. edge or core) you want to monitor ?\n'
                    print 'Default value = ¨edge¨\n'
                    choice = raw_input('Network Part (¨edge¨/¨core¨): ')
                    choice = choice.lower()
                    if (choice == 'core' or choice == 'c'):
                        url_sflow = url_core_sflow
                    else:
                        url_sflow = url_edge_sflow
                    sflow.sflow_flowkeys(url_sflow)
                elif cmd == 'sflow flows':
                    print '\n\nEnter the part of the network (i.e. edge or core) you want to monitor ?\n'
                    print 'Default value = ¨edge¨\n'
                    choice = raw_input('Network Part (¨edge¨/¨core¨): ')
                    choice = choice.lower()
                    if (choice == 'core' or choice == 'c'):
                        url_sflow = url_core_sflow
                    else:
                        url_sflow = url_edge_sflow
                    sflow.sflow_flows(url_sflow)
                elif cmd == 'sflow flow def':
                    print '\n\nEnter the following details for a sFlow flow definition/details...'
                    print '\nNote: If you want to skip an entry, press the enter key\n\n'
                    print 'Enter the part of the network (i.e. edge or core) you want to monitor ?\n'
                    print 'Default value = ¨edge¨\n'
                    choice = raw_input('Network Part (¨edge¨/¨core¨): ')
                    choice = choice.lower()
                    if (choice == 'core' or choice == 'c'):
                        url_sflow = url_core_sflow
                    else:
                        url_sflow = url_edge_sflow
                    print '\n\n'
                    flow_name = raw_input('Enter the sFlow flow Name (Required): ')
                    flow_def = sflow.sflow_flow_def(url_sflow, flow_name)
                elif cmd == 'sflow flow add':
                    flow_data = {}
                    print '\n\nEnter the following details for adding a sFlow flow...'
                    print '\nNote: If you want to skip an entry, press the enter key\n\n'
                    print 'Enter the part of the network (i.e. edge or core) you want to monitor ?\n'
                    print 'Default value = ¨edge¨\n'
                    choice = raw_input('Network Part (¨edge¨/¨core¨): ')
                    choice = choice.lower()
                    if (choice == 'core' or choice == 'c'):
                        url_sflow = url_core_sflow
                    else:
                        url_sflow = url_edge_sflow
                    print '\n\n'
                    flow_name = raw_input('Enter the sFlow Name (Required): ')
                    print '\n\nEnter the flowkeys (seperated by ¨,¨) you want to add to the flow definition...\n'
                    keys = raw_input('Enter the Flowkeys (Required): ')
                    print '\n\nEnter the flow value (e.g. ¨bytes¨, ¨frames¨, etc.) you want to add to the flow definition...\n'
                    value = raw_input('Enter the Flow value (Required): ')
                    print '\n\nEnter the flow filter (seperated by ¨&¨) you want to add to the flow definition...\n'
                    filt = raw_input('Enter the Flow Filter: ')
                    print '\n\nEnter the flow log value  (i.e. ¨true¨ or ¨false¨)...\n'
                    log = raw_input('Enter the Flow Log Value: ')
                    flow_data['keys'] = keys
                    flow_data['value'] = value
                    if not filt == '':
                        flow_data['filter'] = filt
                    if not log == '':
                        flow_data['log'] = log
                    sflow.sflow_flow_add(url_sflow, sflow_header, flow_name, flow_data)
                elif cmd == 'sflow flow del':
                    print '\n\nEnter the following details for deleting a sFlow flow...'
                    print '\nNote: If you want to skip an entry, press the enter key\n\n'
                    print 'Enter the part of the network (i.e. edge or core) you want to monitor ?\n'
                    print 'Default value = ¨edge¨\n'
                    choice = raw_input('Network Part (¨edge¨/¨core¨): ')
                    choice = choice.lower()
                    if (choice == 'core' or choice == 'c'):
                        url_sflow = url_core_sflow
                    else:
                        url_sflow = url_edge_sflow
                    print '\n\n'
                    flow_name = raw_input('Enter the sFlow Name (Required): ')
                    sflow.sflow_flow_del(url_sflow, flow_name)
                elif cmd == 'sflow activeflows':
                    print '\n\nEnter the following details for printing the list of top active sFlow flows...'
                    print '\nNote: If you want to skip an entry, press the enter key\n\n'
                    print 'Enter the part of the network (i.e. edge or core) you want to monitor ?\n'
                    print 'Default value = ¨edge¨\n'
                    choice = raw_input('Network Part (¨edge¨/¨core¨): ')
                    choice = choice.lower()
                    if (choice == 'core' or choice == 'c'):
                        url_sflow = url_core_sflow
                    else:
                        url_sflow = url_edge_sflow
                    print '\n\n'
                    agent = raw_input('Enter the sFlow Agent\'s IP Address (or) the Agent\'s Alias Name (Default value = ¨ALL¨): ')
                    if agent in edge_sflow_agents:
                        agent = edge_sflow_agents[agent]
                    if agent in core_sflow_agents:
                        agent = core_sflow_agents[agent]
                    if agent == '':
                        agent = 'ALL'
                    print '\n'
                    flow_name = raw_input('Enter the sFlow Flow Name (Required): ')
                    sflow.sflow_active_flows(url_sflow, agent, flow_name)
                elif cmd == 'sflow comp flows':
                    print '\n\nEnter the part of the network (i.e. edge or core) you want to monitor ?\n'
                    print 'Default value = ¨edge¨\n'
                    choice = raw_input('Network Part (¨edge¨/¨core¨): ')
                    choice = choice.lower()
                    if (choice == 'core' or choice == 'c'):
                        url_sflow = url_core_sflow
                    else:
                        url_sflow = url_edge_sflow
                    sflow.sflow_comp_flows(url_sflow)
                elif cmd == 'sflow groups':
                    print '\n\nEnter the part of the network (i.e. edge or core) you want to monitor ?\n'
                    print 'Default value = ¨edge¨\n'
                    choice = raw_input('Network Part (¨edge¨/¨core¨): ')
                    choice = choice.lower()
                    if (choice == 'core' or choice == 'c'):
                        url_sflow = url_core_sflow
                    else:
                        url_sflow = url_edge_sflow
                    sflow.sflow_groups(url_sflow)
                elif cmd == 'sflow group def':
                    print '\n\nEnter the following details for a sFlow address group definition/details...'
                    print '\nNote: If you want to skip an entry, press the enter key\n\n'
                    print 'Enter the part of the network (i.e. edge or core) you want to monitor ?\n'
                    print 'Default value = ¨edge¨\n'
                    choice = raw_input('Network Part (¨edge¨/¨core¨): ')
                    choice = choice.lower()
                    if (choice == 'core' or choice == 'c'):
                        url_sflow = url_core_sflow
                    else:
                        url_sflow = url_edge_sflow
                    print '\n\n'
                    group_name = raw_input('Enter the sFlow Address Group Name (Required): ')
                    sflow.sflow_group_def(url_sflow, group_name)
                elif cmd == 'sflow group add':
                    group_data = {}
                    print '\n\nEnter the following details for adding a sFlow address group to categorize network traffic...'
                    print '\nNote: If you want to skip an entry, press the enter key\n\n'
                    print 'Enter the part of the network (i.e. edge or core) you want to monitor ?\n'
                    print 'Default value = ¨edge¨\n'
                    choice = raw_input('Network Part (¨edge¨/¨core¨): ')
                    choice = choice.lower()
                    if (choice == 'core' or choice == 'c'):
                        url_sflow = url_core_sflow
                    else:
                        url_sflow = url_edge_sflow
                    print '\n\n'
                    group_name = raw_input('Enter the sFlow Address Group Name (Required): ')
                    print '\n\nDefine attributes for the sFlow address group (e.g. ¨external¨, ¨internal¨, ¨private¨, ¨multicast¨, etc.)...\n'
                    while True:
                        add_list = []
                        choice = raw_input('Do you want to add an attribute ? (¨yes¨/¨no¨): ')
                        choice = choice.lower()
                        if (choice == 'yes' or choice == 'y'):
                            print '\n'
                            group_attribute = raw_input('Attribute Name: ')
                            print '\n\nEnter the list of addresses you want to add as ¨',group_attribute,'¨...\n'
                            while True:
                                choice = raw_input('Do you want to add an address ? (¨yes¨/¨no¨): ')
                                choice = choice.lower()
                                if (choice == 'yes' or choice == 'y'):
                                    print '\n'
                                    add = raw_input('Address: ')
                                    add_list.append(add)
                                    print '\n'
                                elif (choice == 'no' or choice == '' or choice == 'n'):
                                    print '\n'
                                    break
                                else:
                                    print '\nInvalid entry !!\n'
                                    print '\n'
                            group_data[group_attribute] = add_list
                        elif (choice == 'no' or choice == '' or choice == 'n'):
                            print '\n'
                            break
                        else:
                            print '\nInvalid entry !!\n'
                        print '\n\n'
                    sflow.sflow_group_add(url_sflow, sflow_header, group_name, group_data)
                elif cmd == 'sflow group del':
                    print '\n\nEnter the following details for deleting a sFlow address group...'
                    print '\nNote: If you want to skip an entry, press the enter key\n\n'
                    print 'Enter the part of the network (i.e. edge or core) you want to monitor ?\n'
                    print 'Default value = ¨edge¨\n'
                    choice = raw_input('Network Part (¨edge¨/¨core¨): ')
                    choice = choice.lower()
                    if (choice == 'core' or choice == 'c'):
                        url_sflow = url_core_sflow
                    else:
                        url_sflow = url_edge_sflow
                    print '\n\n'
                    group_name = raw_input('Enter the sFlow Address Group Name (Required): ')
                    sflow.sflow_group_del(url_sflow, group_name)
                elif cmd == 'sflow thresholds':
                    print '\n\nEnter the part of the network (i.e. edge or core) you want to monitor ?\n'
                    print 'Default value = ¨edge¨\n'
                    choice = raw_input('Network Part (¨edge¨/¨core¨): ')
                    choice = choice.lower()
                    if (choice == 'core' or choice == 'c'):
                        url_sflow = url_core_sflow
                    else:
                        url_sflow = url_edge_sflow
                    sflow.sflow_thresholds(url_sflow)
                elif cmd == 'sflow thresh def':
                    print '\n\nEnter the following details for a sFlow threshold definition/details...'
                    print '\nNote: If you want to skip an entry, press the enter key\n\n'
                    print 'Enter the part of the network (i.e. edge or core) you want to monitor ?\n'
                    print 'Default value = ¨edge¨\n'
                    choice = raw_input('Network Part (¨edge¨/¨core¨): ')
                    choice = choice.lower()
                    if (choice == 'core' or choice == 'c'):
                        url_sflow = url_core_sflow
                    else:
                        url_sflow = url_edge_sflow
                    print '\n\n'
                    thresh_name = raw_input('Enter the sFlow Threshold Name (Required): ')
                    sflow.sflow_thresh_def(url_sflow, thresh_name)
                elif cmd == 'sflow thresh add':
                    thresh_data = {}
                    print '\n\nEnter the following details for adding a sFlow threshold limit/value...'
                    print '\nNote: If you want to skip an entry, press the enter key\n\n'
                    print 'Enter the part of the network (i.e. edge or core) you want to monitor ?\n'
                    print 'Default value = ¨edge¨\n'
                    choice = raw_input('Network Part (¨edge¨/¨core¨): ')
                    choice = choice.lower()
                    if (choice == 'core' or choice == 'c'):
                        url_sflow = url_core_sflow
                    else:
                        url_sflow = url_edge_sflow
                    print '\n\n'
                    thresh_name = raw_input('Enter the Threshold Name (Required): ')
                    print '\n\nEnter the metric name for which you want to set a sFlow threshold value...\n'
                    metric = raw_input('Enter the Metric Name (Required): ')
                    print '\n\nEnter the threshold value for the above metric...\n'
                    value = raw_input('Enter the Threshold value (Required): ')
                    print '\n\nEnter the filter (seperated by ¨&¨) you want to add to the threshold definition...\n'
                    filt = raw_input('Enter the Threshold Filter: ')
                    thresh_data['metric'] = metric
                    thresh_data['value'] = value
                    if not filt == '':
                        thresh_data['filter'] = filt
                    sflow.sflow_thresh_add(url_sflow, sflow_header, thresh_name, thresh_data)
                elif cmd == 'sflow thresh del':
                    print '\n\nEnter the following details for deleting a sFlow threshold...'
                    print '\nNote: If you want to skip an entry, press the enter key\n\n'
                    print 'Enter the part of the network (i.e. edge or core) you want to monitor ?\n'
                    print 'Default value = ¨edge¨\n'
                    choice = raw_input('Network Part (¨edge¨/¨core¨): ')
                    choice = choice.lower()
                    if (choice == 'core' or choice == 'c'):
                        url_sflow = url_core_sflow
                    else:
                        url_sflow = url_edge_sflow
                    print '\n\n'
                    thresh_name = raw_input('Enter the sFlow Threshold Name (Required): ')
                    sflow.sflow_thresh_del(url_sflow, thresh_name)
                elif cmd == 'sflow events':
                    print '\n\nDefine a filter (seperated by ¨&¨) to filter out the list of sFlow events (e.g. maxEvents, timeout, etc.)...'
                    print '\nNote: If you want to skip an entry, press the enter key\n\n'
                    print 'Enter the part of the network (i.e. edge or core) you want to monitor ?\n'
                    print 'Default value = ¨edge¨\n'
                    choice = raw_input('Network Part (¨edge¨/¨core¨): ')
                    choice = choice.lower()
                    if (choice == 'core' or choice == 'c'):
                        url_sflow = url_core_sflow
                    else:
                        url_sflow = url_edge_sflow
                    print '\n\n'
                    events_filter = raw_input('Enter the Events Filter: ')
                    response = sflow.sflow_events(url_sflow, events_filter)
                elif cmd == 'core snmp agents':
                    url_snmp = url_core_snmp
                    snmp_agent = snmp.snmp_agents(url_snmp)
                elif cmd == 'snmp agent int':
                    print '\n\nEnter the following details for the list of interfaces of an SNMP agent along with SNMP ifindex to physical description mappings...'
                    print '\nNote: If you want to skip an entry, press the enter key\n\n'
                    print '\n'
                    agent = raw_input('Enter the SNMP Agent\'s IP Address (or) the Agent\'s Alias Name (Required): ')
                    print '\n'
                    url_snmp = url_core_snmp
                    snmp_agent_interfaces = snmp.snmp_agent_interfaces(url_snmp, agent)
                elif cmd == 'snmp int mac':
                    print '\n\nEnter the following details for the MAC (i.e. physical) addresses of the SNMP agent interfaces...'
                    print '\nNote: If you want to skip an entry, press the enter key\n\n'
                    print '\n'
                    agent = raw_input('Enter the SNMP Agent\'s IP Address (or) the Agent\'s Alias Name (Required): ')
                    print '\n'
                    url_snmp = url_core_snmp
                    snmp_interface_mac = snmp.snmp_agent_interfaces_mac(url_snmp, agent)
                elif cmd == 'uti thresh def':
                    url_snmp = url_core_snmp
                    snmp_uti_thresholds = snmp.snmp_uti_thresh_def(url_snmp)
                elif cmd == 'uti thresh add':
                    thresh_data = {}
                    print '\n\nEnter the following details for adding/changing SNMP based interface utilization thresholds...'
                    print '\nNote: If you want to skip an entry, press the enter key\n\n'
                    print 'Enter the SNMP based interface utilization thresholds for incoming and outgoing traffic in % of total available bandwidth...'
                    print '\n'
                    if_in_uti_threshold = raw_input('Incoming Traffic Interface Utilization Threshold (Required): ')
                    if_out_uti_threshold = raw_input('Outgoing Traffic Interface Utilization Threshold (Required): ')
                    thresh_data['ifinutilization'] = if_in_uti_threshold
                    thresh_data['ifoututilization'] = if_out_uti_threshold
                    print '\n'
                    url_snmp = url_core_snmp
                    snmp_uti_thresholds = snmp.snmp_uti_thresh_add(url_snmp, thresh_data)
                elif cmd == 'snmp int events':
                    print '\n\nEnter the following details for the list of triggered network core - SNMP interface monitoring events...'
                    print '\nNote: If you want to skip an entry, press the enter key\n\n'
                    print '\n'
                    agent = raw_input('Enter the SNMP Agent\'s IP Address (or) the Agent\'s Alias Name (Required): ')
                    print '\n'
                    print 'Enter the metric for which you want the list of triggered network core - SNMP interface monitoring events...\n'
                    print 'Default value = ¨utilizations¨\n'
                    choice = raw_input('Network Core - SNMP Interface Monitoring Metric (¨utilization¨/¨status¨): ')
                    choice = choice.lower()
                    if (choice == 'status' or choice == 's'):
                        metric = 'status'
                    else:
                        metric = 'utilization'
                    url_snmp = url_core_snmp
                    snmp_events = snmp.snmp_agent_interface_events(url_snmp, agent, metric)
                elif cmd == 'test 1 topo':
                    print '\n\n'
                    for key in testbed_1_topo:
                        ip = key
                        print 'Switch IP Address :', ip
                        for key in edge_sflow_agents:
                            agent = key
                            if ip == edge_sflow_agents[agent]:
                                alias = agent
                        for key in core_sflow_agents:
                            agent = key
                            if ip == core_sflow_agents[agent]:
                                alias = agent
                        print 'Switch Alias Name :', alias
                        neighbors = testbed_1_topo[ip]
                        print '\nList of the above Switch\'s Direct Neighbors :\n'
                        i = 0
                        for key in neighbors:
                            i += 1
                            ifs = key
                            ip = neighbors[ifs]
                            print 'Neighbor ', i
                            print 'Neighbor Connected through the Switch\'s Physical Interface :', ifs
                            print 'Neighboring Switch IP Address :', ip
                            for key in edge_sflow_agents:
                                agent = key
                                if ip == edge_sflow_agents[agent]:
                                    alias = agent
                            for key in core_sflow_agents:
                                agent = key
                                if ip == core_sflow_agents[agent]:
                                    alias = agent
                            print 'Neighboring Switch Alias Name :', alias
                            print '\n'
                        print '\n\n'
                elif cmd == 'test 2 topo':
                    print '\n\n'
                    for key in testbed_2_topo:
                        ip = key
                        print 'Switch IP Address :', ip
                        for key in edge_sflow_agents:
                            agent = key
                            if ip == edge_sflow_agents[agent]:
                                alias = agent
                        for key in core_snmp_agents:
                            agent = key
                            if ip == core_snmp_agents[agent]:
                                alias = agent
                        print 'Switch Alias Name :', alias
                        neighbors = testbed_2_topo[ip]
                        print '\nList of the above Switch\'s  Direct Neighbors :\n'
                        i = 0
                        for key in neighbors:
                            i += 1
                            ifs = key
                            ip = neighbors[ifs]
                            print 'Neighbor ', i
                            print 'Neighbor Connected through the Node Physical Interface :', ifs
                            print 'Neighboring Switch IP Address :', ip
                            for key in edge_sflow_agents:
                                agent = key
                                if ip == edge_sflow_agents[agent]:
                                    alias = agent
                            for key in core_snmp_agents:
                                agent = key
                                if ip == core_snmp_agents[agent]:
                                    alias = agent
                            print 'Neighboring Switch Alias Name :', alias
                            print '\n'
                        print '\n\n'
                elif cmd == 'test 1 lsps':
                    print '\n\n'
                    for key in testbed_1_lsps:
                        label = key
                        switches = []
                        print 'MPLS LSP Ingress Push Label (i.e. At Network Edge) :', label
                        switches = testbed_1_lsps[label]
                        in_ip = switches[0]
                        print 'MPLS LSP Ingress Switch (i.e. LER) IP Address :', in_ip
                        for key in edge_sflow_agents:
                            agent = key
                            if in_ip == edge_sflow_agents[agent]:
                                in_alias = agent
                        print 'MPLS LSP Ingress Switch (i.e. LER) Alias Name :', in_alias
                        l = len(switches)
                        l = l-1
                        eg_ip = switches[l]
                        print 'MPLS LSP Egress Switch (i.e. LER) IP Address :', eg_ip
                        for key in edge_sflow_agents:
                            agent = key
                            if eg_ip == edge_sflow_agents[agent]:
                                eg_alias = agent
                        print 'MPLS LSP Egress Switch (i.e. LER) Alias Name :', eg_alias
                        print '\nSwitch (i.e. LSRs) Path in the above LSP :\n'
                        i = 0
                        for switch in switches:
                            print '|'
                            print 'Switch ', i
                            ip = switch
                            print 'Switch (i.e. LSR) IP Address :', ip
                            for key in edge_sflow_agents:
                                agent = key
                                if ip == edge_sflow_agents[agent]:
                                    alias = agent
                            for key in core_sflow_agents:
                                agent = key
                                if ip == core_sflow_agents[agent]:
                                    alias = agent
                            print 'Switch (i.e. LSR) Alias Name :', alias
                            print '|'
                        print '\n'
                elif cmd == 'test 2 lsps':
                    print '\n\n'
                    for key in testbed_2_lsps:
                        label = key
                        switches = []
                        print 'MPLS LSP Ingress Push Label (i.e. At Network Edge) :', label
                        switches = testbed_2_lsps[label]
                        in_ip = switches[0]
                        print 'MPLS LSP Ingress Switch (i.e. LER) IP Address :', in_ip
                        for key in edge_sflow_agents:
                            agent = key
                            if in_ip == edge_sflow_agents[agent]:
                                in_alias = agent
                        print 'MPLS LSP Ingress Switch (i.e. LER) Alias Name :', in_alias
                        l = len(switches)
                        l = l-1
                        eg_ip = switches[l]
                        print 'MPLS LSP Egress Switch (i.e. LER) IP Address :', eg_ip
                        for key in edge_sflow_agents:
                            agent = key
                            if eg_ip == edge_sflow_agents[agent]:
                                eg_alias = agent
                        print 'MPLS LSP Egress Switch (i.e. LER) Alias Name :', eg_alias
                        print '\nSwitch (i.e. LSRs) Path in above LSP :\n'
                        i = 0
                        for switch in switches:
                            print '|'
                            print 'Switch ', i
                            ip = switch
                            print 'Switch (i.e. LSR) IP Address :', ip
                            for key in edge_sflow_agents:
                                agent = key
                                if ip == edge_sflow_agents[agent]:
                                    alias = agent
                            for key in core_snmp_agents:
                                agent = key
                                if ip == core_snmp_agents[agent]:
                                    alias = agent
                            print 'Switch (i.e. LSR) Alias Name :', alias
                            print '|'
                        print '\n'
                elif cmd == 'load balancing':
                    pid = subprocess.Popen(args=["gnome-terminal", "--command=python Setup_Load_Balancing_App.py"]).pid
                    print '\n\nOpenning a new gnome terminal...'
                elif cmd == 'edge firewall':
                    pid = subprocess.Popen(args=["gnome-terminal", "--command=python Setup_Edge_Firewall_App.py"]).pid
                    print '\n\nOpenning a new gnome terminal...'
                elif cmd == 'basic connectivity':
                    pid = subprocess.Popen(args=["gnome-terminal", "--command=python Setup_Basic_Connectivity_App.py"]).pid
                    print '\n\nOpenning a new gnome terminal...'
                else:
                    print '\n\nWrong entry'
                    print '\nFor the list of available commands, enter: Command = ¨list¨ or ¨help¨ or ¨?¨\n'
            except KeyboardInterrupt:
                print '\n\n\nSaving all the changes...'
                print '\nYou are now exiting the NaaS main application...\n'
                static_flow_stats = {}
                with open("Statistics_Logs/Static_Flow_Stats.json", "w") as json_file:
                                json.dump(static_flow_stats, json_file)
                firewall_flow_stats = {}
                with open("Statistics_Logs/Edge_Firewall_Flow_Stats.json", "w") as json_file:
                    json.dump(firewall_flow_stats, json_file)
                mpls_push_flow_stats = {}
                with open("Statistics_Logs/MPLS_Push_Flow_Stats.json", "w") as json_file:
                    json.dump(mpls_push_flow_stats, json_file)
                basic_connectivity_flow_stats = {}
                with open("Statistics_Logs/Testbed_1_Basic_Connectivity_Flow_Stats.json", "w") as json_file:
                    json.dump(basic_connectivity_flow_stats, json_file)
                with open("Statistics_Logs/Testbed_2_Basic_Connectivity_Flow_Stats.json", "w") as json_file:
                    json.dump(basic_connectivity_flow_stats, json_file)
                load_balancing_flow_stats = {}
                with open("Statistics_Logs/Testbed_1_Load_Balancing_Flow_Stats.json", "w") as json_file:
                    json.dump(load_balancing_flow_stats, json_file)
                with open("Statistics_Logs/Testbed_2_Load_Balancing_Flow_Stats.json", "w") as json_file:
                    json.dump(load_balancing_flow_stats, json_file)
                sys.exit(0)
            except:
                print '\n\n\nSaving all the changes...'
                print '\nYou are now exiting the NaaS main application...\n'
                static_flow_stats = {}
                with open("Statistics_Logs/Static_Flow_Stats.json", "w") as json_file:
                                json.dump(static_flow_stats, json_file)
                firewall_flow_stats = {}
                with open("Statistics_Logs/Edge_Firewall_Flow_Stats.json", "w") as json_file:
                    json.dump(firewall_flow_stats, json_file)
                mpls_push_flow_stats = {}
                with open("Statistics_Logs/MPLS_Push_Flow_Stats.json", "w") as json_file:
                    json.dump(mpls_push_flow_stats, json_file)
                load_balancing_flow_stats = {}
                with open("Statistics_Logs/Testbed_1_Load_Balancing_Flow_Stats.json", "w") as json_file:
                    json.dump(load_balancing_flow_stats, json_file)
                with open("Statistics_Logs/Testbed_2_Load_Balancing_Flow_Stats.json", "w") as json_file:
                    json.dump(load_balancing_flow_stats, json_file)
                sys.exit(0)









