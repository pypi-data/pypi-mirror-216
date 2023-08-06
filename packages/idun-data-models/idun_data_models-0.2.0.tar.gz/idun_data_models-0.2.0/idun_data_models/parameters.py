import re

MAX_ID_LENGTH = 256
ID_REGEX = r"^[a-zA-Z0-9][a-zA-Z0-9_.-]{0," + re.escape(str(MAX_ID_LENGTH - 1)) + r"}$"
