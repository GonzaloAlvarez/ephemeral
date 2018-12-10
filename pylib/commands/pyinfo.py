#!/usr/bin/env python
import sys
import logging
import ssl
import json

def ssl_protocols():
    __PROTO_TAG = "PROTOCOL_"
    __OP_NO_TAG = "OP_NO_"
    __OP_NO_TAG_LEN = len(__OP_NO_TAG)
    _PROTOS_DATA = list()
    for item_name in dir(ssl):
        if item_name.startswith(__OP_NO_TAG) and item_name[-1].isdigit():  # item_name[-1].isdigit() condition is required because protocol denial (OP_NO_*) constants end in digit(s) (version); therefore constants like OP_NO_TICKET are excluded
            op_no_item = getattr(ssl, item_name)
            if op_no_item:
                proto_name = item_name[__OP_NO_TAG_LEN:]
                _PROTOS_DATA.append((proto_name, getattr(ssl, __PROTO_TAG + proto_name, -1), op_no_item))
    ctx = ssl.create_default_context()
    supported_classes = (ssl.SSLContext,)
    protocols = list()
    for proto_data in _PROTOS_DATA:
        if ctx.options & proto_data[-1] != proto_data[-1]:
            protocols.append(proto_data[0])
    return protocols


def pyinfo(context):
    ssl_protocols_object = ssl_protocols()
    logging.debug('Capabilities for python executable [{}]: {}'.format(sys.executable, ssl_protocols_object))
    print(json.dumps({
        'executable': sys.executable,
        'version_major': sys.version_info[0],
        'ssl_protocols': ssl_protocols_object}))
