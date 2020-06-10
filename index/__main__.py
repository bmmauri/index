import argparse
import json
import jsonschema
import os
import yaml

from index import core

parse = argparse.ArgumentParser(description="Manual chess plan")
parse.add_argument("schema", help="JSON schema")
parse.add_argument("document", help="YAML document")
args = parse.parse_args()

if not os.path.isfile(args.schema) or not os.path.isfile(args.document):
    raise FileNotFoundError

_SCHEMA = json.load(open(args.schema))
_DOCUMENT = yaml.safe_load(open(args.document))

# validation
jsonschema.validate(_DOCUMENT, _SCHEMA)

# index
document = core.Index(document=_DOCUMENT)
print(document.get_exercise_training())
