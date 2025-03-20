from customtkinter import *
from tkinter import ttk
from PIL import Image
import subprocess
import os
from scripts import *

class HomePage(CTkFrame):
    def __init__(self, master, fg_color="transparent"):
        super().__init__(master, fg_color=fg_color)
        self.settings_script = SettingsScript()
        self.BASE_PATH = self.settings_script.get_setting_value("General.Path")
        self.languages_folder = FolderScript(self.BASE_PATH)
        set_appearance_mode(self.settings_script.get_setting_value("Apparence.Theme").lower())
        set_default_color_theme(f"src/json/themes/{self.settings_script.get_setting_value('Apparence.Color')}.json")

        self.setup_frames()
        self.update_left_panel()
        self.initialize_right_panel()
        languages = self.languages_folder.get_folders()
        self.update_middle_panel(languages[0])

    def setup_frames(self):
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.left_panel = CTkFrame(self, width=250, fg_color=["#E5E5E5", "#212121"])
        self.left_panel.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.left_panel.grid_propagate(False)
        self.left_panel.grid_columnconfigure(0, weight=1)
        self.left_panel.grid_rowconfigure(1, weight=1)
        self.middle_panel = CTkFrame(self, fg_color=["#E5E5E5", "#212121"])
        self.middle_panel.grid(row=0, column=1, sticky="nsew", padx=0, pady=5)
        self.middle_panel.grid_columnconfigure(0, weight=1)
        self.middle_panel.grid_rowconfigure(0, weight=0)
        self.middle_panel.grid_rowconfigure(1, weight=0)
        self.middle_panel.grid_rowconfigure(2, weight=1)
        self.right_panel = CTkFrame(self, width=250, fg_color=["#E5E5E5", "#212121"])
        self.right_panel.grid(row=0, column=2, sticky="nsew", padx=5, pady=5)
        self.right_panel.grid_propagate(False)
        self.right_panel.grid_columnconfigure(0, weight=1)

    def update_left_panel(self):
        for widget in self.left_panel.winfo_children():
            widget.destroy()
        self.left_label = CTkLabel(self.left_panel, text="Languages", font=("Arial", 18, "bold"), anchor="w")
        self.left_label.grid(row=0, column=0, sticky="ew", padx=15, pady=15)
        self.left_listbox = CTkScrollableFrame(self.left_panel, fg_color="transparent")
        self.left_listbox.grid(row=1, column=0, sticky="nsew")
        languages = self.languages_folder.get_folders()
        for language in languages:
            language_frame = CTkFrame(self.left_listbox, fg_color=["#D9D9D9", "#292929"])
            language_frame.pack(fill="x", padx=5, pady=(0, 10))
            language_frame.grid_columnconfigure(1, weight=1)
            language_frame.grid_rowconfigure(0, weight=1)
            language_name_label = CTkLabel(language_frame, text=language, font=("Roboto", 12), text_color=["black", "white"], anchor='w')
            language_name_label.grid(row=0, column=1, sticky='nsew', padx=10, pady=5)
            language_frame.bind("<Enter>", lambda e, frame=language_frame: frame.configure(fg_color=["#BFBFBF", "#474747"]))
            language_frame.bind("<Leave>", lambda e, frame=language_frame: frame.configure(fg_color=["#D9D9D9", "#292929"]))
            language_frame.bind("<Button-1>", lambda e, lang=language: self.update_middle_panel(lang))
            for widget in language_frame.winfo_children():
                widget.bind("<Enter>", lambda e, frame=language_frame: frame.configure(fg_color=["#BFBFBF", "#474747"]))
                widget.bind("<Leave>", lambda e, frame=language_frame: frame.configure(fg_color=["#D9D9D9", "#292929"]))
                widget.bind("<Button-1>", lambda e, lang=language: self.update_middle_panel(lang))
        self.left_add_language_img = CTkImage(Image.open("src/assets/add-database.png").resize((25, 25)), size=(25, 25))
        self.left_add_language_btn = CTkButton(
            self.left_panel,
            text="Add language",
            font=("Arial", 14),
            image=self.left_add_language_img,
            compound="left",
            command=self.add_language
        )
        self.left_add_language_btn.grid(row=2, column=0, sticky="ew", padx=20, pady=(0, 15))

    def initialize_right_panel(self):
        self.left_add_language_img = CTkImage(Image.open("src/assets/sad.png").resize((50, 50)), size=(50, 50))
        nothing_frame = CTkFrame(self.right_panel, fg_color="transparent")
        nothing_frame.place(relx=0.5, rely=0.5, anchor='center')
        nothing_img = CTkLabel(nothing_frame, text="", image=self.left_add_language_img, anchor="center")
        nothing_img.pack()
        nothing_label = CTkLabel(nothing_frame, text="No project selected", font=("Arial", 16, "bold"), anchor="center")
        nothing_label.pack()

    def update_middle_panel(self, language):
        for widget in self.left_listbox.winfo_children():
            for w in widget.winfo_children():
                try:
                    w.configure(text_color=["black", "white"], font=("Roboto", 12))
                except Exception:
                    pass
                if w.cget("text") == language:
                    try:
                        w.configure(text_color=self._apply_appearance_mode(ThemeManager.theme["CTkButton"]["fg_color"]), font=("Roboto", 12, 'bold'))
                    except Exception:
                        pass
        projects_folder = FolderScript(f"{self.BASE_PATH}/{language}")
        for widget in self.middle_panel.winfo_children():
            widget.destroy()
        self.create_middle_header(language)
        separator = CTkFrame(self.middle_panel, height=2, fg_color=["gray65", "gray25"])
        separator.grid(row=1, column=0, sticky="ew", padx=15, pady=(0, 15))
        self.middle_listbox = CTkScrollableFrame(self.middle_panel, fg_color="transparent")
        self.middle_listbox.grid(row=2, column=0, sticky="nsew", padx=0, pady=(0, 15))
        for col in range(self.settings_script.get_setting_value("Apparence.Project columns")):
            self.middle_listbox.grid_columnconfigure(col, weight=1)
        for index, filename in enumerate(projects_folder.get_folders()):
            row, column = divmod(index, self.settings_script.get_setting_value("Apparence.Project columns"))
            self.create_project_widget(language, filename, row, column)

    def create_middle_header(self, language):
        self.middle_title_frame = CTkFrame(self.middle_panel, fg_color="transparent")
        self.middle_title_frame.grid(row=0, column=0, sticky="ew", padx=15, pady=15)
        self.middle_title_frame.grid_columnconfigure(0, weight=0)
        self.middle_title_frame.grid_columnconfigure(1, weight=1)
        self.middle_title_img = CTkImage(Image.open("src/assets/python.png").resize((30, 30)), size=(30, 30))
        self.middle_title_image_label = CTkLabel(self.middle_title_frame, text="", image=self.middle_title_img, anchor="w")
        self.middle_title_image_label.grid(row=0, column=0, padx=(0, 5))
        self.middle_title_label = CTkLabel(self.middle_title_frame, text=language, font=("Arial", 18, "bold"), anchor="w")
        self.middle_title_label.grid(row=0, column=1, sticky="ew")
        self.middle_title_edit_img = CTkImage(Image.open("src/assets/edit.png").resize((25, 25)), size=(25, 25))
        self.middle_title_edit_btn = CTkButton(
            self.middle_title_frame,
            text="Edit",
            font=("Arial", 14),
            fg_color=["#D9D9D9", "#292929"],
            hover_color=["#CCCCCC", "#383838"],
            text_color=["black", "white"],
            image=self.middle_title_edit_img,
            compound="left",
            command=lambda: self.edit_language(language)
        )
        self.middle_title_edit_btn.grid(row=0, column=2, padx=(5, 0))
        self.middle_title_add_img = CTkImage(Image.open("src/assets/add-propertie.png").resize((25, 25)), size=(25, 25))
        self.middle_title_add_btn = CTkButton(
            self.middle_title_frame,
            text="Add project",
            font=("Arial", 14),
            image=self.middle_title_add_img,
            compound="left",
            command=lambda: self.add_project(language)
        )
        self.middle_title_add_btn.grid(row=0, column=3, padx=(5, 0))

    def create_project_widget(self, language, filename, row, column):
        file_frame = CTkFrame(self.middle_listbox, fg_color=["#D9D9D9", "#292929"], height=75)
        file_frame.grid(row=row, column=column, sticky="ew", padx=5, pady=5)
        file_frame.grid_columnconfigure(0, weight=1)
        file_frame.grid_rowconfigure(1, weight=1)
        file_frame.grid_propagate(False)
        filename_label = CTkLabel(file_frame, text=filename, font=("Roboto", 12, "bold"), text_color=["black", "white"], anchor="w")
        filename_label.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 0))
        git_img = CTkImage(Image.open("src/assets/git.png").resize((25, 25)), size=(25, 25))
        git_img_label = CTkLabel(file_frame, text="", image=git_img, anchor="e")
        git_img_label.grid(row=1, column=0, sticky='ew', padx=(0, 10))
        file_frame.bind("<Enter>", lambda e: file_frame.configure(fg_color=["#CCCCCC", "#383838"]))
        file_frame.bind("<Leave>", lambda e: file_frame.configure(fg_color=["#D9D9D9", "#292929"]))
        file_frame.bind("<Button-1>", lambda e: self.open_project(language, filename))
        file_frame.bind("<Configure>", lambda e: file_frame.configure(height=file_frame.winfo_width()/2))
        for widget in file_frame.winfo_children():
            widget.bind("<Enter>", lambda e: file_frame.configure(fg_color=["#CCCCCC", "#383838"]))
            widget.bind("<Leave>", lambda e: file_frame.configure(fg_color=["#D9D9D9", "#292929"]))
            widget.bind("<Button-1>", lambda e: self.open_project(language, filename))

    def add_language(self):
        i = 0
        while True:
            new_folder_name = "New Folder " + str(i)
            if new_folder_name not in self.languages_folder.get_folders():
                self.languages_folder.create_folder(new_folder_name)
                self.update_left_panel()
                self.update_middle_panel(new_folder_name)
                break
            i += 1

    def edit_language(self, language):
        self.middle_title_label.grid_forget()
        self.middle_title_edit_btn.grid_forget()
        self.middle_title_add_btn.grid_forget()
        self.edit_language_title_entry = CTkEntry(self.middle_title_frame, placeholder_text=language)
        self.edit_language_title_entry.grid(row=0, column=1, sticky="ew")
        self.middle_title_cancel_img = CTkImage(Image.open("src/assets/close.png").resize((25, 25)), size=(25, 25))
        self.middle_title_cancel_btn = CTkButton(
            self.middle_title_frame,
            text="Cancel",
            font=("Arial", 14),
            fg_color=["#D9D9D9", "#292929"],
            hover_color=["#CCCCCC", "#383838"],
            text_color=["black", "white"],
            image=self.middle_title_cancel_img,
            compound="left",
            command=lambda: self.cancel_edit_language(language)
        )
        self.middle_title_cancel_btn.grid(row=0, column=2, padx=(5, 0))
        self.middle_title_done_img = CTkImage(Image.open("src/assets/done.png").resize((25, 25)), size=(25, 25))
        self.middle_title_done_btn = CTkButton(
            self.middle_title_frame,
            text="Done",
            font=("Arial", 14),
            image=self.middle_title_done_img,
            compound="left",
            command=lambda: self.done_edit_language(language)
        )
        self.middle_title_done_btn.grid(row=0, column=3, padx=(5, 0))
        for widget in self.left_listbox.winfo_children():
            for w in widget.winfo_children():
                try:
                    w.configure(text_color=["black", "white"], font=("Roboto", 12))
                except Exception:
                    pass
                if w.cget("text") == language:
                    try:
                        w.configure(text_color=self._apply_appearance_mode(ThemeManager.theme["CTkButton"]["fg_color"]), font=("Roboto", 12, 'bold'))
                        self.delete_language_img = CTkImage(Image.open("src/assets/trash.png").resize((25, 25)), size=(25, 25))
                        self.delete_language_btn = CTkButton(
                            widget,
                            text='',
                            font=("Arial", 14),
                            fg_color=["#D9D9D9", "#292929"],
                            hover_color=["#BFBFBF", "#474747"],
                            image=self.delete_language_img,
                            compound="left",
                            width=10,
                            command=lambda: self.delete_edit_language(language)
                        )
                        self.delete_language_btn.grid(row=0, column=2, sticky='ns', padx=5, pady=5)
                    except Exception:
                        pass

    def cancel_edit_language(self, language):
        self.edit_language_title_entry.grid_forget()
        self.middle_title_cancel_btn.grid_forget()
        self.middle_title_done_btn.grid_forget()
        self.update_left_panel()
        self.update_middle_panel(language)

    def done_edit_language(self, language):
        projects_folder = FolderScript(self.BASE_PATH)
        projects_folder.rename_folder(language, self.edit_language_title_entry.get())
        self.update_left_panel()
        self.update_middle_panel(self.edit_language_title_entry.get())

    def delete_edit_language(self, language):
        projects_folder = FolderScript(self.BASE_PATH)
        projects_folder.delete_folder(language)
        self.update_left_panel()
        self.update_middle_panel(projects_folder.get_folders()[0])

    def open_project(self, language, project):
        for widget in self.middle_listbox.winfo_children():
            for w in widget.winfo_children():
                try:
                    w.configure(text_color=["black", "white"])
                except Exception:
                    pass
                if w.cget("text") == project:
                    try:
                        w.configure(text_color=self._apply_appearance_mode(ThemeManager.theme["CTkButton"]["fg_color"]))
                    except Exception:
                        pass
        
        for widget in self.right_panel.winfo_children():
            widget.destroy()
        self.right_panel.grid_rowconfigure(3, weight=1)
        self.right_panel.grid_rowconfigure(4, weight=0)
        project_name_label = CTkLabel(self.right_panel, text=project, font=("Arial", 18, "bold"), anchor="w")
        project_name_label.grid(row=0, column=0, sticky='ew', padx=15, pady=(15, 0))
        language_name_label = CTkLabel(self.right_panel, text=language, font=("Arial", 14, 'italic'), text_color=["gray35", "gray65"], anchor='w')
        language_name_label.grid(row=1, column=0, sticky='ew', padx=20, pady=(0,15))
        separator = CTkFrame(self.right_panel, height=2, fg_color=["gray65", "gray25"])
        separator.grid(row=2, column=0, sticky="ew", padx=15, pady=(0, 15))
        self.treeview_frame = CTkFrame(self.right_panel)
        self.treeview_frame.grid(row=3, column=0, sticky="nsew", padx=10, pady=5)
        self.treeview_frame.grid_columnconfigure(0, weight=1)
        self.treeview_frame.grid_rowconfigure(1, weight=1)
        self.treeview_label = CTkLabel(self.treeview_frame, text='TreeView', font=("Arial", 16, "bold"), anchor='w')
        self.treeview_label.grid(row=0, column=0, sticky='ew', padx=10, pady=(10, 0))
        bg_color = self._apply_appearance_mode(ThemeManager.theme["CTkFrame"]["fg_color"])
        text_color = self._apply_appearance_mode(ThemeManager.theme["CTkLabel"]["text_color"])
        selected_color = self._apply_appearance_mode(ThemeManager.theme["CTkButton"]["fg_color"])
        treestyle = ttk.Style()
        treestyle.theme_use('default')
        treestyle.configure("Treeview", background=bg_color, foreground=text_color, fieldbackground=bg_color, borderwidth=0)
        treestyle.map('Treeview', background=[('selected', bg_color)], foreground=[('selected', "#388E3C")])
        self.treeview = ttk.Treeview(self.treeview_frame, show="tree")
        self.treeview.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)
        self.treeview.column("#0", width=200)
        self.open_populate_tree(f"{self.BASE_PATH}/{language}/{project}", "")
        self.img_vscode = CTkImage(Image.open("src/assets/visual-studio.png").resize((25, 25)), size=(25, 25))
        self.img_folder = CTkImage(Image.open("src/assets/folder.png").resize((25, 25)), size=(25, 25))
        self.opens_frame = CTkFrame(self.right_panel, fg_color=["#E5E5E5", "#212121"])
        self.opens_frame.grid(row=4, column=0, sticky="ew", padx=5, pady=5)
        self.opens_frame.grid_columnconfigure(0, weight=1)
        self.opens_frame.grid_columnconfigure(1, weight=1)
        self.open_folder_btn = CTkButton(
            self.opens_frame,
            text="Open",
            font=("Arial", 14),
            image=self.img_folder,
            compound="left",
            command=lambda: self.open_folder(language, project)
        )
        self.open_folder_btn.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        self.open_vscode_btn = CTkButton(
            self.opens_frame,
            text="Open",
            font=("Arial", 14),
            image=self.img_vscode,
            compound="left",
            command=lambda: self.open_vscode(language, project)
        )
        self.open_vscode_btn.grid(row=0, column=1, sticky="ew", padx=5, pady=5)

    def open_populate_tree(self, path, parent):
        try:
            items = sorted(os.listdir(path))
            directories = [item for item in items if os.path.isdir(os.path.join(path, item))]
            files = [item for item in items if os.path.isfile(os.path.join(path, item))]
            for folder in directories:
                folder_path = os.path.join(path, folder)
                folder_id = self.treeview.insert(parent, "end", text=folder, open=False)
                self.open_populate_tree(folder_path, folder_id)
            for file in files:
                self.treeview.insert(parent, "end", text=file, open=False)
        except PermissionError:
            pass

    def open_folder(self, language, project):
        os.startfile(f"{self.BASE_PATH}/{language}/{project}")

    def open_vscode(self, language, project):
        os.system(f'code "{self.BASE_PATH}/{language}/{project}"')

    def add_project(self, language):
        for widget in self.middle_listbox.winfo_children():
            for w in widget.winfo_children():
                try:
                    w.configure(text_color=["black", "white"])
                except Exception:
                    pass
        for widget in self.right_panel.winfo_children():
            widget.destroy()
        self.right_panel.grid_rowconfigure(3, weight=0)
        self.right_panel.grid_rowconfigure(4, weight=1)
        project_name_label = CTkLabel(self.right_panel, text="Create Project", font=("Arial", 18, "bold"), anchor="w")
        project_name_label.grid(row=0, column=0, sticky='ew', padx=15, pady=15)
        separator = CTkFrame(self.right_panel, height=2, fg_color=["gray65", "gray25"])
        separator.grid(row=1, column=0, sticky="ew", padx=15, pady=(0, 15))
        self.name_entry = CTkEntry(self.right_panel, placeholder_text="Project name")
        self.name_entry.grid(row=2, column=0, sticky='ew', padx=15)
        advanced_options_frame = CTkFrame(self.right_panel)
        advanced_options_frame.grid(row=3, column=0, sticky='ew', padx=15, pady=15)
        self.readme_option = CTkCheckBox(
            advanced_options_frame,
            text="README.md",
            command=self.create_populate_tree
        )
        self.readme_option.grid(row=0, column=0, sticky="ew", padx=(10,5), pady=(10,5))
        self.license_option = CTkCheckBox(
            advanced_options_frame,
            text="LICENSE",
            command=self.create_populate_tree
        )
        self.license_option.grid(row=0, column=1, sticky="ew", padx=(5,10), pady=(10,5))
        self.git_option = CTkCheckBox(
            advanced_options_frame,
            text=".git",
            command=self.create_populate_tree
        )
        self.git_option.grid(row=1, column=0, sticky="ew", padx=(10,5), pady=(5,10))
        self.gitignore_option = CTkCheckBox(
            advanced_options_frame,
            text=".gitignore",
            command=self.create_populate_tree
        )
        self.gitignore_option.grid(row=1, column=1, sticky="ew", padx=(5,10), pady=(5,10))
        self.treeview_frame = CTkFrame(self.right_panel)
        self.treeview_frame.grid(row=4, column=0, sticky="nsew", padx=15, pady=0)
        self.treeview_frame.grid_columnconfigure(0, weight=1)
        self.treeview_frame.grid_rowconfigure(0, weight=1)
        bg_color = self._apply_appearance_mode(ThemeManager.theme["CTkFrame"]["fg_color"])
        text_color = self._apply_appearance_mode(ThemeManager.theme["CTkLabel"]["text_color"])
        selected_color = self._apply_appearance_mode(ThemeManager.theme["CTkButton"]["fg_color"])
        treestyle = ttk.Style()
        treestyle.theme_use('default')
        treestyle.configure("Treeview", background=bg_color, foreground=text_color, fieldbackground=bg_color, borderwidth=0)
        treestyle.map('Treeview', background=[('selected', bg_color)], foreground=[('selected', selected_color)])
        self.treeview = ttk.Treeview(self.treeview_frame, show="tree")
        self.treeview.grid(row=0, column=0, sticky="nsew", padx=10, pady=5)
        self.treeview.column("#0", width=200)
        self.create_populate_tree()
        self.create_img = CTkImage(Image.open("src/assets/add-propertie.png").resize((25, 25)), size=(25, 25))
        self.create_btn = CTkButton(
            self.right_panel,
            text="Create",
            font=("Arial", 14),
            image=self.create_img,
            compound="left",
            command=lambda: self.create_project(language)
        )
        self.create_btn.grid(row=5, column=0, sticky='ew', padx=15, pady=15)

    def create_populate_tree(self):
        for item in self.treeview.get_children():
            self.treeview.delete(item)
        src_item = self.treeview.insert("", "end", text="src", open=True)
        self.treeview.insert(src_item, "end", text="main.py", open=True)
        if self.readme_option.get():
            self.treeview.insert("", "end", text="README.md", open=True)
        if self.license_option.get():
            self.treeview.insert("", "end", text="LICENSE", open=True)
        if self.git_option.get():
            self.treeview.insert("", "end", text=".git", open=True)
        if self.gitignore_option.get():
            self.treeview.insert("", "end", text=".gitignore", open=True)

    def create_project(self, language):
        project_name = self.name_entry.get().strip()
        if not project_name:
            print("Le nom du projet est obligatoire.")
            return
        project_folder = os.path.join(self.BASE_PATH, language, project_name)
        os.makedirs(project_folder, exist_ok=True)
        folder_script = FolderScript(project_folder)
        src_folder = folder_script.create_folder("src")
        FolderScript(src_folder).create_file("main.py", content="# Fichier principal\n")
        if self.readme_option.get():
            folder_script.create_file("README.md", content=f"# {project_name}\n")
        if self.license_option.get():
            folder_script.create_file("LICENSE", content="Votre licence ici")
        if self.git_option.get():
            folder_script.create_folder(".git")
        if self.gitignore_option.get():
            folder_script.create_file(".gitignore", content="# Fichiers à ignorer\n")
        print(f"Projet '{project_name}' créé avec succès dans {project_folder}.")
        self.update_middle_panel(language)
        self.open_project(language, project_name)
