# Morgans

> A **d3vn0mi** project.

Morgans is a comprehensive toolset designed for processing ODT (OpenDocument Text) files. It integrates multiple functionalities, including document generation, encryption, obfuscation, and serving files via a simple HTTP server. This tool is ideal for scenarios requiring document manipulation or security-focused operations.

## Scripts Overview

### 1. `odt_generator.py`

This script is responsible for modifying the content of ODT documents based on a given template and output path. It provides functions that can be used to generate benign or malicious ODT files.

#### Features:
- Modifies the content of ODT files using specified templates.
- Can be used as a standalone script or imported as a module.

### 2. `mass_odt_gen.py`

This script generates a mix of benign and malicious ODT documents using filenames provided in a text file. It imports and utilizes the functionality provided by `odt_generator.py`.

#### Features:
- Generates up to 50 unique ODT files with a specified ratio of benign to malicious documents.
- Uses a list of filenames from an external text file (`filenames.txt`).
- Automatically creates an output folder to store the generated files.
- Provides a summary file listing the generated files and their types.

#### Usage:
```bash
python mass_odt_gen.py <num_files> <percentage_malicious> --file-list <path_to_filenames.txt>
```

#### Arguments:
- `num_files`: The number of files to generate, up to a maximum of 50 to ensure uniqueness.
- `percentage_malicious`: The percentage of files that should be malicious.
- `--file-list` or `-f`: Path to a text file containing a list of filenames to use.

#### Example:
```bash
python mass_odt_gen.py 30 40 --file-list filenames.txt
```

#### `filenames.txt` Format:
The `filenames.txt` file should be a plain text file where each line contains a single filename (without extensions or suffixes). Here is an example of what `filenames.txt` might look like:

```
finance_report
sales_forecast
annual_summary
meeting_minutes
strategy_outline
project_plan
budget_review
employee_handbook
customer_survey
market_research
...
```

### 3. `mass_odt_enc_obf.py`

This script provides a comprehensive solution for processing multiple ODT files. It includes features for encrypting specified patterns within ODT files, obfuscating text, and even serving files via a simple HTTP server.

#### Features:
- Encrypts specific patterns within ODT files using XOR encryption.
- Obfuscates variable names, functions, and specific strings in StarBasic code within ODT files.
- Moves benign ODT files to a separate directory after processing.
- Zips the processed files into a single archive.
- Serves the current directory over HTTP.

#### Usage:
```bash
python mass_odt_enc_obf.py --dir <folder_path> [options]
```

#### Arguments:
- `--dir` or `-d`: Directory containing the ODT files to process (required).
- `--macro-dir` or `-md`: Directory within the ODT file where the macro is located. Default is `Basic/Standard`.
- `--macro-file` or `-mf`: The macro file to encrypt within the ODT files. Default is `Module1.xml`.
- `--obfuscate` or `-obf`: Enables the obfuscation of strings and variables.
- `--encrypt-strings` or `-es`: File containing patterns for encryption.
- `--obfuscate-strings` or `-os`: File containing patterns for obfuscation.
- `--obfuscate-vars` or `-ov`: Enables the obfuscation of variable names in the code.

#### Example:
```bash
python mass_odt_enc_obf.py --dir ./odt_files --encrypt-strings enc_strings.txt --obfuscate --obfuscate-vars
```

### 4. `morgans.py`

`morgans.py` is the core script of this toolset. It integrates and manages the functionalities provided by `mass_odt_gen.py` and `mass_odt_enc_obf.py`. This is the only script the user needs to run to access all features.

#### Usage:
```bash
python morgans.py [subcommand] [options]
```

#### Subcommands:
- `gen`: Calls `mass-odt-gen.py` to generate ODT documents.
- `encobf`: Calls `mass-odt-enc-obf.py` to encrypt and obfuscate ODT documents.

#### Example Commands:
- Generate Documents:
  ```bash
  python morgans.py gen 30 40 --file-list filenames.txt
  ```
- Encrypt and Obfuscate Documents:
  ```bash
  python morgans.py encobf --dir ./odt_files --encrypt-strings enc_strings.txt --obfuscate --obfuscate-vars
  ```


## Installation

To use these scripts, you need to have Python installed on your system along with the required packages. You can install the dependencies using either of the following commands:

```bash
pip install -r requirements.txt
# or, to install the single dependency directly:
pip install odfpy
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Author

Created and maintained by **d3vn0mi**.

