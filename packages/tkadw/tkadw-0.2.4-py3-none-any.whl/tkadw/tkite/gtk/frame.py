from tkadw import AdwDrawFrame


class GTkFrame(AdwDrawFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def default_palette(self):
        self.palette_gtk_light()

    def palette_gtk_light(self):
        self.palette(
            {
                "frame": {
                    "back": "#f6f5f4",
                    "border": "#d5d0cc",
                    "border_width": 2,
                }
            }
        )

    def palette_gtk_dark(self):
        self.palette(
            {
                "frame": {
                    "back": "#353535",
                    "border": "#353535",
                    "border_width": 2,
                }
            }
        )


class GTkDarkFrame(GTkFrame):
    def default_palette(self):
        self.palette_gtk_dark()


if __name__ == '__main__':
    from tkinter import Tk
    root = Tk()
    frame = GTkFrame()
    frame.pack(fill="both", expand="yes", padx=2, pady=2)
    frame2 = GTkDarkFrame()
    frame2.pack(fill="both", expand="yes", padx=2, pady=2)
    root.mainloop()