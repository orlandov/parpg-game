del *.dll
del .\..\..\*.dll
del .\..\editor\*.dll
del .\..\pychan_demo\*.dll
del .\..\rio_de_hola\*.dll

copy .\..\..\build\win32\binaries\mingw\*.dll *.*
copy .\..\..\build\win32\binaries\mingw\*.dll .\..\..\*.*
copy .\..\..\build\win32\binaries\mingw\*.dll .\..\editor\*.*
copy .\..\..\build\win32\binaries\mingw\*.dll .\..\pychan_demo\*.*
copy .\..\..\build\win32\binaries\mingw\*.dll .\..\rio_de_hola\*.*
