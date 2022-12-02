class Machine:
    def __init__(self, callback, batch_size: int = 10):
        self.vib_left = []
        self.vib_right = []
        self.temp = []
        self.batch_size = batch_size
        self.callback = callback

    def trigger(self):
        if self.is_batch():
            self.callback()
            self.clear_batch()

    def is_batch(self):
        return len(self.vib_left) > self.batch_size \
               and len(self.temp) > self.batch_size \
               and len(self.vib_right) > self.batch_size

    def clear_batch(self):
        del self.vib_left[:self.batch_size]
        del self.vib_right[:self.batch_size]
        del self.temp[:self.batch_size]

    def add_vib_left(self, data):
        self.vib_left.extend(data)

    def add_vib_right(self, data):
        self.vib_right.extend(data)

    def add_vib(self, data_list):
        self.add_vib_left(data_list[0])
        self.add_vib_right(data_list[1])
        self.trigger()

    def add_temp(self, data):
        self.temp.extend(data)
        self.trigger()


class DataController:
    def __init__(self, model_req, batch_size):
        self.machine1 = Machine(model_req, batch_size)
        self.machine2 = Machine(model_req, batch_size)

    def add_vib(self, message: dict):
        self.machine1.add_vib([message['machine1_left'], message['machine1_right']])
        self.machine1.add_vib([message['machine2_left'], message['machine2_right']])

    def add_temp(self, message: dict):
        self.machine1.add_temp(message['machine1'])
        self.machine1.add_temp(message['machine2'])
