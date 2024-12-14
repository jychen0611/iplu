output: neurotrie.o main.c
	gcc -O0 neurotrie.o main.c  -Wall -std=c99 -o main

neurotrie.o: trie/neurotrie.c trie/neurotrie.h
	gcc -O0 -Wall -std=c99 -c trie/neurotrie.c

clean:
	rm *.o main