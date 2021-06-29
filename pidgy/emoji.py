"""pidgy emoji support.

* IPython emoji completion
* emoji name munging to python using emoji aliases as variable names.

this module works as a standalone extension for `IPython` emoji support

    %load_ext pidgy.emoji

this approach uses the tokenize module and can determininstically replace
emoji based on specific token patterns.
"""
import contextlib
import io
import tokenize

import emoji

locale = __import__("locale").getlocale()[0].partition("_")[0]
emoji.ESCAPED_EMOJI = dict(
    zip(
        map(lambda x: x.encode("unicode-escape"), emoji.UNICODE_EMOJI[locale]),
        emoji.UNICODE_EMOJI[locale].values(),
    )
)


def get_escaped_alias(s):
    # the tokenizer returns unicode escaped characters we'll need to invert
    e = s.encode("unicode-escape")
    if e in emoji.ESCAPED_EMOJI:
        return emoji.ESCAPED_EMOJI[e]
    return s


def complete(self, event):
    """emoji completion for ipython"""
    import emoji

    return [
        x[1:]
        for x in emoji.EMOJI_ALIAS_UNICODE_ENGLISH
        if x[1:].startswith(event.symbol) and "-" not in x
    ]


def emojize(lines):
    """a clean up transformer for eomoji"""
    with contextlib.suppress(IndentationError, ValueError):
        return tangle_emojis("".join(lines)).splitlines(True)
    return lines


def get_spaces_between(a, b):
    # space between tokens
    return a.start[1] - b.end[1]


def tangle_emojis(str):
    """a strategy with the tokenize module to include emoji as valid code &
    include them in strings"""
    tokens = []
    current_line = 0
    emoji_buffer = []  # tokens relating to emoji
    emoji_token_buffer = []  # a temporary buffer of possible emoji
    line_buffer = []  # token per lines

    for token in tokenize.tokenize(io.BytesIO(str.encode()).readline):
        if current_line != token.start[0]:
            # reset the buffers on each line.
            if emoji_buffer:

                # we have to shift the tokens when we find emoji to account for the :
                offset, line, prior = 0, "", None

                # build the line for the token
                for t in line_buffer:
                    if t in emoji_buffer and t.string == ":":
                        # offset the start and end for colon seen
                        offset -= 1
                        continue

                    # update the line
                    line += (
                        " " * get_spaces_between(t, prior) if prior else ""
                    ) + t.string
                    prior = t

                offset = 0
                # append the adjusted tokens to the final tokens
                for t in line_buffer:
                    if t in emoji_buffer:
                        if t.string == ":":
                            offset -= 1
                            continue
                    tokens.append(
                        tokenize.TokenInfo(
                            t.type,
                            t.string,
                            (t.start[0], t.start[1] + offset),
                            (t.end[0], t.end[1] + offset),
                            line,
                        )
                    )
            else:
                # push the line buffer to the final tokens
                tokens.extend(line_buffer)

            # clear the buffers
            line_buffer.clear()
            emoji_buffer.clear()

        # update the current line
        current_line = token.start[0]

        if token.string == ":":
            if emoji_token_buffer:
                if get_spaces_between(token, emoji_token_buffer[-1]):
                    line_buffer.extend(emoji_token_buffer)
                    emoji_token_buffer.clear()

            emoji_token_buffer.append(token)

            if len(emoji_token_buffer) == 1:
                continue

            if len(emoji_token_buffer) == 3:
                emoji_buffer.extend(emoji_token_buffer)
                line_buffer.extend(emoji_token_buffer)
                emoji_token_buffer.clear()
            if len(emoji_token_buffer) == 2:
                line_buffer.append(emoji_token_buffer.pop(0))
        elif token.type == tokenize.NAME:
            if emoji_token_buffer:
                if not get_spaces_between(token, emoji_token_buffer[-1]):
                    emoji_token_buffer.append(token)
                    continue
                else:
                    line_buffer.extend(emoji_token_buffer)
                    emoji_token_buffer.clear()
            line_buffer.append(token)

        elif token.type == tokenize.STRING:
            import emoji

            token = tokenize.TokenInfo(
                token.type,
                emoji.emojize(token.string, use_aliases=True),
                token.start,
                token.end,
                token.line,
            )
            line_buffer.append(token)
        elif token.type == tokenize.ERRORTOKEN:
            possible_emoji = get_escaped_alias(token.string)
            if possible_emoji != token.string:
                emoji_buffer.append(
                    tokenize.TokenInfo(
                        tokenize.NAME,
                        possible_emoji.strip(":"),
                        token.start,
                        token.end,
                        token.line,
                    )
                )
                line_buffer.append(emoji_buffer[-1])
            else:
                line_buffer.append(token)
        elif token.type == tokenize.NEWLINE:
            line_buffer.extend(emoji_token_buffer)
            emoji_token_buffer.clear()
            line_buffer.append(token)
        else:
            line_buffer.append(token)

    # push whatever is left in the line buffer
    tokens.extend(line_buffer)

    # convert the tokens to a string

    return tokenize.untokenize(tokens).decode()


def load_ipython_extension(shell):
    shell.set_hook("complete_command", complete, re_key=".*:\S*")
    shell.input_transformer_manager.cleanup_transforms.append(emojize)


def unload_ipython_extension(shell):
    shell.input_transformer_manager.cleanup_transforms = [
        x
        for x in shell.input_transformer_manager.cleanup_transforms
        if x is not emojize
    ]
