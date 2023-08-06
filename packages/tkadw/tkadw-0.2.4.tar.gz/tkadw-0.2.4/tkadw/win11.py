from tkadw import AdwDrawRoundButton3, AdwDrawRoundFrame3, AdwDrawRoundEntry3, AdwDrawRoundText3


class Win11Button(AdwDrawRoundButton3):
    def palette_win11_light(self):
        self.palette(
            {
                "button": {
                    "radius": 13,
                    "back": "#fdfdfd",
                    "border": "#ededed",
                    "text_back": "#202020",
                    "border_width": 1,

                    "active": {
                        "back": "#f9f9f9",
                        "border": "#d5d5d5",
                        "text_back": "#202020",
                        "border_width": 1,
                    },

                    "pressed": {
                        "back": "#fafafa",
                        "border": "#ebebeb",
                        "text_back": "#202020",
                        "border_width": 1,
                    },
                }
            }
        )

    def palette_win11_dark(self):
        self.palette(
            {
                "button": {
                    "radius": 13,
                    "back": "#2a2a2a",
                    "border": "#313131",
                    "text_back": "#ebebeb",
                    "border_width": 1,

                    "active": {
                        "back": "#2f2f2f",
                        "border": "#313131",
                        "text_back": "#ebebeb",
                        "border_width": 1,
                    },

                    "pressed": {
                        "back": "#232323",
                        "border": "#2c2c2c",
                        "text_back": "#ebebeb",
                        "border_width": 1,
                    },
                }
            }
        )

    def palette_win11_alight(self):
        self.palette(
            {
                "button": {
                    "radius": 13,
                    "back": "#0560b6",
                    "border": "#1a6cba",
                    "text_back": "#ebebeb",
                    "border_width": 1,

                    "active": {
                        "back": "#1e6fbc",
                        "border": "#307bc2",
                        "text_back": "#ebebeb",
                        "border_width": 1,
                    },

                    "pressed": {
                        "back": "#327ec5",
                        "border": "#4288ca",
                        "text_back": "#ebebeb",
                        "border_width": 1,
                    },
                }
            }
        )

    def palette_win11_adark(self):
        self.palette(
            {
                "button": {
                    "radius": 13,
                    "back": "#57c8ff",
                    "border": "#64cdff",
                    "text_back": "#1c1c1c",
                    "border_width": 1,

                    "active": {
                        "back": "#51b7eb",
                        "border": "#5fbced",
                        "text_back": "#1c1c1c",
                        "border_width": 1,
                    },

                    "pressed": {
                        "back": "#4ba6d5",
                        "border": "#59aed9",
                        "text_back": "#1c1c1c",
                        "border_width": 1,
                    },
                }
            }
        )

    def default_palette(self):
        self.palette_win11_light()


class Win11DarkButton(Win11Button):
    def default_palette(self):
        self.palette_win11_dark()


class Win11AccentButton(Win11Button):
    def default_palette(self):
        self.palette_win11_alight()


class Win11DarkAccentButton(Win11Button):
    def default_palette(self):
        self.palette_win11_adark()


class Win11Frame(AdwDrawRoundFrame3):
    def palette_win11_light(self):
        self.palette(
            {
                "frame": {
                    "radius": 15,
                    "back": "#fafafa",
                    "border": "#e7e7e7",
                    "border_width": 2,
                }
            }
        )

    def palette_win11_dark(self):
        self.palette(
            {
                "frame": {
                    "radius": 15,
                    "back": "#1c1c1c",
                    "border": "#2f2f2f",
                    "border_width": 2,
                }
            }
        )

    def default_palette(self):
        self.palette_win11_light()


class Win11DarkFrame(Win11Frame):
    def default_palette(self):
        self.palette_win11_dark()


class Win11Entry(AdwDrawRoundEntry3):
    def palette_win11_light(self):
        self.palette(
            {
                "entry": {
                    "radius": 13,
                    "padding": (8, 8),

                    "back": "#fdfdfd",
                    "border": "#ebebeb",
                    "text_back": "#18191c",
                    "border_width": 1,

                    "bottom_line": "#8a8a8a",
                    "bottom_width": 1,

                    "focusin": {
                        "back": "#ffffff",
                        "border": "#ebebeb",
                        "text_back": "#18191c",
                        "border_width": 1,

                        "bottom_line": "#005fb8",
                        "bottom_width": 2,
                    }
                },
            }
        )

    def palette_win11_dark(self):
        self.palette(
            {
                "entry": {
                    "radius": 13,
                    "padding": (8, 8),

                    "back": "#292929",
                    "border": "#292929",
                    "text_back": "#e7e9eb",
                    "border_width": 1,

                    "bottom_line": "#989898",
                    "bottom_width": 1,

                    "focusin": {
                        "back": "#1c1c1c",
                        "border": "#2c2c2c",
                        "text_back": "#e7e9eb",
                        "border_width": 1,

                        "bottom_line": "#57c8ff",
                        "bottom_width": 2,
                    }
                },
            }
        )

    def palette_win11_alight(self):
        self.palette(
            {
                "entry": {
                    "radius": 13,
                    "padding": (8, 8),

                    "back": "#fdfdfd",
                    "border": "#ebebeb",
                    "text_back": "#18191c",
                    "border_width": 1,

                    "bottom_line": "#8a8a8a",
                    "bottom_width": 1,

                    "focusin": {
                        "back": "#ffffff",
                        "border": "#ebebeb",
                        "text_back": "#18191c",
                        "border_width": 1,

                        "bottom_line": "#005fb8",
                        "bottom_width": 2,
                    }
                },
            }
        )

    def palette_win11_adark(self):
        self.palette(
            {
                "entry": {
                    "radius": 13,
                    "padding": (8, 8),

                    "back": "#292929",
                    "border": "#292929",
                    "text_back": "#e7e9eb",
                    "border_width": 1,

                    "bottom_line": "#989898",
                    "bottom_width": 1,

                    "focusin": {
                        "back": "#1c1c1c",
                        "border": "#2c2c2c",
                        "text_back": "#e7e9eb",
                        "border_width": 1,

                        "bottom_line": "#57c8ff",
                        "bottom_width": 2,
                    }
                },
            }
        )

    def default_palette(self):
        self.palette_win11_light()


class Win11DarkEntry(Win11Entry):
    def default_palette(self):
        self.palette_win11_dark()


class Win11TextBox(AdwDrawRoundText3):
    def palette_win11_light(self):
        self.palette(
            {
                "text": {
                    "radius": 13,
                    "padding": (8, 8),

                    "back": "#fdfdfd",
                    "border": "#ebebeb",
                    "text_back": "#18191c",
                    "border_width": 1,

                    "bottom_line": "#8a8a8a",
                    "bottom_width": 1,

                    "focusin": {
                        "back": "#ffffff",
                        "border": "#ebebeb",
                        "text_back": "#18191c",
                        "border_width": 1,

                        "bottom_line": "#005fb8",
                        "bottom_width": 2,
                    }
                },
            }
        )

    def palette_win11_dark(self):
        self.palette(
            {
                "text": {
                    "radius": 13,
                    "padding": (8, 8),

                    "back": "#292929",
                    "border": "#292929",
                    "text_back": "#e7e9eb",
                    "border_width": 1,

                    "bottom_line": "#989898",
                    "bottom_width": 1,

                    "focusin": {
                        "back": "#1c1c1c",
                        "border": "#2c2c2c",
                        "text_back": "#e7e9eb",
                        "border_width": 1,

                        "bottom_line": "#57c8ff",
                        "bottom_width": 2,
                    }
                },
            }
        )

    def default_palette(self):
        self.palette_win11_light()


class Win11DarkTextBox(Win11TextBox):
    def default_palette(self):
        self.palette_win11_dark()


if __name__ == '__main__':
    from tkadw import Adw
    root = Adw()

    frame = Win11Frame(root)

    button = Win11Button(frame.frame, text="Win11Button")
    button.pack(fill="x", padx=10, pady=10)

    button3 = Win11AccentButton(frame.frame, text="Win11AccentButton")
    button3.pack(fill="x", padx=10, pady=10)

    entry = Win11Entry(frame.frame, text="Win11Entry")
    entry.pack(fill="x", padx=10, pady=10)

    textbox = Win11TextBox(frame.frame)
    textbox.pack(fill="x", padx=10, pady=10)

    frame.pack(fill="y", side="right", expand="yes")

    frame2 = Win11DarkFrame(root)

    button2 = Win11DarkButton(frame2.frame, text="Win11DarkButton")
    button2.pack(fill="x", padx=10, pady=10)

    button4 = Win11DarkAccentButton(frame2.frame, text="Win11DarkAccentButton")
    button4.pack(fill="x", padx=10, pady=10)

    entry2 = Win11DarkEntry(frame2.frame, text="Win11DarkEntry")
    entry2.pack(fill="x", padx=10, pady=10)

    textbox2 = Win11DarkTextBox(frame2.frame)
    textbox2.pack(fill="x", padx=10, pady=10)

    frame2.pack(fill="y", side="left", expand="yes")

    root.mainloop()