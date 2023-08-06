# -*- coding: utf-8 -*-

from .profile_data import PiData
from jennifer.pconstants import *


class PiExternalCall(PiData):
    def __init__(self, active_object, protocol, host, port, text_hash):
        PiData.__init__(self)

        self.type = PiData.TYPE_EXTERNAL_CALL
        self.text_hash = text_hash
        self.start_time = active_object.get_current_point_time()
        self.start_cpu = active_object.get_end_of_cpu_time()
        self.end_time = 0
        self.end_cpu = 0

        # proxy로 넘어간 후 처리되는 데이터
        self.host = host
        self.port = port

        protocol = protocol.lower()
        if protocol == 'https':
            self.call_type = REMOTE_CALL_TYPE_HTTPS
        else:
            self.call_type = REMOTE_CALL_TYPE_HTTP
        self.desc_hash = text_hash
        self.error_hash = 0

    def get_type(self):
        return self.type
