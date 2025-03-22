from customtkinter import *
from pages import *
from scripts import *

class DevDockApp(CTk):
    def __init__(self):
        # Initialize the main application window
        super().__init__()

        # Configure window properties
        self.title("DevDock")
        self.geometry("1000x500")
        self.minsize(1000, 500)
        self.iconbitmap("src/assets/logo.ico")

        # Initialize core scripts
        self.pages_script = PageScript()
        self.settings_script = SettingsScript()

        # Initialize pages
        self.home_page = HomePage(self, self.pages_script)
        self.settings_page = SettingsPage(self, self.pages_script)


        # Display the home page initially
        self.pages_script.pack_page(self.home_page)


if __name__ == "__main__":
    app = DevDockApp()
    app.mainloop()
