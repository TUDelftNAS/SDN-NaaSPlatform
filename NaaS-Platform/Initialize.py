#!/usr/bin/env python
# -*- coding: utf-8 -*-



# Initializing and running the Network-as-a-Service (NaaS) platform

print '\n\n\n***Welcome to the Network-as-a-Service (NaaS) Platform***\n\n'



# Importing NaaS platform's main application

from Main_App import *



# Initializing and running the NaaS platform's main application

print '\n\nStarting the NaaS Platform\'s Main Application...\n'
print '\n\nYou are now entering the NaaS Platform\'s Main Application...\n\n'


# Initializing the NaaS platform and its architecture

naas = naas_initialize()
naas.odl_config()
naas.edge_sflow_config()
naas.core_sflow_config()
naas.core_snmp_config()


# Accepting the configured management IP addresses of the underlying OF/OVS (i.e. OpenFlow/Open vSwitch) switches that are connected to the ODL controller

odl_switch_ip = odl_ip()


# Assigning alias names to the network OF/OVS switches, sFlow agents, and SNMP agents

switch_odl_alias = odl_alias()
edge_agent_sflow_alias = edge_sflow_alias()
core_agent_sflow_alias = core_sflow_alias()
core_agent_snmp_alias = core_snmp_alias()


# Accepting user commands to manually perform NaaS related operations and functions (i.e. ODL controller and sFlow-RT network analyzer related REST/RESTCONF API calls)

manual = naas_manual()

