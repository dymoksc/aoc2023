#include <stdio.h>

int main() {
	int sum = 0;
	char c, d1 = 0, d2;
	while (scanf("%c", &c) != EOF) {
		if (c == '\n') {
			int num = (int) (d1 - '0') * 10 + (int) (d2 - '0');
			sum += num;
			d1 = 0;
		}
		if (c >= '0' && c <= '9') {
			d2 = c;
			if (d1 == 0) d1 = c;
		}
	}
	printf("%d\n", sum);

	return 0;
}
