import os
from tkinter import ttk
from customtkinter import *
from PIL import Image, ImageTk
from scripts import FolderScript  # Assurez-vous que ce module est accessible

class AddProjectTopLevel(CTkToplevel):
    def __init__(self, master, path, language):
        super().__init__(master)
        self.path = path
        self.language = language  # Vous pouvez utiliser ce paramètre pour personnaliser le contenu
        self.parent = master
        width, height = 310, 400
        posx = self.parent.winfo_x() + self.parent.winfo_width() // 2 - width // 2
        posy = self.parent.winfo_y() + self.parent.winfo_height() // 2 - height // 2
        
        self.title("Create project")
        self.geometry(f"{width}x{height}+{posx}+{posy}")
        self.minsize(width, height)

        self.init_ui()

    def init_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(4, weight=1)

        self.title_label = CTkLabel(self, text="Create project", font=("Arial", 16, "bold"), anchor="w")
        self.title_label.grid(row=0, column=0, sticky="ew", padx=10, pady=10)

        separator = CTkFrame(self, height=2, fg_color=["gray65", "gray25"])
        separator.grid(row=1, column=0, sticky="ew", padx=10, pady=5)

        self.name_frame = CTkFrame(self, fg_color="transparent")
        self.name_frame.grid(row=2, column=0, sticky="ew", padx=10, pady=5)
        self.name_frame.grid_columnconfigure(1, weight=1)

        self.name_label = CTkLabel(self.name_frame, text="Name : ", font=("Arial", 14), anchor="w")
        self.name_label.grid(row=0, column=0, sticky="ew", padx=5, pady=5)

        self.name_entry = CTkEntry(self.name_frame, font=("Arial", 14))
        self.name_entry.grid(row=0, column=1, sticky="ew", padx=5, pady=5)

        self.options_frame = CTkFrame(self)
        self.options_frame.grid(row=3, column=0, sticky="ew", padx=10, pady=5)

        self.readme_option = CTkCheckBox(
            self.options_frame, text="README.md", font=("Arial", 14),
            fg_color=["#4CAF50", "#388E3C"], hover_color=["#43A047", "#2E7D32"],
            command=self.populate_tree
        )
        self.readme_option.grid(row=0, column=0, sticky="ew", padx=5, pady=5)

        self.license_option = CTkCheckBox(
            self.options_frame, text="LICENSE", font=("Arial", 14),
            fg_color=["#4CAF50", "#388E3C"], hover_color=["#43A047", "#2E7D32"],
            command=self.populate_tree
        )
        self.license_option.grid(row=0, column=1, sticky="ew", padx=5, pady=5)

        self.git_option = CTkCheckBox(
            self.options_frame, text=".git", font=("Arial", 14),
            fg_color=["#4CAF50", "#388E3C"], hover_color=["#43A047", "#2E7D32"],
            command=self.populate_tree
        )
        self.git_option.grid(row=1, column=0, sticky="ew", padx=5, pady=5)

        self.gitignore_option = CTkCheckBox(
            self.options_frame, text=".gitignore", font=("Arial", 14),
            fg_color=["#4CAF50", "#388E3C"], hover_color=["#43A047", "#2E7D32"],
            command=self.populate_tree
        )
        self.gitignore_option.grid(row=1, column=1, sticky="ew", padx=5, pady=5)

        bg_color = self._apply_appearance_mode(ThemeManager.theme["CTkFrame"]["fg_color"])
        text_color = self._apply_appearance_mode(ThemeManager.theme["CTkLabel"]["text_color"])
        selected_color = self._apply_appearance_mode(ThemeManager.theme["CTkButton"]["fg_color"])

        treestyle = ttk.Style()
        treestyle.theme_use('default')
        treestyle.configure("Treeview", background=bg_color, foreground=text_color, fieldbackground=bg_color, borderwidth=0)
        treestyle.map('Treeview', background=[('selected', bg_color)], foreground=[('selected', selected_color)])

        self.treeview = ttk.Treeview(self, show="tree")
        self.treeview.grid(row=4, column=0, sticky="nsew", padx=10, pady=5)
        self.treeview.column("#0", width=200)

        self.populate_tree()

        self.create_img = CTkImage(
            Image.open("src/assets/add-propertie.png").resize((25, 25)), size=(25, 25)
        )
        self.create_btn = CTkButton(
            self, text="Create", font=("Arial", 14),
            fg_color=["#4CAF50", "#388E3C"], hover_color=["#43A047", "#2E7D32"],
            image=self.create_img, compound="left",
            command=self.create_project
        )
        self.create_btn.grid(row=5, column=0, padx=5, pady=5)

    def populate_tree(self):
        # Efface le contenu existant pour éviter les doublons
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

    def create_project(self):
        project_name = self.name_entry.get().strip()
        if not project_name:
            print("Le nom du projet est obligatoire.")
            return

        # Utilisation de self.path pour définir le chemin de base
        project_folder = os.path.join(self.path, project_name)
        os.makedirs(project_folder, exist_ok=True)
        print(f"Dossier du projet créé : {project_folder}")

        folder_script = FolderScript(project_folder)
        src_folder = folder_script.create_folder("src")
        # Création du fichier main.py dans le dossier src
        FolderScript(src_folder).create_file("main.py", content="# Fichier principal\n")
        print("Dossier 'src' et fichier 'main.py' créés.")

        if self.readme_option.get():
            folder_script.create_file("README.md", content=f"# {project_name}\n")
            print("Fichier README.md créé.")
        if self.license_option.get():
            folder_script.create_file("LICENSE", content="Votre licence ici")
            print("Fichier LICENSE créé.")
        if self.git_option.get():
            folder_script.create_folder(".git")
            print("Dossier .git créé.")
        if self.gitignore_option.get():
            folder_script.create_file(".gitignore", content="# Fichiers à ignorer\n")
            print("Fichier .gitignore créé.")

        print(f"Projet '{project_name}' créé avec succès dans {project_folder}.")
