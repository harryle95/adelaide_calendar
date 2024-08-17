import asyncio

from passlib.context import CryptContext

password_context = CryptContext(schemes=["argon2"], deprecated="auto")

__all__ = ("hash_plain_text_password", "validate_password")


async def hash_plain_text_password(password: str | bytes) -> str:
    """Hash a plain-text password to be stored in database

    Args:
        password (str | bytes): plain-text password

    Returns:
        str: hashed password

    Note:
        abit hairy here to make it an async runnable.
        If you don't need async, just call password_context.hash(password)
    """
    return await asyncio.get_running_loop().run_in_executor(None, password_context.hash, password)


async def validate_password(plain_text: str | bytes, hashed: str) -> bool:
    """Check whether plain_text password matched hashed password in database

    Args:
        plain_text (str | bytes): plain-text value provided by user, whose hash should match hashed
        hashed (str): hashed password stored in db

    Returns:
        bool: True if correct plain_text is provided
    """
    valid, _ = await asyncio.get_running_loop().run_in_executor(
        None, password_context.verify_and_update, plain_text, hashed
    )
    return bool(valid)
