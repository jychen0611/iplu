#include "neurotrie.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>


int main()
{
    FILE *file = fopen("dataset/routes-293", "r");
    if (!file) {
        perror("Error opening file");
        return EXIT_FAILURE;
    }
    char *line;
    while (fgets(line, sizeof(line), file)) {
        /* Split ip and next hop */
        __uint128_t ip;
        uint32_t next_hop;
       
        printf("%s\n", line);
    }
    return 0;
}