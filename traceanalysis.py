import argparse
import networkx as nx


#extrai os argumentos
parser = argparse.ArgumentParser(description="Descrição")
parser.add_argument("-f","--file",dest="filename",help="the trace file that will be analyzed", metavar="FILENAME")
parser.add_argument("-n","--numberOfNodes",dest="numberOfNodes",help="the number of nodes in the network", metavar="NUMBER")
parser.add_argument("-e","--end",dest="endtime",help="trace ending time", metavar="ENDTIME")
args = parser.parse_args()

#inicia as variáveis globais
def _init():
    global g, last_file_position, f, number_of_nodes, endtime

    #inicializa com um valor default
    number_of_nodes = int(args.numberOfNodes) if args.numberOfNodes else 10

    g = nx.Graph()
    g.add_nodes_from(range(number_of_nodes))

    last_file_position = None
    #print("_init")
    filename = args.filename if args.filename else "default_file"
    f = open(filename)

    endtime = args.endtime if args.endtime else 10000


#pega a linha do trace e retorna um dicionário com os dados
def get_event(line):
    l = line.split()
    d = dict()
    d["from"] = int(l[2]);
    d["to"] = int(l[3]);
    d["event"] = l[1];
    d["time"] = int(l[0]);
    d["status"] = l[4];
    return d

#return True se a conexão está aberta
def is_opening(event):
    if event["status"].lower() == "up":
        return True
    elif event["status"].lower() == "down":
        return False
    else:
        raise Exception("Não é evento de up nem de down")

#initing é inclusivo, ending é exclusivo
def init_graph(initing, ending):
    g.add_nodes_from(range(initing, ending))

#aplica um evento ao grafo (add ou remove uma aresta)
def apply_graph_change(event):
    if is_opening(event):
        g.add_edge(event["from"],event["to"])
    else:
        g.remove_edge(event["from"],event["to"])

#e: o evento a ser processado
def process_events(e):
    apply_graph_change(e)
    #faz outras coisas: salva relatório, mede alguma coisa, etc...
    pass

#retorna os eventos neste instante
def get_events_at_instant(time):
    global last_file_position
    last_file_position = f.tell()
    l = f.readline()
    e = get_event(l)
    _list = []

    while e["time"] == time:
        _list.append(e)
        last_file_position = f.tell()

    #volta o ponteiro do arquivo para a última linha que foi lida
    f.seek(last_file_position)

    return _list

#roda a análise do início ao fim
def run():
    for instant in range(0,endtime):
        events = get_events_at_instant(instant)
        for e in events:
            process_events(e)


def main():
    _init()
    run()

if __name__ == "__main__":
    main()

#conceito de como o processo dos eventos deve funcionar
'''
while now <= end:
    while event_time <= now:
        processa_evento() #apply_graph_change()
        line = f.readline()
        event = get_event(line)

    now = now + 1

'''