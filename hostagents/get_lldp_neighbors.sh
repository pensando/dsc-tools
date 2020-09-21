#!/bin/bash
for intf in `ls /sys/class/net/ | grep 'enp'` ;
do
peer_mgmt_ip=`lldptool get-tlv -n -i $intf -V mngAddr | grep IPv4`
peer_name=`lldptool get-tlv -n -i $intf -V sysName | grep -v TLV`
peer_port=`lldptool get-tlv -n -i $intf -V portDesc | grep -v TLV`
peer_desc=`lldptool get-tlv -n -i $intf -V sysDesc | grep -v TLV | head -1`
#local_ip=`lldptool get-tlv  -i $intf -V mngAddr | grep IPv4`
if [ -z "$peer_name" ]
then
   echo "Mgmt controller device" > /dev/null
else
   echo "$intf,$peer_mgmt_ip,$peer_name,$peer_port,$peer_desc"
fi
done
