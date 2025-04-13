from customtkinter import *
from PIL import Image
from tkinter import filedialog, END
from tkinter import messagebox

from scripts import *

class FirstLaunchPage(CTkFrame):
    def __init__(self, master, on_login_success):
        super().__init__(master, fg_color="transparent")

        self.master = master
        self.on_login_success = on_login_success
        self.master.title("First Launch Page")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.settings_script = SettingsScript()
        self.settings = self.settings_script.get_settings()

        initial_theme = self.settings_script.get_setting_value("Apparence.Theme")
        initial_color = self.settings_script.get_setting_value("Apparence.Color")

        set_appearance_mode(initial_theme.lower())
        set_default_color_theme(f"src/json/themes/{initial_color}.json")

        self.current_theme = initial_theme
        self.current_color = initial_color
        self.current_page = 1

        self.page_1()

    def page_1(self):

        self.master.geometry("400x400")

        set_appearance_mode(self.current_theme.lower())
        set_default_color_theme(f"src/json/themes/{self.current_color}.json")

        self.page_1_frame = CTkFrame(self)
        self.page_1_frame.grid(row=0, column=0, sticky="nsew")
        self.page_1_frame.grid_columnconfigure(0, weight=1)
        self.page_1_frame.grid_rowconfigure(2, weight=1)

        self.logo_image = CTkImage(Image.open("src/assets/logo.png"), size=(75, 75))
        self.logo_label = CTkLabel(self.page_1_frame, text="", image=self.logo_image, font=("Arial", 24))
        self.logo_label.grid(row=0, column=0, padx=20, pady=20)

        self.title_label = CTkLabel(self.page_1_frame, text="Welcome to DevDock!", font=("Arial", 24))
        self.title_label.grid(row=1, column=0, padx=20, pady=20)

        self.description_label = CTkLabel(
            self.page_1_frame, 
            text="This is the first launch page of the app.\nPlease follow the instructions to proceed.",
            font=("Arial", 12)
        )
        self.description_label.grid(row=2, column=0, padx=20, pady=20)

        self.next_button = CTkButton(self.page_1_frame, text="Next", command=self.next_page, font=("Arial", 12))
        self.next_button.grid(row=3, column=0, padx=20, pady=20)

    def page_2(self):

        self.master.geometry("600x400")

        self.page_2_frame = CTkFrame(self)
        self.page_2_frame.grid(row=0, column=0, sticky="nsew")
        self.page_2_frame.grid_columnconfigure(0, weight=1)
        self.page_2_frame.grid_columnconfigure(1, weight=1)
        self.page_2_frame.grid_rowconfigure(2, weight=1)

        self.logo_image = CTkImage(Image.open("src/assets/logo.png"), size=(50, 50))
        self.title_label = CTkLabel(
            self.page_2_frame, 
            text="  DevDock", 
            font=("Arial", 24), 
            image=self.logo_image, 
            compound="left"
        )
        self.title_label.grid(row=1, column=0, columnspan=2, padx=20, pady=20)

        self.content_frame = CTkFrame(self.page_2_frame, fg_color="transparent")
        self.content_frame.grid(row=2, column=0, columnspan=2, padx=20, pady=20)

        self.description_label = CTkLabel(
            self.content_frame, 
            text="Let's customize your application.\nLet's start by choosing the appearance", 
            font=("Arial", 12)
        )
        self.description_label.grid(row=0, column=0, columnspan=2, padx=20, pady=20)

        self.theme_option_menu = CTkOptionMenu(
            self.content_frame, 
            values=list(self.settings["Apparence"]["Theme"].keys()), 
            command=self.preview_theme
        )
        self.theme_option_menu.grid(row=1, column=0, padx=20)
        self.theme_option_menu.set(self.current_theme)

        self.color_option_menu = CTkOptionMenu(
            self.content_frame, 
            values=list(self.settings["Apparence"]["Color"].keys()), 
            command=self.preview_theme
        )
        self.color_option_menu.grid(row=1, column=1, padx=20)
        self.color_option_menu.set(self.current_color)

        self.buttons_frame = CTkFrame(self.page_2_frame, fg_color="transparent")
        self.buttons_frame.grid(row=4, column=0, columnspan=2, sticky='ew', padx=20, pady=20)
        self.buttons_frame.grid_columnconfigure(1, weight=1)

        self.back_button = CTkButton(self.buttons_frame, text="Back", command=self.next_page, font=("Arial", 12))
        self.back_button.grid(row=0, column=0)

        self.next_button = CTkButton(self.buttons_frame, text="Next", command=self.next_page, font=("Arial", 12))
        self.next_button.grid(row=0, column=2)

    def page_3(self):
        self.master.geometry("500x400")

        self.page_3_frame = CTkFrame(self)
        self.page_3_frame.grid(row=0, column=0, sticky="nsew")
        self.page_3_frame.grid_columnconfigure(0, weight=1)
        self.page_3_frame.grid_rowconfigure(2, weight=1)

        self.logo_image = CTkImage(Image.open("src/assets/logo.png"), size=(50, 50))
        self.title_label = CTkLabel(
            self.page_3_frame, 
            text="  DevDock", 
            font=("Arial", 24), 
            image=self.logo_image, 
            compound="left"
        )
        self.title_label.grid(row=1, column=0, padx=20, pady=20)

        self.content_frame = CTkFrame(self.page_3_frame, fg_color="transparent")
        self.content_frame.grid(row=2, column=0, columnspan=2, padx=20, pady=20)

        self.description_label = CTkLabel(
            self.content_frame, 
            text="Last step,\nSelect the path to your dev folder.", 
            font=("Arial", 12)
        )
        self.description_label.grid(row=0, column=0, padx=20, pady=20)

        self.path_entry = CTkEntry(self.content_frame, placeholder_text="Path to your dev folder", width=300)
        self.path_entry.grid(row=1, column=0, padx=20, pady=20)

        self.path_button = CTkButton(self.content_frame, text="Browse", command=self.browse_path)
        self.path_button.grid(row=2, column=0, padx=20)

        self.buttons_frame = CTkFrame(self.page_3_frame, fg_color="transparent")
        self.buttons_frame.grid(row=4, column=0, columnspan=2, sticky='ew', padx=20, pady=20)
        self.buttons_frame.grid_rowconfigure(0, weight=1)
        self.buttons_frame.grid_columnconfigure(1, weight=1)

        self.back_button = CTkButton(self.buttons_frame, text="Back", command=self.next_page, font=("Arial", 12))
        self.back_button.grid(row=0, column=0)
        self.finish_button = CTkButton(self.buttons_frame, text="Finish", command=self.finish_setup, font=("Arial", 12))
        self.finish_button.grid(row=0, column=2)

    def next_page(self):
        if self.current_page == 1:
            self.current_page = 2
            self.page_1_frame.grid_forget()
            self.page_2()
        elif self.current_page == 2:
            self.current_page = 3
            self.page_2_frame.grid_forget()
            self.page_3()
        elif self.current_page == 3:
            self.current_page = 1
            self.page_3_frame.grid_forget()
            self.page_1()

    def preview_theme(self, _):
        self.current_theme = self.theme_option_menu.get()
        self.current_color = self.color_option_menu.get()

        set_appearance_mode(self.current_theme.lower())
        set_default_color_theme(f"src/json/themes/{self.current_color}.json")

        if self.current_page == 2:
            self.page_2_frame.destroy()
            self.page_2()

    def browse_path(self):
        path = filedialog.askdirectory()
        if path:
            self.path_entry.delete(0, END)
            self.path_entry.insert(0, path)

    def finish_setup(self):
        path = self.path_entry.get()
        if not path:
            messagebox.showerror("Error", "Please select a valid path.")
            return

        self.settings_script.change_setting("General.Path", path)
        self.settings_script.change_setting("Apparence.Theme", self.current_theme)
        self.settings_script.change_setting("Apparence.Color", self.current_color)

        self.destroy()

        self.on_login_success()

if __name__ == "__main__":
    root = CTk()
    app = FirstLaunchPage(root)
    app.pack(expand=True, fill="both")
    root.mainloop()
