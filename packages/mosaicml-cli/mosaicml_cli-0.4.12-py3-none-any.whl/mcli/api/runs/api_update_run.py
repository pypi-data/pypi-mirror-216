""" Update the data of a run. """
from __future__ import annotations

from concurrent.futures import Future
from typing import Any, Dict, Optional, Union, overload

from typing_extensions import Literal

from mcli.api.engine.engine import get_return_response, run_singular_mapi_request
from mcli.api.model.run import Run
from mcli.config import MCLIConfig

__all__ = ['update_run']

QUERY_FUNCTION = 'updateRun'
VARIABLE_DATA_GET_RUNS = 'getRunsData'
VARIABLE_DATA_UPDATE_RUN = 'updateRunData'
QUERY = f"""
mutation UpdateRun(${VARIABLE_DATA_GET_RUNS}: GetRunsInput!, ${VARIABLE_DATA_UPDATE_RUN}: UpdateRunInput!) {{
  {QUERY_FUNCTION}({VARIABLE_DATA_GET_RUNS}: ${VARIABLE_DATA_GET_RUNS}, {VARIABLE_DATA_UPDATE_RUN}: ${VARIABLE_DATA_UPDATE_RUN}) {{
    id
    name
    createdByEmail
    status
    createdAt
    startedAt
    completedAt
    updatedAt
    reason
    priority
    maxRetries
    preemptible
    retryOnSystemFailure
    resumptions {{
        clusterName
        cpus
        gpuType
        gpus
        nodes
        executionIndex
        startTime
        endTime
        status
    }}
  }}
}}"""


@overload
def update_run(run: Union[str, Run],
               update_run_data: Dict[str, Any],
               *,
               timeout: Optional[float] = 10,
               future: Literal[False] = False) -> Run:
    ...


@overload
def update_run(run: Union[str, Run],
               update_run_data: Dict[str, Any],
               *,
               timeout: Optional[float] = None,
               future: Literal[True] = True) -> Future[Run]:
    ...


def update_run(run: Union[str, Run],
               update_run_data: Dict[str, Any],
               *,
               timeout: Optional[float] = 10,
               future: bool = False):
    """Update a run's data in the MosaicML platform.

    Args:
        run (``Optional[str | ``:class:`~mcli.api.model.run.Run` ``]``):
            A run or run name to update. Using :class:`~mcli.api.model.run.Run` objects is most
            efficient. See the note below.
        update_run_data (`Dict[str, Any]`): The data to update the run with. This can include
            `preemptible`, `priority`, `maxRetries`, and `retryOnSystemFailure`. Keys not specified in this
            dictionary will not be modified.
        timeout (``Optional[float]``): Time, in seconds, in which the call should complete.
            If the call takes too long, a :exc:`~concurrent.futures.TimeoutError`
            will be raised. If ``future`` is ``True``, this value will be ignored.
        future (``bool``): Return the output as a :class:`~concurrent.futures.Future`. If True, the
            call to :func:`update_run` will return immediately and the request will be
            processed in the background. This takes precedence over the ``timeout``
            argument. To get the list of :class:`~mcli.api.model.run.Run` output,
            use ``return_value.result()`` with an optional ``timeout`` argument.

    Raises:
        MAPIException: Raised if updating the requested run failed

    Returns:
        If future is False:
            Updated :class:`~mcli.api.model.run.Run` object
        Otherwise:
            A :class:`~concurrent.futures.Future` for the list
    """
    variables = {
        VARIABLE_DATA_GET_RUNS: {
            'filters': {
                'name': {
                    'in': [run.name if isinstance(run, Run) else run]
                },
            }
        },
        VARIABLE_DATA_UPDATE_RUN: update_run_data,
    }

    cfg = MCLIConfig.load_config()
    if cfg.user_id:
        variables[VARIABLE_DATA_GET_RUNS]['entity'] = {
            'userIds': [cfg.user_id],
        }

    response = run_singular_mapi_request(
        query=QUERY,
        query_function=QUERY_FUNCTION,
        return_model_type=Run,
        variables=variables,
    )
    return get_return_response(response, future=future, timeout=timeout)
