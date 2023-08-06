from setuptools import setup, find_packages

# Read long description from README
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='azure_vault_loader',
    version='0.1.0',
    url='https://github.com/jason-weirather/azure-vault-loader',
    author='Jason L Weirather',
    author_email='jason.weirather@gmail.com',
    description='Load secrets from Azure key vault into the environment of a process',

    long_description=long_description,
    long_description_content_type="text/markdown",

    packages=find_packages(),    
    install_requires=[
         'azure-keyvault-secrets',
         'azure-identity'
      ],
    entry_points={
        'console_scripts': [
            'load_azure_secrets = azure_vault_loader.cli:main',
            'obfuscate_service_principals = azure_vault_loader.cli:run_obfuscate_service_principals',
        ],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3.9',
    ],
)

