#!/usr/bin/env python3

import argparse
import sys
import cli

parser = argparse.ArgumentParser(description='Syslog spcific VLAN learn MAC addresses')
parser.add_argument("VLAN", type=int, help="VLAN ID of table that will be checked")
args = parser.parse_args()

vlan = args.VLAN

if vlan not in range(1,4095):
  sys.exit("VLAN ID must be between 1 and 4094")

# CONST
syslog_level = 6

# Start log
nul = cli.execute('send log 6 event-type="MAC logging start", vlan-id={}'.format(vlan))

# Collecting MAC address table
# Example command:
# 'show mac address-table vlan 1 | i DYNAMIC'
# Example output:
# 1    000a.000b.000c    DYNAMIC     Gi1/0/1
command = 'show mac address-table vlan {} | i DYNAMIC'.format(vlan)
lines = cli.execute(command).split('\n')
no_mac = True
for line in lines:
  a = line.split()
	# After splitting the line list contents should be:
	# a[0] = VLAN ID
	# a[1] = MAC address
	# a[2] = "DYNAMIC"
	# a[3] = Interface
  if len(a)==4:
    msg = 'event-type="MAC info", vlan-id={}, mac={}, interface={}'.format(a[0], a[1], a[3])
    nul = cli.execute('send log {} {}'.format(syslog_level, msg))
    no_mac = False
if no_mac:
  nul = cli.execute('send log 6 event-type="No MAC info", vlan-id={}'.format(vlan))

# End log
nul = cli.execute('send log 6 event-type="MAC logging end", vlan-id={}'.format(vlan))