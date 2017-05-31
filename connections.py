__author__ = "Juliano Fischer Naves"

class Event:
    def __init__(self, from_node, to_node, init_time, status):
        self.from_node = from_node
        self.to_node = to_node
        self.init_time = init_time
        self.status = status

    def is_opening(self):
        if self.status == "up":
            return True
        else:
            return False


class Connection:
    def __init__(self,from_node=None,to_node=None,init_time=None,event=None):

        self.end_time = None

        if event:
            self.from_node = event.from_node
            self.to_node = event.to_node
            self.init_time = event.init_time

            if from_node:
                print("WARNING: from_node will be ignored because event was passed")
            if to_node:
                print("WARNING: to_node will be ignored because event was passed")
            if init_time:
                print("WARNING: init_time will be ignored because event was passed")
        else:
            self.from_node = from_node
            self.to_node = to_node
            self.init_time = init_time

    def duration(self):
        assert self.end_time, "end_time not set - unable to compute duration"
        return self.end_time - self.init_time

    def get_id(self):
        return str(min(self.from_node, self.to_node)) + ":"+str(max(self.from_node,self.to_node))