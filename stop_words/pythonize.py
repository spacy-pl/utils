template = """
from __future__ import unicode_literals

STOP_WORDS = set(\"""{}\""".split())
"""

with open("data/stop_words.txt") as f:
    sw = f.read().split()

stop_words = "\n"
last_char = "a"
i = 0
for word in sw:
    if word[0] != last_char:
        stop_words += "\n\n"
        last_char = word[0]
        i = 0
    elif i % 10 == 9:
        stop_words += "\n"
    else:
        stop_words += " "
    i += 1
    stop_words += word
result = template.format(stop_words)


with open("data/stop_words.py", "w") as f:
    f.write(result)
