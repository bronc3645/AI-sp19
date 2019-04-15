# Makefile

CC = c++
OBJECTS = Action.o Agent.o Location.o Orientation.o Percept.o WumpusWorld.o Search.o

PYTHON-DEF = -DPYTHON
PYTHON-OBJ = Action.o PyAgent.o Location.o Orientation.o Percept.o WumpusWorld.o

PYTHON_CONFIG = python-config
PYTHON-INC = $(shell $(PYTHON_CONFIG) --includes)
PYTHON-LIB = $(shell $(PYTHON_CONFIG) --ldflags)

# Settings for MacOS
# PYTHON-INC = -I/System/Library/Frameworks/Python.framework/Versions/2.7/include/python2.7
# PYTHON-LIB = -L/System/Library/Frameworks/Python.framework/Versions/2.7/lib -lpython2.7

# Settings for CentOS Linux
#PYTHON-INC = -I/usr/include/python2.7
#PYTHON-LIB = -L/usr/lib64 -lpython2.7

all: wumpsim

pywumpsim: wumpsim.h wumpsim.cc $(PYTHON-OBJ)
	$(CC) -o pywumpsim wumpsim.cc $(PYTHON-DEF) $(PYTHON-INC) $(PYTHON-OBJ) $(PYTHON-LIB)

wumpsim: wumpsim.h wumpsim.cc $(OBJECTS)
	$(CC) -o wumpsim wumpsim.cc $(OBJECTS)

Action.o: Action.h Action.cc
	$(CC) -c Action.cc

Agent.o: Agent.h Agent.cc
	$(CC) -c Agent.cc

PyAgent.o: PyAgent.h PyAgent.cc
	$(CC) -c PyAgent.cc $(PYTHON-INC)

Location.o: Location.h Location.cc
	$(CC) -c Location.cc

Orientation.o: Orientation.h Orientation.cc
	$(CC) -c Orientation.cc

Percept.o: Percept.h Percept.cc
	$(CC) -c Percept.cc

WumpusWorld.o: WumpusWorld.h WumpusWorld.cc
	$(CC) -c WumpusWorld.cc

Search.o: Search.h Search.cc
	$(CC) -c Search.cc

clean:
	rm -rf *.o *.pyc __pycache__ wumpsim pywumpsim
