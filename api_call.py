import requests, os
from dotenv import load_dotenv

load_dotenv(dotenv_path=r"config\.env")
KEYGEN_TOKEN = os.getenv("KEYGEN_TOKEN")
PRODUCT_ID = os.getenv("KEYGEN_PRODUCT_ID")
ACCOUNT_ID = os.getenv("KEYGEN_ACCOUNT_ID")
POLICY_ID = os.getenv("KEYGEN_POLICY_ID")

def verify_key(license_key: str):
    url = f"https://api.keygen.sh/v1/accounts/{ACCOUNT_ID}/licenses/actions/validate-key"

    headers = {
        "Content-Type": "application/vnd.api+json",
        "Accept": "application/vnd.api+json"
    }
    
    data = {
        "meta": {
            "key": license_key,
            "scope": {
                "policy": POLICY_ID
            }
        }
    }

    try:
        r = requests.post(url, json=data, headers=headers)
        if r.status_code == 200:
            response_data = r.json()
            print(f"Successfully verified Key: {license_key}")
            return {"valid": True,
                    "data": response_data["data"],
                    "meta": response_data["meta"]
                    }
        else:
            error = r.text()
            print(f"Failed to verify Key: {license_key}")
            return {"valid": False,
                    "status": r.status_code,
                    "error": error
                    }
    except Exception as e:
        print(f"Error while verifying the Key: {license_key}: {e}")
        return {"valid": False, "error": str(e)}

def activate_key(license_key: str, machine_udid: str) -> dict:
    validate_data = verify_key(license_key)
    data = validate_data.get("data")
    if data == None:
        meta = validate_data.get("meta")
        return {"success": False, "error": meta["code"], "machine_id": None}

    license_id = data["id"]
    license_name = data["attributes"].get("name", license_key)

    url_machine = f"https://api.keygen.sh/v1/accounts/{ACCOUNT_ID}/machines"
    headers_auth = {
        "Authorization": f"Bearer {KEYGEN_TOKEN}",
        "Content-Type": "application/vnd.api+json",
        "Accept": "application/vnd.api+json"
    }
    data_machine = {
        "data": {
            "type": "machines",
            "attributes": {
                "fingerprint": machine_udid,
                "name": license_name
            },
            "relationships": {
                "license": {
                    "data": {
                        "type": "licenses",
                        "id": license_id
                    }
                }
            }
        }
    }

    try:
        r2 = requests.post(url_machine, json=data_machine, headers=headers_auth)
        resp = r2.json()
        if r2.status_code == 201:
            print(f"Successfuly activated the Key: {license_key}")
            return {
                "success": True,
                "error": None,
                "machine_id": resp["data"]["id"],
                "status": r2.status_code
            }
        else:
            detail = resp.get("errors", [{}])[0].get("detail", "Activation failed")
            print(f"Failed to activate the Key: {license_key}")
            return {
                "success": False,
                "error": f"{detail} (status {r2.status_code})",
                "machine_id": None,
                "status": r2.status_code
            }
    except Exception as e:
        print(f"Error while activating the Key: {license_key}: {e}")
        return {"success": False, "error": str(e), "machine_id": None}

def create_key(license_key: str, license_name: str, license_time: int | None):
    url = f"https://api.keygen.sh/v1/accounts/{ACCOUNT_ID}/licenses"
    headers = {
        "Content-Type": "application/vnd.api+json",
        "Accept": "application/vnd.api+json",
        "Authorization": f"Bearer {KEYGEN_TOKEN}"
    }

    attributes = {
        "name": license_name,
    }

    if license_time:
        attributes["expiry"] = license_time
    if license_key:
        attributes["key"] = license_key

    data = {
        "data": {
            "type": "licenses",
            "attributes": attributes,
            "relationships": {
                "policy": {
                    "data": {
                        "type": "policies",
                        "id": POLICY_ID
                    }
                }
            }
        }
    }

    try:
        r = requests.post(url, json=data, headers=headers)
        if r.status_code == 201:
            key_data = r.json()
            license_key = key_data["data"]["attributes"]["key"]
            print(f"Successfully created Key: {license_key} ({license_name})")
            return {"success": True,
                    "data": key_data,
                    "status_code": r.status_code
                    }
        else:
            error = r.text()
            print(f"Failed to create Key: {license_key} ({license_name}), status: {r.status_code}, error: {error}")
            return error
    except Exception as e:
        print(f"Error while creating Key: {license_key} ({license_name}) - {e}")