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

