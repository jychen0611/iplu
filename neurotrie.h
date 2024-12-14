
#include <stdint.h>

struct innode{
    /* 1 ~ 128 */
    uint8_t stride;
    struct bit_vec *bit_vec_ptr;
    struct innode *innode_ptr;
    struct leaf *leaf_ptr;
    /* for child node headr array */
    struct innode *next;
};

struct bit_vec{
    uint32_t innode_vec;
    uint8_t innode_ctr;
    uint32_t leaf_vec;
    uint8_t leaf_ctr;
    /* for bit vector array */
    struct bit_vec *next;
};

struct leaf{
    uint32_t next_hop;
    /* for next hop array */
    struct leaf *next;
};

static struct leaf* lookup();
static void insert();