#! /bin/env bash

## selinux disable 
sed -i 's/SELINUX=enforcing/SELINUX=disabled/' /etc/selinux/config

## iptables stop
service iptables stop
chkconfig iptables off
