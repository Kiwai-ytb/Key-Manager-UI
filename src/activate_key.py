import customtkinter as ctk
from api_call import activate_key
from config.utilities import get_uuid

def activate_key_tab(app):
        print("\nActivate Key tab opened!")

        key_frame = ctk.CTkFrame(app.main_frame)
        key_title = ctk.CTkLabel(key_frame, text="Please enter your Key to Activate it:", font=app.main_font)
        app.key_input = ctk.CTkEntry(key_frame, placeholder_text="Put your Key here", font=app.main_font, width=450)
        activate_button = ctk.CTkButton(app.main_frame, text="Activate it!", command=lambda: on_activate(app), font=app.main_font)

        app.message_frame = ctk.CTkFrame(app.main_frame, fg_color="transparent")
        app.success_msg = None
        app.fail_msg = None
        app.no_key_msg = None

        key_frame.pack(padx=20, pady=10, fill="both")
        key_title.pack(side="left", padx=10, pady=10)
        app.key_input.pack(side="right", padx=10, pady=10)
        activate_button.pack(padx=20, pady=0, fill="both")
        app.message_frame.pack(padx=20, pady=10, fill="both", expand=True)

def on_activate(app):
    if app.success_msg is not None:
        app.success_msg.destroy()
        app.success_msg = None  
    if app.fail_msg is not None:
        app.fail_msg.destroy()
        app.fail_msg = None
    if app.no_key_msg is not None:
        app.no_key_msg.destroy()
        app.no_key_msg = None
    license_key = app.key_input.get().strip()
    if not license_key:
        print(f"No license key were entered!")
        app.no_key_msg = ctk.CTkLabel(app.message_frame, text="Please enter a Key", text_color="red", font=app.main_font)
        app.no_key_msg.pack(padx=10, pady=10)
        return
    
    len_k = len(license_key)
    print(f"license_key fetched: {license_key}")

    machine_udid = get_uuid()
    print(f"machine_udid fetched: {machine_udid}")

    result = activate_key(license_key, machine_udid)

    if result.get("success"):
        app.success_msg = ctk.CTkLabel(app.message_frame, text=f"Key `{license_key}` successfuly activated!", text_color="green", font=app.main_font)
        app.success_msg.pack(padx=10, pady=10)
        app.key_input.delete(first_index=0, last_index=len_k)
        print("Successfuly activated the key!")
    elif result.get("status") == 422:
        app.fail_msg = ctk.CTkLabel(app.message_frame, text="Key is already activate!", text_color="red", font=app.main_font)
        app.fail_msg.pack(padx=10, pady=10)
        print(f"Couln't activate the key! (already activated)")
    elif result.get("error") == "NOT_FOUND":
        app.fail_msg = ctk.CTkLabel(app.message_frame, text="Unvalid Key!", text_color="red", font=app.main_font)
        app.fail_msg.pack(padx=10, pady=10)
        print(f"Couln't activate the key! (unvalid key)")
    else:
        app.fail_msg = ctk.CTkLabel(app.message_frame, text=f"Key `{license_key}` couln't be activated!\nError: {result.get("error")}", text_color="red", font=app.main_font)
        app.fail_msg.pack(padx=10, pady=10)
        print(f"Couln't activate the key! ({result.get("error")})")