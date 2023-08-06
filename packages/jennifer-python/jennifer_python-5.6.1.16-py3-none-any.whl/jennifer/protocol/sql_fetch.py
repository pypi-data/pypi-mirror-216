from .profile_data import PiData


class PiSqlFetch(PiData):
    def __init__(self, active_object, count):
        PiData.__init__(self)

        self.type = PiData.TYPE_SQL_FETCH
        self.start_time = active_object.get_current_point_time()
        self.start_cpu = active_object.get_end_of_cpu_time()
        self.end_time = 0
        self.end_cpu = 0
        self.count = count

    def get_type(self):
        return self.type
