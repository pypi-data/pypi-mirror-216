from tkadw import AdwDrawRoundButton3, AdwDrawRoundFrame3, AdwDrawRoundEntry3, AdwDrawRoundText3


class BiliBiliButton(AdwDrawRoundButton3):
    def palette_bilibili_light(self):
        self.palette(
            {
                "button": {
                    "radius": 16,
                    "back": "#ffffff",
                    "border": "#e3e5e7",
                    "text_back": "#18191c",
                    "border_width": 1,

                    "active": {
                        "back": "#e3e5e7",
                        "border": "#e3e5e7",
                        "text_back": "#18191c",
                        "border_width": 1,
                    },

                    "pressed": {
                        "back": "#eceff0",
                        "border": "#e3e5e7",
                        "text_back": "#6d7479",
                        "border_width": 1,
                    },
                }
            }
        )

    def palette_bilibili_dark(self):
        self.palette(
            {
                "button": {
                    "radius": 16,
                    "back": "#242628",
                    "border": "#2f3134",
                    "text_back": "#dcdee0",
                    "border_width": 1,

                    "active": {
                        "back": "#2f3134",
                        "border": "#2f3134",
                        "text_back": "#dcdee0",
                        "border_width": 1,
                    },

                    "pressed": {
                        "back": "#26282a",
                        "border": "#2f3134",
                        "text_back": "#a9abad",
                        "border_width": 1,
                    },
                }
            }
        )

    def default_palette(self):
        self.palette_bilibili_light()


class BiliBiliDarkButton(BiliBiliButton):
    def default_palette(self):
        self.palette_bilibili_dark()


class BiliBiliFrame(AdwDrawRoundFrame3):
    def palette_bilibili_light(self):
        self.palette(
            {
                "frame": {
                    "radius": 18,
                    "back": "#ffffff",
                    "border": "#f1f2f3",
                    "border_width": 2,
                }
            }
        )

    def palette_bilibili_dark(self):
        self.palette(
            {
                "frame": {
                    "radius": 18,
                    "back": "#17181a",
                    "border": "#232527",
                    "border_width": 2,
                }
            }
        )

    def default_palette(self):
        self.palette_bilibili_light()


class BiliBiliDarkFrame(BiliBiliFrame):
    def default_palette(self):
        self.palette_bilibili_dark()


class BiliBiliEntry(AdwDrawRoundEntry3):
    def palette_bilibili_light(self):
        self.palette(
            {
                "entry": {
                    "radius": 16,
                    "padding": (8, 8),

                    "back": "#ffffff",
                    "border": "#e3e5e7",
                    "text_back": "#18191c",
                    "border_width": 1,

                    "bottom_line": "#eaeaea",
                    "bottom_width": 0,

                    "focusin": {
                        "back": "#ffffff",
                        "border": "#ff6699",
                        "text_back": "#18191c",
                        "border_width": 1,

                        "bottom_line": "#185fb4",
                        "bottom_width": 0,
                    }
                },
            }
        )

    def palette_bilibili_dark(self):
        self.palette(
            {
                "entry": {
                    "radius": 16,
                    "padding": (8, 8),

                    "back": "#17181a",
                    "border": "#2f3134",
                    "text_back": "#e7e9eb",
                    "border_width": 1,

                    "bottom_line": "#eaeaea",
                    "bottom_width": 0,

                    "focusin": {
                        "back": "#17181a",
                        "border": "#d44e7d",
                        "text_back": "#e7e9eb",
                        "border_width": 1,

                        "bottom_line": "#d44e7d",
                        "bottom_width": 0,
                    }
                },
            }
        )

    def default_palette(self):
        self.palette_bilibili_light()


class BiliBiliDarkEntry(BiliBiliEntry):
    def default_palette(self):
        self.palette_bilibili_dark()


class BiliBiliTextBox(AdwDrawRoundText3):
    def palette_bilibili_light(self):
        self.palette(
            {
                "text": {
                    "radius": 16,
                    "padding": (8, 8),

                    "back": "#ffffff",
                    "border": "#e3e5e7",
                    "text_back": "#18191c",
                    "border_width": 1,

                    "bottom_line": "#eaeaea",
                    "bottom_width": 0,

                    "focusin": {
                        "back": "#ffffff",
                        "border": "#ff6699",
                        "text_back": "#18191c",
                        "border_width": 1,

                        "bottom_line": "#185fb4",
                        "bottom_width": 0,
                    }
                },
            }
        )

    def palette_bilibili_dark(self):
        self.palette(
            {
                "text": {
                    "radius": 16,
                    "padding": (8, 8),

                    "back": "#17181a",
                    "border": "#2f3134",
                    "text_back": "#e7e9eb",
                    "border_width": 1,

                    "bottom_line": "#eaeaea",
                    "bottom_width": 0,

                    "focusin": {
                        "back": "#17181a",
                        "border": "#d44e7d",
                        "text_back": "#e7e9eb",
                        "border_width": 1,

                        "bottom_line": "#d44e7d",
                        "bottom_width": 0,
                    }
                },
            }
        )

    def default_palette(self):
        self.palette_bilibili_light()


class BiliBiliDarkTextBox(BiliBiliTextBox):
    def default_palette(self):
        self.palette_bilibili_dark()


if __name__ == '__main__':
    from tkadw import Adw
    root = Adw()

    frame = BiliBiliFrame(root)

    button = BiliBiliButton(frame.frame, text="BiliBiliButton")
    button.pack(fill="x", padx=10, pady=10)

    entry = BiliBiliEntry(frame.frame, text="BiliBiliEntry")
    entry.pack(fill="x", padx=10, pady=10)

    textbox = BiliBiliTextBox(frame.frame)
    textbox.pack(fill="x", padx=10, pady=10)

    frame.pack(fill="y", side="right", expand="yes")

    frame2 = BiliBiliDarkFrame(root)

    button2 = BiliBiliDarkButton(frame2.frame, text="BiliBiliDarkButton")
    button2.pack(fill="x", padx=10, pady=10)

    entry2 = BiliBiliDarkEntry(frame2.frame, text="BiliBiliDarkEntry")
    entry2.pack(fill="x", padx=10, pady=10)

    textbox2 = BiliBiliDarkTextBox(frame2.frame)
    textbox2.pack(fill="x", padx=10, pady=10)

    frame2.pack(fill="y", side="left", expand="yes")

    root.mainloop()