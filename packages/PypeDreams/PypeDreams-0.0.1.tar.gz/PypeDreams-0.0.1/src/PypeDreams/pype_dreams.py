import hashlib
from PypeDreams.compress import compress
from PypeDreams.adjectives import adjectives
from PypeDreams.animals import animals
from PypeDreams.colors import colors
from PypeDreams.clothing import clothing

def to_styled(words, style):
    styled_words = []
    if style == 'titlecase':
        for word in words:
            styled_words.append(word.title())
    elif style == 'lowercase':
        for word in words:
            styled_words.append(word.lower())
    elif style == 'uppercase':
        for word in words:
            styled_words.append(word.upper())
    else:
        raise ValueError('Unknown style')
    return styled_words


def pype_dreamer(input, style='titlecase', separator=' '):
    hex_digest = hashlib.md5(input.encode(encoding = 'UTF-8', errors = 'strict')).hexdigest()
    pairs = [hex_digest[i:i+2] for i in range(0, len(hex_digest), 2)]
    bytes = [int(pair, 16) for pair in pairs]
    compressed = compress(bytes, 4)



    adjective = adjectives[compressed[0]]
    color = colors[compressed[1]]
    animal = animals[compressed[2]]
    clothes = clothing[compressed[3]]
    additional_text = 'wearing'
    styled_words = to_styled([adjective, color, animal, additional_text, clothes], style)


    return styled_words[0] + separator + styled_words[1] + separator + styled_words[2] + separator + styled_words[3] + separator + 'a' + separator + styled_words[4]



