#  Copyright (c) 2023 Roboto Technologies, Inc.

import argparse
import json
import sys

from ...domain.orgs import Org, OrgRole, OrgType
from ..command import (
    RobotoCommand,
    RobotoCommandSet,
)
from ..context import CLIContext


def create(args, context: CLIContext, parser: argparse.ArgumentParser):
    record = Org.create(
        creator_user_id=None,
        name=args.name,
        org_type=args.type,
        org_delegate=context.orgs,
        bind_email_domain=args.bind_email_domain,
    )
    sys.stdout.write(json.dumps(record.to_dict()) + "\n")


def create_setup_parser(parser):
    parser.add_argument(
        "--name", type=str, required=True, help="A human readable name for this org"
    )
    parser.add_argument(
        "--type",
        type=str,
        choices=OrgType._member_names_,
        help="The type of org you're creating",
    )

    parser.add_argument(
        "--bind-email-domain",
        action="store_true",
        help="Automatically add new users with your email domain to this org",
    )


def delete(args, context: CLIContext, parser: argparse.ArgumentParser):
    Org.by_org_id(org_id=args.org, org_delegate=context.orgs).delete()
    sys.stdout.write("Successfully deleted!\n")


def delete_setup_parser(parser):
    parser.add_argument(
        "--org",
        type=str,
        required=True,
        help="The org_id for the org you're about to delete.",
    )


def get(args, context: CLIContext, parser: argparse.ArgumentParser):
    record = Org.by_org_id(org_id=args.org, org_delegate=context.orgs)
    sys.stdout.write(json.dumps(record.to_dict()) + "\n")


def get_setup_parser(parser):
    parser.add_argument(
        "--org",
        type=str,
        required=True,
        help="The org_id for the org you want to see.",
    )


def list_orgs(args, context: CLIContext, parser: argparse.ArgumentParser):
    records = Org.by_user_id(user_id=None, org_delegate=context.orgs)
    for record in records:
        sys.stdout.write(json.dumps(record.to_dict()) + "\n")


def list_roles(args, context: CLIContext, parser: argparse.ArgumentParser):
    records = OrgRole.by_user_id(user_id=None, org_delegate=context.orgs)
    for record in records:
        sys.stdout.write(json.dumps(record.to_dict()) + "\n")


create_command = RobotoCommand(
    name="create",
    logic=create,
    setup_parser=create_setup_parser,
    command_kwargs={"help": "Creates a new organization"},
)


delete_command = RobotoCommand(
    name="delete",
    logic=delete,
    setup_parser=delete_setup_parser,
    command_kwargs={"help": "Deletes an existing organization"},
)


get_command = RobotoCommand(
    name="get",
    logic=get,
    setup_parser=get_setup_parser,
    command_kwargs={"help": "Gets metadata for a single organization"},
)


list_orgs_command = RobotoCommand(
    name="list-orgs",
    logic=list_orgs,
    command_kwargs={"help": "Lists the orgs that you're a member of"},
)


list_roles_command = RobotoCommand(
    name="list-roles",
    logic=list_roles,
    command_kwargs={
        "help": "Lists the roles that you have in orgs that you're a member of"
    },
)


commands = [
    create_command,
    delete_command,
    get_command,
    list_orgs_command,
    list_roles_command,
]

command_set = RobotoCommandSet(
    name="orgs",
    help="Commands for interacting with orgs.",
    commands=commands,
)
