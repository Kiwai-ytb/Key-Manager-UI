import customtkinter as ctk
from api_call import hwid_reset_key

def hwid_reset_key_tab(app):
        print("\nHWID Reset Key tab opened!")

        key_frame = ctk.CTkFrame(app.main_frame)
        key_title = ctk.CTkLabel(key_frame, text="Please enter your Key to HWID Reset it:", font=app.main_font)
        app.key_input = ctk.CTkEntry(key_frame, placeholder_text="Put your Key here", font=app.main_font, width=450)
        activate_button = ctk.CTkButton(app.main_frame, text="Reset it!", command=lambda: on_reset(app), font=app.main_font)

        app.message_frame = ctk.CTkFrame(app.main_frame, fg_color="transparent")
        app.success_msg = None
        app.fail_msg = None
        app.no_key_msg = None

        key_frame.pack(padx=20, pady=10, fill="both")
        key_title.pack(side="left", padx=10, pady=10)
        app.key_input.pack(side="right", padx=10, pady=10)
        activate_button.pack(padx=20, pady=0, fill="both")
        app.message_frame.pack(padx=20, pady=10, fill="both", expand=True)

def on_reset(app):
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

    result = hwid_reset_key(license_key)
    custom_code = result.get("custom_code")

    if result.get("success") == True:
        app.success_msg = ctk.CTkLabel(app.message_frame, text=f"Key `{license_key}` successfully reseted!", text_color="green", font=app.log_font)
        app.success_msg.pack(padx=10, pady=10)
        app.key_input.delete(first_index=0, last_index=len_k)
        print("Successfuly reseted the key!")
    elif custom_code == "INVALID":
        app.fail_msg = ctk.CTkLabel(app.message_frame, text=f"Key `{license_key}` is invalid!", text_color="red", font=app.log_font)
        app.fail_msg.pack(padx=10, pady=10)
        print(f"Couln't reset the key! (invalid key)")
    elif custom_code == "NO_MACHINE":
        app.fail_msg = ctk.CTkLabel(app.message_frame, text=f"Key `{license_key}` is not associated with any machine!", text_color="red", font=app.log_font)
        app.fail_msg.pack(padx=10, pady=10)
        print(f"Couln't reset the key! (no_machine)")
    else:
        app.fail_msg = ctk.CTkLabel(app.message_frame, text=f"Key `{license_key}` couln't be verified!\nError: {result.get("errors")}", text_color="red", font=app.log_font)
        app.fail_msg.pack(padx=10, pady=10)
        print(f"Couln't reset the key! ({result.get("errors")})")