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



Initializing and running all the required python executable files of the NaaS Platform


# Initializing and running the Network-as-a-Service (NaaS) platform (i.e. main application)

xterm -e ./Initialize.py &


# Initializing and running the Network-as-a-Service (NaaS) platform's basic connectivity application 

xterm -e ./Setup_Basic_Connectivity_App.py &


# Initializing and running the Network-as-a-Service (NaaS) platform's load balancing application

xterm -e ./Setup_Load_Balancing_App.py &


# Initializing and running the Network-as-a-Service (NaaS) platform's edge firewall application

xterm -e ./Setup_Edge_Firewall_App.py &





