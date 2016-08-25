#!/bin/bash

# 
chmod -R a+rX /opt/cs50/help50
chmod -R a+x /opt/cs50/help50/bin/*

#
umask 0022

# 
mkdir -p /opt/cs50/bin
ln -s /opt/cs50/help50/bin/help50 /opt/cs50/bin/help50
