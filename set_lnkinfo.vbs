Dim WshShell, strDesk, strWinDir, objLink
Set WshShell = CreateObject("WScript.Shell") ''创建对象
strDesk = WshShell.SpecialFolders(WScript.Arguments.Item(0)) ''桌面文件夹路径
Set objLink = WshShell.CreateShortcut(strDesk & "\" & WScript.Arguments.Item(1))
objLink.TargetPath = WScript.Arguments.Item(2)
objLink.WorkingDirectory = WScript.Arguments.Item(3)
objLink.WindowStyle = WScript.Arguments.Item(4)
objLink.Description = WScript.Arguments.Item(5)
objLink.IconLocation = WScript.Arguments.Item(6)
objLink.Save