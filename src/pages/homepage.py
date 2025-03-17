from customtkinter import *
from PIL import Image, ImageTk
from scripts import *
from pages.projecttoplvl import ProjectTopLevel
from pages.addprojecttoplvl import AddProjectTopLevel

class HomePage(CTkFrame):
    def __init__(self, master, fg_color="transparent"):
        super().__init__(master, fg_color=fg_color)
        
        self.languages_folder = FolderScript("C:/Users/USER/Documents/DEV")

        self.setup_frames()
        self.init_ui()

        self.update_right_frame(self.languages_folder.get_folders()[1])

    def setup_frames(self):
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.left_frame = CTkFrame(self, width=250, fg_color=["#E5E5E5", "#212121"])
        self.left_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        self.right_frame = CTkFrame(self, fg_color=["#E5E5E5", "#212121"])
        self.right_frame.grid(row=0, column=1, sticky="nsew", padx=(0, 5), pady=5)

        self.left_frame.grid_propagate(False)
        self.left_frame.grid_columnconfigure(0, weight=1)
        self.left_frame.grid_rowconfigure(1, weight=1)

        self.right_frame.grid_columnconfigure(0, weight=1)
        self.right_frame.grid_rowconfigure(0, weight=1)

    def init_ui(self):

        self.left_label = CTkLabel(self.left_frame, text="Languages", font=("Arial", 18, "bold"), anchor="w")
        self.left_label.grid(row=0, column=0, sticky="ew", padx=15, pady=15)

        self.left_listbox = CTkScrollableFrame(self.left_frame, fg_color="transparent")
        self.left_listbox.grid(row=1, column=0, sticky="nsew")

        for l in range(len(self.languages_folder.get_folders())):
            btn = CTkButton(self.left_listbox, 
                            text=self.languages_folder.get_folders()[l], 
                            font=("Roboto ", 12), 
                            text_color=["black", "white"], 
                            fg_color=["#D9D9D9", "#292929"], 
                            hover_color=["#BFBFBF", "#474747"], 
                            command=lambda language=self.languages_folder.get_folders()[l]: self.update_right_frame(language))
            
            btn.pack(fill="x", padx=5, pady=(0,10))

        self.left_add_language_img = CTkImage(Image.open("src/assets/add-database.png").resize((25, 25)), size=(25, 25))
        self.left_add_language_btn = CTkButton(self.left_frame, text="Add language", font=("Arial", 14), fg_color=["#4CAF50", "#388E3C"], hover_color=["#43A047", "#2E7D32"], image=self.left_add_language_img, compound="left")
        self.left_add_language_btn.grid(row=2, column=0, sticky="ew", padx=20, pady=(0,15))

    def update_right_frame(self, language):
        
        for widget in self.left_listbox.winfo_children():
            widget.configure(fg_color=["#D9D9D9", "#292929"])
            if widget.cget("text") == language:
                widget.configure(fg_color=["#CCCCCC", "#383838"])

        projects_folder = FolderScript(f"C:/Users/USER/Documents/DEV/{language}")

        for widget in self.right_frame.winfo_children():
            widget.destroy()

        self.right_frame.grid_columnconfigure(0, weight=1)
        self.right_frame.grid_rowconfigure(0, weight=0)
        self.right_frame.grid_rowconfigure(1, weight=0)
        self.right_frame.grid_rowconfigure(2, weight=1)

        self.right_title_frame = CTkFrame(self.right_frame, fg_color="transparent")
        self.right_title_frame.grid(row=0, column=0, sticky="ew", padx=15, pady=15)
        self.right_title_frame.grid_columnconfigure(0, weight=0)
        self.right_title_frame.grid_columnconfigure(1, weight=1)
        
        self.right_title_img = CTkImage(Image.open("src/assets/python.png").resize((30, 30)), size=(30, 30))
        self.right_title_add_img = CTkImage(Image.open("src/assets/add-propertie.png").resize((25, 25)), size=(25, 25))

        self.right_title_image_label = CTkLabel(self.right_title_frame, text="", image=self.right_title_img, anchor="w")
        self.right_title_image_label.grid(row=0, column=0, padx=(0,5))
        self.right_title_label = CTkLabel(self.right_title_frame, text=language, font=("Arial", 18, "bold"), anchor="w")
        self.right_title_label.grid(row=0, column=1, sticky="ew")

        self.right_title_add_btn = CTkButton(self.right_title_frame, text="Add project", font=("Arial", 14), fg_color=["#4CAF50", "#388E3C"], hover_color=["#43A047", "#2E7D32"], image=self.right_title_add_img, compound="left", command=lambda: AddProjectTopLevel(self, path='C:/Users/USER/Documents/DEV', language=language))
        self.right_title_add_btn.grid(row=0, column=2, padx=(5,0))

        separator = CTkFrame(self.right_frame, height=2, fg_color=["gray65", "gray25"])
        separator.grid(row=1, column=0, sticky="ew", padx=15, pady=(0,15))

        self.right_listbox = CTkScrollableFrame(self.right_frame, fg_color="transparent")
        self.right_listbox.grid(row=2, column=0, sticky="nsew", padx=0, pady=(0,15))

        self.right_listbox.grid_columnconfigure(0, weight=1)
        self.right_listbox.grid_columnconfigure(1, weight=1)
        self.right_listbox.grid_columnconfigure(2, weight=1)

        for index, filename in enumerate(projects_folder.get_folders()):
            row, column = divmod(index, 3)
            file_frame = CTkFrame(self.right_listbox, fg_color=["#D9D9D9", "#292929"], height=75)
            file_frame.grid(row=row, column=column, sticky="ew", padx=5, pady=5)

            file_frame.grid_columnconfigure(0, weight=1)
            file_frame.grid_rowconfigure(0, weight=1)
            file_frame.grid_rowconfigure(1, weight=1)
            file_frame.grid_rowconfigure(2, weight=1)

            filename_label = CTkLabel(file_frame, text=filename, font=("Roboto ", 12, 'bold'), text_color=["black", "white"], anchor="w")
            filename_label.grid(column=0, row=0, sticky="ew", padx=10, pady=(10,0))

            file_seperator = CTkFrame(file_frame, height=2, fg_color=["gray65", "gray25"])
            file_seperator.grid(column=0, row=1, sticky="ew", padx=5, pady=5)

            file_size = CTkLabel(file_frame, text=f"{len(FolderScript(f'C:/Users/USER/Documents/DEV/{language}/{filename}').get_files())} files", font=("Roboto ", 12), text_color=["black", "white"], anchor="w")
            file_size.grid(column=0, row=2, sticky="ew", padx=15, pady=(0,10))

            file_frame.bind("<Enter>", lambda e, frame=file_frame: frame.configure(fg_color=["#BFBFBF", "#474747"]))
            file_frame.bind("<Leave>", lambda e, frame=file_frame: frame.configure(fg_color=["#D9D9D9", "#292929"]))
            file_frame.bind("<Button-1>", lambda e, filename=filename: ProjectTopLevel(self, f"{self.languages_folder.folder_path}/{language}/{filename}", filename))
            for widget in file_frame.winfo_children():
                widget.bind("<Enter>", lambda e, frame=file_frame: frame.configure(fg_color=["#BFBFBF", "#474747"]))
                widget.bind("<Leave>", lambda e, frame=file_frame: frame.configure(fg_color=["#D9D9D9", "#292929"]))
                widget.bind("<Button-1>", lambda e, filename=filename: ProjectTopLevel(self, f"{self.languages_folder.folder_path}/{language}/{filename}", filename))
        