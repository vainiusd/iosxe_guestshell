#!/bin/sh
# Cisco Python cli library logs it activity to file /data/iosp.log
# There is no rotation configured, so simply moving/overwriting it.
mv /data/iosp.log /data/iosp.log1