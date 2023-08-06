from tkinter import Frame
from tkadw import AdwDrawEngine


class GTkNoteBook(AdwDrawEngine):
    def __init__(self, ):
        super().__init__(bd=0, highlightthickness=0)

        self.default_palette()

        self.bind("<Configure>", lambda event: self.__draw())

        self.frame = None

        self.tabs = {}

    def add(self, frame, text: str = ""):
        self.tabs[frame._w] = [frame, text]
        if len(self.tabs) == 1:
            self.show(frame)
            self.__draw()

    def show(self, frame):
        self.frame = frame
        self.__draw()

    def __draw(self):
        self.notebook_tabs = self.create_rectangle(self.notebook_tabs_button_padding[0],
                                                   self.notebook_tabs_button_padding[1],
                                                   50+self.notebook_tabs_button_padding[0],
                                                   30+self.notebook_tabs_button_padding[1],
                                                   fill=self.notebook_tabs_button_back, outline=self.notebook_tabs_button_border, width=self.notebook_tabs_button_borderwidth)
        self.notebook_text = self.create_text()
        if self.frame is not None:
            self.notebook_frame = self.create_window(self.winfo_width()/2, self.winfo_height()/2+15, width=self.winfo_width(), height=self.winfo_height()-30, window=self.frame)

    def default_palette(self):
        self.palette_light()

    def palette_light(self):
        self.palette(
            {
                "notebook_frame_back": "#f8f8f8",

                "notebook_tabs_button_padding": (5, 5),

                "notebook_tabs_button_back": "#ffffff",
                "notebook_tabs_button_border": "#eaeaea",
                "notebook_tabs_button_borderwidth": 1,
            }
        )

    def palette_dark(self):
        self.palette(
            {
                "notebook_frame_back": "#f8f8f8",

                "notebook_tabs_button_back": "#ffffff",
                "notebook_tabs_button_border": "#eaeaea",
                "notebook_tabs_button_borderwidth": 1,
            }
        )

    def palette(self, dict=None):
        if dict is not None:
            self.notebook_frame_back = dict["notebook_frame_back"]

            self.notebook_tabs_button_padding = dict["notebook_tabs_button_padding"]

            self.notebook_tabs_button_back = dict["notebook_tabs_button_back"]
            self.notebook_tabs_button_border = dict["notebook_tabs_button_border"]
            self.notebook_tabs_button_borderwidth = dict["notebook_tabs_button_borderwidth"]

            try:
                self._draw(None)
            except AttributeError:
                pass
        else:
            return {
                "notebook_frame_back": self.notebook_frame_back,

                "notebook_tabs_button_padding": self.notebook_tabs_button_padding,

                "notebook_tabs_button_back": self.notebook_tabs_button_back,
                "notebook_tabs_button_border": self.notebook_tabs_button_border,
                "notebook_tabs_button_borderwidth": self.notebook_tabs_button_borderwidth,
            }


if __name__ == '__main__':
    from tkinter import Tk
    root = Tk()

    notebook = GTkNoteBook()
    #notebook.configure(background="#000000")
    frame = Frame()
    #frame.configure(background="#000000")
    notebook.add(frame)
    notebook.pack(fill="both", expand="yes")

    root.mainloop()