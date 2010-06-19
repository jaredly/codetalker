
// Empty recycle bin

#include <windows.h>
#include <shlobj.h>
#define WIN32_LEAN_AND_MEAN

int WINAPI WinMain (HINSTANCE hInstance, HINSTANCE hPrevInstance,
PSTR szCmdLine, int iCmdShow)
{

if(MessageBox(NULL, "Press ok to empty the Recycle Bin.", "recycler", MB_YESNO | MB_ICONINFORMATION) != IDYES)
return FALSE;


SHEmptyRecycleBin(NULL, "", 0);

return FALSE ;
}
