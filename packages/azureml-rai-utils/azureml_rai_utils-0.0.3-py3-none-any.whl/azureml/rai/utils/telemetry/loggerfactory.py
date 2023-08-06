# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

import json
import logging
import logging.handlers
import sys
import time
import traceback
from contextlib import contextmanager
from functools import wraps

import pkg_resources

AZ_ERROR = "azureml-telemetry package must be installed to use LoggerFactory"

try:
    from azureml.telemetry import get_telemetry_log_handler
    from azureml.telemetry.activity import ActivityLoggerAdapter, ActivityType
    from azureml.telemetry.activity import log_activity as _log_activity
    from azureml.telemetry.logging_handler import AppInsightsLoggingHandler
    azureml_telemetry_installed = True
except ImportError:
    azureml_telemetry_installed = False
    print(AZ_ERROR)

instrumentation_key = "8a122f06-112a-4c18-8c2f-711c7fb5780f"

try:
    DEFAULT_ACTIVITY_TYPE = ActivityType.INTERNALCALL
except NameError:
    DEFAULT_ACTIVITY_TYPE = "INTERNALCALL"

telemetry_enabled = True


class LoggerFactory:
    _module_name = None
    _module_version = None
    _component_name = None

    @staticmethod
    def get_logger(name, module_name, module_version, component_name,
                   verbosity=logging.DEBUG):
        if not azureml_telemetry_installed:
            raise ImportError(AZ_ERROR)
        LoggerFactory._module_name = module_name
        LoggerFactory._module_version = module_version
        LoggerFactory._component_name = component_name
        logger = logging.getLogger(__name__).getChild(name)
        logger.propagate = False
        logger.setLevel(verbosity)
        if not LoggerFactory._found_handler(logger,
                                            AppInsightsLoggingHandler):
            logger.addHandler(
                get_telemetry_log_handler(
                    component_name=component_name,
                    instrumentation_key=instrumentation_key,
                )
            )

        LoggerFactory.track_python_environment(logger)

        return logger

    @staticmethod
    def track_python_environment(logger):
        packages = pkg_resources.working_set
        payload = {d.project_name: d.version for d in packages}
        activity_logger = ActivityLoggerAdapter(
            logger, {"python_environment": json.dumps(payload)}
        )
        activity_logger.info("Logging python environment.")

    @staticmethod
    def track_activity(
        logger,
        activity_name,
        activity_type=DEFAULT_ACTIVITY_TYPE,
        input_custom_dimensions=None,
    ):
        component_name = LoggerFactory._component_name
        default_custom_dimensions = {"app_name": component_name}
        if input_custom_dimensions is not None:
            custom_dimensions = default_custom_dimensions.copy()
            custom_dimensions.update(input_custom_dimensions)
        else:
            custom_dimensions = default_custom_dimensions
        custom_dimensions.update(
            {
                "source": component_name,
                "moduleName": LoggerFactory._module_name,
                "moduleVersion": LoggerFactory._module_version,
            }
        )

        run_info = LoggerFactory._try_get_run_info()
        if run_info is not None:
            custom_dimensions.update(run_info)

        if telemetry_enabled:
            return _log_activity(
                logger, activity_name, activity_type, custom_dimensions
            )
        else:
            return _run_without_logging(
                logger, activity_name, activity_type, custom_dimensions
            )

    @staticmethod
    def _found_handler(logger, handler_type):
        for log_handler in logger.handlers:
            if isinstance(log_handler, handler_type):
                return True
        return False

    @staticmethod
    def _try_get_run_info():
        try:
            import os
            import re

            location = os.environ.get("AZUREML_SERVICE_ENDPOINT")
            location = re.compile("//(.*?)\\.").search(location).group(1)
        except Exception:
            location = os.environ.get("AZUREML_SERVICE_ENDPOINT", "")
        return {
            "subscription": os.environ.get("AZUREML_ARM_SUBSCRIPTION", ""),
            "run_id": os.environ.get("AZUREML_RUN_ID", ""),
            "resource_group": os.environ.get("AZUREML_ARM_RESOURCEGROUP", ""),
            "workspace_name": os.environ.get("AZUREML_ARM_WORKSPACE_NAME", ""),
            "experiment_id": os.environ.get("AZUREML_EXPERIMENT_ID", ""),
            "location": location,
        }


def track(
    get_logger,
    custom_dimensions=None,
    activity_type=DEFAULT_ACTIVITY_TYPE,
    force_flush=True,
):
    def monitor(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            logger = get_logger()
            try:
                with LoggerFactory.track_activity(
                    logger, func.__name__, activity_type, custom_dimensions
                ) as al:
                    try:
                        return func(*args, **kwargs)
                    except Exception as e:
                        # local logger
                        if type(al) == type(logger):
                            raise
                        al.activity_info["exception_type"] = str(type(e))
                        al.activity_info["stacktrace"] = "\n".join(
                            _extract_and_filter_stack(
                                e, traceback.extract_tb(sys.exc_info()[2])
                            )
                        )
                        raise
            except Exception:
                raise
            finally:
                msg = ("Wait 30s for application insights " +
                       "async channel to flush")
                if force_flush and logger.handlers:
                    for handler in logger.handlers:
                        handler.flush()
                        handler_name = type(handler).__name__
                        if handler_name == "AppInsightsLoggingHandler":
                            print(msg)
                            time.sleep(30)

        return wrapper

    return monitor


def _extract_and_filter_stack(e, traces):
    ret = [str(type(e))]

    for trace in traces:
        ret.append(
            f'File "{trace.filename}", line {trace.lineno} in {trace.name}')
        ret.append(f"  {trace.line}")
    return ret


@contextmanager
def _run_without_logging(logger, activity_name, activity_type,
                         custom_dimensions):
    yield logger
