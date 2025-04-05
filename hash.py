import bcrypt
import sys

def crack_bcrypt_hashes():
    target_hashes = [
        "$2y$10$6j94/mAY3rFtD4.nC9sMzemBOrxRLDsV5Vf.S7sbrcUGyisfvAHIu",
        "$2y$10$4nM8NEmnYevMM6OVfwjFbeMwLHVtbO/azniBNYIIn4fEd47eXraBe"
    ]
    found_passwords = {}

    try:
        with open("rockyou.txt", "r", encoding="latin-1") as file:
            for line_number, line in enumerate(file, 1):
                password = line.strip()
                if not password:
                    continue  # Skip empty lines

                # Bcrypt has a 72-byte limit, so truncate if necessary
                password_bytes = password.encode('utf-8')[:72]

                # Check against remaining target hashes
                for hash_str in list(target_hashes):
                    try:
                        if bcrypt.checkpw(password_bytes, hash_str.encode('utf-8')):
                            print(f"\n[SUCCESS] Hash: {hash_str}\nPassword: {password}")
                            found_passwords[hash_str] = password
                            target_hashes.remove(hash_str)  # Stop checking this hash
                    except Exception as e:
                        print(f"\n[ERROR] Line {line_number}: {str(e)}")
                        continue

                # Exit early if all hashes are cracked
                if not target_hashes:
                    break

                # Print progress
                if line_number % 1000 == 0:
                    print(f"Checked {line_number} passwords...", end='\r', flush=True)

    except FileNotFoundError:
        print("[ERROR] rockyou.txt not found in the current directory.")
        sys.exit(1)

    # Final results
    print("\n\nCracking results:")
    for hash_str, pwd in found_passwords.items():
        print(f"Hash: {hash_str} => Password: {pwd}")
    if target_hashes:
        print("\nFailed to crack these hashes:", ", ".join(target_hashes))

if __name__ == "__main__":
    crack_bcrypt_hashes()
