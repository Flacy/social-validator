from social_validator import shared
from social_validator.exceptions import ValidationError

# Restrictions for usernames
USERNAME_MIN_LENGTH = 4
USERNAME_MAX_LENGTH = 25

# Restrictions for messages
MESSAGE_MIN_LENGTH = 1
MESSAGE_MAX_LENGTH = 500


def is_valid_username(username: str) -> bool:
    """
    Checks if a given username is valid based on certain criteria described in
    :py:func:`validate_username`.

    :return: ``True``, if all the conditions are met, otherwise ``False``.
    """
    return (
        USERNAME_MIN_LENGTH <= len(username) <= USERNAME_MAX_LENGTH
        and username[0] != "_"
        and not username.isdigit()
        and shared.is_valid_id(username)
    )


def is_valid_message(text: str) -> bool:
    """
    Checks if a given text is valid based on certain criteria described in
    :py:func:`validate_message`.

    :return: ``True``, if all the conditions are met, otherwise ``False``
    """
    return MESSAGE_MIN_LENGTH <= len(text) <= MESSAGE_MAX_LENGTH and text.isprintable()


def validate_username(username: str) -> str:
    """
    Validates a username based on the following criteria:

    - The length of the username must be 4 to 25 characters long.
    - The username must not start with an underscore.
    - The username must not consist entirely of digits.
    - The username must consist of: A-Za-z, 0-9 and underscores.

    :param username: User text ID
    :return: Input username
    :raise ValidationError: If the username does not meet the criteria
    """
    if not is_valid_username(username):
        raise ValidationError(
            "Username must be 4 to 25 characters long, exclude the underscore as the first "
            "character, and can only consist of: A-Za-z, 0-9 and underscores",
            input_value=username,
        )

    return username


def validate_message(text: str) -> str:
    """
    Validates a text based on the following criteria:

    - The text must be between 1 and 500 characters, inclusive.
    - The text must not contain any escaped characters.

    :param text: Message text
    :return: Input text
    :raise ValidationError: if the text does not meet the criteria
    """
    if not is_valid_message(text):
        raise ValidationError(
            "Message must contain between 1 and 500 characters, inclusive, "
            "and must not have any escaped characters",
            input_value=text,
        )

    return text
