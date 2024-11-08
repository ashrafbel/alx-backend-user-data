#!/usr/bin/env python3
"""
Encrypting passwords
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """function hashes the password using bcrypt with salt"""
    passWordBytes = password.encode('utf-8')
    hashSalted = bcrypt.hashpw(passWordBytes, bcrypt.gensalt())
    return hashSalted