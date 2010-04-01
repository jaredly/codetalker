
// Free disk space : Windows 95 and 98
#include <windows.h>
#include <stdio.h>
#include <stdlib.h> 
void main(void)
{
char szBuffer[MAX_PATH+100];
UINT nRow = 0;
UINT nDrive = 0;
DWORD dwLogicalDrives = GetLogicalDrives();

for ( nDrive = 0; nDrive<32; nDrive++ )
{
if ( dwLogicalDrives & (1 << nDrive) )
{
UINT uType; // type of drive.
DWORD dwBytesPerSector = 0; // bytes per sector
DWORD dwSectorsPerCluster=0; // sectors per cluster
DWORD dwTotalClusters = 0; // total clusters
DWORD dwFreeClusters = 0; // free clusters
DWORD dwVolumeSerialNumber=0;// volume serial number
DWORD dwMaxNameLength=0; // max component length
DWORD dwFileSystemFlags=0; // file system flags
DWORD dwFreeSpace = 0; // free space available
DWORD dwTotalSpace = 0; // total space available
char szFileSysName[129]; // the file system
char szLabel[129]; // the volume name
// Get disk information.
wsprintf( szBuffer, "%c:\\", nDrive+'A' );
uType = GetDriveType(szBuffer);
GetDiskFreeSpace(szBuffer, &dwBytesPerSector,
&dwSectorsPerCluster, &dwFreeClusters, &dwTotalClusters);
dwFreeSpace = dwBytesPerSector * dwSectorsPerCluster * dwFreeClusters;
dwTotalSpace = dwBytesPerSector * dwSectorsPerCluster * dwTotalClusters;
printf("%s\n", szBuffer);
wsprintf(szBuffer, " Type: %s, Disk Space: %ld, Free: %ld",
(uType == DRIVE_REMOVABLE) ? "FLOPPY" :
((uType == DRIVE_FIXED) ? "HARD DISK" :
((uType == DRIVE_REMOTE) ? "NETWORK" :
((uType == DRIVE_CDROM) ? "CDROM" :
((uType == DRIVE_RAMDISK) ? "RAMDISK" :
((uType == 1) ? "DOES NOT EXIST" :
"UNKNOWN DRIVE TYPE" ))))), dwTotalSpace, dwFreeSpace );
printf("%s\n", szBuffer);
}
}
}
