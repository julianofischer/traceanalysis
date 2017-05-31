# coding: utf-8

__author__ = "Juliano Fischer Naves"


class Event:
    def __init__(self, d):
        self.from_node = d["from"]
        self.to_node = d["to"]
        self.time = d["time"]
        self.__status = d["status"]

        if self.__status == "up":
            self.opening = True
        elif self.__status == "down":
            self.opening = False
        else:
            raise Exception("Evento não é down nem up")

    def is_opening(self):
        return self.opening


class Connection:
    def __init__(self, event):

        self.end_time = None

        if event:
            self.from_node = event.from_node
            self.to_node = event.to_node
            self.init_time = event.init_time

    def duration(self):
        assert self.end_time, "end_time not set - unable to compute duration"
        return self.end_time - self.init_tim

    def get_id(self):
        return str(min(self.from_node, self.to_node)) + ":"+str(max(self.from_node,self.to_node))

    # Se a conexão já foi fechada
    def was_closed(self):
        return self.end_time != None

    # def __eq__(self, other):
    #    return isinstance(other,self.__class__) and self.from_node == other.from_node and self.to_node == other.to_node and self.init_time == other.init_time

    def is_same_connections(self, c):
        return (c.from_node == self.from_node and self.to_node == c.to_node) or (
        c.from_node == self.to_node and c.to_node == self.from_node)

        # def __hash__(self):
        #    if self.from_node > self.to_node:
        #        return hash((self.from_node, self.to_node))
        #    else:
        #        return hash((self.to_node,self.from_node))
