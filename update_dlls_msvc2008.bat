del *.dll
del .\..\..\*.dll
del .\..\editor\*.dll
del .\..\pychan_demo\*.dll
del .\..\rio_de_hola\*.dll

copy .\..\..\build\win32\binaries\msvc2008\*.dll *.*
copy .\..\..\build\win32\binaries\msvc2008\*.dll .\..\..\*.*
copy .\..\..\build\win32\binaries\msvc2008\*.dll .\..\editor\*.*
copy .\..\..\build\win32\binaries\msvc2008\*.dll .\..\pychan_demo\*.*
copy .\..\..\build\win32\binaries\msvc2008\*.dll .\..\rio_de_hola\*.*
