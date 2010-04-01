
// Create a Messagebox in C

/*works on Visual C++ and LCC win32*/
#include <windows.h> 
int WINAPI WinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance, LPSTR lpCmdLine, int nCmdShow) {
MessageBox (NULL, "Hello World" , "Hello", 0);
return 0;
}
