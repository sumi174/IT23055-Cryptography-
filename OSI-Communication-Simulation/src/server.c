
#include <winsock2.h>
#include <ws2tcpip.h>
#include <stdio.h>
#include <stdint.h>
#include <string.h>
#include "layers.h"

#define PORT 8080

int recv_all(SOCKET s, char *buffer, int length) {
    int total = 0;

    while (total < length) {
        int n = recv(s, buffer + total, length - total, 0);

        if (n <= 0)
            return -1;

        total += n;
    }

    return 0;
}

int send_all(SOCKET s, const char *buffer, int length) {
    int total = 0;

    while (total < length) {
        int n = send(s, buffer + total, length - total, 0);

        if (n <= 0)
            return -1;

        total += n;
    }

    return 0;
}

int main(void) {
    WSADATA wsa;

    if (WSAStartup(MAKEWORD(2, 2), &wsa) != 0) {
        printf("Winsock initialization failed!\n");
        return 1;
    }

    SOCKET server = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);

    if (server == INVALID_SOCKET) {
        printf("Socket creation failed!\n");
        WSACleanup();
        return 1;
    }

    struct sockaddr_in address;
    memset(&address, 0, sizeof(address));

    address.sin_family = AF_INET;
    address.sin_addr.s_addr = htonl(INADDR_ANY);
    address.sin_port = htons(PORT);

    if (bind(server, (struct sockaddr *)&address,
             sizeof(address)) == SOCKET_ERROR) {
        printf("Bind failed: %d\n", WSAGetLastError());
        closesocket(server);
        WSACleanup();
        return 1;
    }

    if (listen(server, 5) == SOCKET_ERROR) {
        printf("Listen failed!\n");
        closesocket(server);
        WSACleanup();
        return 1;
    }

    printf("====================================\n");
    printf("       OSI SIMULATION SERVER\n");
    printf("====================================\n");
    printf("Server listening on port %d...\n", PORT);

    while (1) {
        SOCKET client = accept(server, NULL, NULL);

        if (client == INVALID_SOCKET)
            continue;

        printf("\nClient connected!\n");

        uint32_t net_length;

        if (recv_all(client, (char *)&net_length,
                     sizeof(net_length)) == 0) {

            uint32_t length = ntohl(net_length);

            if (length > 0 && length < MAX_PACKET) {
                char packet[MAX_PACKET];
                char message[MAX_PACKET];

                if (recv_all(client, packet, (int)length) == 0) {
                    packet[length] = '\0';

                    printf("\n--- DECAPSULATION ---\n");

                    if (decapsulate(packet, message,
                                    sizeof(message)) == 0) {

                        const char *ack =
                            "ACK: Message received successfully";

                        uint32_t ack_length =
                            (uint32_t)strlen(ack);

                        uint32_t ack_net = htonl(ack_length);

                        send_all(client, (char *)&ack_net,
                                 sizeof(ack_net));

                        send_all(client, ack,
                                 (int)ack_length);
                    }
                }
            } else {
                printf("Invalid packet length!\n");
            }
        }

        closesocket(client);
        printf("\nClient disconnected.\n");
    }

    closesocket(server);
    WSACleanup();

    return 0;
}
