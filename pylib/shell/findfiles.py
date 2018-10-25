#!/usr/bin/env python
import os

def find_file(search_path, filename):
    for dirpath, dirnames, filenames in os.walk(search_path):
        if filename in filenames:
            return os.path.join(dirpath, filename)

    return None
