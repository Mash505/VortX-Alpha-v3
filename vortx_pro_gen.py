#!/usr/bin/env python3
import json
import base64
import time
import os
import hashlib
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

def generate_pro_license():
    print("\n" + "="*40)
    print("   VORTX ALPHA v3.0 ENTERPRISE GEN")
    print("      MA Traders Research Lab")
    print("="*40)
    
    # 1. Customer Input
    customer = input("[+] Customer Name (e.g., Reliance): ").strip()
    machine_id = input("[+] Customer Machine ID: ").strip()
    days = int(input("[+] License Duration (Days): "))
    
    if not customer or not machine_id:
        print("\n[!] ERROR: Customer Name aur Machine ID zaroori hai!")
        return

    # 2. Key Derivation (Master Security Logic)
    # Yeh wahi logic hai jo hamare VORTX main code ko unlock karega
    salt = b"VORTX_MA_TRADERS_2026_ENTERPRISE"
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA512(),
        length=32,
        salt=salt + machine_id.encode()[:16],
        iterations=200000
    )
    encryption_key = base64.urlsafe_b64encode(kdf.derive(machine_id.encode()))
    fernet = Fernet(encryption_key)

    # 3. License Payload
    expiry = int(time.time()) + (days * 86400)
    license_data = {
        "customer": customer,
        "machine_id": machine_id,
        "expiry": expiry,
        "domain": "matraders.com",
        "version": "3.0.1-GOLD",
        "generated_at": time.strftime('%Y-%m-%d %H:%M:%S')
    }

    # 4. Encryption & Encoding
    try:
        encrypted_payload = fernet.encrypt(json.dumps(license_data).encode())
        final_key = base64.b64encode(encrypted_payload).decode()

        # 5. Save to .lic file
        filename = f"{customer.replace(' ', '_')}_vortx.lic"
        with open(filename, "w") as f:
            f.write(final_key)
        
        print("\n" + "—"*40)
        print(f"✅ SUCCESS: License File Generated!")
        print(f"📂 File Name: {filename}")
        print(f"⏳ Expiry: {time.ctime(expiry)}")
        print("—"*40)
        print("\n[INFO] Yeh file client ko bhejein aur unhe")
        print("VortX directory mein paste karne ko kahein.")
        
    except Exception as e:
        print(f"\n[!] ERROR: License generate nahi ho paya: {e}")

if __name__ == "__main__":
    generate_pro_license()
