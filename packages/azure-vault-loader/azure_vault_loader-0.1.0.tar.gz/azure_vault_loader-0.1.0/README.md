# Azure Vault Loader

Azure Vault Loader is a Python command-line utility for securely loading secrets from Azure Key Vault into environment variables. It is designed to enable secure execution of commands on remote servers, by ensuring that secrets are loaded as environment variables only at the time of command execution, thereby reducing the exposure of sensitive data.

The utility makes use of Azure's role-based access control (RBAC) and Azure Key Vault, a cloud service for securely storing and accessing secrets. A "secret" in Azure Key Vault could be a password, a token, an API key, a connection string, or any other piece of data that is sensitive and needs to be kept secure.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install Azure Vault Loader.

```bash
pip install azure-vault-loader
```

## Usage

```bash
load_azure_secrets -k obfuscation_key -p principals -m map -u url -c command with or without arguments
```

- `-k, --obfuscation_key`: The key used for reading an obfuscated principals file. If this option is provided, the tool will attempt to decrypt the service principals file.
- `-p, --principals`: The Azure service principals. This file can be in plain JSON format or obfuscated using the `obfuscate_service_principals` command.
- `-m, --map`: The JSON file containing secret names and the environment variable names as key-value pairs. This map dictates which Azure secrets get loaded into which environment variables.
- `-c, --command`: The command to run after loading secrets. This can include one or more arguments.
- `-u, --url`: The URL of your Azure Key Vault.
- `-v, --verbose`: Enable verbose mode.

### Secret-Environment Variables Map

The `map` argument requires a JSON file that contains a mapping between the secret names in your Azure Key Vault and the environment variables that they correspond to. 

Here is an example of what the contents of the JSON file might look like:

```json
{
    "databasepasswordsecret": "DB_PASSWORD",
    "apikeysecret": "API_KEY"
}
```

In the example above, `database_password_secret` and `api_key_secret` are the names of secrets stored in Azure Key Vault. When the `load_azure_secrets` command is run, the secrets corresponding to these names will be fetched from the Azure Key Vault, and then loaded into the `DB_PASSWORD` and `API_KEY` environment variables, respectively. 

The purpose of this is to abstract the actual values of the secrets, allowing you to change the secrets in the Azure Key Vault without having to change your code or your environment setup. As long as the secret name and corresponding environment variable name remain the same, you can change the value of the secret in Azure Key Vault at any time, and the `load_azure_secrets` command will always fetch the most current value.

```bash
obfuscate_service_principals -j json -o output -k key
```

- `-j, --json`: The JSON file containing service principals to obfuscate.
- `-o, --output`: The output file for the obfuscated service principals.
- `-k, --key`: The key for obfuscation.

## License

[Apache 2.0](https://www.apache.org/licenses/LICENSE-2.0)
