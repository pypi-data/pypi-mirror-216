#  Copyright (c) 2023 Roboto Technologies, Inc.

import argparse
import json
import os
import pathlib


def JsonFileOrStrType(arg):
    arg_type = "string"

    if os.path.isfile(arg):
        arg_type = "file"
        with open(arg, "r") as f:
            payload = f.read()
    else:
        payload = arg

    try:
        return json.loads(payload)
    except ValueError:
        raise argparse.ArgumentTypeError(
            "Could not interpret payload {} '{}' as JSON".format(arg_type, arg)
        )


class KeyValuePairsAction(argparse.Action):
    value_dict: dict[str, str] = {}

    def __call__(self, parser, namespace, values, option_string):
        for pair in values:
            key, value = pair.split("=")
            if key in self.value_dict:
                raise parser.error(
                    f"Key '{key}' was defined multiple times for '{self.dest}'"
                )
            self.value_dict[key] = value

        setattr(namespace, self.dest, self.value_dict)


def ExistingPathlibPath(arg):
    path = pathlib.Path(arg)
    if not path.exists():
        raise argparse.ArgumentTypeError(f"Provided path '{arg}' does not exist!")
    return path
