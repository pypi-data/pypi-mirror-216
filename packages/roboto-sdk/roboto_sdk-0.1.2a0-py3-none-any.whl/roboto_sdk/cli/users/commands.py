#  Copyright (c) 2023 Roboto Technologies, Inc.

import argparse
import json
import sys

from ..command import (
    RobotoCommand,
    RobotoCommandSet,
)
from ..context import CLIContext


def whoami(args, context: CLIContext, parser: argparse.ArgumentParser):
    sys.stdout.write(
        json.dumps(context.http.get(context.http.url("v1/users/whoami")).from_json())
        + "\n"
    )


whoami_command = RobotoCommand(
    name="whoami",
    logic=whoami,
    command_kwargs={"help": "Gets detailed identity information about the caller."},
)

commands = [whoami_command]

command_set = RobotoCommandSet(
    name="users",
    help="Commands for obtaining information about yourself or other users.",
    commands=commands,
)
