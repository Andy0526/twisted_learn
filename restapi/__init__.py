# -*- coding: utf-8 -*-

import re

pattern = '^a...s$'
result = re.match(pattern, 'abyss')
print result.group()

pattern = '[abc]'
for s in ['a', 'ac', 'Hey Jude', 'abc de ca']:
    result = re.match(pattern, s)
    if result:
        print s, result.group()

pattern = '(a|b|c)xz'
for s in ['ab xz', 'abxz', 'abxz', 'axz cabxz']:
    result = re.search(pattern, s)
    if result:
        print s, result.groups()

pattern = r'Python'

for s in ['I like Python', 'I like Python']:
    result = re.findall(pattern, s)
    print result
