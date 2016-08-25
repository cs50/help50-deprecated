#!/bin/bash

# remove /opt/cs50/bin/help50 and any empty parents
rm -f /opt/cs50/bin/help50
rmdir --ignore-fail-on-non-empty -p /opt/cs50/bin
