Dim objShell, objFolder, objFolderItem, objShellLink, s, k
Set objShell = CreateObject("Shell.Application")
Set objFolder = objShell.NameSpace(WScript.Arguments.Item(0))
Set objFolderItem = objFolder.ParseName(WScript.Arguments.Item(1))
Set objShellLink = objFolderItem.GetLink
s = objShellLink.Path & vbLf
s = s & objShellLink.WorkingDirectory & vbLf
s = s & objShellLink.Hotkey & vbLf
s = s & objShellLink.ShowCommand & vbLf
s = s & objShellLink.Description
WScript.Echo s