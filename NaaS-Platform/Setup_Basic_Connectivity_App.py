#!/usr/bin/env python
# -*- coding: utf-8 -*-



# Initializing and running the Network-as-a-Service (NaaS) platform's basic connectivity application

print '\n\n\n***Welcome to the Network-as-a-Service (NaaS) Platform\'s Basic Connectivity Application***\n\n'



# Importing NaaS platform's basic connectivity application

from Basic_Connectivity_App import *



# Initializing and running the NaaS platform's basic connectivity application

try:
    print '\n\nStarting the NaaS Platform\'s Basic Connectivity Application...\n'
    print '\n\nYou are now entering the NaaS Platform\'s Basic Connectivity Application...\n\n'
    print 'Choose the testbed network for which you wish to provide basic connectivity (i.e. testbed-1/testbed-2) ?\n\n'
    print 'testbed-1 - Testbed network (i.e. edge + core) of sFlow enabled open (i.e. OF/OVS) switches'
    print '\n'
    print 'testbed-2 - Testbed network with legacy switches at network core and open (i.e. OF/OVS) switches at the network edge'
    print '\n\n\nDefault value = ¨testbed-1¨\n'
    choice = raw_input('Testbed Network Type (¨testbed-1¨/¨testbed-2¨): ')
    choice = choice.lower()
    if (choice == 'testbed-2' or choice == '2'):
        test = testbed_network_2()
    else:
        test = testbed_network_1()
except KeyboardInterrupt:
    print '\n\n\nSaving all the changes...'
    print '\nYou are now exiting the NaaS platform\'s basic connectivity application...\n'
    sys.exit(0)
except:
    print '\n\n\nSaving all the changes...'
    print '\nYou are now exiting the NaaS platform\'s basic connectivity application...\n'
    sys.exit(0)
