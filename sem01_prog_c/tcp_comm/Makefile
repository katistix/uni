CC = gcc
CFLAGS = -Wall -Wextra -std=c99

CLIENT = tcp_client
CLIENT_SRC = tcp_client.c

.PHONY: all clean run

all: $(CLIENT)

$(CLIENT): $(CLIENT_SRC)
	$(CC) $(CFLAGS) -o $(CLIENT) $(CLIENT_SRC)

run: $(CLIENT)
	./$(CLIENT)

clean:
	rm -f $(CLIENT)