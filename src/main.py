from customtkinter import *
from pages import *
from scripts import *

class DevDockApp(CTk):
    def __init__(self):
        super().__init__()

        self.title("DevDock")
        self.geometry("1000x500")
        self.minsize(1000, 500)
        self.iconbitmap("src/assets/logo.ico")

        self.page_script = PageScript()

        self.page_script.pack_page(SettingsPage(self))

if __name__ == "__main__":
    app = DevDockApp()
    app.mainloop()
