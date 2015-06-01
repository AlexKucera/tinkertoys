#!/bin/bash

DISK=$( diskutil list | grep BackupSystem | awk '{print $6}' )
echo $DISK