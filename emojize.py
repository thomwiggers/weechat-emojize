"""
Weechat plugin to convert emoji shortcodes to unicode emoji.

This plugin is a thin wrapper around the emoji package for python.
It converts emoji shortcodes to Unicode emoji.

This package is based on the emoji_aliases.py script by Mike Reinhardt.

License: CC0
Author: Thom Wiggers
Repository: https://github.com/thomwiggers/weechat-emojize

This plugin supports python 3 and requires the emoji python package.
"""

import emoji
import weechat

weechat.register(
    "emojize",
    "Thom Wiggers",
    "1.0.0",
    "CC0",
    "Convert emoji shortcodes to unicode emoji",
    "",  # shutdown function
    "utf-8",
)

NEEDSPLIT = (
    'irc_in2_PRIVMSG',
    'irc_in2_NOTICE',
    'irc_in2_PART',
    'irc_in2_QUIT',
    'irc_in2_KNOCK',
    'irc_in2_AWAY'
)


HOOKS = (
    "away",
    "cnotice",
    "cprivmsg",
    "kick",
    "knock",
    "notice",
    "part",
    "privmsg",
    "quit",
    "wallops",
)


def convert_emoji(_data, modifier, _modifier_data, string):
    """Convert the emoji in event messages"""
    # Check if this message has a segment we shouldn't touch.
    if modifier in NEEDSPLIT:
        try:
            (start, msg) = string.split(' :', 1)
        except ValueError:
            if 'PART' not in modifier:
                print("Couldn't split and emojize '{}'".format(string))
            (start, msg) = (string, '')

        msg = emoji.emojize(msg, use_aliases=True)
        return start + ' :' + msg

    return emoji.emojize(string, use_aliases=True)


for hook in HOOKS:
    weechat.hook_modifier("irc_in2_{}".format(hook), "convert_emoji", "")

weechat.hook_modifier("input_text_for_buffer", "convert_emoji", "")
