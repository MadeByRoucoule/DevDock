from tkinter import ttk
from customtkinter import *
from PIL import Image

class ProjectTopLevel(CTkToplevel):
    def __init__(self, master, project_path, project_name):
        super().__init__(master)

        self.parent = master
        width, height = 310, 400
        posx, posy = ( self.parent.winfo_x() + self.parent.winfo_width()//2 ) - width // 2, ( self.parent.winfo_y() + self.parent.winfo_height()//2 ) - height // 2
        
        self.title(f"Project : {project_name}")
        self.geometry(f"{width}x{height}+{posx}+{posy}")
        self.minsize(width, height)

        self.project_path = project_path
        self.project_name = project_name

        self.img_vscode = CTkImage(Image.open("src/assets/visual-studio.png").resize((25, 25)), size=(25, 25))
        self.img_folder = CTkImage(Image.open("src/assets/folder.png").resize((25, 25)), size=(25, 25))

        self.init_ui()
        

    def init_ui(self):
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=0)

        self.title_frame = CTkFrame(self, fg_color=["#E5E5E5", "#212121"])
        self.title_frame.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        self.title = CTkLabel(self.title_frame, text=self.project_name, font=("Arial", 16, "bold"), anchor="w")
        self.title.grid(row=0, column=0, sticky="ew", padx=10, pady=10)

        self.content_frame = CTkFrame(self, fg_color=["#E5E5E5", "#212121"])
        self.content_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=(0,5))
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_rowconfigure(1, weight=1)

        self.content_label = CTkLabel(self.content_frame, text="Project treeview", font=("Arial", 14, "bold"), anchor="w")
        self.content_label.grid(row=0, column=0, sticky="ew", padx=10, pady=5)

        bg_color = self._apply_appearance_mode(ThemeManager.theme["CTkFrame"]["fg_color"])
        text_color = self._apply_appearance_mode(ThemeManager.theme["CTkLabel"]["text_color"])
        selected_color = self._apply_appearance_mode(ThemeManager.theme["CTkButton"]["fg_color"])

        treestyle = ttk.Style()
        treestyle.theme_use('default')
        treestyle.configure("Treeview", background=bg_color, foreground=text_color, fieldbackground=bg_color, borderwidth=0)
        treestyle.map('Treeview', background=[('selected', bg_color)], foreground=[('selected', selected_color)])

        self.treeview = ttk.Treeview(self.content_frame, show="tree")
        self.treeview.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)
        self.treeview.column("#0", width=200)

        self.populate_tree(self.project_path, "")

        self.opens_frame = CTkFrame(self, fg_color=["#E5E5E5", "#212121"])
        self.opens_frame.grid(row=2, column=0, sticky="ew", padx=5, pady=5)

        self.open_folder_btn = CTkButton(self.opens_frame, text="Open folder", font=("Arial", 14), fg_color=["#4CAF50", "#388E3C"], hover_color=["#43A047", "#2E7D32"], image=self.img_folder, compound="left")
        self.open_folder_btn.grid(row=0, column=0, sticky="ew", padx=5, pady=5)

        self.open_vscode_btn = CTkButton(self.opens_frame, text="Open vscode", font=("Arial", 14), fg_color=["#4CAF50", "#388E3C"], hover_color=["#43A047", "#2E7D32"], image=self.img_vscode, compound="left")
        self.open_vscode_btn.grid(row=0, column=1, sticky="ew", padx=5, pady=5)

    def populate_tree(self, path, parent):
        try:
            items = sorted(os.listdir(path))
            
            directories = [item for item in items if os.path.isdir(os.path.join(path, item))]
            files = [item for item in items if os.path.isfile(os.path.join(path, item))]

            for folder in directories:
                folder_path = os.path.join(path, folder)
                folder_id = self.treeview.insert(parent, "end", text=folder, open=False)
                self.populate_tree(folder_path, folder_id)  

            for file in files:
                self.treeview.insert(parent, "end", text=file, open=False)

        except PermissionError:
            pass