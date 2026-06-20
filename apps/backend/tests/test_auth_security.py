def test_password_hash_verifies_correct_password():
    from app.auth.security import hash_password, verify_password

    password_hash = hash_password("correct horse battery staple")

    assert password_hash != "correct horse battery staple"
    assert verify_password("correct horse battery staple", password_hash) is True
    assert verify_password("wrong password", password_hash) is False


def test_totp_secret_and_code_verification_are_time_scoped():
    from app.auth.totp import generate_totp_secret, generate_totp_code, verify_totp_code

    secret = generate_totp_secret()
    code = generate_totp_code(secret, for_time=1_735_689_600)

    assert verify_totp_code(secret, code, at_time=1_735_689_600) is True
    assert verify_totp_code(secret, code, at_time=1_735_689_600 + 120) is False
