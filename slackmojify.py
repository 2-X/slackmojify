import sys
import pyperclip

from text_mappings import big_letter_templates


def is_slackmoji(some_text):
    """Determines if some text is a slackmoji (i.e. starts and ends with `:`).

    Args:
        some_text (str): The text to check.

    Returns:
        bool: Whether or not the given text is a slackmoji.

    Examples:
        >>> is_slackmoji(":smile:")
        True
        >>> is_slackmoji(":smile")
        False
    """
    return some_text.startswith(":") and some_text.endswith(":")


def fix_slackmoji(some_text):
    """Turn some text into a slackmoji.

    Args:
        some_text (str): The text to convert.

    Returns:
        str: The given text as a slackmoji.

    Examples:
        >>> fix_slackmoji(":smile:")
        :smile:
        >>> fix_slackmoji(":smile")
        :smile:
        >>> fix_slackmoji("smile")
        :smile:
    """
    start_colon = ("" if some_text.startswith(":") else ":")
    end_colon = ("" if some_text.endswith(":") else ":")
    return start_colon + some_text + end_colon

def slackmojify(foreground_emoji, background_emoji, text, horizontal=False):
    """Convert the text into a giant slackmoji art.

    The slackmoji art is made out of the provided slackmojis

    Args:
        foreground_emoji (str): The slackmoji that will make up the text.
        background_emoji (str): The slackmoji that will serve as the background.
        text (str): The text to convert to giant slackmoji art.

    Returns:
        str: A series of slackmoji text formatted to produce the supplied text
            when sent in Slack.

    Notes:
        If the input text is too long the slackmoji art will not show
        up correctly!

    Examples:
        >>> slackmojify(":smile:", ":heart:", "a")
        ":heart::heart::heart::heart::heart::heart::heart::heart::heart:
        :heart::heart::heart::smile::smile::heart::heart::heart::heart:
        :heart::heart::smile::heart::heart::smile::heart::heart::heart:
        :heart::heart::smile::heart::heart::smile::heart::heart::heart:
        :heart::heart::smile::smile::smile::smile::heart::heart::heart:
        :heart::heart::smile::heart::heart::smile::heart::heart::heart:
        :heart::heart::smile::heart::heart::smile::heart::heart::heart:
        :heart::heart::smile::heart::heart::smile::heart::heart::heart:
        :heart::heart::heart::heart::heart::heart::heart::heart::heart:"
    """

    # ensure values are slackmojis
    foreground_emoji = fix_slackmoji(foreground_emoji)
    background_emoji = fix_slackmoji(background_emoji)

    # init each row to match the height of the letters
    rows = [""] * len(big_letter_templates["a"].split("\n"))

    def add_letter_horizontal(letter, lines):
        new_lines = []

        # add the letter's line to each line
        letter_text = big_letter_templates[letter.lower()].split("\n")
        for line, add_text in zip(lines, letter_text):
            new_line = line + add_text
            new_lines.append(new_line)

        # add some padding between letters
        return new_lines
    
    def add_letter_vertical(letter, lines):
        # add the letter's line to each line
        letter_text = big_letter_templates[letter.lower()].split("\n")

        letter_text = [background_emoji + t + background_emoji for t in letter_text]
        
        # add some padding between letters
        return lines + letter_text

    # pick the direction to add letters
    if horizontal:
        # add padding
        rows = add_letter_horizontal(" ", rows)
        # run add_letter over our text
        for char in text:
            rows = add_letter_horizontal(char, rows)

            # add space between letters
            if char != " ":
                rows = add_letter_horizontal("|", rows)
        # add padding
        rows = add_letter_horizontal(" ", rows)
    else:
        # run add_letter over our text
        for char in text:
            rows = add_letter_vertical(char, rows)

    # replace `-` with background and `X` with foreground emojis
    rows = [
        line.replace("-", background_emoji).replace("X", foreground_emoji)
        for line in rows
    ]

    # turn array into string
    emoji_text = "\n".join(rows)

    # set our clipboard to this text
    pyperclip.copy(emoji_text)

    # inform the user
    print((
        f"The slackmoji text for '{text}' using '{foreground_emoji}' on"
        f"'{background_emoji}' has been copied to your clipboard."
    ))


def main(sys_args):
    slackmojify(sys_args[0], sys_args[1], " ".join(sys_args[2:]))


# run some command like:
# >>> make_slackmoji_text.py :evilparrot: :sadparrot: goodbye
if __name__ == "__main__":
    main(sys.argv[1:])

