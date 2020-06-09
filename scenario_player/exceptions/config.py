class ConfigurationError(ValueError):
    """Generic error thrown if there was an error while reading the scenario file."""


class TokenFileError(ConfigurationError):
    """There was an error while reading a token configuration from disk."""


class TokenFileMissing(TokenFileError):
    """We tried re-using a token, but no token.info file exists for it."""
