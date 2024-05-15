def convertBytes(sz) -> str:
    if not sz:
        return ""
    sz = int(sz)
    ind = 0
    Units = {0: " ", 1: "K", 2: "M", 3: "G", 4: "T", 5: "P", 6: "E", 7: "Z", 8: "Y"}
    while sz > 2**10:
        sz /= 2**10
        ind += 1
    return f"{round(sz, 2)} {Units[ind]}B"


def convertTime(s: int) -> str:
    mss = s * 1000
    s, ms = divmod(mss, 1000)
    m, s = divmod(s, 60)
    hr, m = divmod(m, 60)
    days, hr = divmod(hr, 24)
    convertedTime = (
        (f"{int(days)}days, " if days else "")
        + (f"{int(hr)}h, " if hr else "")
        + (f"{int(m)}m, " if m else "")
        + (f"{int(s)}s, " if s else "")
    )
    return convertedTime[:-2]


font_dict = {
    "sans bold": {
        "a": "𝙖",
        "b": "𝙗",
        "c": "𝙘",
        "d": "𝙙",
        "e": "𝙚",
        "f": "𝙛",
        "g": "𝙜",
        "h": "𝙝",
        "i": "𝙞",
        "j": "𝙟",
        "k": "𝙠",
        "l": "𝙡",
        "m": "𝙢",
        "n": "𝙣",
        "o": "𝙤",
        "p": "𝙥",
        "q": "𝙦",
        "r": "𝙧",
        "s": "𝙨",
        "t": "𝙩",
        "u": "𝙪",
        "v": "𝙫",
        "w": "𝙬",
        "x": "𝙭",
        "y": "𝙮",
        "z": "𝙯",
        "A": "𝘼",
        "B": "𝘽",
        "C": "𝘾",
        "D": "𝘿",
        "E": "𝙀",
        "F": "𝙁",
        "G": "𝙂",
        "H": "𝙃",
        "I": "𝙄",
        "J": "𝙅",
        "K": "𝙆",
        "L": "𝙇",
        "M": "𝙈",
        "N": "𝙉",
        "O": "𝙊",
        "P": "𝙋",
        "Q": "𝙌",
        "R": "𝙍",
        "S": "𝙎",
        "T": "𝙏",
        "U": "𝙐",
        "V": "𝙑",
        "W": "𝙒",
        "X": "𝙓",
        "Y": "𝙔",
        "Z": "𝙕",
    }
    #'': {'a': '', 'b': '', 'c': '', 'd': '', 'e': '', 'f': '', 'g': '', 'h': '', 'i': '', 'j': '', 'k': '', 'l': '', 'm': '', 'n': '', 'o': '', 'p': '', 'q': '', 'r': '', 's': '', 't': '', 'u': '', 'v': '', 'w': '', 'x': '', 'y': '', 'z': ''}
    #              'A': '', 'B': '', 'C': '', 'D': '', 'E': '', 'F': '', 'G': '', 'H': '', 'I': '', 'J': '', 'K': '', 'L': '', 'M': '', 'N': '', 'O': '', 'P': '', 'Q': '', 'R': '', 'S': '', 'T': '', 'U': '', 'V': '', 'W': '', 'X': '', 'Y': '', 'Z': ''}
}


def change_font(text, name="sans bold"):
    return text.translate(str.maketrans(font_dict[name.lower()]))
