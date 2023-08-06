import ctypes
import commctrl
import win32api
import win32gui

class EasyDesktop:
    def __init__(self):
        self.desktop = self._get_desktop_window()

    def go_to_xy(self, idx, x, y):
        lparam = (y << 16) | x
        print(lparam)
        win32gui.SendMessage(self.desktop, commctrl.LVM_SETITEMPOSITION, idx, lparam)

    def get_item_count(self):
        return win32gui.SendMessage(self.desktop, commctrl.LVM_GETITEMCOUNT, 0, 0)

    def get_screen_size(self):
        monitor_info = win32api.GetMonitorInfo(win32api.EnumDisplayMonitors(None, None)[0][0])
        monitor_rect = monitor_info["Work"]
        width = monitor_rect[2] - monitor_rect[0]
        height = monitor_rect[3] - monitor_rect[1]
        return width, height

    def _get_desktop_window(self):
        shell_window = ctypes.windll.user32.GetShellWindow()
        shell_dll_defview = win32gui.FindWindowEx(shell_window, 0, "SHELLDLL_DefView", "")

        if shell_dll_defview == 0:
            # If the shell_dll_defview is not found, search for the SysListView32 window directly
            sys_listview_container = []
            win32gui.EnumWindows(self._enum_windows_callback, sys_listview_container)
            sys_listview = sys_listview_container[0]
        else:
            sys_listview = win32gui.FindWindowEx(shell_dll_defview, 0, "SysListView32", "FolderView")

        return sys_listview

    def _enum_windows_callback(hwnd, extra):
        class_name = win32gui.GetClassName(hwnd)
        if class_name == "WorkerW":
            child = win32gui.FindWindowEx(hwnd, 0, "SHELLDLL_DefView", "")
            if child != 0:
                sys_listview = win32gui.FindWindowEx(child, 0, "SysListView32", "FolderView")
                extra.append(sys_listview)
                return False
        return True
