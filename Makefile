output: neurotrie.o main.c
	gcc -O0 neurotrie.o main.c  -Wall -std=c99 -o main

neurotrie.o: neurotrie.c neurotrie.h
	gcc -O0 -Wall -std=c99 -c neurotrie.c

clean:
	rm *.o main