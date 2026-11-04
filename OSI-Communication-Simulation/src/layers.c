
#include "layers.h"
#include <stdio.h>
#include <string.h>

static int add_header(const char *header, const char *data,
                      char *out, size_t size) {
    int n = snprintf(out, size, "%s|%s", header, data);
    return (n < 0 || (size_t)n >= size) ? -1 : 0;
}

static int remove_header(const char *header, const char *packet,
                         char *out, size_t size) {
    size_t len = strlen(header);

    if (strncmp(packet, header, len) != 0 ||
        packet[len] != '|') {
        printf("ERROR: Invalid %s header\n", header);
        return -1;
    }

    const char *data = packet + len + 1;

    if (strlen(data) + 1 > size)
        return -1;

    strcpy(out, data);
    return 0;
}

int encapsulate(const char *message, char *packet, size_t size) {
    char a[MAX_PACKET], b[MAX_PACKET];

    if (strlen(message) + 1 > sizeof(a))
        return -1;

    strcpy(a, message);

    printf("[Layer 7] Application: Original message\n");

    printf("[Layer 6] Presentation: Adding format header\n");
    if (add_header("PRESENTATION", a, b, sizeof(b))) return -1;
    strcpy(a, b);

    printf("[Layer 5] Session: Adding session ID\n");
    if (add_header("SESSION-01", a, b, sizeof(b))) return -1;
    strcpy(a, b);

    printf("[Layer 4] Transport: TCP transport header simulation\n");
    if (add_header("TRANSPORT-TCP", a, b, sizeof(b))) return -1;
    strcpy(a, b);

    printf("[Layer 3] Network: Adding IP information\n");
    if (add_header("NETWORK-LOCAL", a, b, sizeof(b))) return -1;
    strcpy(a, b);

    printf("[Layer 2] Data Link: Adding frame information\n");
    if (add_header("DATALINK-LOCAL", a, b, sizeof(b))) return -1;
    strcpy(a, b);

    printf("[Layer 1] Physical: Byte stream transmission\n");
    if (add_header("PHYSICAL-BITS", a, b, sizeof(b))) return -1;

    if (strlen(b) + 1 > size)
        return -1;

    strcpy(packet, b);

    printf("\n[SENDER] Encapsulation completed!\n");
    return 0;
}

int decapsulate(const char *packet, char *message, size_t size) {
    char a[MAX_PACKET], b[MAX_PACKET];

    if (strlen(packet) + 1 > sizeof(a))
        return -1;

    strcpy(a, packet);

    printf("[Layer 1] Physical: Receiving byte stream\n");
    if (remove_header("PHYSICAL-BITS", a, b, sizeof(b))) return -1;
    strcpy(a, b);

    printf("[Layer 2] Data Link: Removing frame header\n");
    if (remove_header("DATALINK-LOCAL", a, b, sizeof(b))) return -1;
    strcpy(a, b);

    printf("[Layer 3] Network: Removing IP information\n");
    if (remove_header("NETWORK-LOCAL", a, b, sizeof(b))) return -1;
    strcpy(a, b);

    printf("[Layer 4] Transport: Processing TCP payload\n");
    if (remove_header("TRANSPORT-TCP", a, b, sizeof(b))) return -1;
    strcpy(a, b);

    printf("[Layer 5] Session: Removing session information\n");
    if (remove_header("SESSION-01", a, b, sizeof(b))) return -1;
    strcpy(a, b);

    printf("[Layer 6] Presentation: Restoring data format\n");
    if (remove_header("PRESENTATION", a, b, sizeof(b))) return -1;

    if (strlen(b) + 1 > size)
        return -1;

    strcpy(message, b);

    printf("[Layer 7] Application: Original message received!\n");
    printf("\nOriginal Message: %s\n", message);

    return 0;
}
