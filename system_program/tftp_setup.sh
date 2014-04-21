#! /bin/env bash

## download and installation
yum install -y tftp tftp-server xinetd

## boot start up
chkconfig xinetd on

## create the tftp home server
if [[ ! -d '/tftp_home' ]]
then
 mkdir /tftp_home
 chmod 777 /tftp_home
 cp ./bootscript.py /tftp_home/bootscript.py
 chmod 777 /tftp_home/bootscript.py
fi

## backup the original(init) file
xinetd_tftp_config_bak="/tftp_home/tftp.bak"
if [[ ! -f $xinetd_tftp_config_bak ]]
then
 cp /etc/xinetd.d/tftp $xinetd_tftp_config_bak
fi

## remove the configuration
sed -i '/disable/d' /etc/xinetd.d/tftp
sed -i '/server_args/d' /etc/xinetd.d/tftp

## insert the configuration
sed -i '10i\        disable                 = no' /etc/xinetd.d/tftp
sed -i '13i\        server_args             = -c -s /tftp_home' /etc/xinetd.d/tftp

## iptables rule re-configuration
sed -i '/icmp-host-prohibited/d' /etc/sysconfig/iptables
sed -i '/--dport 69/d' /etc/sysconfig/iptables
sed -i '10i\-A INPUT -m state --state NEW -m udp -p udp -m udp --dport 69 -j ACCEPT' /etc/sysconfig/iptables
service iptables restart

## service restart xinetd daemon
/etc/init.d/xinetd restart
