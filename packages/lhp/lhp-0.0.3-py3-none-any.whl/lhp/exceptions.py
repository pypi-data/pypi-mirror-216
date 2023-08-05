"""Asynchronous client for the Länderübergreifendes Hochwasserportal (LHP) API."""


class LHPError(Exception):
    """Generic LHP exception."""


class LHPConnectionError(LHPError):
    """LHP connection exception."""
