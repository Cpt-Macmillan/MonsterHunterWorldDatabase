del /f MHWDB-x64.exe & 
pyinstaller -w -F -i images\Nergigante.ico src\Application.py & 
move dist\Application.exe ..\MonsterHunterWorld & 
ren Application.exe MHWDB-x64.exe &

del /f MHWDB-x86.exe & 
%PYTHON32%\scripts\pyinstaller.exe -w -F -i images\Nergigante.ico src\Application.py & 
move dist\Application.exe ..\MonsterHunterWorld & 
ren Application.exe MHWDB-x86.exe