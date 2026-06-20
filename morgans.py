import argparse
import mass_odt_gen  # Importing as a module
import mass_odt_enc_obf  # Importing as a module
from logger_setup import setup_logger  # Import the setup_logger function

def run_mass_odt_gen(args):
    output_folder = mass_odt_gen.find_or_create_output_dir()
    file_list = mass_odt_gen.load_file_names(args.file_list)
    mass_odt_gen.generate_documents(args.num_files, args.percentage_malicious, output_folder, file_list)

def run_mass_odt_enc_obf(args):
    mass_odt_enc_obf.process_odt_files(
        dir_path=args.dir,
        strings_to_encrypt=mass_odt_enc_obf.load_patterns(args.encrypt_strings),
        strings_to_obfuscate=mass_odt_enc_obf.load_patterns(args.obfuscate_strings) if args.obfuscate else [],
        obfuscate_vars=args.obfuscate_vars,
        macro_folder=args.macro_dir,
        macro_file=args.macro_file
    )
    
    
def display_banner():
    banner = """      
    ___  ___ _____ ______  _____   ___   _   _  _____ 
    |  \/  ||  _  || ___ \|  __ \ / _ \ | \ | |/  ___|
    | .  . || | | || |_/ /| |  \// /_\ \|  \| |\ `--. 
    | |\/| || | | ||    / | | __ |  _  || . ` | `--. \ 
    | |  | |\ \_/ /| |\ \ | |_\ \| | | || |\  |/\__/ /
    \_|  |_/ \___/ \_| \_| \____/\_| |_/\_| \_/\____/ 
                                                    
                                                        
    Created by d3vn0mi
    """
    print(banner)


def main():
    logger = setup_logger()  # Initialize the logger

    display_banner()
    parser = argparse.ArgumentParser(description="Morgans - The Core Tool for ODT Document Processing")
    subparsers = parser.add_subparsers(dest='command')

    # Subparser for mass-odt-gen
    parser_gen = subparsers.add_parser('gen', help="Generate a mix of benign and malicious .odt documents.")
    parser_gen.add_argument("num_files", type=int, help="The number of files to generate.")
    parser_gen.add_argument("percentage_malicious", type=float, help="The percentage of files that should be malicious.")
    parser_gen.add_argument("--file-list", "-f", type=str, required=True, help="Path to a text file containing a list of filenames to use.")
    parser_gen.set_defaults(func=run_mass_odt_gen)

    # Subparser for mass-odt-enc-obf
    parser_enc_obf = subparsers.add_parser('encobf', help="Encrypt and obfuscate patterns in .odt files.")
    parser_enc_obf.add_argument("--dir", "-d", required=True, help="Folder containing .odt files.")
    parser_enc_obf.add_argument("--macro-dir", "-md", default="Basic/Standard", help="Folder path of the macro within the .odt file.")
    parser_enc_obf.add_argument("--macro-file", "-mf", default="Module1.xml", help="File name of the macro to be encrypted.")
    parser_enc_obf.add_argument("--obfuscate", "-obf", default=False, action='store_true', help="Enable obfuscation")
    parser_enc_obf.add_argument("--encrypt-strings", "-es", default="enc_strings.txt", help="Patterns for encryption, as a file path or a comma-separated list.")
    parser_enc_obf.add_argument("--obfuscate-strings", "-os", default="obf_strings.txt", help="Patterns for obfuscation, as a file path or a comma-separated list.")
    parser_enc_obf.add_argument("--obfuscate-vars", "-ov", default=False, action='store_true', help="Enable obfuscation of variable names.")
    parser_enc_obf.set_defaults(func=run_mass_odt_enc_obf)

    args = parser.parse_args()

    if args.command:
        args.func(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
