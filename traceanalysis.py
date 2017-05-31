# coding: utf-8

import argparse

import networkx as nx

from connections import Connection, Event

COMPONENTS_FILE_NAME = "components_log.txt"

# extracting arguments
parser = argparse.ArgumentParser(description="Descrição")
parser.add_argument("-f","--file",dest="filename",help="the trace file that will be analyzed", metavar="FILENAME")
parser.add_argument("-n","--numberOfNodes",dest="numberOfNodes",help="the number of nodes in the network", metavar="NUMBER")
parser.add_argument("-e","--end",dest="endtime",help="trace ending time", metavar="ENDTIME")
parser.add_argument("-s", "--step", dest="log_step", help="The step for logging component information",
                    metavar="NUMBER")
args = parser.parse_args()


# connected_components_log_file = open("connected_components_log")


# inicia as variáveis globais
def _init():
    global g, last_file_position, f, number_of_nodes, endtime, created_connections, \
        open_connections, largest_connected_component, logging_step, last_log, connected_components_log

    # inicializa com um valor default
    number_of_nodes = int(args.numberOfNodes)

    g = nx.Graph()
    g.add_nodes_from(range(number_of_nodes))

    last_file_position = None
    # print("_init")
    filename = args.filename
    f = open(filename)

    # default value is 30
    logging_step = int(args.log_step) if int(args.log_step) else 30

    endtime = int(args.endtime)

    created_connections = []
    open_connections = []
    connected_components_log = []
    largest_connected_component = 0
    last_log = 0


# pega a linha do trace e retorna um objeto de Event
def get_event(line):
    l = line.split()
    d = dict()
    d["from"] = int(l[2])
    d["to"] = int(l[3])
    d["event"] = l[1]
    d["time"] = int(l[0])
    d["status"] = l[4]
    e = Event(d)
    return e


''' initing é inclusivo, ending é exclusivo
def init_graph(initing, ending):
    g.add_nodes_from(range(initing, ending))
'''


# aplica um evento ao grafo (add ou remove uma aresta)
def apply_graph_change(event):
    if event.is_opening():
        g.add_edge(event.from_node, event.to_node)
    else:
        g.remove_edge(event.from_node, event.to_node)


# e:o evento a ser processado
def process_event(e):
    # print ("processing event: "+str(e))
    # cria ou remove uma aresta do grafo
    apply_graph_change(e)

    # adiciona uma conexão a open_connections ou encerra uma conexão
    if e.is_opening():
        c = Connection(e)
        open_connections.append(c)
        created_connections.append(c)
        # print ("Opening connection "+str(c))
    else:
        # é um evento que fecha a conexão
        # print("Fecha conexão")
        close_connection(e)

    # faz outras coisas: salva relatório, mede alguma coisa, etc...
    pass


# recebe um evento por parâmetro e remove uma conexão de open_connections além de adicionar o tempo de encerramento
# da conexão no objeto de Connection
def close_connection(e):
    to_remove = None
    for c in open_connections:
        if c.is_same_connection(e):
            c.end_time = e.time
            to_remove = c
            break
    open_connections.remove(to_remove)


# retorna os eventos neste instante
def get_events_at_instant(time):
    global last_file_position
    last_file_position = f.tell()
    l = f.readline().strip()
    _list = []

    # end of the file
    if len(l) == 0:
        return _list

    e = get_event(l)

    while e.time == time:
        _list.append(e)
        last_file_position = f.tell()
        l = f.readline().strip()

        # end of the file
        if len(l) == 0:
            break

        e = get_event(l)

    # volta o ponteiro do arquivo para a última linha que foi lida
    f.seek(last_file_position)

    return _list


# roda a análise do início ao fim
def run():
    global largest_connected_component, last_log

    for instant in range(0, endtime+1):
        # print("Instant %d" % (instant,))
        events = get_events_at_instant(instant)

        for e in events:
            # print (e)
            process_event(e)

        # get the largest_connected_component
        connected_components = nx.connected_components(g)
        larger = max([len(x) for x in connected_components])
        largest_connected_component = larger if larger > largest_connected_component else largest_connected_component

        list_of_connected_components = list(nx.connected_components(g))

        # instant is equivalent to 'now'
        if instant - last_log > logging_step:
            last_log = instant
            connected_components_log.append("%d    %s\n" % (instant, str(list_of_connected_components)))

    close_remaining_connections(endtime)
    # perform post processing information extraction
    post_processing()


# setting end time for connections which are not closed at trace ending
def close_remaining_connections(t):
    for c in open_connections:
        c.end_time = t


# perform post processing information extraction
def post_processing():
    # write down the log information
    print("Number of connections: %d" % (get_number_of_connections(),))
    print("Average number of connections (per nodes): %f" % (get_average_number_of_connections(),))
    print("Connections per minute: %f" % (get_connections_per_minute(),))
    print("Total connection time: %d" % (get_total_connection_time(),))
    print("Average connection time (per connection): %f" % (get_average_connection_time()))
    print("Largest connected component: %d" % (largest_connected_component,))
    do_the_log()


def do_the_log():
    # logging components
    components_file = open(COMPONENTS_FILE_NAME, "w+")
    components_file.writelines([str(c) for c in connected_components_log])

    # loggin connections
    connections_out_file = open("connections_out_file.txt", "w+")
    connections_out_file.writelines([str(c)+"\n" for c in created_connections])


def get_number_of_connections():
    return len(created_connections)


def get_average_number_of_connections():
    return get_number_of_connections() / number_of_nodes


def get_total_connection_time():
    return sum(c.duration() for c in created_connections)


def get_average_connection_time():
    return get_total_connection_time() / get_number_of_connections()


def get_connections_per_minute():
    minutes = endtime / 60
    return get_number_of_connections() / minutes


def main():
    _init()
    run()

if __name__ == "__main__":
    main()

# conceito de como o processo dos eventos deve funcionar
'''
while now <= end:
    while event_time <= now:
        processa_evento() #apply_graph_change()
        line = f.readline()
        event = get_event(line)

    now = now + 1

'''