import argparse
import os
import subprocess
import json

from azure.identity import ClientSecretCredential
from azure.keyvault.secrets import SecretClient

from .crypto_utils import decrypt_service_principals, obfuscate_service_principals

def main():
    """
    Reads either a plain text or obfuscated service principal file, fetches secrets from Azure Key Vault
    and sets them as environment variables. Afterwards, it runs a provided command with these environment variables.

    The command line arguments expected by the function are:
    -v, --verbose: Show more outputs
    -k, --obfuscation_key: An optional file containing a key used for decrypting an obfuscated principals file.
    -p, --principals: Path to the file containing the Azure service principals.
    -m, --map: Path to a JSON file containing a mapping between secret names and environment variable names.
    -u, --url: The URL of your Azure Key Vault.
    -c, --command: The command to run after loading the secrets. All arguments after -c are considered part of the command.

    Example usage:
    python main.py -k obfuscation_key -p principals.json -m map.json -c python script.py arg1 arg2 -u https://yourvault.vault.azure.net/
    """
    parser = argparse.ArgumentParser(description='Load secrets from Azure Key Vault into environment variables.')
    parser.add_argument('-v', '--verbose', action='store_true', help='Show more details')
    parser.add_argument('-k', '--obfuscation_key', help='The key used for reading an obfuscated principals file')
    parser.add_argument('-p', '--principals', help='The Azure service principals', required=True)
    parser.add_argument('-m', '--map', help='The JSON file containing secret names and the environment variable names as key-value pairs', required=True)
    parser.add_argument('-u', '--url', help='The URL of your Azure Key Vault', required=True)
    parser.add_argument('-c', '--command', nargs=argparse.REMAINDER, help='The command to run after loading secrets', required=True)
    args = parser.parse_args()

    if args.verbose:
        print(f'Map: {args.map}')
        print(f'Command: {args.command}')

    # If an obfuscation key is given, decrypt the service principals file
    if args.obfuscation_key:
        with open(args.principals, 'rb') as f:
            encrypted_principals = f.read()
        with open(args.obfuscation_key) as f:
            obfuscation_key = f.read().strip()
        key_data = decrypt_service_principals(obfuscation_key, encrypted_principals)
    else:
        # Load the service principals from the key file
        with open(args.principals, 'r') as f:
            key_data = json.load(f)

    # Create a secret client using the service principals
    credential = ClientSecretCredential(key_data['tenant'], key_data['appId'], key_data['password'])
    secret_client = SecretClient(vault_url=args.url, credential=credential)

    # Load the secret-envvar mapping from the json file
    with open(args.map, 'r') as json_file:
        secret_mapping = json.load(json_file)

    # Fetch each secret and set it as an environment variable
    for secret_name, envvar_name in secret_mapping.items():
        secret = secret_client.get_secret(secret_name)
        os.environ[envvar_name] = secret.value

    # Run the command with the loaded environment variables
    subprocess.run(args.command)



def run_obfuscate_service_principals():
    """
    Reads a service principal file, obfuscates it using a provided key, and writes the result to an output file.

    The command line arguments expected by the function are:
    -v, --verbose: Show more outputs
    -j, --json: Path to the JSON file containing the service principals to obfuscate.
    -o, --output: Path to the output file for the obfuscated service principals.
    -k, --key: The file containing the text key for obfuscation.

    Example usage:
    python run_obfuscate_service_principals.py -j principals.json -o obfuscated_principals -k obfuscation_key
    """
    parser = argparse.ArgumentParser(description='Obfuscate Azure service principals.')
    parser.add_argument('-v', '--verbose', action='store_true', help='Show more details')
    parser.add_argument('-j', '--json', help='The JSON file containing service principals to obfuscate', required=True)
    parser.add_argument('-o', '--output', help='The output file for the obfuscated service principals', required=True)
    parser.add_argument('-k', '--key', help='Read a key from a text file for obfuscation', required=True)
    args = parser.parse_args()

    # Load service principals from JSON file
    with open(args.json, 'r') as f:
        service_principals = json.load(f)

    with open(args.key, 'r') as f:
        obfuscation_key = f.read().strip()

    obfuscated_service_principals = obfuscate_service_principals(obfuscation_key,service_principals)

    # Write obfuscated service principals to output file
    with open(args.output, 'wb') as f:
        f.write(obfuscated_service_principals)

    if args.verbose:
        print(f'Service principals obfuscated and written to: {args.output}')
