all:
	g++ -o lcap main.cpp src/pcap.cpp src/Websocket.cpp -lpcap -lpthread -lwebsockets #-W -Wall

clean:
	rm lcap