// demonstrates expected ';' in 'for' statement

#include <stdio.h>

int main(void)
{
    for (int i = 0, i < 5, i++)
    {
        printf("%i\n", i);
    }
}
