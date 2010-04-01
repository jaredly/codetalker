
// Delete recent documents in C

#include <windows.h>
#include <shlobj.h>
#define WIN32_LEAN_AND_MEAN

int WINAPI WinMain (HINSTANCE hInstance, HINSTANCE hPrevInstance,
PSTR szCmdLine, int iCmdShow)
{

if(MessageBox(NULL, "Press ok to empty the Recent documents folder.", "recycler", MB_YESNO | MB_ICONINFORMATION) != IDYES)
return FALSE;

SHAddToRecentDocs(SHARD_PATH, NULL);


return FALSE ;
}
