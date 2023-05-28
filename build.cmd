@echo off
:getvtag
set /P ver= <"version.txt"
if "%ver%"=="" (
    goto getvtag
)
if "%1"=="build" (
    echo [BUILD]building... 1/2
    pyinstaller -F -p "." -i dashedgeless.ico -n on_start on_start.py
    copy /Y dist\on_start.exe .\
    echo [BUILD]building... 2/2
    pyinstaller -F -p "." -i dashedgeless.ico -n on_load on_load.py
    copy /Y dist\on_load.exe .\
    rmdir /S /Q build
    rmdir /S /Q dist
    del /Q *.spec
)
if "%1"=="7z" (
    echo [BUILD]packing... 1/3
    mkdir "../tmp/dashedgeless"
    xcopy /I "*" "../tmp/dashedgeless/"
    copy "dashedgeless.cmd" "../tmp"
    echo "../dashedgeless_%ver%_dashedgeless (bot).7z">"../tmp/dashedgeless/whitelist.txt"
    del /Q "../tmp/dashedgeless/*.log"
    del /Q "../tmp/dashedgeless/.tip*.log"
    echo [BUILD]packing... 2/3
    del /Q "../dashedgeless_*_dashedgeless (bot).7z"
    7z a "../dashedgeless_%ver%_dashedgeless (bot).7z" "../tmp/*"
    echo [BUILD]packing... 3/3
    rmdir /S /Q "../tmp"
)
if "%1"=="v" (
    echo --- Build tools [dashedgeless] ---
    echo version: %ver%
)
if "%1"=="" (
    echo --- Build tools [dashedgeless] ---
    echo version: %ver%
    build build
    build 7z
)
if "%1"=="mv" (
    move "../dashedgeless_%ver%_dashedgeless (bot).7z" "dashedgeless_%ver%_dashedgeless (bot).7z"
)