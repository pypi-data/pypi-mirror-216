# Copyright (c) 2021-2023, NVIDIA CORPORATION. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Definition of Pipeline module - Direct Acyclic Graph (DAG) of commands execution."""
import contextlib
import sys
import traceback
from typing import Any, Dict, List

from model_navigator.commands.base import CommandOutput, CommandStatus, ExecutionUnit
from model_navigator.configuration.common_config import CommonConfig
from model_navigator.core.package import Package
from model_navigator.core.status import Status
from model_navigator.exceptions import ModelNavigatorUserInputError
from model_navigator.logger import LOGGER, LoggingContext, StdoutLogger
from model_navigator.utils.common import pad_string


class Pipeline:
    """Definition of Direct Acyclic Graph (DAG) of commands execution."""

    def __init__(
        self,
        name: str,
        execution_units: List[ExecutionUnit],
    ):
        """Initialization of object.

        Args:
            name: Name of the pipeline
            execution_units: List of execution units objects
        """
        self.name = name
        self.id = name.lower().replace(" ", "_").replace("-", "_")
        self.execution_units = execution_units

    def run(self, config: CommonConfig, package: Package, **kwargs) -> Dict[str, Any]:
        """Execute pipeline.

        Args:
            config: A global config provided by user
            package: Package descriptor for collecting the pipeline execution status
            **kwargs: Additional keyword arguments

        Returns:
            Dictionary with shared parameters
        """
        LOGGER.info(pad_string(f"Pipeline {self.name!r} started"))
        shared_parameters = kwargs
        for execution_unit in self.execution_units:
            command_output = self._execute_unit(
                execution_unit=execution_unit, config=config, status=package.status, shared_parameters=shared_parameters
            )
            package._update_status(
                execution_unit=execution_unit,
                command_output=command_output,
                shared_parameters=shared_parameters,
            )
            if command_output.output is not None:
                shared_parameters.update(command_output.output)
                for name, value in command_output.output.items():
                    if name in config.__dataclass_fields__:
                        setattr(config, name, value)
        return shared_parameters

    def _execute_unit(
        self, execution_unit: ExecutionUnit, config: CommonConfig, status: Status, shared_parameters: Dict
    ) -> CommandOutput:
        """Execute a single unit.

        Args:
            execution_unit: A unit to execute
            shared_parameters: Parameters shared between execution units

        Returns:
            Command execution result
        """
        log_dir = (
            execution_unit.config.workspace / execution_unit.model_config.path.parent
            if execution_unit.model_config
            else None
        )

        if execution_unit.config.debug:
            redirect_stdout_context = StdoutLogger(LOGGER)
        else:
            redirect_stdout_context = contextlib.nullcontext()
        with LoggingContext(log_dir=log_dir), redirect_stdout_context:
            LOGGER.info(pad_string(f"Command {execution_unit.command.name()!r} started"))
            input_paramters = {
                **execution_unit.config.__dict__,
                **shared_parameters,
            }

            input_paramters.update(execution_unit.kwargs)
            if execution_unit.runner_cls:
                input_paramters["runner_cls"] = execution_unit.runner_cls
            if execution_unit.model_config:
                input_paramters.update(**execution_unit.model_config.get_config_dict_for_command())
            try:
                command_output = execution_unit.command(status).run(
                    **input_paramters
                )  # pytype: disable=not-instantiable
            except ModelNavigatorUserInputError as e:
                command_output = CommandOutput(status=CommandStatus.FAIL)

                if config.verbose and e.__context__:
                    LOGGER.info(e.__context__)

                error = traceback.format_exc()
                LOGGER.warning(
                    "Command finished with ModelNavigatorUserInputError. "
                    "The error is considered as external error. Usually caused by "
                    "incompatibilities between the model and the target formats and/or runtimes. "
                    "Please review the command output.\n"
                    f"{error}"
                )
            except Exception:
                command_output = CommandOutput(status=CommandStatus.FAIL)
                error = traceback.format_exc()
                LOGGER.error(f"Command finished with unexpected error: {error}")

            if command_output.status == CommandStatus.FAIL and execution_unit.command.is_required():
                sys.exit("The required command has failed. Please, review the log and verify the reported problems.")

            return command_output
