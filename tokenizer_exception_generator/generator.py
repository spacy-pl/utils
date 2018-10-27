from html.parser import HTMLParser
import xml.etree.ElementTree as ET
import sre_yield
import re


class Rule:
    """
    Same structure as Segment's
    """

    def __init__(self, breaking: bool, before_pattern_str: str = None, after_pattern_str: str = None):
        self.breaking = breaking
        self.before_pattern_str = before_pattern_str
        self.after_pattern_str = after_pattern_str

    def __str__(self):
        return f"breaking: {self.breaking} | before: {self.before_pattern_str} | after: {self.after_pattern_str}"


class MyHTMLParser(HTMLParser):
    def __init__(self):
        self.exceptions = []
        super().__init__()

    def handle_data(self, data):
        self.exceptions += [data]


def get_rules_from_xml(filename='segment.srx'):
    tree = ET.parse(filename)  # parse XML file
    root = tree.getroot()  # access file's root

    polish_rules = root[1][0][1]  # this is not a nice solution, but a working one
    # Other languagerule nodes that may interest us are GeneralImportant, ByLineBreak, ByTwoLineBreaks

    rules = []
    for rule in polish_rules:
        # a rule looks like this:
        # tag: rule, attrib: {'break': 'yes' or 'no'}
        # |- tag: beforebreak, tag.text: <regex>
        # |- tag: afterbreak, tag.text: <regex>
        #

        breaking = True if rule.attrib['break'] == 'yes' else False
        before_pattern_str = rule[0].text
        after_pattern_str = rule[1].text
        rules += [Rule(breaking, before_pattern_str, after_pattern_str)]

    return rules


def parse_html(filename):
    parser = MyHTMLParser()

    exc_ = []

    with open(filename, 'r', encoding="utf8") as f:
        parser.feed(f.read())

        for e in parser.exceptions:
            if e != '\n' and e.endswith('.'):
                exc_ += [e]

    return exc_


rules = get_rules_from_xml()

exception_rules = []

for rule in rules:
    if not rule.breaking and rule.after_pattern_str is None or rule.after_pattern_str == "":
        exception_rules += [rule]

pl_lowercase = u'aąbcćdeęfghijklłmnńoóprsśtuwyzźż'
pl_uppercase = pl_lowercase.upper()

final_exceptions = []

for rule in exception_rules:

    # replace unicode properties with standard regex
    pattern = rule.before_pattern_str\
        .replace("\p{Lu}", "[" + pl_uppercase + "]")\
        .replace("\p{Ll}", "[" + pl_lowercase + "]")\
        .replace("(?iu)", "")

    if '+' in pattern:
        continue
    try:
        a = list(sre_yield.AllStrings(pattern))
        final_exceptions += a

    except:
        print(f"Error in {rule}")

excluded_characters = ['\\', '\t', '\x0b', '\b', '\r', '\x0c', '\n', ')', '(', ',']

# filter out exceptions that contain characters such as \r, remove trailing spaces
# for example, for each X. X. type rule there was a X.\rX. rule in the XML file
final_exceptions = [a.rstrip("\n\r ").lstrip(" ") for a in final_exceptions if not any(exc in a for exc in excluded_characters)]

# filter out exceptions that don't contain any letters
final_exceptions = [fe for fe in final_exceptions if re.search(f'.*[{pl_lowercase}{pl_uppercase}].*', fe)]

# avoid duplicates
final_exceptions = set(final_exceptions)

# merge with exceptions from wikipedia
for fn in [f'skroty{i}.html' for i in range(1,4)]:
    tmp = parse_html(fn)
    tmp = set(tmp)
    final_exceptions |= tmp

# convert back to a sorted list
final_exceptions = sorted(list(final_exceptions))

with open('exception_list.py', 'w+', encoding='utf-8') as f:
    f.write('polish_exceptions = ')
    f.write(str(final_exceptions))
