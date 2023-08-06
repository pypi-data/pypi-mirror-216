import argparse
import sys


class CustomHelpFormatter(argparse.HelpFormatter):
    def _format_action_invocation(self, action):
        if not action.option_strings or action.nargs == 0:
            return super()._format_action_invocation(action)
        default = self._get_default_metavar_for_optional(action)
        args_string = self._format_args(action, default)

        # Align the args_string with the maximum width
        option_strings = (', '.join(action.option_strings)).ljust(17)

        return option_strings + ' ' + args_string

    def format_help(self):
        help_text = super().format_help()
        return help_text + '\n'  # Append an empty line at the end

    def __init__(self, prog):
        super().__init__(prog, max_help_position=40, width=100)


class CustomArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        self.print_usage(sys.stderr)
        error_message = message + '\n'  # Add an empty line after the error message
        self.exit(2, '%s: error: %s\n' % (self.prog, error_message))
