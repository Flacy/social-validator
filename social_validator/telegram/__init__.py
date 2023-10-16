from typing import Literal, Tuple

from social_validator.exceptions import ValidationError

# Restrictions for user, channel and bot identifiers
ID_MIN_LENGTH = 5
ID_MAX_LENGTH = 32

# Restrictions for description (about) field
DESCRIPTION_USER_MAX_LENGTH = 70
DESCRIPTION_GROUP_MAX_LENGTH = 255
DESCRIPTION_CHANNEL_MAX_LENGTH = DESCRIPTION_GROUP_MAX_LENGTH
DESCRIPTION_BOT_MAX_LENGTH = 120

# Restrictions for chat names
CHAT_NAME_MIN_LENGTH = 1
CHAT_NAME_MAX_LENGTH = 128

# Restrictions for user and bot names
FIRST_NAME_MIN_LENGTH = 1
FIRST_NAME_MAX_LENGTH = 64
LAST_NAME_MAX_LENGTH = 64

# Restrictions for messages
MESSAGE_MIN_LENGTH = 1
MESSAGE_MAX_LENGTH = 4096
# message with media files included
MEDIA_MESSAGE_MAX_LENGTH = 1024

# Restrictions for commands
COMMAND_MIN_LENGTH = 1
COMMAND_MAX_LENGTH = 32
COMMAND_DESCRIPTION_MAX_LENGTH = 256

ChatType = Literal["user", "group", "channel", "bot"]


def _is_valid_name(s: str) -> bool:
    """
    Checks the string for matching the pattern: A-Za-z, 0-9, _
    """
    # use a small hack to avoid performing additional checks
    s = s.replace("_", "A")
    return s.isascii() and s.isalnum()


def _is_valid_first_char(s: str) -> bool:
    """
    Checks the first character for the fact that it is not a digit or an
    underscore.
    """
    if not s:
        # empty string
        return False

    char = s[0]
    return not char.isdigit() and char != "_"


def _get_description_length_limit(t: ChatType) -> int:
    """
    Gets the maximum allowed length for the description based on the channel
    type.
    If an invalid type is specified, a ValueError will be thrown.
    """
    if t == "user":
        return DESCRIPTION_USER_MAX_LENGTH
    elif t == "group":
        return DESCRIPTION_GROUP_MAX_LENGTH
    elif t == "channel":
        return DESCRIPTION_CHANNEL_MAX_LENGTH
    elif t == "bot":
        return DESCRIPTION_BOT_MAX_LENGTH
    else:
        raise ValueError(f"Unexpected chat type: {t}")


def is_valid_id(_id: str) -> bool:
    return (
        _is_valid_first_char(_id)
        and (ID_MIN_LENGTH <= len(_id) <= ID_MAX_LENGTH)
        and _is_valid_name(_id)
    )


def is_bot_id(_id: str) -> bool:
    return _id.endswith("bot")


def is_valid_description(text: str, *, chat_type: ChatType = "user") -> bool:
    return len(text) <= _get_description_length_limit(chat_type)


def is_valid_chat_name(name: str) -> bool:
    return CHAT_NAME_MIN_LENGTH <= len(name) <= CHAT_NAME_MAX_LENGTH


def is_valid_first_name(name: str) -> bool:
    return FIRST_NAME_MIN_LENGTH <= len(name) <= FIRST_NAME_MAX_LENGTH


def is_valid_last_name(name: str) -> bool:
    return len(name) <= LAST_NAME_MAX_LENGTH


def is_valid_full_name(first_name: str, last_name: str = "") -> bool:
    return is_valid_first_name(first_name) and is_valid_last_name(last_name)


def is_valid_message(text: str, *, include_media: bool = False) -> bool:
    return (
        MESSAGE_MIN_LENGTH
        <= len(text)
        <= (MESSAGE_MAX_LENGTH if not include_media else MEDIA_MESSAGE_MAX_LENGTH)
    )


def is_valid_command(cmd: str) -> bool:
    return (COMMAND_MIN_LENGTH <= len(cmd) <= COMMAND_MAX_LENGTH) and (
        _is_valid_name(cmd)
    )


def validate_id(_id: str) -> str:
    """
    Validates the text identifier of the user/channel/bot.
    This a public identifier by which you can find the desired chat
    (available by ``t.me/%id%``).

    Only ID characters are allowed: A-Za-z, 0-9 and underscores.
    ID only start with a letter and must contain from 5 to 32
    characters.

    :param _id: User, channel or bot identifier
    :return: Input value, converted to lower-case
    :raises ValidationError: if the passed value contains non-ascii characters,
        spaces or other special chars not provided by Telegram
    """
    if not is_valid_id(_id):
        raise ValidationError(
            "ID must be length from 5 to 32 chars, starts with a letter and consists of: A-Za-z, 0-9 and underscores",
            input_value=_id,
        )

    return _id.lower()


def validate_bot_id(_id: str) -> str:
    """
    Validates the text identifier and checks the suffix "bot". Only ID
    characters are allowed.

    :param _id: Bot identifier
    :return: Input value, converted to lower-case
    :raises ValidationError: if the passed value does not have a ``bot`` suffix,
        contains non-ascii characters, spaces or other special chars not
        provided by Telegram
    """
    _id = validate_id(_id)

    if not is_bot_id(_id):
        raise ValidationError("Bot ID must have the suffix 'bot'", input_value=_id)

    return _id


def validate_description(text: str, *, chat_type: ChatType = "user") -> str:
    """
    Validates the description (about) field for the selected chat type.
    All characters are allowed.

    Each type has a different maximum length:
        * user - 70
        * group - 255
        * channel - 255
        * bot - 120

    :param text: biography (about) text
    :param chat_type: type of chat in which the text is located
    :return: Input text
    :raises ValueError: if the specified chat type is invalid
    :raises ValidationError: if the passed text exceeds the maximum allowed
        length
    """
    if not is_valid_description(text, chat_type=chat_type):
        length_limit = _get_description_length_limit(chat_type)
        raise ValidationError(
            f"Description text must contain no more than {length_limit} characters for '{chat_type}' chat type",
            input_value=text,
        )

    return text


def validate_chat_name(name: str) -> str:
    """
    Validates the name of channel or group for the minimum (1) and maximum (128)
    length of characters. All characters are allowed.

    :param name: Channel or group name
    :return: Input name
    :raises ValidationError: if there are not enough characters in passed name,
        or their number exceeds the maximum allowed length
    """
    if not is_valid_chat_name(name):
        raise ValidationError(
            f"Chat name must contain from {CHAT_NAME_MIN_LENGTH} to {CHAT_NAME_MAX_LENGTH} characters",
            input_value=name,
        )

    return name


def validate_full_name(*, first_name: str, last_name: str = "") -> Tuple[str, str]:
    """
    Validates the first and last name separately for the length limit.
    All characters are allowed. Passed names must not exceed 64 characters.
    The first name can't be empty, the last name, on the contrary, can.

    :param first_name: User's first name
    :param last_name: User's last name
    :return: Tuple of input parameters (first_name, last_name)
    :raises ValidationError: if there are not enough characters in passed name,
        or their number exceeds the maximum allowed length
    """
    if not is_valid_first_name(first_name):
        raise ValidationError(
            f"First name must contain from {FIRST_NAME_MIN_LENGTH} to {FIRST_NAME_MAX_LENGTH} characters",
            input_value=first_name,
        )
    if not is_valid_last_name(last_name):
        raise ValidationError(
            f"Last name must not exceed {LAST_NAME_MAX_LENGTH} characters",
            input_value=last_name,
        )

    return first_name, last_name


def validate_message(text: str, *, include_media: bool = False) -> str:
    """
    Validates the text message from user/channel/bot. All characters are
    allowed. The length must always be at least one character. The maximum
    length is calculated from the include_media condition if it is true, then
    the maximum length will be 1024, otherwise 4096.

    :param text: Message text
    :param include_media: Does the message additionally include media files
    :return: Input text
    :raises ValidationError: if the text is empty or the length limit is
        exceeded
    """
    if not is_valid_message(text, include_media=include_media):
        raise ValidationError(
            f"Message must contain from {MESSAGE_MIN_LENGTH} to "
            f"{MESSAGE_MAX_LENGTH if not include_media else MEDIA_MESSAGE_MAX_LENGTH} "
            f"characters with include_media={include_media}",
            input_value=text,
        )

    return text


def validate_command(cmd: str) -> str:
    """
    Validates the bot text command for the minimum (1) and maximum (32) length.
    Only ID characters are allowed: A-Za-z, 0-9 and underscores.

    Please note: Each command is stored in lower-case, but for a more concise
    implementation, uppercase characters are also available for you. They will
    be converted to the lower-case

    :param cmd: Bot text command
    :return: Input command, converted to lower-case
    :raises ValidationError: if the command is empty, or the length limit is
        exceeded, or contains characters that are not allowed by Telegram.
    """
    if not is_valid_command(cmd):
        raise ValidationError(
            f"Command must contain from {COMMAND_MIN_LENGTH} to {COMMAND_MAX_LENGTH} "
            f"characters and consist of: A-Za-z, 0-9 and underscores",
            input_value=cmd,
        )

    return cmd.lower()
