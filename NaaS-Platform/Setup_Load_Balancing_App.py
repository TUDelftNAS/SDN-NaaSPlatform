#!/usr/bin/env python
# -*- coding: utf-8 -*-



# Initializing and running the Network-as-a-Service (NaaS) platform's load balancing application

print '\n\n\n***Welcome to the Network-as-a-Service (NaaS) Platform\'s Load Balancing Application***\n\n'



# Importing NaaS platform's load balancing application

from Load_Balancing_App import *



# Initializing and running the NaaS platform's load balancing application

try:
    print '\n\nStarting the NaaS Platform\'s Load Balancing Application...\n'
    print '\n\nYou are now entering the NaaS Platform\'s Load Balancing Application...\n\n'
    print 'Choose the testbed network for which you wish to load balance (i.e. testbed-1/testbed-2) ?\n\n'
    print 'testbed-1 - Testbed network (i.e. edge + core) of sFlow enabled open (i.e. OF/OVS) switches'
    print '\n'
    print 'testbed-2 - Testbed network with legacy (i.e. vendor-specific) switches at network core and open (i.e. OF/OVS) switches at the network edge'
    print '\n\n\nDefault value = ¨testbed-1¨\n'
    choice = raw_input('Testbed Network Type (¨testbed-1¨/¨testbed-2¨): ')
    choice = choice.lower()
    if (choice == 'testbed-2' or choice == '2'):
        test = load_balance_testbed_network_2()
    else:
        test = load_balance_testbed_network_1()
except KeyboardInterrupt:
    print '\n\n\nSaving all the changes...'
    print '\nYou are now exiting the NaaS platform\'s load balancing application...\n'
    sys.exit(0)
except:
    print '\n\n\nSaving all the changes...'
    print '\nYou are now exiting the NaaS platform\'s load balancing application...\n'
    sys.exit(0)








