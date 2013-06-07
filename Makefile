# Makefile
# Autor: Olivier BLIN
# Date: sam. 07/06/2013
#
# Actions :
#	make all 		: compilation (default)
#	make clean 		: remove .o
#	make mrproper 	: remove .o and EXE


CC=g++
EXEC=lcap
SRC=src/
INC=include/

# Linker Flag
LDFLAGS=-lpcap -lpthread -lwebsockets
# Compilation Flag
CFLAGS=-ggdb -I$(INC) -Wall

#ALL
all: $(EXEC)

##################################################

# MAIN
main.o: main.cpp
	@echo $^
	@$(CC) -c $^ $(CFLAGS)

# Network sniffer
Pcap.o: $(SRC)Pcap.cpp
	@echo $^
	@$(CC) -c $^ $(CFLAGS)

# Websocket manager
Websocket.o: $(SRC)Websocket.cpp
	@echo $^
	@$(CC) -c $^ $(CFLAGS)

# Websocket manager
Json.o: $(SRC)Json.cpp
	@echo $^
	@$(CC) -c $^ $(CFLAGS)


##################################################

# Link edition and EXE creation
$(EXEC): main.o Pcap.o Websocket.o Json.o
	@echo "Link output files..."
	@$(CC) -o $@  $^ $(LDFLAGS)
	@echo "OK"
	@echo "Program name is $(EXEC)"

##################################################

clean:
	rm -f *.o

##################################################

mrproper: clean
	rm -f $(EXEC)

# End Makefile