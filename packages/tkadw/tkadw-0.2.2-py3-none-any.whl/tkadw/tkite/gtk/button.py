from tkadw import AdwDrawRoundButton3


class GTkButton(AdwDrawRoundButton3):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def default_palette(self):
        self.palette_gtk_light()

    def palette_gtk_light(self):
        self.palette(
            {
                "button": {
                    "radius": 11,
                    "back": "#f6f5f4",
                    "border": "#ccc6c1",
                    "text_back": "#2e3436",
                    "border_width": 1.3,

                    "active": {
                        "back": "#f8f8f7",
                        "border": "#dad6d2",
                        "text_back": "#2e3436",
                        "border_width": 1.3,
                    },

                    "pressed": {
                        "back": "#dad6d2",
                        "border": "#dad6d2",
                        "text_back": "#2e3436",
                        "border_width": 1.3,
                    },
                }
            }
        )

    def palette_gtk_dark(self):
        self.palette(
            {
                "button": {
                    "radius": 11,
                    "back": "#353535",
                    "border": "#1b1b1b",
                    "text_back": "#eeeeec",
                    "border_width": 1.3,

                    "active": {
                        "back": "#373737",
                        "border": "#1b1b1b",
                        "text_back": "#eeeeec",
                        "border_width": 1.3,
                    },

                    "pressed": {
                        "back": "#1e1e1e",
                        "border": "#282828",
                        "text_back": "#eeeeec",
                        "border_width": 1.3,
                    },
                }
            }
        )

    def palette_gtk_red(self):
        self.palette(
            {
                "button": {
                    "radius": 11,
                    "back": "#d81a23",
                    "border": "#851015",
                    "text_back": "#ffffff",
                    "border_width": 1.3,

                    "active": {
                        "back": "#bc171e",
                        "border": "#9c1319",
                        "text_back": "#ffffff",
                        "border_width": 1.3,
                    },

                    "pressed": {
                        "back": "#a0131a",
                        "border": "#9c1319",
                        "text_back": "#ffffff",
                        "border_width": 1.3,
                    },
                }
            }
        )

    def palette_gtk_blue(self):
        self.palette(
            {
                "button": {
                    "radius": 11,
                    "back": "#2d7fe3",
                    "border": "#15539e",
                    "text_back": "#ffffff",
                    "border_width": 1.3,

                    "active": {
                        "back": "#1a65c2",
                        "border": "#185fb4",
                        "text_back": "#ffffff",
                        "border_width": 1.3,
                    },

                    "pressed": {
                        "back": "#1961b9",
                        "border": "#185fb4",
                        "text_back": "#ffffff",
                        "border_width": 1.3,
                    },
                }
            }
        )


class GTkDarkButton(GTkButton):
    def default_palette(self):
        self.palette_gtk_dark()


class GTkDestructiveButton(GTkButton):
    def default_palette(self):
        self.palette_gtk_red()


class GTkSuggestedButton(GTkButton):
    def default_palette(self):
        self.palette_gtk_blue()


if __name__ == '__main__':
    from tkinter import Tk
    from tkadw import GTkFrame, GTkDarkFrame

    root = Tk()

    frame = GTkFrame(root)

    button1 = GTkButton(frame.frame, text="GTkButton")
    button1.pack(fill="x", ipadx=5, padx=5, pady=5)

    button3 = GTkSuggestedButton(frame.frame, text="GTkSuggestedButton")
    button3.pack(fill="x", ipadx=5, padx=5, pady=5)

    frame.pack(fill="both", expand="yes", side="right")

    frame2 = GTkDarkFrame(root)

    button2 = GTkDarkButton(frame2.frame, text="GTkDarkButton")
    button2.pack(fill="x", ipadx=5, padx=5, pady=5)

    button4 = GTkDestructiveButton(frame2.frame, text="GTkDestructiveButton")
    button4.pack(fill="x", ipadx=5, padx=5, pady=5)

    frame2.pack(fill="both", expand="yes", side="left")

    root.mainloop()