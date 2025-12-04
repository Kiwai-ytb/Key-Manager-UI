import subprocess
from datetime import datetime

def get_uuid():
    try:
        lines = [l.strip() for l in subprocess.check_output("wmic csproduct get uuid", shell=True).decode().splitlines() if l.strip()]
        if len(lines) >= 2: 
            return lines[1]
        return "Not Found"
    except Exception:
        return "Not Found"
    
def format_timestamp(timestamp_str: str) -> str:
    try:
        dt = datetime.strptime(timestamp_str, "%Y-%m-%dT%H:%M:%S.%fZ")
        return dt.strftime("%Y-%m-%d: %Hh%M")
    except ValueError:
        try:
            dt = datetime.strptime(timestamp_str, "%Y-%m-%dT%H:%M:%SZ")
            return dt.strftime("%Y-%m-%d: %Hh%M")
        except ValueError as e:
            return f"Invalid format: {e}"