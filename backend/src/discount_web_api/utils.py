from functools import wraps
import logging
from re import I

from django.http import HttpResponse, JsonResponse

from .exceptions import DiscountAppException

logger = logging.getLogger(__name__)


def activity_monitor(monitor):
    """Create a decorator that logs function calls using the provided monitor."""

    def log_activity(func):
        @wraps
        def _log_activity(*args, **kwargs):
            # monitor.emit()
            return func(*args, **kwargs)


def handle_error(func):
    """Decorator that generates a 500 error msg for unhandled exceptions."""

    @wraps
    def _handle_error(*args, **kwargs):
        try:

            return func(*args, **kwargs)

        except DiscountAppException:
            logger.exception("Application failure.")
            return JsonResponse(
                "Application Failure. See logs for more information.", status=400
            )

        except:
            logger.exception("Unhandled exception.")
            return JsonResponse(
                "Internal Failure. See logs for more information.", status=500
            )
