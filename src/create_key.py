import customtkinter as ctk
from api_call import create_key
from datetime import datetime, timedelta, timezone

def parse_license_time(input_str: str) -> str | None:
    if input_str is None:
        return None
        
    input_str = input_str.upper()
    now = datetime.now(timezone.utc)

    if input_str == "LIFETIME":
        return None

    unit = input_str[-1]
    try:
        value = int(input_str[:-1])
    except ValueError:
        return None

    if unit == "D":
        delta = timedelta(days=value)
    elif unit == "W":
        delta = timedelta(weeks=value)
    elif unit == "M":
        delta = timedelta(days=30 * value)
    elif unit == "Y":
        delta = timedelta(days=365 * value)
    else:
        return None

    expiry_date = now + delta
    return expiry_date.isoformat() + "Z"

def create_key_tab(app):
        print("\nActivate Key tab opened!")

        name_frame = ctk.CTkFrame(app.main_frame)
        name_title = ctk.CTkLabel(name_frame, text="Please enter the name of the Key (user's name):", font=app.main_font)
        app.name_input = ctk.CTkEntry(name_frame, placeholder_text="Put the name here", font=app.main_font, width=450)

        time_frame = ctk.CTkFrame(app.main_frame)
        time_title = ctk.CTkLabel(time_frame, text="Please enter the time of the Key:", font=app.main_font)
        app.time_input = ctk.CTkEntry(time_frame, placeholder_text="Put the time here (1D, 1W, 1M, 1Y / Default = LIFETIME)", font=app.main_font, width=450)

        custom_key_frame = ctk.CTkFrame(app.main_frame)
        custom_key_title = ctk.CTkLabel(custom_key_frame, text="Please enter a custom Key (6 char min & optionnal):", font=app.main_font)
        app.custom_key_input = ctk.CTkEntry(custom_key_frame, placeholder_text="Put the custom Key here", font=app.main_font, width=450)

        activate_button = ctk.CTkButton(app.main_frame, text="Create it!", command=lambda: on_create(app), font=app.main_font)

        app.message_frame = ctk.CTkFrame(app.main_frame, fg_color="transparent")
        app.info_msg = None
        app.success_msg = None
        app.fail_msg = None
        app.no_key_msg = None

        name_frame.pack(padx=20, pady=10, fill="both")
        name_title.pack(side="left", padx=10, pady=10)
        app.name_input.pack(side="right", padx=10, pady=10)

        time_frame.pack(padx=20, pady=0, fill="both")
        time_title.pack(side="left", padx=10, pady=10)
        app.time_input.pack(side="right", padx=10, pady=10)

        custom_key_frame.pack(padx=20, pady=10, fill="both")
        custom_key_title.pack(side="left", padx=10, pady=10)
        app.custom_key_input.pack(side="right", padx=10, pady=10)

        activate_button.pack(padx=20, pady=0, fill="both")
        app.message_frame.pack(padx=20, pady=10, fill="both", expand=True)

def on_create(app):
    if app.success_msg is not None:
        app.success_msg.destroy()
        app.success_msg = None
    if app.info_msg is not None:
        app.info_msg.destroy()
        app.info_msg = None
    if app.fail_msg is not None:
        app.fail_msg.destroy()
        app.fail_msg = None
    if app.no_key_msg is not None:
        app.no_key_msg.destroy()
        app.no_key_msg = None

    license_name = app.name_input.get().strip()
    license_time = app.time_input.get().strip()
    custom_license = app.custom_key_input.get().strip()

    if not license_name:
        print(f"No license name were entered!")
        app.no_key_msg = ctk.CTkLabel(app.message_frame, text="Please enter a Key name", text_color="red", font=app.main_font)
        app.no_key_msg.pack(padx=10, pady=10)
        return
    
    len_name = len(license_name)
    print(f"license_name fetched: {license_name}")

    if not license_time:
        license_time = "LIFETIME"
    
    expiry = parse_license_time(license_time)
    len_time = len(license_time)
    print(f"license_time fetched: {license_time}")

    if custom_license:
        len_custom = len(custom_license)
        print(f"custom_license fetched: {custom_license}")

    result = create_key(license_name=license_name, license_time=expiry, license_key=custom_license)
    received_data = result.get("data")
    data = received_data["data"]
    license_key = data["attributes"]["key"]
    expiry = data["attributes"]["expiry"]
    status = data["attributes"]["status"]

    if result.get("success"):
        app.success_msg = ctk.CTkLabel(app.message_frame, text=f"Key `{license_name}` successfuly created!", text_color="green", font=app.log_font)
        app.success_msg.pack(padx=10, pady=10)
        app.info_msg = ctk.CTkLabel(app.message_frame, text=f"Name: {license_name}\nKey: {license_key}\nExpiry: {expiry}\nStatus: {status}", font=app.log_font)
        app.info_msg.pack(padx=10, pady=10, fill="both")
        app.name_input.delete(first_index=0, last_index=len_name)
        if license_time:
            app.time_input.delete(first_index=0, last_index=len_time)
        if custom_license:
            app.custom_key_input.delete(first_index=0, last_index=len_custom)
        print("Successfuly created the key!")
    else:
        app.fail_msg = ctk.CTkLabel(app.message_frame, text=f"Key `{license_key}` couln't be created!\nError: {result.get("error")}", text_color="red", font=app.main_font)
        app.fail_msg.pack(padx=10, pady=10)
        print(f"Couln't create the key! ({result.get("error")})")