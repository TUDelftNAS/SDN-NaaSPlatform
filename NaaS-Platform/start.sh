#!/bin/sh



# Initializing and running all the required python executable files of the NaaS Platform


# Initializing and running the Network-as-a-Service (NaaS) platform (i.e. main application)

xterm -e ./Initialize.py &


# Initializing and running the Network-as-a-Service (NaaS) platform's basic connectivity application 

xterm -e ./Setup_Basic_Connectivity_App.py &


# Initializing and running the Network-as-a-Service (NaaS) platform's load balancing application

xterm -e ./Setup_Load_Balancing_App.py &


# Initializing and running the Network-as-a-Service (NaaS) platform's edge firewall application

xterm -e ./Setup_Edge_Firewall_App.py &





