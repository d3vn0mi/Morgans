import random
import argparse
import os
import glob
import zipfile
from io import BytesIO
import re
import string
import shutil
import http.server
import socketserver
import logging
from logger_setup import setup_logger  # Import the setup_logger function


def serve_directory(port=8889):
    """
    Serve the current directory over HTTP on the specified port.
    """
    logger = logging.getLogger('logger')
    Handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", port), Handler) as httpd:
        logger.info(f"Serving the current directory at http://localhost:{port}")
        httpd.serve_forever()

def zip_dir(dir_path, output_zip):
    """
    Zip the contents of dir_path into a zip file named output_zip.
    """
    
    logger = logging.getLogger('logger')

    with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(dir_path):
            for file in files:
                zipf.write(os.path.join(root, file), 
                           os.path.relpath(os.path.join(root, file), 
                                      os.path.join(dir_path, '..')))
    logger.info(f"Directory '{dir_path}' has been zipped into '{output_zip}'")


def move_benign_files(source_dir, destination_dir):
    """
    Move files ending with '_benign.odt' from source_dir to destination_dir.
    """
    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)

    for filename in os.listdir(source_dir):
        if filename.endswith('_benign.odt'):
            source_path = os.path.join(source_dir, filename)
            new_filename = remove_suffix(filename)
            destination_path = os.path.join(destination_dir, new_filename)
            shutil.copy(source_path, destination_path)
            print(f"Moved: {filename} and renamed it to {new_filename}")


def remove_suffix(filename):
    pattern = r'(_malicious|_benign)(?=\.odt$)'
    new_filename = re.sub(pattern, '', filename)
    return new_filename

# -------- obfuscation functions --------

def generate_random_string(length=10):
    """Generate a random string of fixed length."""
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for _ in range(length))

def obfuscate_starbasic_strings(code, patterns):
    """Obfuscate specified patterns in the given StarBasic code."""
    logger = logging.getLogger('logger')

    obfuscation_map = {pattern: generate_random_string() for pattern in patterns}
    for pattern, obfuscated in obfuscation_map.items():
        logger.info(f"Obfuscating string -> {pattern}")
        code = re.sub(r'\b{}\b'.format(re.escape(pattern)), obfuscated, code)
    return code

def obfuscate_starbasic_vars(code):
    """
    Obfuscate function names, subroutine names, and variable names in the given StarBasic code.
    This version ensures that keywords and structure are not modified.
    """
    logger = logging.getLogger('logger')
    logger.info("Obfuscating all declared variables...")
    var_pattern = re.compile(r'\bDim\s+(\w+)\s+As\s+\w+', re.IGNORECASE)
    
    var_names = set(match.group(1) for match in var_pattern.finditer(code))
    obfuscation_map = {var_name: generate_random_string() for var_name in var_names}
    
    obfuscated_script = code
    for var_name, obfuscated_name in obfuscation_map.items():
        logger.debug(f"Var: {var_name} => {obfuscated_name}")
        obfuscated_script = re.sub(r'\b{}\b'.format(re.escape(var_name)), obfuscated_name, obfuscated_script)

    return obfuscated_script

# -------- encryption functions --------
def xor_encrypt(data, key):
    """Encrypts data using XOR encryption with the given key."""
    return bytes([b ^ key for b in data])

def load_patterns(strings_file):
    """Load patterns from a file."""
    with open(strings_file, 'r') as file:
        return [line.strip() for line in file.readlines()]

def create_dir(original_dir_path, dir_name):
    """Create a new directory for the encrypted files if it doesn't already exist."""
    encrypted_dir_path = f"{original_dir_path}_{dir_name}"
    if not os.path.exists(encrypted_dir_path):
        os.makedirs(encrypted_dir_path)
    return encrypted_dir_path
    
def process_odt_files(dir_path, strings_to_encrypt,strings_to_obfuscate, obfuscate_vars, macro_dir="Basic/Standard", macro_file="Module1.xml"):
    logger = logging.getLogger('logger')
    odt_files = glob.glob(os.path.join(dir_path, "*.odt"))
    encrypted_dir_path = create_dir(dir_path,"encrypted")
    keys_dir_path = create_dir(dir_path, "keys")
    i = 0 
    for odt_path in odt_files:
        xor_key = random.randint(1, 255) 
        if odt_path.endswith('_benign.odt'):  # Skip files ending with '_benign.odt'
            continue
        
        memory_file = BytesIO()
        with zipfile.ZipFile(odt_path, 'r') as zip_ref, zipfile.ZipFile(memory_file, 'w') as new_zip:
            for item in zip_ref.infolist():
                if not item.filename.endswith(f"{macro_dir}/{macro_file}"):
                    new_zip.writestr(item, zip_ref.read(item.filename))
                else:
                    i += 1
                    content = zip_ref.read(item.filename).decode()
                    logger.info(f"{i}:{item.filename}")
                    encrypted_content = encrypt_starbasic_strings(content, strings_to_encrypt, xor_key)
                    logger.debug("---------------- Encrypted content ---------------------")
                    logger.debug(encrypted_content)
                    logger.debug("---------------- End of Encrypted content --------------")
                    if strings_to_obfuscate:
                        encrypted_content = obfuscate_starbasic_strings(encrypted_content,strings_to_obfuscate)
                    if obfuscate_vars:
                        encrypted_content = obfuscate_starbasic_vars(encrypted_content)
                    new_zip.writestr(item, encrypted_content.encode())

        logger.info(odt_path)
        odt_path = remove_suffix(odt_path)
        encrypted_odt_path = os.path.join(encrypted_dir_path, os.path.basename(odt_path))
        with open(encrypted_odt_path, 'wb') as f_out:
            f_out.write(memory_file.getvalue())
        
        key_filename = f"{os.path.splitext(os.path.basename(odt_path))[0]}_key.txt"
        key_file_path = os.path.join(keys_dir_path, key_filename)
        with open(key_file_path, 'w') as key_file:
            key_file.write(str(xor_key))

    print("Cleaning up ....and packaging....")
    logger.info(f"Odt file path {dir_path} | Encrypted directory path {encrypted_dir_path}")
    move_benign_files(source_dir=dir_path, destination_dir=encrypted_dir_path)
    zip_dir(dir_path = encrypted_dir_path, output_zip="for_student.zip")


def encrypt_starbasic_strings(content, patterns, xor_key):
    """Encrypt specified patterns in the content and replace them, considering encoded quotes."""
    logger = logging.getLogger('logger')

    for pattern in patterns:
        logger.debug(f"Prior replacing -> {pattern}")
        encoded_pattern = pattern.replace('"', '&quot;').replace("'", "&apos;")
        logger.debug(f"After replacing -> {encoded_pattern}")
        if encoded_pattern in content:
            logger.debug(f"Before cutting first and last element -> {pattern}")
            clean_pattern = pattern[1:-1]
            logger.debug(f"After cutting first and last element -> {clean_pattern}")
            encrypted_bytes = xor_encrypt(clean_pattern.encode(), xor_key)
            encrypted_string = encrypted_bytes.hex()
            formated_encrypted_string = f'XORDecrypt("{encrypted_string}", xk)'
            content = content.replace(encoded_pattern, formated_encrypted_string)
    return content


def main():
    logger = setup_logger()
    parser = argparse.ArgumentParser(description="Encrypt specified patterns in file content.")
    parser.add_argument("--dir", "-d", required=True, help="Directory containing .odt files.")
    parser.add_argument("--macro-dir","-md", default="Basic/Standard", help="Directory path of the macro within the .odt file.")
    parser.add_argument("--macro-file","-mf", default="Module1.xml", help="File name of the macro to be encrypted.")
    parser.add_argument("--obfuscate","-obf", default=False, action='store_true', help="Enable obfuscation")
    parser.add_argument("--encrypt-strings", "-es",default="enc_strings.txt", help="Patterns for encryption, as a file path or a comma-separated list.")
    parser.add_argument("--obfuscate-strings", "-os", default="obf_strings.txt", help="Patterns for obfuscation, as a file path or a comma-separated list.")
    parser.add_argument("--obfuscate-vars", "-ov", default=False, action='store_true', help="Enable obfuscation of variable names.")
    parser.add_argument("--serve", "-s", default=False, action='store_true', help="Serve the processed directory over HTTP after processing.")
    parser.add_argument("--port", "-p", type=int, default=8889, help="Port to serve on when --serve is enabled.")

    args = parser.parse_args()

    strings_to_obfuscate = []
    strings_to_encrypt = []
    if args.encrypt_strings:
        logger.info("Encrypting user supplied strings....")
        strings_to_encrypt = load_patterns(args.encrypt_strings)
        logger.debug(f"Strings to encrypt -> {strings_to_encrypt}")
    if args.obfuscate:
        if args.obfuscate_strings:
            strings_to_obfuscate = load_patterns(args.obfuscate_strings)
            logger.info("Obfuscating user supplied strings....")
            logger.debug(f"Strings to obfuscate -> {strings_to_obfuscate}")

    process_odt_files(args.dir,
                      strings_to_encrypt,
                      strings_to_obfuscate,
                      obfuscate_vars=args.obfuscate_vars,
                      macro_dir= args.macro_dir,
                      macro_file=args.macro_file)

    if args.serve:
        serve_directory(port=args.port)  # Blocking; serves until Ctrl+C

if __name__ == "__main__":
    main()
