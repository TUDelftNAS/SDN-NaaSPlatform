#!/bin/sh



# # #Copyright (C) 2015, Delft University of Technology, Faculty of Electrical Engineering, Mathematics and Computer Science, Network Architectures and Services and TNO, ICT - Service Enabling and Management, Mani Prashanth Varma Manthena, Niels van Adrichem, Casper van den Broek and F. A. Kuipers
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

 Initializing and running all the required python executable files of the SNMP Web Application


# Initializing and running the SNMP based web application - RESTful web services

xterm -e ./SNMP_Main_App.py &


# SNMP based interface monitoring application - Face - a MPLS (i.e. Juniper Legacy Switch) core switch

xterm -e ./Face_Interface_Status_Monitoring_App.py &

xterm -e ./Face_Interface_Utilization_Monitoring_App.py &


# SNMP based interface monitoring application - BA - a MPLS (i.e. Juniper Legacy Switch) core switch

xterm -e ./BA_Interface_Status_Monitoring_App.py &

xterm -e ./BA_Interface_Utilization_Monitoring_App.py &


# SNMP based interface monitoring application - Murdock - a MPLS (i.e. Juniper Legacy Switch) core switch

xterm -e ./Murdock_Interface_Status_Monitoring_App.py &

xterm -e ./Murdock_Interface_Utilization_Monitoring_App.py &


# SNMP based interface monitoring application - Hannibal - a MPLS (i.e. Juniper Legacy Switch) core switch

xterm -e ./Hannibal_Interface_Status_Monitoring_App.py &

xterm -e ./Hannibal_Interface_Utilization_Monitoring_App.py &


