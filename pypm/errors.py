class Error(Exception):
    """Base class for other exceptions"""
    pass

class SetuptoolFailure(Error):
    """Raised when setuptool encounters an error"""
    def __init__(self, message, errors='002'):

        # Call the base class constructor with the parameters it needs
        super().__init__(message)

        # Now for your custom code...
        self.errors = errors

class PackageJsonNotFound(Error):
    """Raised when package.json is not found"""
    def __init__(self, message, errors='001'):

        # Call the base class constructor with the parameters it needs
        super().__init__(message)

        # Now for your custom code...
        self.errors = errors

class NoSetupConfiguration(Error):
    """Raised when 'setup' key in package.json is not found"""
    def __init__(self, message, errors='003'):

        # Call the base class constructor with the parameters it needs
        super().__init__(message)

        # Now for your custom code...
        self.errors = errors
