#include "trie/neurotrie.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void read_line(char *line, __uint128_t *ip, uint8_t *len, uint32_t *next_hop){
    /* Split prefix and mask */
    char tok1[]="/";
    char pre[100];
    sprintf(pre,"%s\0",strtok(line,tok1));
    /* Handle ip prefix */
	char tok2[]=":";
	char hex[100];
	sprintf(hex,"%s\0",strtok(pre,tok2));
    uint32_t shift = 128;
    
    while(1){
        shift -= 16;
        __uint128_t decimal = strtoull(hex, NULL, 16); 
        *ip += (decimal << shift);

        char *token = strtok(NULL,tok2);
        if(!token)
            break;
        sprintf(hex,"%s\0",token);
    }
	/* Caculate nexthop */
	*next_hop = *ip % 1000;
    /* Fix me: handle mask */
}

int main()
{
    FILE *file = fopen("dataset/routes-293", "r");
    if (!file) {
        perror("Error opening file");
        return EXIT_FAILURE;
    }
    char *line = malloc(100*sizeof(char));
    int k=10;
    while (fgets(line, 100*sizeof(char), file) && k--) {
        /* Split ip and next hop */
        __uint128_t ip = 0;
        uint32_t next_hop = 0;
        uint8_t len;
        read_line(line, &ip, &len, &next_hop);
        /* Print uint128 in hex */
        printf ("IP prefix: 0x%lx%lx\r\n", (uint64_t) (ip >> 64), (uint64_t) ip);
        printf("Next-hop: %d\n", next_hop);
    }
    free(line);
    fclose(file);
    return 0;
}