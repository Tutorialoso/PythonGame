from tkinter import *

class Application(Frame):
    def __init__(self, master):
        super(Application, self).__init__(master)
        self.grid()
        self.create_widgets()
    def create_widgets(self):
        Label(self, text = "DotDot Game").grid(row = 0, column = 0, columnspan = 4)
        Button(self, text = "Settings", command = self.launch_settings).grid(sticky = S)
    def launch_settings(self):
        settings = Tk()
        settings.title("Settings - DotDot")
        settings.geometry("300x500")
        sett = Settings(settings)
        settings.mainloop()

class Settings(Frame):
    def __init__(self, master):
        super(Settings, self).__init__(master)
        self.grid()
        self.display_options()
    def display_options(self):
        Label(self, text = "Settings").grid(row = 0, column = 0, columnspan = 4)

root = Tk()
root.title("DotDot")
root.geometry("800x600")
app = Application(root)
root.mainloop()
