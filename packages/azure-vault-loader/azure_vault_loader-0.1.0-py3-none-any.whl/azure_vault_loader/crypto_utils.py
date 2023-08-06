import base64
import json

from cryptography.fernet import Fernet

def decrypt_service_principals(obfuscation_key, encrypted_principals):
    """
    Decrypts service principals using an obfuscation key.

    Args:
        obfuscation_key (str): The key used for obfuscation. It should be a string and is padded or truncated to ensure it is 32 bytes long.
        encrypted_principals (bytes): The encrypted service principals. This should be in bytes, as outputted by obfuscate_service_principals.

    Returns:
        dict: A Python dictionary containing the decrypted service principals.
    """
    # Ensure the obfuscation key is 32 bytes long
    padded_key = (obfuscation_key[:32] + (32 * '0'))[:32]
    encoded_key = base64.urlsafe_b64encode(padded_key.encode())

    # Create a Fernet cipher
    fernet = Fernet(encoded_key)

    # Decode and decrypt the service principals
    decrypted_service_principals = fernet.decrypt(encrypted_principals)
    return json.loads(decrypted_service_principals.decode())


def obfuscate_service_principals(obfuscation_key, principals):
    """
    Obfuscates service principals using an obfuscation key.

    Args:
        obfuscation_key (str): The key used for obfuscation. It should be a string and is padded or truncated to ensure it is 32 bytes long.
        principals (dict): The service principals to obfuscate. This should be a Python dictionary.

    Returns:
        bytes: The obfuscated service principals, in bytes.
    """
    # Encode the key, ensure it's 32 bytes long
    padded_key = (obfuscation_key[:32] + (32 * '0'))[:32]
    encoded_key = base64.urlsafe_b64encode(padded_key.encode())

    # Obfuscate service principals
    fernet = Fernet(encoded_key)
    return fernet.encrypt(json.dumps(principals).encode())
