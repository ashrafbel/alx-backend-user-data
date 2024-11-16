#!/usr/bin/env python3
"""
BasicAuth module
"""
from api.v1.auth.auth import Auth
import base64


class BasicAuth(Auth):
    """
    BasicAuth class that inherits from Auth
    """
    def extract_base64_authorization_header(
            self,
            authorization_header: str) -> str:
        """
        Extract Base64 part from Authorization header for Basic Authentication
        """
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith("Basic "):
            return None
        return authorization_header[6:]

    def decode_base64_authorization_header(
            self,
            base64_authorization_header: str) -> str:
        """ Decode the Base64 encoded string into a UTF-8 string. """
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            decoded_bytes = base64.b64decode(base64_authorization_header)
            return decoded_bytes.decode('utf-8')
        except (base64.binascii.Error, UnicodeDecodeError):
            return None

    def extract_user_credentials(self, decoded_base64_authorization_header: str) -> (str, str):
        """
        Extract user email and password from the decoded Base64 authorization header.

        Args:
            decoded_base64_authorization_header (str): Decoded Base64 authorization header.

        Returns:
            tuple: A tuple containing the user email and password, or (None, None) if invalid.
        """
        if not isinstance(decoded_base64_authorization_header, str):
            return None, None
        if ':' not in decoded_base64_authorization_header:
            return None, None
        user_email, password = decoded_base64_authorization_header.split(':', 1)
        return user_email, password
