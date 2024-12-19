#include <stdint.h>

struct pop_innode{
    uint8_t vector;
    uint8_t leafvec;
    /* Point to L array */
    struct pop_leaf *base0;
    /* Point to N array */
    struct pop_innode *base1;
    /* for N array */
    struct pop_innode *next;
};

struct pop_leaf{
    uint16_t next_hop;
    /* for L array */
    struct pop_leaf *next; 
};

/* Lookup the pop trie */
struct pop_leaf* pop_lookup(struct pop_innode *t, __uint128_t key);
/* Insert prefix to pop trie */
static void insert(struct pop_innode *t, __uint128_t prefix, uint16_t next_hop)