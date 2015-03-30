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



# This script requires installation of a python module called PySNMP - a cross-platform, pure-Python SNMP engine implementation
# Its documentation is available at http://pysnmp.sourceforge.net/



# SNMP based interface bandwidth utilization monitoring application - Hannibal - a MPLS (i.e. Juniper Legacy Switch) core switch

print '\n\n\n***Welcome to the SNMP based Interface Bandwidth Utilization Monitoring Application'
print 'For SNMP Agent - Hannibal - a MPLS (i.e. Juniper Legacy Switch) Core Switch***\n\n'



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



# SNMP Agent Configuration Details (i.e. Hannibal)

agent_ip='139.63.246.114'
agent_port = 161
community='public'



# SNMP MIB OID for interface in and out packet/bytes count (i.e. in Octets)

if_in_octets = (1,3,6,1,2,1,2,2,1,10) # (Object : ifInOctets, OID : 1.3.6.1.2.1.2.2.1.10)
if_out_octets = (1,3,6,1,2,1,2,2,1,16) # (Object : ifOutOctets, OID : 1.3.6.1.2.1.2.2.1.16)



# Configuring PySNMP module to poll SNMP interface in and out packet/bytes count - SNMP Version : v2c

generator = cmdgen.CommandGenerator()
comm_data = cmdgen.CommunityData('Hannibal', community, 1) 
transport = cmdgen.UdpTransportTarget((agent_ip, agent_port))



# Physical interface to SNMP IfIndex mapping

with open("Config/Device_Interfaces/Hannibal_Interface_List.json") as json_file:
            if_list = {}
            if_list = json.load(json_file)



# Monitoring interfaces for high bandwidth utilization events - SNMP polling interval is 20 seconds

if_speed = 1000000000 # 1 Gbps links - constant maximum speed links
if_in_prev_time = 0
if_out_prev_time = 0


while True:
    with open("Config/Thresholds/Utilization_Thresholds.json") as json_file:
        uti_thresholds = {}
        uti_thresholds = json.load(json_file)
    if_in_uti_threshold = int(uti_thresholds['ifinutilization'])
    if_out_uti_threshold = int(uti_thresholds['ifoututilization'])
    print 'Interface Utilization Threshold for Incoming Traffic: ', if_in_uti_threshold
    print 'Interface Utilization Threshold for Outgoing Traffic: ', if_out_uti_threshold
    print '\n\n'
    if_in_octets_call = getattr(generator, 'nextCmd')
    response = (errorIndication, errorStatus, errorIndex, varBinds)\
             = if_in_octets_call(comm_data, transport, if_in_octets)
    if_in_cur_time = time.time()
    if_in_time_diff = if_in_cur_time - if_in_prev_time
    if_in_prev_time = if_in_cur_time
    if_in_stat = response[3]
    if_out_octets_call = getattr(generator, 'nextCmd')
    response = (errorIndication, errorStatus, errorIndex, varBinds)\
             = if_out_octets_call(comm_data, transport, if_out_octets)

    if_out_cur_time = time.time()
    if_out_time_diff = if_out_cur_time - if_out_prev_time
    if_out_prev_time = if_out_cur_time
    if_out_stat = response[3]
    with open("Logs/Hannibal_If_In_Octet.json") as json_file:
            if_in_octet_prev_stat = {}
            if_in_octet_prev_stat = json.load(json_file)
    with open("Logs/Hannibal_If_Out_Octet.json") as json_file:
            if_out_octet_prev_stat = {}
            if_out_octet_prev_stat = json.load(json_file)
    i = 0
    high_uti_events = {}
    if_in_octet_stat = {}
    if_out_octet_stat = {}
    for (ifis, ifos) in zip(if_in_stat, if_out_stat) :
        obj = ifis[0][0]
        obj = str(obj)
        obj_list = obj.split(".")
        if (obj_list[10] == '503' or obj_list[10] == '505' or obj_list[10] == '506'):
            print 'Interface ID: ', obj_list[10]
            print '\nInterface Physical Description: ', if_list[obj_list[10]]
            print '\nInterface Total Available Bandwidth/Speed in bits per second: ', if_speed
            if_in_octet_cur = float(ifis[0][1])
            if_out_octet_cur = float(ifos[0][1])
            if_in_octet_prev = float(if_in_octet_prev_stat[obj_list[10]])
            if_out_octet_prev = float(if_out_octet_prev_stat[obj_list[10]])
            if_in_octet_diff = float(if_in_octet_cur - if_in_octet_prev)
            if_out_octet_diff = float(if_out_octet_cur - if_out_octet_prev)
            if_in_down = float(if_in_time_diff*if_speed)
            if_out_down = float(if_out_time_diff*if_speed)
            if_in_utilization = float((if_in_octet_diff)/ (if_in_down))
            if_out_utilization = float((if_out_octet_diff)/(if_out_down))
            if_in_utilization = float(if_in_utilization*8*100)
            if_out_utilization = float(if_out_utilization*8*100)
            print '\nInterface Total Incoming Bits in the time period of ', if_in_time_diff, ' seconds :', (if_in_octet_diff*8)
            print '\nInterface Total Outgoing Bits in the time period of ', if_out_time_diff, ' seconds :', (if_out_octet_diff*8)
            print '\nInterface Incoming Traffic Utilization in % of Total Available Bandwidth:', if_in_utilization
            print '\nInterface outgoing Traffic Utilization in % of Total Available Bandwidth:', if_out_utilization
            if if_in_utilization >= if_in_uti_threshold:
                i += 1
                event_id = str(i)
                update_time = time.time()
                update_time = str(update_time)
                if_in_utilization = str(if_in_utilization)
                high_uti_info = { 'Agent' : agent_ip, 'Interface ID' : obj_list[10], 'Metric' : 'ifinutilization', 'Value' : if_in_utilization, 'Last Updated' : update_time}
                print '\n\n\n***Detected an High Bandwidth Utilization Event***\n\n'
                print '\n\nEvent Information/Details: \n'
                print high_uti_info
                print '\n\n'
                high_uti_events[event_id] = high_uti_info
            if if_out_utilization >= if_out_uti_threshold:
                i += 1
                event_id = str(i)
                update_time = time.time()
                update_time = str(update_time)
                if_out_utilization = str(if_out_utilization)
                high_uti_info = { 'Agent' : agent_ip, 'Interface ID' : obj_list[10], 'Metric' : 'ifoututilization', 'Value' : if_out_utilization, 'Last Updated' : update_time}
                print '\n\n\n***Detected an High Bandwidth Utilization Event***\n\n'
                print '\n\nEvent Information/Details: \n'
                print high_uti_info
                print '\n\n'
                high_uti_events[event_id] = high_uti_info
            if_in_octet_prev = if_in_octet_cur
            if_out_octet_prev = if_out_octet_cur
            if_in_octet_prev = int(if_in_octet_prev)
            if_out_octet_prev = int(if_out_octet_prev)
            if_in_octet_stat[obj_list[10]] = if_in_octet_prev
            if_out_octet_stat[obj_list[10]] = if_out_octet_prev
            print '\n\n'
    with open("Events/Interface/Hannibal_Utilizations.json", "w") as json_file:
        json.dump(high_uti_events, json_file)
    with open("Logs/Hannibal_If_In_Octet.json", "w") as json_file:
        json.dump(if_in_octet_stat, json_file)
    with open("Logs/Hannibal_If_Out_Octet.json", "w") as json_file:
        json.dump(if_out_octet_stat, json_file)
    if high_uti_events == {}:
        print '\n\n***No High Bandwidth Utilization Events***\n\n'
    time.sleep(20)







