//string1.c
// setting value to string
#include <stdio.h>
#include <string.h>

int main ()
{
  char sMyName [20];
  strcpy (sMyName,"Toad B. dePond");
  printf ("%s \n", sMyName);
  return 0;
}

/*
Functions to manipulate strings
The cstring library (string.h) defines many functions to perform some manipulation operations with C-like strings (like already explained strcpy). Here you have a brief with the most usual: 
strcat:   char* strcat (char* dest, const char* src); 
Appends src string at the end of dest string. Returns dest. 

strcmp:   int strcmp (const char* string1, const char* string2); 
Compares strings string1 and string2. Returns 0 is both strings are equal. 

strcpy:   char* strcpy (char* dest, const char* src); 
Copies the content of src to dest. Returns dest. 

strlen:   size_t strlen (const char* string); 
Returns the length of string. 
NOTE: char* is the same as char[] 

*/