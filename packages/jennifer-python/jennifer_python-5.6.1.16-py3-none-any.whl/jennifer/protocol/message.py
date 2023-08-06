from .profile_data import PiData


class PiMessage(PiData):
    def __init__(self, active_object, message):
        PiData.__init__(self)
        self.type = PiData.TYPE_MESSAGE
        self.start_time = active_object.get_current_point_time()
        self.message = message
        self.time = 0

    def get_type(self):
        return self.type

    def print_description(self):
        print(' ' * (self.parent_index + 4), 'Message', self.parent_index, self.index, self.message)
