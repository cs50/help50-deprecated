// demonstrates control reaches end of non-void function

#include <stdio.h>

int foo()
{
    int x = 28;
}

int main(void)
{
    foo();
}
