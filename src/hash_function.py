LETTER_GROUPS = {
    1: ['а', 'б'],
    2: ['в', 'г', 'ґ', 'д', 'е', 'є'],
    3: ['ж', 'з', 'и', 'і', 'ї', 'й'],
    4: ['к', 'л', 'м'],
    5: ['н', 'о', 'п'],
    6: ['р', 'с', 'т'],
    7: ['у', 'ф', 'х'],
    8: ['ц', 'ч', 'ш', 'щ'],
    9: ['ь', 'ю', 'я']
}

def build_letter_map():
    mapping = {}
    for code, letters in LETTER_GROUPS.items():
        for letter in letters:
            mapping[letter] = code
    return mapping

LETTER_MAP = build_letter_map()

def encode_name(name: str, max_letters: int = 3, total_length: int = 10) -> str:
    name = name.lower()
    hash_code = ""

    for i in range(max_letters):
        if i < len(name):
            letter = name[i]
            digit = LETTER_MAP.get(letter, 0)
        else:
            digit = 0
        hash_code += str(digit)

    middle_fill = total_length - max_letters - 2
    hash_code += "0" * middle_fill

    name_length = min(len(name), 99)
    hash_code += f"{name_length:02d}"

    return hash_code

def hash_name(name: str) -> int:
    return int(encode_name(name))
