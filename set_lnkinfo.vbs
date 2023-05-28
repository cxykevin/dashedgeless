Dim objShell, objFolder, strWinDir, objFolderItem, objShellLink
Set objShell = CreateObject("Shell.Application")  ''创建对象
Set objFolder = objShell.NameSpace(WScript.Arguments.Item(0))
Set objFolderItem = objFolder.ParseName(WScript.Arguments.Item(1))
Set objShellLink = objFolderItem.GetLink
objShellLink.SetIconLocation strWinDir & WScript.Arguments.Item(2), 0
objShellLink.Save