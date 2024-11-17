#!/usr/bin/env python3
""" SessionAuth module """
from api.v1.auth.auth import Auth
import uuid
import os
from flask import request


class SessionAuth(Auth):
    """Session authentication class"""
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        Creates a Session ID for a given user_id
        """
        if user_id is None or not isinstance(user_id, str):
            return None
        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        إرجاع User ID بناءً على Session ID.
        """
        if session_id is None or not isinstance(session_id, str):
            return None
        return self.user_id_by_session_id.get(session_id)

    def session_cookie(self, request=None):
        """
        returns a cookie value from a request
        """
        if request is None:
            return None
        session_name = os.getenv("SESSION_NAME")
        if not session_name:
            return None
        return request.cookies.get(session_name)
