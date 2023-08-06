# -*- coding: utf-8 -*-

from .profile_data import PiData
from jennifer.pconstants import *


class PiSql(PiData):
    def __init__(self, active_object, query_hash, query, params, query_format, host, port, db_type):
        PiData.__init__(self)

        self.active_object = active_object
        self.type = PiData.TYPE_SQL_EXEC

        self.start_time = active_object.get_current_point_time()
        self.start_cpu = active_object.get_end_of_cpu_time()
        self.end_time = 0
        self.end_cpu = 0

        self.is_sync = True
        self.method_type = SQL_DEF_PSTMT_EXE_QRY
        self.key = query_hash
        
        self.dbc = 0
        self.sherpaOracleSequence = 0
        self.sherpaOracleInstanceName = ''

        self.inlineParameters = []
        self.boundParameters = []

        self.dataSourceOrConnectionName = None

        # 아래의 필드는 Proxy 측에서 사용
        self.query = query
        self.params = params
        self.query_format = query_format
        self.port = port
        self.host = host
        self.db_type = db_type
        self.error_hash = 0

    def get_type(self):
        return self.type
