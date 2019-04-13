#!/usr/bin/env python3

import re
import yaml

sam_template = './app-sam-template.yaml'
static_routes = './static_routes.yaml'
compiled_sam = './app-sam.yaml'

with open(sam_template) as f:
    sam = f.read()

with open(static_routes) as f:
    routes = yaml.load(f)

match_string = r'( +){{static_events}}'
indent = re.search(f'\n{match_string}\n', sam).group(1)

events = ''
for key, value in routes.items():
    events += '\n'.join([
        f'{indent}{key}:',
        f'{indent}  Type: Api',
        f'{indent}  Properties:',
        f'{indent}    RestApiId: !Ref BrwyattWeb',
        f'{indent}    Path: \'{value}\'',
        f'{indent}    Method: GET',
        '',
    ])

with open(compiled_sam, 'w') as f:
    f.write(re.sub(match_string, events, sam))
