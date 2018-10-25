#!/usr/bin/env python
import os
import zipfile

def unpack_zipball(zip_filename, dest_path):
    if not os.path.exists(dest_path):
        os.makedirs(dest_path)
    zip_file = zipfile.ZipFile(zip_filename, 'r')
    zip_file.extractall(dest_path)
    zip_file.close()


