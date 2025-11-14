FROM ubuntu:22.04

RUN apt-get update && apt-get install -y gcc

COPY tcp_client.c /tcp_client.c

RUN gcc -o tcp_client tcp_client.c

CMD ["./tcp_client"]
