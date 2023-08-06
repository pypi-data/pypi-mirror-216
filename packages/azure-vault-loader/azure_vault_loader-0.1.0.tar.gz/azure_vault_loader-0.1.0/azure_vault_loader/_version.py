try:
    from importlib.metadata import version
except ModuleNotFoundError:
    from importlib_metadata import version
__version__ = version('azure_vault_loader')
