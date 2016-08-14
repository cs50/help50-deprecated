#include <stdio.h>

char *GetString();
int main(void)
{
    char *s = GetString();
    printf("hello, %s\n", s);
}
