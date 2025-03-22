from customtkinter import *
from CTkMenuBar import *
import webbrowser
import os
from scripts import *

class MenuBar:
    def __init__(self, master, home_page, settings_script):

        self.master = master
        self.home_page = home_page
        self.settings_script = settings_script

        self.init_menubar()

    def init_menubar(self):
        # Initialize menubar based on OS
        self.menu_bar = CTkMenuBar(self.master, bg_color=self.master._apply_appearance_mode(ThemeManager.theme["CTkFrame"]["fg_color"]))

        # Add main menu buttons
        button_file = self.menu_bar.add_cascade("File")
        button_settings = self.menu_bar.add_cascade("Settings")
        button_about = self.menu_bar.add_cascade("About")

        # Create dropdown for File menu
        dropdown_file = CustomDropdownMenu(widget=button_file)

        # Submenu for 'New' options
        sub_menu_new = dropdown_file.add_submenu('New')
        sub_menu_new.add_option("Language", self.home_page.add_language)

        # Submenu for creating a new project
        sub_menu_new_project = sub_menu_new.add_submenu("Project")
        for language in self.home_page.languages:
            sub_menu_new_project.add_option(language, lambda lang=language: self.home_page.add_project(lang))

        # Submenu for 'Open' options
        sub_menu_open = dropdown_file.add_submenu('Open')
        for language in self.home_page.languages:
            sub_menu_open_lang = sub_menu_open.add_submenu(language)
            projects_folder = FolderScript(f"{self.settings_script.get_setting_value('General.Path')}/{language}")
            for filename in projects_folder.get_folders():
                sub_menu_open_lang_project = sub_menu_open_lang.add_submenu(filename)
                sub_menu_open_lang_project.add_option("Open project", lambda lang=language, project=filename: self.home_page.open_project(lang, project))
                sub_menu_open_lang_project.add_option("Open folder", lambda lang=language, project=filename: self.home_page.open_folder(lang, project))
                sub_menu_open_lang_project.add_option("Open in vscode", lambda lang=language, project=filename: self.home_page.open_vscode(lang, project))

        dropdown_file.add_separator()

        dropdown_file.add_option("Exit", self.master.destroy)

        # Create dropdown for Settings menu
        dropdown_settings = CustomDropdownMenu(widget=button_settings)
        dropdown_settings.add_option("Preferences", self.home_page.open_settings)
        dropdown_settings.add_option("Update", self.home_page.update)

        # Create dropdown for About menu
        dropdown_about = CustomDropdownMenu(widget=button_about)
        dropdown_about.add_option(option="Github", command=lambda: webbrowser.open("https://github.com/MadeByRoucoule/DevDock"))

    def destroy_bar(self):
        self.menu_bar.destroy()