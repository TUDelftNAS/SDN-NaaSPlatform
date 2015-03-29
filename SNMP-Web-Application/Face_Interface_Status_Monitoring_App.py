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



# This script requires installation of a python module called PySNMP - a cross-platform, pure-Python SNMP engine implementation
# Its documentation is available at http://pysnmp.sourceforge.net/



# SNMP based interface operating status monitoring application - Face - a MPLS (i.e. Juniper Legacy Switch) core switch

print '\n\n\n***Welcome to the SNMP based Interface Operating Status Monitoring Application'
print 'For SNMP Agent - Face - a MPLS (i.e. Juniper Legacy Switch) Core Switch***\n\n'



# Importing Python modules

import os, sys
import socket
import random
import time
import json
from struct import pack, unpack
from datetime import datetime as dt



# Importing PySNMP python module - a cross-platform, pure-Python SNMP engine implementation

from pysnmp.entity.rfc3413.oneliner import cmdgen
from pysnmp.proto.rfc1902 import Integer, IpAddress, OctetString



# SNMP Agent Configuration Details (i.e. Face)

agent_ip='139.63.246.113'
agent_port = 161
community='public'



# SNMP MIB OID for interface operating status statistics (Object : ifOperStatus, OID : 1.3.6.1.2.1.2.2.1.8)

if_op_status = (1,3,6,1,2,1,2,2,1,8)



# Configuring PySNMP module to poll SNMP interface operating status statistics - SNMP Version : v2c

generator = cmdgen.CommandGenerator()
comm_data = cmdgen.CommunityData('Face', community, 1) 
transport = cmdgen.UdpTransportTarget((agent_ip, agent_port))



# Physical interface to SNMP IfIndex mapping

with open("Config/Device_Interfaces/Face_Interface_List.json") as json_file:
            if_list = {}
            if_list = json.load(json_file)



# Monitoring interfaces for failure events - SNMP polling interval is 20 seconds

while True:
    if_stat_call = getattr(generator, 'nextCmd')
    response = (errorIndication, errorStatus, errorIndex, varBinds)\
             = if_stat_call(comm_data, transport, if_op_status)
    if_stat = response[3]
    i = 0
    int_fail_events = {}
    for ifs in if_stat:
        obj = ifs[0][0]
        stat = ifs[0][1]
        obj = str(obj)
        stat = str(stat)
        obj_list = obj.split(".")
        if (obj_list[10] == '509' or obj_list[10] == '503' or obj_list[10] == '505'):
            print 'Interface ID: ', obj_list[10]
            print '\nInterface Description: ', if_list[obj_list[10]]
            print '\nInterface Operating Status: ', stat
            if stat != '1':
                i += 1
                event_id = str(i)

                update_time = time.time()
                update_time = str(update_time)
                int_fail_info = { 'Agent' : agent_ip, 'Interface ID' : obj_list[10], 'Metric' : 'ifoperstatus', 'Value' : 'down', 'Last Updated' : update_time}
                print '\n\n***Detected an Interface Failure/Down Event***\n\n'
                print '\n\nEvent Information/Details: \n'
                print int_fail_info
                print '\n\n'
                int_fail_events[event_id] = int_fail_info
            print '\n\n'
    with open("Events/Interface/Face_Operational_Status.json", "w") as json_file:
        json.dump(int_fail_events, json_file)
    if int_fail_events == {}:
        print '\n\n***All Interfaces are operating properly***\n\n'
    time.sleep(20)






