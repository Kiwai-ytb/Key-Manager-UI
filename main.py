import customtkinter as ctk, sys, os
from src.activate_key import activate_key_tab
from src.verify_key import verify_key_tab
from src.create_key import create_key_tab
from src.delete_key import delete_key_tab
from src.key_infos import key_infos_tab

def resource_path(relative_path: str) -> str:
    if hasattr(sys, "frozen"):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(__file__)
    return os.path.join(base_path, relative_path)

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Basic parameters
        self.geometry("800x750")
        self.title("Kiwai's Key Manager")

        self.icon_path = resource_path(r"Alya.ico")
        self.iconbitmap(self.icon_path)

        ctk.set_appearance_mode("system")
        ctk.set_default_color_theme("dark-blue")

        self.title_font = ctk.CTkFont(family="Segoe UI Bold", size=30)
        self.main_font = ctk.CTkFont(family="Segoe UI", size=15)
        self.log_font = ctk.CTkFont(family="Segoe UI Italic", size=20)

        # Frames
        self.title_frame = ctk.CTkFrame(self)
        self.title_frame.pack(padx=20, pady=20, fill="both")

        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(padx=20, pady=20, fill="both", expand=True)

        self.ty_frame = ctk.CTkFrame(self)
        self.ty_frame.pack(padx=20, pady=20, fill="both")

        self.title = ctk.CTkLabel(self.title_frame, text="Welcome to Kiwai's Key Manager", font=self.title_font)
        self.title.pack(padx=10, pady=10)

        self.tabview = ctk.CTkTabview(self.title_frame, height=60, width=500, fg_color="transparent", command=self.on_tab_change)
        self.tabview.pack(fill="both")
        self.tab_verify_key = self.tabview.add("Verify Key")
        self.tab_activate_key = self.tabview.add("Activate Key")
        self.tab_create_key = self.tabview.add("Create Key")
        self.tab_delete_key = self.tabview.add("Delete Key")
        self.tab_key_info = self.tabview.add("Key Info")
        self.tabview.set("Verify Key")

        self.ty_msg = ctk.CTkLabel(self.ty_frame, text="Made by Kiwai with <3", font=self.main_font)
        self.ty_msg.pack(padx=10, pady=10)
        
        verify_key_tab(self)
        
        return
    
    def build_delete_key_tab(self):
        print("\nDelete Key tab opened!")
        return
    
    def build_key_info_tab(self):
        print("\nKey Info tab opened!")
        return
    
    def on_tab_change(self):
        self.clear_main_frame()

        tab_name = self.tabview.get()
        if tab_name == "Verify Key":
            verify_key_tab(self)
        elif tab_name == "Activate Key":
            activate_key_tab(self)
        elif tab_name == "Create Key":
            create_key_tab(self)
        elif tab_name == "Delete Key":
            delete_key_tab(self)
        elif tab_name == "Key Info":
            key_infos_tab(self)

    def clear_main_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

app = App()
app.mainloop()