// demonstrates implicit declaration of function

#include <stdio.h>

int main(void)
{
    char *s = GetString();
    printf("hello, %s\n", s);
}
