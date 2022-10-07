# MAC logging over syslog

## Structure

- Guestshell enabled on Cat9000
- EEM Cron initiates a python script in guesthell
- Script collects MAC address table dynamic entries for a specified VLAN
- Script parses MAC address table and forwards to syslog as K,V pairs.

## Deployment

1. Enable IOX and guestshell
```
! Enable IOX
conf t
iox
app-hosting appid guestshell
 app-vnic management guest-interface 0
end
! Wait until iox-service is running
! Enable guestshell
guestshell enable
```
2. Copy/create pyhton script
```
# guestshell run bash
[guestshell@guestshell ~]$ cd /bootflash/guest-share/
[guestshell@guestshell guest-share]$ vi mac_log.py
< -- paste script -->
```
3. Configure EEM. One applet per VLAN or add additonal actions per logged VLAN
```
! Replace ####
conf t
event manager applet MAC_LOG_VLAN#### authorization bypass
 description EEM cron scheduler for MAC logging python script
 event timer cron cron-entry "*/5 * * * *"
 action 0001 cli command "enable"
 action 0002 cli command "terminal length 0"
 action 0003 cli command "guestshell run python3 bootflash:/guest-share/mac_log.py ####"
end
```

## Operations

### EEM:
EEM active events running:
`show event manager policy active`
EEM event history:
`show event manager history events`

### Guestshell
Check iox service status. All should be running.
`show iox-service`

### Example logs
MAC addresses exist.
```
Oct  3 15:45:04.252: %SYS-6-USERLOG_INFO: Message from tty73(user id: shxUnknown TTY): Start of MAC logging script for VLAN 1020
Oct  3 15:45:05.483: %SYS-6-USERLOG_INFO: Message from tty73(user id: shxUnknown TTY): vlan-id=1020, mac=0001.0002.0003, interface=Gi1/0/16
Oct  3 15:45:11.023: %SYS-6-USERLOG_INFO: Message from tty73(user id: shxUnknown TTY): End of MAC logging script for VLAN 1020
```
No MAC addresses on switch.
```
Oct  3 15:10:04.047: %SYS-6-USERLOG_INFO: Message from tty73(user id: shxUnknownTTY): Start of MAC logging script for VLAN 1020
Oct  3 15:10:05.278: %SYS-6-USERLOG_INFO: Message from tty73(user id: shxUnknownTTY): No MAC addresses found in VLAN 1020
Oct  3 15:10:05.894: %SYS-6-USERLOG_INFO: Message from tty73(user id: shxUnknownTTY): End of MAC logging script for VLAN 1020
```
