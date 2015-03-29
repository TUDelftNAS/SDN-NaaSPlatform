#!/bin/sh



# Initializing and running all the required python executable files of the SNMP Web Application


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


