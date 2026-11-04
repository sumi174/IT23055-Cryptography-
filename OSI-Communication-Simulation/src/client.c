
#include <winsock2.h>
#include <ws2tcpip.h>
#include <stdio.h>
#include <stdint.h>
#include <string.h>
#include "layers.h"

#define SERVER_IP "127.0.0.1"
#define PORT 8080

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

int main(int argc, char *argv[]) {
    WSADATA wsa;

    if (WSAStartup(MAKEWORD(2, 2), &wsa) != 0)
        return 1;

    const char *message =
        (argc > 1) ? argv[1] : "Hello from OSI Client";

    char packet[MAX_PACKET];

    printf("====================================\n");
    printf("        OSI SIMULATION CLIENT\n");
    printf("====================================\n");

    printf("\n--- ENCAPSULATION ---\n");

    if (encapsulate(message, packet, sizeof(packet)) != 0) {
        printf("Encapsulation failed!\n");
        WSACleanup();
        return 1;
    }

    SOCKET client = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);

    if (client == INVALID_SOCKET) {
        printf("Socket creation failed!\n");
        WSACleanup();
        return 1;
    }

    struct sockaddr_in server;
    memset(&server, 0, sizeof(server));

    server.sin_family = AF_INET;
    server.sin_port = htons(PORT);
    server.sin_addr.s_addr = inet_addr(SERVER_IP);

    printf("\nConnecting to server...\n");

    if (connect(client, (struct sockaddr *)&server,
                sizeof(server)) == SOCKET_ERROR) {
        printf("Connection failed! Start server first.\n");
        closesocket(client);
        WSACleanup();
        return 1;
    }

    uint32_t length = (uint32_t)strlen(packet);
    uint32_t net_length = htonl(length);

    if (send_all(client, (char *)&net_length,
                 sizeof(net_length)) != 0 ||
        send_all(client, packet, (int)length) != 0) {

        printf("Sending failed!\n");
        closesocket(client);
        WSACleanup();
        return 1;
    }

    printf("Packet sent successfully: %u bytes\n", length);

    uint32_t ack_net;

    if (recv_all(client, (char *)&ack_net,
                 sizeof(ack_net)) == 0) {

        uint32_t ack_length = ntohl(ack_net);

        if (ack_length > 0 && ack_length < MAX_PACKET) {
            char ack[MAX_PACKET];

            if (recv_all(client, ack, (int)ack_length) == 0) {
                ack[ack_length] = '\0';
                printf("\nServer response: %s\n", ack);
            }
        }
    }

    closesocket(client);
    WSACleanup();

    printf("\nClient finished successfully!\n");

    return 0;
}
