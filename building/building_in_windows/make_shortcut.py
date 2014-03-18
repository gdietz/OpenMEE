import os, sys
import pythoncom
from win32com.shell import shell, shellcon

shortcut = pythoncom.CoCreateInstance (
  shell.CLSID_ShellLink,
  None,
  pythoncom.CLSCTX_INPROC_SERVER,
  shell.IID_IShellLink
)
shortcut.SetPath (sys.executable)
shortcut.SetDescription ("Python %s" % sys.version)
shortcut.SetIconLocation (sys.executable, 0)

desktop_path = shell.SHGetFolderPath (0, shellcon.CSIDL_DESKTOP, 0, 0)
persist_file = shortcut.QueryInterface (pythoncom.IID_IPersistFile)
persist_file.Save (os.path.join (desktop_path, "python.lnk"), 0)