#!/usr/bin/env python3
"""task 3 module.
"""
from flask import request
from typing import List, TypeVar


class Auth:
    "Auth class"
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        "A method to check if authentication is required."
        if path is None:
            return True
        if not excluded_paths:
            return True
        normalized_path = path.rstrip("/")
        excluded_paths_normalized = [
            excluded_path.rstrip("/") for excluded_path in excluded_paths
        ]
        if normalized_path in excluded_paths_normalized:
            return False
        return True

    def authorization_header(self, request=None) -> str:
        """ Method to retrieve the authorization header. """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        "Method to extract user from the request."
        return None
