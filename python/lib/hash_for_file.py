#!/usr/bin/env python
# encoding: utf-8

import os, hashlib

def hash_for_file(fileName, block_size=8192):
	hashvalue = hashlib.sha1()
	f = open(fileName, "r")
	while True:
		data = f.read(block_size)
		if not data:
			break
		hashvalue.update(data)
	return hashvalue.digest()