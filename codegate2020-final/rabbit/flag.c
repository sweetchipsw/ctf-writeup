#pragma warning(disable:4996)
#include<stdio.h>
#include<math.h>       //sqrt()
#define NUM 1048576

int main(void)
{

	static int prime[NUM + 1] = { 0, };
	static int primefinal[NUM + 1] = { 0, };
	static char finaldata[NUM * 4 + 1] = {0,};

	int i, j, Limit;



	for (i = 2; i <= NUM; i++)
		prime[i] = 1;

	Limit = (int)sqrt(NUM);
	for (i = 2; i <= Limit; i++) {
		if (prime[i] == 1) {
			for (j = 2 * i; j <= NUM; j++) {
				if (j % i == 0)
					prime[j] = 0;
			}
		}
	}

	int idxz = 0;
	for (i = 2; i <= NUM; i++)
		if (prime[i] == 1)
			primefinal[idxz++] = i;
	printf("\n");

	//printf("%d", primefinal[0]);

	int idx2 = 0;
	int idx = 0;
	int wtf = 82025; 

	printf("Start calculating.. \n");


	do {
		idx2 = idx;
		do {
			int mapidx = primefinal[idx2] + primefinal[idx];
			if (mapidx > 0x100000 * 4) {
				printf("assert..%x %x %x %x %x", mapidx, primefinal[idx2], primefinal[idx], idx2, idx);
				return 0;
			}
			//printf("%d\n", mapidx);
			finaldata[mapidx]++;
			1 + 1;
			idx += 1;
			1 + 1;
		} while (idx != wtf);
		idx = idx2 + 1;
	} while (idx2 + 1 != wtf);

	
	int asd[] = { 1500, 2160, 2178, 2412, 2454, 3880, 4930, 5138, 12360, 15378, 15972, 16734, 17808, 18126, 19524, 19728, 21700, 22026, 23660, 27480, 27550, 27692, 28830, 29830, 30640, 31066, 31720, 32960, 33286, 34480, 35392, 35714, 35994, 36160, 36312, 37380, 37622, 38214, 39324, 39414, 40504, 40528, 40894, 40914, 41044, 41322, 41626, 41804, 41854, 41860, 42018, 42238, 42342, 42586, 42724, 43148, 43168, 43214, 43442, 0 };
	int arrSize = sizeof(asd) / sizeof(asd[0]);
	for (int z = 0; z < arrSize; z++) {
		printf("%c", finaldata[asd[z]]);
	}

	return 0;

}