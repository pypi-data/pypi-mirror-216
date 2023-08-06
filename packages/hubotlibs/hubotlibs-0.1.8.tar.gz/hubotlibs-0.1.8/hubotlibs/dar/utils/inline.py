from math import ceil

from pyrogram.types import InlineKeyboardButton

from haidar import *


class EqInlineKeyboardButton(InlineKeyboardButton):
    def __eq__(self, other):
        return self.text == other.text

    def __lt__(self, other):
        return self.text < other.text

    def __gt__(self, other):
        return self.text > other.text


def paginate_modules(user_id, page_n, datadict, prefix, chat=None):
    
    data = {}
    dataa = datadict.copy()
    if user_id in BASICID:
        filter_set = {'limit', 'broadcast', 'help'}
        for key, value in dataa.items():
            if key in filter_set:
                data[key] = value
            
    
    elif user_id in MEDIUMID:
        filter_set = {'limit', 'broadcast', 'pilter', 'help', 'afk', 'antipm'}
        for key, value in dataa.items():
            if key in filter_set:
                data[key] = value
            
        
    elif user_id in PREMIUMID or user_id in DEVS:
        data = datadict

    if not chat:
        modules = sorted(
            [
                EqInlineKeyboardButton(
                    x.__MODULE__,
                    callback_data="{}_module({})".format(
                        prefix, x.__MODULE__.replace(" ", "_").lower()
                    ),
                )
                for x in data.values()
            ]
        )
    else:
        modules = sorted(
            [
                EqInlineKeyboardButton(
                    x.__MODULE__,
                    callback_data="{}_module({},{})".format(
                        prefix, chat, x.__MODULE__.replace(" ", "_").lower()
                    ),
                )
                for x in data.values()
            ]
        )
    line = 4
    pairs = list(zip(modules[::2], modules[1::2]))
    i = 0
    for m in pairs:
        for _ in m:
            i += 1
    if len(modules) - i == 1:
        pairs.append((modules[-1],))
    elif len(modules) - i == 2:
        pairs.append(
            (
                modules[-2],
                modules[-1],
            )
        )

    max_num_pages = ceil(len(pairs) / line)
    modulo_page = page_n % max_num_pages

    if len(pairs) > line:
        pairs = pairs[modulo_page * line : line * (modulo_page + 1)] + [
            (
                EqInlineKeyboardButton(
                    "❮",
                    callback_data="{}_prev({})".format(prefix, modulo_page),
                ),
                EqInlineKeyboardButton(
                    "❯",
                    callback_data="{}_next({})".format(prefix, modulo_page),
                ),
            )
        ]

    return pairs

def paginate_moduless(page_n, module_dict, prefix, chat=None):
    if not chat:
        modules = sorted(
            [
                EqInlineKeyboardButton(
                    x.__MODULE__,
                    callback_data="{}_module({})".format(
                        prefix, x.__MODULE__.replace(" ", "_").lower()
                    ),
                )
                for x in module_dict.values()
            ]
        )
    else:
        modules = sorted(
            [
                EqInlineKeyboardButton(
                    x.__MODULE__,
                    callback_data="{}_module({},{})".format(
                        prefix, chat, x.__MODULE__.replace(" ", "_").lower()
                    ),
                )
                for x in module_dict.values()
            ]
        )
    line = 4
    pairs = list(zip(modules[::2], modules[1::2]))
    i = 0
    for m in pairs:
        for _ in m:
            i += 1
    if len(modules) - i == 1:
        pairs.append((modules[-1],))
    elif len(modules) - i == 2:
        pairs.append(
            (
                modules[-2],
                modules[-1],
            )
        )

    max_num_pages = ceil(len(pairs) / line)
    modulo_page = page_n % max_num_pages

    if len(pairs) > line:
        pairs = pairs[modulo_page * line : line * (modulo_page + 1)] + [
            (
                EqInlineKeyboardButton(
                    "❮",
                    callback_data="{}_prev({})".format(prefix, modulo_page),
                ),
                EqInlineKeyboardButton(
                    "❯",
                    callback_data="{}_next({})".format(prefix, modulo_page),
                ),
            )
        ]

    return pairs
