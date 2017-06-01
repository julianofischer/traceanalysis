# traceanalysis
## Extracted information
- largest connected component
- total number of connections
- connections per minute
- total connection time
- average connection time (per connection)
- average number of connections (per node)
- connected components evolution (each -step seconds)
- max node degree
- average node degree (per nodes per second)


## Prerequisites
### [Python3+](http://www.python.org/)
    sudo apt-get install python3
### [Networkx](https://networkx.github.io/)
    sudo apt-get install python3-networkx
    
## Usage
    traceanalysis.py [-h] [-f FILENAME] [-n NUMBER] [-e ENDTIME]
                            [-s NUMBER]

    Description

    arguments:
      -h, --help            show this help message and exit
      -f FILENAME, --file FILENAME
                            the trace file that will be analyzed
      -n NUMBER, --numberOfNodes NUMBER
                            the number of nodes in the network
      -e ENDTIME, --end ENDTIME
                            trace ending time
      -s NUMBER, --step NUMBER
                            The step for logging component information


### Usage example
     python3 traceanalysis.py -n 62 -e 10000 --step 60 -f rollernet
