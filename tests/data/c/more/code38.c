
// Connect to a site example
#include<windows.h>
#include<wininet.h>
#include<stdio.h> 
int main()
{

HINTERNET Initialize,Connection,File;
DWORD dwBytes;
char ch;
Connection = InternetConnect(Initialize,"www.xxx.com",INTERNET_DEFAULT_HTTP_PORT,
NULL,NULL,INTERNET_SERVICE_HTTP,0,0);

File = HttpOpenRequest(Connection,NULL,"/index.html",NULL,NULL,NULL,0,0);

if(HttpSendRequest(File,NULL,0,NULL,0))
{
while(InternetReadFile(File,&ch,1,&dwBytes))
{
if(dwBytes != 1)break;
putchar(ch);
}
}
InternetCloseHandle(File);
InternetCloseHandle(Connection);
InternetCloseHandle(Initialize);
return 0;
}
