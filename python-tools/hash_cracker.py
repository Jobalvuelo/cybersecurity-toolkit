import hashlib
import sys
from datetime import datetime

def crack_md5(target_hash, worldlist_path):
    print(f"\n[*] Target hash: {target_hash}")
    print(f"[*] Wordlist: {worldlist_path}")
    print(f"[*] Started at: {datetime.now().strftime('%H:%M:%S')}")
    print("-" * 40)
    
    try:
        with open(worldlist_path, "r", encoding="latin-1") as f:
            words = f.readlines()
            
        print(f"[*] Loaded {len(words)} passwords to try...")
        
        for i, word in enumerate(words):
            word = word.strip()
            word_hash = hashlib.md5(word.encode()).hexdigest()
            
            if word_hash == target_hash:
                print(f"\n[+] PASSWORD FOUND: {word}")
                print(f"[+] Cracked in {i + 1} attempts")
                print(f"[+] Finished at: {datetime.now().strftime('%H:%M:%S')}")
                return word
            
        print("\n[-] Password not found in wordlist.")
        return None

    except FileNotFoundError:
        print(f"[ERROR] Wordlist not found: {worldlist_path}")
        return None
    
def crack_sha256(target_hash, wordlist_path):
    print(f"\n[*] Target hash (SHA256): {target_hash}")
    print(f"[*] Wordlist: {wordlist_path}")
    print("-" * 40)
    
    try:
        with open(wordlist_path, "r", encoding="latin-1") as f:
            words = f.readlines()
            
        for i, word in enumerate(words):
            word = word.strip()
            word_hash = hashlib.sha256(word.encode()).hexdigest()
            
            if word_hash == target_hash:
                print(f"\n^[+] PASSWORD FOUND: {word}")
                print(f"[+] Cracked in {i + 1} attempts")
                return word
        
        print("\n[-] Password not found in wordlist.")
        return None
    
    except FileNotFoundError:
        print(f"[ERROR] Wordlist not found: {wordlist_path}")
        return None

def main():
    print("=" * 50)
    print("    HASH CRACKER v1.0 - by Ayoub")
    print("=" * 50)
    
    print("\n[1] Crack MD5 hash")
    print("[2] Crack SHA256 hash")
    print("[3] Generate hash from text")
    
    choice = input("\nSelect option: ")
    
    if choice == "1":
        target = input("Enter MD5 hash: ")
        wordlist = input("Enter wordlist path: ")
        crack_md5(target, wordlist)
        
    elif choice == "2":
        target = input("Enter SHA256 hash: ")
        wordlist = input("Enter wordlist path: ")
        crack_sha256(target, wordlist)
        
    elif choice == "3":
        text = input("Enter text to hash: ")
        print(f"\n MD5: {hashlib.md5(text.encode()).hexdigest()}")
        print(f" SHA256: {hashlib.sha256(text.encode()).hexdigest()}")
        
    else:
        print("[ERROR] Invalid option.")
        
if __name__ == "__main__":
    main()