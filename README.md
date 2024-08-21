# Key-Logger
This project is a keylogger written in Python that includes various functionalities such as capturing keystrokes, system information, clipboard data, audio recordings, and screenshots. The project also includes scripts for generating encryption keys and decrypting files.

## Project Structure

1. **`KeyLoggerTool.py`**: The main script for logging keystrokes, system information, clipboard data, recording audio, and taking screenshots. It also handles sending these logs via email and encrypting the files.

2. **`KeyGeneration.py`**: A script to generate a new encryption key using the `cryptography` library.

3. **`FileDecryption.py`**: A script to decrypt files that were encrypted by the `advanced_keylogger.py` script.

## Features

- **Keystroke Logging**: Captures and logs all keyboard inputs.
- **System Information**: Collects details about the system such as the processor, OS, and IP addresses.
- **Clipboard Monitoring**: Logs the contents of the clipboard.
- **Audio Recording**: Records audio from the microphone.
- **Screenshot Capturing**: Takes screenshots of the desktop.
- **Email Reporting**: Sends collected data and logs via email.
- **File Encryption**: Encrypts collected data before sending it.
- **File Decryption**: Decrypts files that were encrypted.

## Prerequisites

Make sure you have the following Python packages installed:
- `pynput`
- `scipy`
- `sounddevice`
- `cryptography`
- `requests`
- `Pillow`
- `pywin32`

## Setup

1. **Generate an Encryption Key**: Run key_generator.py to generate a new encryption key. This key will be used to encrypt and decrypt files.
2. **Configure the Keylogger**: Open advanced_keylogger.py.
Update the email_user, email_pass, recipient_email, and encryption_key variables with appropriate values.
Set save_path to the directory where you want the logs and other files to be saved.
3. **Run the Keylogger**: Execute advanced_keylogger.py to start the keylogger. It will collect data, encrypt it, and send it to the specified email.
4. **Decrypt Files**: Use file_decryptor.py to decrypt files that have been encrypted by the keylogger. Update the script with the correct encryption key and file paths before running it.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contact

For any questions or issues, please contact  bhallaaamna@gmail.com.
