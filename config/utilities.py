import os, subprocess, sys

def resource_path(relative_path: str) -> str:
    if hasattr(sys, "frozen"):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(__file__)
    return os.path.join(base_path, relative_path)

def get_uuid():
    try:
        lines = [l.strip() for l in subprocess.check_output("wmic csproduct get uuid", shell=True).decode().splitlines() if l.strip()]
        if len(lines) >= 2: 
            return lines[1]
        return "Not Found"
    except Exception:
        return "Not Found"