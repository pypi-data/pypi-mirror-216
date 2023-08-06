from tkadw import AdwDrawText


class GTkTextBox(AdwDrawText):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def default_palette(self):
        self.palette_gtk_light()

    def palette_gtk_light(self):
        self.palette(
            {
                "text": {
                    "padding": (5, 5),

                    "back": "#ffffff",
                    "border": "#cdc7c2",
                    "text_back": "#000000",
                    "border_width": 1,

                    "bottom_line": "#eaeaea",
                    "bottom_width": 0,

                    "focusin": {
                        "back": "#ffffff",
                        "border": "#3584e4",
                        "text_back": "#000000",
                        "border_width": 1,

                        "bottom_line": "#185fb4",
                        "bottom_width": 0,
                    }
                },
            }
        )

    def palette_gtk_dark(self):
        self.palette(
            {
                "text": {
                    "padding": (5, 5),

                    "back": "#2d2d2d",
                    "border": "#1f1f1f",
                    "text_back": "#cccccc",
                    "border_width": 1,

                    "bottom_line": "#eaeaea",
                    "bottom_width": 0,

                    "focusin": {
                        "back": "#2d2d2d",
                        "border": "#3584e4",
                        "text_back": "#ffffff",
                        "border_width": 1,

                        "bottom_line": "#3584e4",
                        "bottom_width": 0,
                    }
                },
            }
        )


class GTkDarkTextBox(GTkTextBox):
    def default_palette(self):
        self.palette_gtk_dark()


if __name__ == '__main__':
    from tkinter import Tk
    from tkadw import GTkFrame, GTkDarkFrame

    root = Tk()
    root.configure(background="#1f1f1f")

    frame = GTkFrame(root)

    textbox1 = GTkTextBox(frame.frame)
    textbox1.pack(fill="x", ipadx=5, padx=5, pady=5)

    frame.pack(fill="both", expand="yes", side="right")

    frame2 = GTkDarkFrame(root)

    textbox2 = GTkDarkTextBox(frame2.frame)
    textbox2.pack(fill="x", ipadx=5, padx=5, pady=5)

    frame2.pack(fill="both", expand="yes", side="left")

    root.mainloop()
