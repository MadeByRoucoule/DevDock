from customtkinter import *
from pages import *
from scripts import *

class DevDockApp(CTk):
    def __init__(self):
        super().__init__()

        # Configure window properties
        self.iconbitmap("src/assets/logo.ico")

        self.pages_script = PageScript()
        self.settings_script = SettingsScript()

        self.settings = self.settings_script.get_settings()

        if self.settings["General"]["Path"] == "":
            self.first_launch_page = FirstLaunchPage(self, on_login_success=self.launch_home_page)
            self.pages_script.pack_page(self.first_launch_page)
        else:
            self.launch_home_page()

    def launch_home_page(self):

        self.geometry("1000x500")
        self.minsize(1000, 500)

        self.home_page = HomePage(self, self.pages_script)
        self.settings_page = SettingsPage(self, self.pages_script)

        self.title("DevDock - Home")
        self.pages_script.pack_page(self.home_page)

if __name__ == "__main__":
    app = DevDockApp()
    app.mainloop()
