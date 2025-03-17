from customtkinter import *
from pages import HomePage
class DevDockApp(CTk):
    def __init__(self):
        super().__init__()
        
        self.title("DevDock")
        self.geometry("800x500")
        self.minsize(800, 500)
        self.iconbitmap("src/assets/logo.ico")

        self.init_ui()
    
    def init_ui(self):
        self.homepage = HomePage(self)
        self.homepage.pack(fill="both", expand=True)

if __name__ == "__main__":
    set_appearance_mode("dark")
    app = DevDockApp()
    app.mainloop()
