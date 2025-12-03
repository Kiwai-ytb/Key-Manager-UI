import customtkinter as ctk
from api_call import delete_key, verify_key

def delete_key_tab(app):
        print("\nDelete Key tab opened!")

        key_frame = ctk.CTkFrame(app.main_frame)
        key_title = ctk.CTkLabel(key_frame, text="Please enter your Key to Delete it:", font=app.main_font)
        app.key_input = ctk.CTkEntry(key_frame, placeholder_text="Put your Key here", font=app.main_font, width=450)
        activate_button = ctk.CTkButton(app.main_frame, text="Delete it!", command=lambda: on_delete(app), font=app.main_font)

        app.message_frame = ctk.CTkFrame(app.main_frame, fg_color="transparent")
        app.success_msg = None
        app.fail_msg = None
        app.no_key_msg = None

        key_frame.pack(padx=20, pady=10, fill="both")
        key_title.pack(side="left", padx=10, pady=10)
        app.key_input.pack(side="right", padx=10, pady=10)
        activate_button.pack(padx=20, pady=0, fill="both")
        app.message_frame.pack(padx=20, pady=10, fill="both", expand=True)

def on_delete(app):
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

    verify_result = verify_key(license_key)
    data = verify_result.get("data")
    meta = verify_result.get("meta")

    if verify_result.get("valid") == True and data != None:
        license_id = data["id"]
        result = delete_key(license_id)
        if result:
            app.success_msg = ctk.CTkLabel(app.message_frame, text=f"Key `{license_key}` is deleted!", text_color="green", font=app.log_font)
            app.success_msg.pack(padx=10, pady=10)
            app.key_input.delete(first_index=0, last_index=len_k)
            print("Successfuly deleted the key!")
    elif meta["code"] == "NOT_FOUND":
        app.fail_msg = ctk.CTkLabel(app.message_frame, text=f"Key `{license_key}` is unvalid!", text_color="red", font=app.log_font)
        app.fail_msg.pack(padx=10, pady=10)
        print(f"Couln't delete the key! (unvalid key)")
    else:
        app.fail_msg = ctk.CTkLabel(app.message_frame, text=f"Key `{license_key}` couln't be deleted!\nError: {result}", text_color="red", font=app.log_font)
        app.fail_msg.pack(padx=10, pady=10)
        print(f"Couln't delete the key! ({result})")