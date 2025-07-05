from cryptography.fernet import Fernet

# 2. Load your saved key
with open('secret.key', 'rb') as f:
    key = f.read()

cipher = Fernet(key)

# 3. Read your masked CSV
with open('masked_temperature.csv', 'rb') as f:
    data = f.read()

# 4. Encrypt it
encrypted = cipher.encrypt(data)

# 5. Write out the encrypted file
with open('masked_temperature.csv.enc', 'wb') as f:
    f.write(encrypted)

print("Encrypted file saved as masked_temperature.csv.enc")
