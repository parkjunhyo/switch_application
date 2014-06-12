#! /bin/env bash

## mysql security risk update
sed -i '/local-infile=0/d' /etc/my.cnf
sed -i '2i\local-infile=0' /etc/my.cnf
service mysqld restart

## logging security risk update
chkconfig rsyslog on
service rsyslog restart

## rpc security risk update
service rpcbind stop
chkconfig rpcbind off

service vncserver stop
chkconfig vncserver off

##
