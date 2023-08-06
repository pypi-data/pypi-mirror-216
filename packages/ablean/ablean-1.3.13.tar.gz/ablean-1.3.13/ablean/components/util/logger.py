# QUANTCONNECT.COM - Democratizing Finance, Empowering Individuals.
# Lean CLI v1.0. Copyright 2021 QuantConnect Corporation.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import platform
import sys
from typing import Any, List, Optional

import click
import maskpass
from rich.console import Console
from rich.progress import BarColumn, Progress, TextColumn

from ablean.models.pydantic import Option


class Logger:
    """The Logger class handles all output printing."""

    def __init__(self) -> None:
        """Creates a new Logger instance."""
        # In Docker the terminal size is unknown, so we disable rich's text wrapping by setting width to a high value
        if os.environ.get("QC_LOCAL_GUI", "false") == "true":
            width = 999999
        else:
            width = None

        self._console = Console(markup=False, highlight=False, emoji=False, width=width)
        self.debug_logging_enabled = False

    def debug(self, message: Any) -> None:
        """Logs a debug message if debug logging is enabled.

        :param message: the message to log
        """
        if self.debug_logging_enabled:
            self._console.print(message, style="grey50")

    def info(self, message: Any) -> None:
        """Logs an info message.

        :param message: the message to log
        """
        self._console.print(message)

    def warn(self, message: Any) -> None:
        """Logs a warning message.

        :param message: the message to log
        """
        self._console.print(message, style="yellow")

    def error(self, message: Any) -> None:
        """Logs an error message.

        :param message: the message to log
        """
        self._console.print(message, style="red")

    def progress(
        self, prefix: str = "", suffix: str = "{task.percentage:0.0f}%"
    ) -> Progress:
        """Creates a Progress instance.

        :param prefix: the text to show before the bar (defaults to a blank string)
        :param suffix: the text to show after the bar (defaults to the task's percentage)
        :return: a Progress instance which can be used to display progress bars
        """
        progress = Progress(
            TextColumn(prefix), BarColumn(), TextColumn(suffix), console=self._console
        )
        progress.start()
        return progress

    def prompt_list(
        self,
        text: str,
        options: List[Option],
        default: Optional[str] = None,
        multiple: bool = False,
    ) -> Any:
        """Asks the user to select an option from a list of possible options.

        The user will not be prompted for input if there is only a single option.

        :param text: the text to display before prompting
        :param options: the available options
        :param default: the default value if no input is given
        :return: the chosen option's id
        """

        def validate_option(input_value: Any):
            try:
                index = int(input_value)
                if 0 < index <= len(options):
                    return options[index - 1].id
            except ValueError:
                option = next(
                    (option for option in options if option.label == input_value), None
                )
                if option is not None:
                    return option.id

            self.info("Please enter the number or label of an option")

        if len(options) == 1:
            self.info(f"{text}: {options[0].label}")
            return options[0].id

        self.info(f"{text}:")
        for i, option in enumerate(options):
            self.info(f"{i + 1}) {option.label}")

        while True:
            if not multiple:
                user_input = click.prompt(
                    "Enter an option", type=str, default=default, show_default=True
                )
                user_selected_value = validate_option(user_input)
                if user_selected_value is not None:
                    return user_selected_value
            else:
                user_selected_values = []
                user_inputs = click.prompt(
                    "To enter multiple options, seprate them with comma.",
                    type=str,
                    default=default,
                    show_default=True,
                )
                user_inputs = str(user_inputs).strip(",").split(",")
                expected_outputs = len(user_inputs)
                for user_input in user_inputs:
                    user_selected_value = validate_option(user_input)
                    if user_selected_value is not None:
                        user_selected_values.append(user_selected_value)
                if len(user_selected_values) == expected_outputs:
                    return user_selected_values

    def prompt_password(self, text: str, default: Optional[str] = None) -> str:
        """Asks the user for a string value while masking the given input.

        :param text: the text to display before prompting
        :param default: the default value if no input is given
        :return: the given input
        """
        if default is not None:
            text = f"{text} [{'*' * len(default)}]"

        # Masking does not work properly in WSL2 and when the input is not coming from a keyboard
        if "microsoft" in platform.uname().release.lower() or not sys.stdin.isatty():
            return click.prompt(text, default=default, show_default=False)

        while True:
            user_input = maskpass.askpass(f"{text}: ")

            if len(user_input) == 0 and default is not None:
                return default

            if len(user_input) > 0:
                return user_input
