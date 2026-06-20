from __future__ import annotations

import base64
import hashlib
import hmac
import secrets
import struct
import time

_TIME_STEP_SECONDS = 30
_DIGITS = 6


def generate_totp_secret() -> str:
    return base64.b32encode(secrets.token_bytes(20)).decode("ascii").rstrip("=")


def generate_totp_code(secret: str, *, for_time: int | None = None) -> str:
    timestamp = int(time.time() if for_time is None else for_time)
    counter = timestamp // _TIME_STEP_SECONDS
    key = _decode_secret(secret)
    message = struct.pack(">Q", counter)
    digest = hmac.new(key, message, hashlib.sha1).digest()
    offset = digest[-1] & 0x0F
    binary = struct.unpack(">I", digest[offset : offset + 4])[0] & 0x7FFFFFFF
    code = binary % (10**_DIGITS)
    return f"{code:0{_DIGITS}d}"


def verify_totp_code(secret: str, code: str, *, at_time: int | None = None) -> bool:
    timestamp = int(time.time() if at_time is None else at_time)
    candidate = generate_totp_code(secret, for_time=timestamp)
    return hmac.compare_digest(candidate, code)


def _decode_secret(secret: str) -> bytes:
    padding = "=" * ((8 - len(secret) % 8) % 8)
    return base64.b32decode((secret + padding).encode("ascii"), casefold=True)
