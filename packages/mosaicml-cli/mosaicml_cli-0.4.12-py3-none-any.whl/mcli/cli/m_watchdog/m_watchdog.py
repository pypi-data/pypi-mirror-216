"""mcli watchdog endpoint"""
from __future__ import annotations

import argparse
import logging
# from http import HTTPStatus
from typing import Optional

from mcli.api.exceptions import cli_error_handler
from mcli.api.model.run import Run, RunStatus
from mcli.api.runs.api_get_runs import get_run
from mcli.api.runs.api_update_run import update_run
from mcli.utils.utils_logging import OK

logger = logging.getLogger(__name__)

# pylint: disable-next=invalid-name
WATCHDOG_EXAMPLES = """

Examples:

# Enable watchdog for a run
> mcli watchdog hero-run-1234

# Disable watchdog for a run
> mcli watchdog hero-run-1234 --disable
"""


@cli_error_handler('mcli watchdog')
def watchdog_entrypoint(
    run_name: str,
    disable: Optional[bool] = False,
    **kwargs,
):
    del kwargs
    return watchdog(run_name=run_name, disable=disable)


# pylint: disable-next=too-many-statements
def watchdog(
    run_name: str,
    disable: Optional[bool] = False,
    **kwargs,
) -> int:
    del kwargs

    run: Run = get_run(run=run_name)

    if run.status in [RunStatus.FAILED, RunStatus.STOPPED, RunStatus.TERMINATING, RunStatus.COMPLETED]:
        logger.warning(f"Run {run.name} is already in a terminal state. Try enabling watchdog for an active run.")
        return 1

    if disable:
        update_run(run, {'retryOnSystemFailure': False})
        logger.info(f'{OK} Disabled watchdog for run: {run_name}. If a system failure is thrown, '
                    'your run will not be retried.')
        return 0

    update_run(run, {'retryOnSystemFailure': True})
    logger.info(f'{OK} Enabled watchdog for run: {run_name}. If a system failure is thrown, your run '
                'will automatically be retried.')
    return 0


def _configure_argparser(parser: argparse.ArgumentParser) -> argparse.ArgumentParser:
    parser.add_argument('run_name', type=str, help='The name of the run')
    parser.add_argument(
        '--disable',
        action='store_true',
        default=False,
        dest='disable',
        help='Disable watchdog for a run',
    )
    parser.set_defaults(func=watchdog_entrypoint, parser=parser)
    return parser


def add_watchdog_argparser(subparser: argparse._SubParsersAction,) -> argparse.ArgumentParser:
    watchdog_parser: argparse.ArgumentParser = subparser.add_parser(
        'watchdog',
        description='Enable or disable watchdog on an existing training run. Enabling '
        'this will automatically resume the run if there is a system failure (i.e. node failure). '
        'To disable watchdog, pass the --disable flag. By default, watchdog is disabled.',
        help='Enable or disable watchdog on a run',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=WATCHDOG_EXAMPLES,
    )
    return _configure_argparser(parser=watchdog_parser)
