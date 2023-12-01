#include <stdio.h>
#include <string.h>

#define BUF_SIZE 1024

int main() {
	const char* d_str[] = {
		"zero",
		"one",
		"two",
		"three",
		"four",
		"five",
		"six",
		"seven",
		"eight",
		"nine",
	};

	int sum = 0;
	char c, d1 = 0, d2;
	char buf[BUF_SIZE];
	buf[BUF_SIZE] = 0;
	int counter = 0;
	while (scanf("%c", &c) != EOF) {
		if (c == '\n') {
			int num = (int) (d1 - '0') * 10 + (int) (d2 - '0');
			printf("%d\n", num);
			sum += num;
			d1 = 0;
			counter = 0;
		} else if (c <= '0' || c >= '9') {
			buf[counter++ % BUF_SIZE] = c;
			for (int i = 0; i < sizeof(d_str) / sizeof(char *); ++i) {
				int match = 1;
				for (int j = 0; j < strlen(d_str[i]); ++j) {
					if (buf[(counter % BUF_SIZE) - strlen(d_str[i]) + j] != d_str[i][j]) {
						match = 0;
						break;
					}
				}
				if (match == 1) {
					c = (char) i + '0';
					break;
				}

			}
		}
		if (c >= '0' && c <= '9') {
			d2 = c;
			if (d1 == 0) d1 = c;
		}
	}
	printf("%d\n", sum);

	return 0;
}
