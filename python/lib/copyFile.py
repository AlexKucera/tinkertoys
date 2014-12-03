#!/usr/bin/env python
# encoding: utf-8
"""
copyFile.py

Created by Alexander Kucera on 2013-05-23.
Copyright (c) 2013 BabylonDreams. All rights reserved.
"""

import os, shutil

def copyFile(src, dst, buffer_size=10485760, perserveFileDate=True):
    '''
    Copies a file to a new location. Much faster performance than Apache Commons due to use of larger buffer
    @param src:    Source File
    @param dst:    Destination File (not file path)
    @param buffer_size:    Buffer size to use during copy
    @param perserveFileDate:    Preserve the original file date
    '''
    #    Check to make sure destination directory exists. If it doesn't create the directory
    dstParent, dstFileName = os.path.split(dst)
    if(not(os.path.exists(dstParent))):
        os.makedirs(dstParent)
    
    #    Optimize the buffer for small files
    buffer_size = min(buffer_size,os.path.getsize(src))
    if(buffer_size == 0):
        buffer_size = 1024
    
    if shutil._samefile(src, dst):
        raise shutil.Error("`%s` and `%s` are the same file" % (src, dst))
    for fn in [src, dst]:
        try:
            st = os.stat(fn)
        except OSError:
            # File most likely does not exist
            pass
        else:
            # XXX What about other special files? (sockets, devices...)
            if shutil.stat.S_ISFIFO(st.st_mode):
                raise shutil.SpecialFileError("`%s` is a named pipe" % fn)
    with open(src, 'rb') as fsrc:
        with open(dst, 'wb') as fdst:
            shutil.copyfileobj(fsrc, fdst, buffer_size)
    
    if(perserveFileDate):
        shutil.copystat(src, dst)