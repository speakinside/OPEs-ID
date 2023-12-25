from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("OPEs_ID")
except PackageNotFoundError:
    # package is not installed
    pass