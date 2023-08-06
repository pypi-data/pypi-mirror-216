from tkadw import AdwDrawLabel


class GTkLabel(AdwDrawLabel):
    def default_palette(self):
        self.palette_light()

    def palette_gtk_light(self):
        self.palette_light()

    def palette_gtk_dark(self):
        self.palette_dark()


class GTkDarkLabel(GTkLabel):
    def default_palette(self):
        self.palette_gtk_dark()
