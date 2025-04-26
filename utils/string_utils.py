"""
String Replacement Utility

This module provides a utility function to perform string replacements, supporting both single and multiple replacements in one operation.

Functions:
    replace_string(for_replaced: str, replaced_item: str, item_for_replace):
        Replaces occurrences of a substring in a given string with one or more replacement values.

Args:
    for_replaced (str): The original string where replacements will be performed.
    replaced_item (str): The substring to be replaced.
    item_for_replace (str | list): The replacement value(s). Can be a single string or a list of strings.

Returns:
    str: The resulting string after all replacements are applied.

Behavior:
    - If `item_for_replace` is a list, replaces `replaced_item` sequentially with each item in the list.
    - If `item_for_replace` is a single value, replaces all occurrences of `replaced_item` with it.
    - Replacement is case-sensitive and occurs only once per item in the list if `item_for_replace` is a list.
"""

import allure

from .logger import log_allure


@allure.step("Replace String")
def replace_string(for_replaced: str, replaced_item: str, item_for_replace):
    """
    Replaces a specified substring in a string with one or more values.

    Args:
        for_replaced (str): The string in which the replacement will be performed.
        replaced_item (str): The substring to be replaced.
        item_for_replace (str | list): The replacement value(s). If a list is provided, replacements are performed sequentially.

    Returns:
        str: The updated string after performing the replacements.

    Example Usage:
        - Single Replacement:
            replace_string("Hello, World!", "World", "Universe")
            -> "Hello, Universe!"
        - Multiple Replacements:
            replace_string("A B C D", "B", ["X", "Y", "Z"])
            -> "A X C D" (only the first occurrence is replaced in this case)
    """
    if isinstance(item_for_replace, list):
        for replacement in item_for_replace:
            for_replaced = for_replaced.replace(replaced_item, replacement, 1)
    else:
        for_replaced = for_replaced.replace(replaced_item, item_for_replace)

    log_allure(f"Replaced String: {for_replaced}")
    return for_replaced
