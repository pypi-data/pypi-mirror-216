"""Utility methods for string.
"""
import re


def remove_comments(string_file):
    """Removes the comments from an uop file to make it readable for our
    ConfigParser. It removes the following patterns: // and /* .. */

    :param str string_file: The string where to remove the comments

    :returns: The same text, but without all the commented lines
    :return type: str
    """
    pattern = r"(\".*?\"|\'.*?\')|(/\*.*?\*/|//[^\r\n]*$)"
    regex = re.compile(pattern, re.MULTILINE | re.DOTALL)

    def _replacer(match):
        if match.group(2) is not None:
            return ""
        else:
            return match.group(1)

    return regex.sub(_replacer, string_file)
