
#ifndef LAYERS_H
#define LAYERS_H

#include <stddef.h>

#define MAX_PACKET 8192

int encapsulate(const char *message, char *packet, size_t size);
int decapsulate(const char *packet, char *message, size_t size);

#endif
