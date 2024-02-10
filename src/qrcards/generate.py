import re
import yaml
from segno import helpers

def slugify(s):
  slug = re.sub(r'[^a-zA-Z0-9]+', '-', s)
  return slug.lower()

def generate():
  addresses = []
  with open('addresses.yml', 'r') as stream:
    try:
      addresses = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
      print(exc)

  for address in addresses:
    name = address['name']
    qrcode = helpers.make_vcard(name=name, displayname=address['display'],
                                email=address['emails'], phone=address['phones'],
                                url=address['urls'])
    qrcode.save(f'cards/{slugify(name)}.svg', scale=4)
