#include <stdio.h>
#include <cs50.h>
int main(void)
{
    
    string name  = get_string("Hello, what is your name? ");
    
    printf("Hello, %s\n", name);
}