from jennifer.pconstants import *


class OutRemoteCall:
    def __init__(self, call_type=REMOTE_CALL_TYPE_NONE, host='', port=0, request_hash=0, recv_sid=0, recv_oid=0, desc_hash=0):
        self.call_type = call_type
        self.host = host
        self.port = port
        self.request_hash = request_hash
        self.recv_sid = recv_sid
        self.recv_oid = recv_oid
        self.desc_hash = desc_hash
