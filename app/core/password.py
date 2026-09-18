# ============================================================
# Standard Library
# ============================================================

# None

# ============================================================
# Third Party
# ============================================================

from passlib.context import CryptContext

# ============================================================
# Password Context
# ============================================================

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
)


# ============================================================
# Password Utilities
# ============================================================

def hash_password(password: str) -> str:
    """
    Hash a plain text password using bcrypt.

    Args:
        password: Plain text password.

    Returns:
        Hashed password.
    """

    return pwd_context.hash(password)


def verify_password(
    plain_password: str,
    hashed_password: str,
) -> bool:
    """
    Verify a plain password against its hashed value.

    Args:
        plain_password: Password entered by the user.
        hashed_password: Password stored in database.

    Returns:
        True if password matches, otherwise False.
    """

    return pwd_context.verify(
        plain_password,
        hashed_password,
    )