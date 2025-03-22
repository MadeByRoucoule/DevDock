from customtkinter import *
from PIL import Image
from scripts import *

class SettingsPage(CTkFrame):
    def __init__(self, master, pages_script, fg_color="transparent"):
        # Initialize SettingsPage
        super().__init__(master, fg_color=fg_color)

        # Load settings
        self.settings_script = SettingsScript()
        self.settings = self.settings_script.get_settings()

        # Apply appearance settings
        set_appearance_mode(self.settings_script.get_setting_value("Apparence.Theme").lower())
        theme_path = f"src/json/themes/{self.settings_script.get_setting_value('Apparence.Color')}.json"
        set_default_color_theme(theme_path)

        # Store references
        self.pages_script = pages_script

        # Setup UI
        self.setup_frames()
        self.initialize_left_panel()
        self.update_middle_panel(list(self.settings.keys())[0])

    def setup_frames(self):
        # Configure grid layout
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Left panel for settings categories
        self.left_panel = CTkFrame(self, width=250)
        self.left_panel.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.left_panel.grid_propagate(False)
        self.left_panel.grid_columnconfigure(0, weight=1)
        self.left_panel.grid_rowconfigure(1, weight=1)

        # Middle panel for settings content
        self.middle_panel = CTkFrame(self)
        self.middle_panel.grid(row=0, column=1, sticky="nsew", padx=(0, 5), pady=5)
        self.middle_panel.grid_columnconfigure(0, weight=1)

    def initialize_left_panel(self):
        # Get colors from theme
        bg_color = self._apply_appearance_mode(ThemeManager.theme["CTkFrame"]["top_fg_color"])
        hover_color = self._apply_appearance_mode(ThemeManager.theme["CTkFrame"]["border_color"])

        # Settings label
        self.left_label = CTkLabel(
            self.left_panel,
            text="Settings",
            font=("Arial", 18, "bold"),
            anchor="w"
        )
        self.left_label.grid(row=0, column=0, sticky="ew", padx=15, pady=15)

        # Frame for settings list
        self.left_listbox = CTkFrame(self.left_panel, fg_color="transparent")
        self.left_listbox.grid(row=1, column=0, sticky="nsew")

        # Loop through settings tabs
        for tab in self.settings.keys():
            tab_frame = CTkFrame(self.left_listbox, fg_color=bg_color)
            tab_frame.pack(fill="x", padx=15, pady=(0, 10))
            tab_name = CTkLabel(
                tab_frame,
                text=tab,
                font=("Roboto", 12),
                text_color=["black", "white"],
                anchor='w'
            )
            tab_name.grid(row=0, column=1, sticky='nsew', padx=10, pady=5)

            # Bind events for hover effect and tab selection
            for widget in [tab_frame, tab_name]:
                widget.bind("<Enter>", lambda e, frame=tab_frame: frame.configure(fg_color=hover_color))
                widget.bind("<Leave>", lambda e, frame=tab_frame: frame.configure(fg_color=bg_color))
                widget.bind("<Button-1>", lambda e, t=tab: self.update_middle_panel(t))

        # Done button
        self.left_done_img = CTkImage(
            Image.open("src/assets/done.png").resize((25, 25)),
            size=(25, 25)
        )
        self.left_done_btn = CTkButton(
            self.left_panel,
            text='Done',
            image=self.left_done_img,
            compound='left',
            command=self.apply_changes
        )
        self.left_done_btn.grid(row=2, column=0, sticky='ew', padx=15, pady=15)

    def update_middle_panel(self, tab):
        # Reset text color and font for all tab labels in the left panel
        for widget in self.left_listbox.winfo_children():
            for w in widget.winfo_children():
                try:
                    w.configure(text_color=["black", "white"], font=("Roboto", 12))
                except Exception:
                    pass
                if w.cget("text") == tab:
                    try:
                        w.configure(
                            text_color=self._apply_appearance_mode(ThemeManager.theme["CTkButton"]["fg_color"]),
                            font=("Roboto", 12, 'bold')
                        )
                    except Exception:
                        pass

        # Clear existing widgets in the middle panel
        for widget in self.middle_panel.winfo_children():
            widget.destroy()

        # Create header and settings list
        self.create_middle_header(tab)
        separator = CTkFrame(self.middle_panel, height=2, fg_color=["gray65", "gray25"])
        separator.grid(row=1, column=0, sticky="ew", padx=15, pady=(0, 15))
        self.middle_listbox = CTkScrollableFrame(self.middle_panel, fg_color="transparent")
        self.middle_listbox.grid(row=2, column=0, sticky="nsew", padx=0, pady=(0, 15))

        # Add settings to the middle panel
        for setting in self.settings[tab]:
            setting_frame = CTkFrame(
                self.middle_listbox,
                fg_color=self._apply_appearance_mode(ThemeManager.theme["CTkFrame"]["top_fg_color"])
            )
            setting_frame.pack(fill="x", padx=15, pady=(0, 10))
            setting_name = CTkLabel(setting_frame, text=setting, font=("Roboto", 12))
            setting_name.pack(side="left", padx=10, pady=10)

            # Handle different setting types
            if isinstance(self.settings[tab][setting], dict) and set(self.settings[tab][setting].keys()) == {"state", "from", "to"}:
                # Slider setting
                slider_value_label = CTkLabel(
                    setting_frame,
                    text=str(self.settings[tab][setting]["state"])
                )
                slider_value_label.pack(side='right', padx=10, pady=10)
                slider = CTkSlider(
                    setting_frame,
                    from_=self.settings[tab][setting]["from"],
                    to=self.settings[tab][setting]["to"],
                    number_of_steps=int(self.settings[tab][setting]["to"] - self.settings[tab][setting]["from"])
                )
                slider.set(self.settings[tab][setting]["state"])
                slider.pack(side='right', padx=(10, 0), pady=10)
                slider.configure(command=lambda value, tab=tab, setting=setting, label=slider_value_label: self.slider_callback(value, tab, setting, label))
            elif isinstance(self.settings[tab][setting], dict):
                # Option menu setting
                optionmenu = CTkOptionMenu(
                    setting_frame,
                    values=list(self.settings[tab][setting].keys()),
                    command=lambda choice, tab=tab, setting=setting: self.update_setting(tab, setting, choice)
                )
                active_option = None
                for opt, val in self.settings[tab][setting].items():
                    if isinstance(val, dict) and "state" in val and val["state"] == 1:
                        active_option = opt
                        break
                    elif val == 1:
                        active_option = opt
                        break
                if active_option is None:
                    active_option = list(self.settings[tab][setting].keys())[0]
                optionmenu.set(active_option)
                optionmenu.pack(side='right', padx=10, pady=10)
            elif isinstance(self.settings[tab][setting], str):
                # Entry setting
                entry = CTkEntry(
                    setting_frame,
                    placeholder_text=self.settings[tab][setting]
                )
                entry.pack(side='right', padx=10, pady=10)
                entry.bind("<Return>", lambda e, tab=tab, setting=setting, widget=entry: self.update_setting(tab, setting, widget.get()))
                entry.bind("<FocusOut>", lambda e, tab=tab, setting=setting, widget=entry: self.update_setting(tab, setting, widget.get()))

    def create_middle_header(self, tab):
        # Frame for header content
        self.middle_title_frame = CTkFrame(self.middle_panel, fg_color="transparent")
        self.middle_title_frame.grid(row=0, column=0, sticky="ew", padx=15, pady=15)
        self.middle_title_frame.grid_columnconfigure(0, weight=0)
        self.middle_title_frame.grid_columnconfigure(1, weight=1)

        # Tab title label
        self.middle_title_label = CTkLabel(
            self.middle_title_frame,
            text=tab,
            font=("Arial", 18, "bold"),
            anchor="w"
        )
        self.middle_title_label.grid(row=0, column=1, sticky="ew")

    def slider_callback(self, value, tab, setting, label):
        # Update slider value label
        rounded_value = round(value)
        label.configure(text=str(rounded_value))
        self.update_setting(tab, setting, rounded_value)

    def update_setting(self, tab, setting, new_value):
        # Update setting value in the settings dictionary
        if isinstance(self.settings[tab][setting], dict):
            if set(self.settings[tab][setting].keys()) == {"state", "from", "to"}:
                self.settings[tab][setting]["state"] = new_value
            elif new_value in self.settings[tab][setting]:
                for opt in self.settings[tab][setting]:
                    if isinstance(self.settings[tab][setting][opt], dict) and "state" in self.settings[tab][setting][opt]:
                        self.settings[tab][setting][opt]["state"] = 1 if opt == new_value else 0
                    else:
                        self.settings[tab][setting][opt] = 1 if opt == new_value else 0
            else:
                self.settings[tab][setting] = new_value
        else:
            self.settings[tab][setting] = new_value

    def apply_changes(self):
        # Save settings and return to home page
        from pages.homepage import HomePage
        self.settings_script.settings = self.settings
        self.settings_script.save_settings()
        self.pages_script.change_page(HomePage(self.master, self.pages_script))
