#  Copyright (c) 2023 Roboto Technologies, Inc.
import argparse
from typing import Any, Callable

from ..context import CLIContext


class RobotoCommand(object):
    _name: str
    _logic: Callable[
        [Any, CLIContext, argparse.ArgumentParser], None
    ]  # Args, CLIContext
    _inner_setup_parser: Callable[[Any], None] | None  # Parser
    _command_kwargs: dict[str, Any] | None

    def __init__(
        self,
        name: str,
        logic: Callable[[Any, CLIContext, argparse.ArgumentParser], None],
        command_kwargs: dict | None,
        setup_parser: Callable[[Any], None] | None = None,
    ):
        self._name = name
        self._logic = logic
        self._inner_setup_parser = setup_parser
        self._command_kwargs = command_kwargs

    @property
    def name(self):
        return self._name

    @property
    def command_kwargs(self):
        if self._command_kwargs is not None:
            return self._command_kwargs
        return {}

    def setup_parser(self, parser, context):
        def context_aware_logic(args):
            return self._logic(args, context, parser)

        parser.set_defaults(func=context_aware_logic)
        if self._inner_setup_parser is not None:
            self._inner_setup_parser(parser)


class RobotoCommandSet(object):
    _name: str
    _help: str
    _commands: list[RobotoCommand]
    _context: CLIContext | None

    def __init__(self, name, help, commands):
        self._name = name
        self._help = help
        self._commands = commands

    def add_to_subparsers(self, parent_subparsers, context: CLIContext):
        self._context = context

        command_set_parser = parent_subparsers.add_parser(self._name, help=self._help)
        subparsers = command_set_parser.add_subparsers()
        subparsers.required = True

        for command in self._commands:
            command_parser = subparsers.add_parser(
                command.name, **command.command_kwargs
            )
            command.setup_parser(command_parser, context)
