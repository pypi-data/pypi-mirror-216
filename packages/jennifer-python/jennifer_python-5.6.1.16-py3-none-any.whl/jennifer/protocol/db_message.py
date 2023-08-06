from .profile_data import PiData


class PiDBMessage(PiData):

    def __init__(self, active_object, message_type, message):
        PiData.__init__(self)

        self.type = PiData.TYPE_DB_MESSAGE
        self.message = message
        self.message_type = message_type
        self.start_time = active_object.get_current_point_time()
        self.start_cpu = active_object.get_end_of_cpu_time()
        self.end_time = 0
        self.end_cpu = 0

    def get_type(self):
        return self.type
