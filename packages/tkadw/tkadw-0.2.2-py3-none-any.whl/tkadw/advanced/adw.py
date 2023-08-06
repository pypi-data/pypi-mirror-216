from tkinter import Tk


class Adw(Tk):
    def __init__(self, *args, title: str = "adw", icon="light", windark: bool = True, wincaption=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.title(title)
        from tkadw.advanced.icon import adwite_light_photo, adwite_dark_photo
        if icon.lower() == "dark":
            icon = adwite_dark_photo()
        elif icon.lower() == "light":
            icon = adwite_light_photo()
        self.iconphoto(False, icon)

        from sys import platform
        if platform == "win32" and windark:
            try:
                from ctypes import windll, wintypes, byref, c_int, sizeof
                value = c_int(1)
                windll.dwmapi.DwmSetWindowAttribute(
                    windll.user32.GetParent(self.winfo_id()),  # 窗柄 输入值
                    20,  # 类型 DWMWA_USE_IMMERSIVE_DARK_MODE = 20
                    byref(value),  # 数值 启用
                    sizeof(value)  # 大小 数值大小
                )
            except:
                pass
        if platform == "win32" and wincaption is not None:
            from sys import platform
            from ctypes import windll, byref, sizeof, c_int
            from ctypes.wintypes import RGB
            windll.dwmapi.DwmSetWindowAttribute(windll.user32.GetParent(self.winfo_id()), 35, byref(c_int(RGB(wincaption[0], wincaption[1], wincaption[2]))),
                                                sizeof(c_int))


if __name__ == '__main__':
    root = Adw(icon="light")
    root.mainloop()
