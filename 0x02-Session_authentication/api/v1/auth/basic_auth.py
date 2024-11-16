#!/usr/bin/env python3
"""
BasicAuth module
"""
from api.v1.auth.auth import Auth
import base64
from typing import Tuple, TypeVar
from models.user import User


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

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """
        Extract user email and password from
        the decoded Base64 authorization header.
        Args:
            decoded_base64_authorization_header (str):
            Decoded Base64 authorization header.
        Returns:
            tuple: A tuple containing the user email and password,
            or (None, None) if invalid.
        """
        if not isinstance(decoded_base64_authorization_header, str):
            return None, None
        if ':' not in decoded_base64_authorization_header:
            return None, None
        user_email, password = decoded_base64_authorization_header.split(
            ':', 1
        )
        return user_email, password

    def user_object_from_credentials(
            self,
            user_email: str, user_pwd: str) -> TypeVar('User'):
        """
        Retrieve a User instance using email and password.

        Args:
            user_email (str): The user's email.
            user_pwd (str): The user's password.

        Returns:
            User: The User instance if valid credentials are provided.
                  None otherwise.
        """
        if not isinstance(user_email, str) or not isinstance(user_pwd, str):
            return None
        users = User.search({"email": user_email})
        if not users or len(users) == 0:
            return None
        user = users[0]
        if not user.is_valid_password(user_pwd):
            return None
        return user

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Retrieves the User instance for a given request.

        Args:
            request: The incoming request to extract the user from.

        Returns:
            The User instance or None if authorization fails or if any of the
            checks fail.
        """
        authorization_header = self.authorization_header(request)
        if not authorization_header:
            return None
        base64_authorization = self.extract_base64_authorization_header(
            authorization_header)
        if not base64_authorization:
            return None
        decoded_base64 = self.decode_base64_authorization_header(
            base64_authorization)
        if not decoded_base64:
            return None
        user_email, user_pwd = self.extract_user_credentials(decoded_base64)
        if not user_email or not user_pwd:
            return None
        user = self.user_object_from_credentials(user_email, user_pwd)
        return user
