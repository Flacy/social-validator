from social_validator import shared
from social_validator.exceptions import ValidationError

# Restrictions for username
USERNAME_MIN_LENGTH = 3
USERNAME_MAX_LENGTH = 30

# YouTube has two types of links leading to a channel.
# The first type is displayed with an "@" symbol and contains the exact address
# with hyphens, underscores, and dots.
# The second type doesn't contain the "@" symbol and ignores any hyphens and
# underscores. The dots in this type also have significance.
_IGNORED_CHARACTERS = frozenset(("_", "-"))

RESERVED_USERNAMES = frozenset(
    (
        "blog",
        "browse",
        "channels",
        "explore",
        "favorites",
        "feed",
        "gaming",
        "help",
        "kids",
        "live",
        "logout",
        "movies",
        "music",
        "playlist",
        "search",
        "settings",
        "signin",
        "signup",
        "sports",
        "support",
        "trending",
        "upload",
        "video",
        "videos",
        "watch",
    )
)


def _replace_ignored_chars(s: str, replace: str) -> str:
    """
    Replaces all characters from the :py:const:`_IGNORED_CHARACTERS` with the
    specified one.
    """
    for char in _IGNORED_CHARACTERS:
        s = s.replace(char, replace)

    return s


def is_valid_username(username: str, *, strct: bool = True) -> bool:
    """
    Checks the given username for character correctness.
    More detailed validation criteria are described in
    :py:func:`validate_username`.

    :return: ``True``, if all the conditions are met, otherwise ``False``.
    """
    username = _replace_ignored_chars(username, "_" if strct else "")

    return (
        USERNAME_MIN_LENGTH <= len(username) <= USERNAME_MAX_LENGTH
        and username[0] != "."
        and not username.isdigit()
        and shared.is_valid_id(username.replace(".", "_"))
    )


def is_reserved_username(username: str) -> bool:
    """
    Checks whether the username is reserved.
    Case-insensitive.

    Refer to the :py:const:`RESERVED_USERNAMES` for the complete list of words.

    :return: ``True`` if **username** is reserved, ``False`` otherwise
    """
    return username.lower() in RESERVED_USERNAMES


def validate_username(username: str, *, strict: bool = True) -> str:
    """
    Validates a username based on the following criteria:

    - The username contains between 3 and 30 characters, inclusively;
    - It consist of A-Za-z, digits, hyphens, underscores, and dots;
    - It doesn't start with a dot;
    - It is not entirely composed of digits;
    - It is not a reserved word.

    All reserved words are listed in :py:const:`RESERVED_USERNAMES`

    It is important to highlight the "strict" argument. It determines whether
    the strict validation will be enabled or not.
    When it is enabled, the validation will be strict and all characters will
    be preserved.
    When it is disabled, a soft validation will be performed,
    ignoring hyphens and underscores.

    This is due to the specific algorithms used by YouTube. When following a
    link that includes the "@" symbol, a strict search will be conducted.
    Otherwise, a soft search will be used.

    :param username: User text ID
    :param strict: Is the username includes "@" symbol
    :return: Input username, converted to lower-case. If the strict mode is
        disabled, all hyphens and underscores will be removed.
    :raise ValidationError: If the username does not meet the criteria
    """
    if not is_valid_username(username, strct=strict):
        raise ValidationError(
            "Username must have between 3 and 20 characters, including hyphens, "
            "underscores and dots, can't consist entirely of numbers, and can't "
            "start with a dot",
            input_value=username,
        )
    elif is_reserved_username(username):
        raise ValidationError(
            "Username must not be a reserved word",
            input_value=username,
        )

    if not strict:
        # Replace them because they are not considered by YouTube
        username = _replace_ignored_chars(username, "")

    return username.lower()
