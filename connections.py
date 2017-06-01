# coding: utf-8

__author__ = "Juliano Fischer Naves"


class Event:
    def __init__(self, d):
        self.from_node = d["from"]
        self.to_node = d["to"]
        self.time = d["time"]
        self.__status = d["status"].lower()
        self.opening = None

        #print("Constructing event with status %s" % (self.__status,))

        if self.__status == "up":
            self.opening = True
        elif self.__status == "down":
            self.opening = False
        else:
            raise Exception("Evento não é down nem up (%s)" % (self.__status,))

    def is_opening(self):
        return self.opening

    def __str__(self):
        return "event [%d,%d,%d,%s]" % (self.time, self.from_node, self.to_node, self.__status)


class Connection:
    def __init__(self, event):

        self.end_time = None

        if event:
            self.from_node = event.from_node
            self.to_node = event.to_node
            self.init_time = event.time

    def duration(self):
        assert self.end_time, "end_time not set - unable to compute duration"
        return self.end_time - self.init_time

    def get_id(self):
        return str(min(self.from_node, self.to_node)) + ":"+str(max(self.from_node,self.to_node))

    # Se a conexão já foi fechada
    def was_closed(self):
        return self.end_time is None

    # def __eq__(self, other):
    #    return isinstance(other,self.__class__) and self.from_node == other.from_node and self.to_node == other.to_node and self.init_time == other.init_time

    def is_same_connection(self, c):
        return (c.from_node == self.from_node and self.to_node == c.to_node) or (
            c.from_node == self.to_node and c.to_node == self.from_node)

        # def __hash__(self):
        #    if self.from_node > self.to_node:
        #        return hash((self.from_node, self.to_node))
        #    else:
        #        return hash((self.to_node,self.from_node))

    def __str__(self):
        end = self.end_time if self.end_time is not None else -1
        return "connection [%d, %d, %d, %d]" % (self.init_time, self.from_node, self.to_node, end)
