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

        self.pages_script = PageScript()
        self.settings_script = SettingsScript()

        self.home_page = HomePage(self, self.pages_script)
        self.settings_page = SettingsPage(self, self.pages_script)

        self.pages_script.pack_page(self.home_page)


if __name__ == "__main__":
    app = DevDockApp()
    app.mainloop()
