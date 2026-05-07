import json, base64, time, os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

def generate_pro_license():
    print("--- VORTX ALPHA ENTERPRISE KEY GENERATOR ---")
    
    # 1. Input Details
    customer = input("Customer Name (e.g. Reliance): ")
    machine_id = input("Enter Customer's Machine ID (from their mobile/PC): ")
    days = int(input("License Duration (Days): "))
    
    # 2. Key Derivation (Wahi Master Salt jo hamare main code mein hai)
    salt = b"VORTX_MA_TRADERS_2026_ENTERPRISE"
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA512(),
        length=32,
        salt=salt + machine_id.encode()[:16],
        iterations=200000
    )
    encryption_key = base64.urlsafe_b64encode(kdf.derive(machine_id.encode()))
    fernet = Fernet(encryption_key)

    # 3. Data Structure
    expiry = int(time.time()) + (days * 86400)
    license_data = {
        "customer": customer,
        "machine_id": machine_id,
        "expiry": expiry,
        "version": "3.0.1-GOLD"
    }

    # 4. Final Encryption
    encrypted_payload = fernet.encrypt(json.dumps(license_data).encode())
    final_key = base64.b64encode(encrypted_payload).decode()

    # 5. Save to File
    filename = f"{customer}_license.lic"
    with open(filename, "w") as f:
        f.write(final_key)
    
    print("\n" + "="*30)
    print(f"✅ SUCCESS: License File Generated!")
    print(f"📂 File: {filename}")
    print(f"⏳ Valid for: {days} Days")
    print("="*30)

if __name__ == "__main__":
    generate_pro_license()
