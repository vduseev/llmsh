from functools import wraps
from typing import Any

import typer
from litellm.exceptions import (
    AuthenticationError,
    NotFoundError,
    BadRequestError,
    UnprocessableEntityError,
    Timeout,
    PermissionDeniedError,
    RateLimitError,
    ContextWindowExceededError,
    ContentPolicyViolationError,
    ServiceUnavailableError,
    APIError,
    APIConnectionError,
    APIResponseValidationError,
    OpenAIError,
    BudgetExceededError,
)

from llmsh.cli.renderer import console


_authentication_error = """[red]Authentication failed.[/red]
Please check your API key is set correctly and try again.
"""
_not_found_error = """[red]Not found.[/red]
Please check the model name and try again.
"""
_bad_request_error = """[red]Bad request.[/red]"""
_unprocessable_entity_error = """[red]Unprocessable entity.[/red]"""
_timeout_error = """[red]Timeout error.[/red]"""
_permission_denied_error = """[red]Permission denied.[/red]"""
_rate_limit_error = """[red]Rate limit exceeded.[/red]"""
_context_window_exceeded_error = """[red]Context window exceeded.[/red]"""
_content_policy_violation_error = """[red]Content policy violation.[/red]"""
_service_unavailable_error = """[red]Service unavailable.[/red]"""
_api_error = """[red]API error.[/red]
Invalid response object returned by the API.
"""
_api_connection_error = """[red]API connection error.[/red]
Possibility of incorrect request method being used.
"""
_api_response_validation_error = """[red]API response validation error.[/red]"""
_openai_error = """[red]OpenAI error.[/red]"""
_budget_exceeded_error = """[red]Budget exceeded.[/red]"""


def handle_exceptions(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        has_error_occurred = True
        result: Any = None
        try:
            result = f(*args, **kwargs)
            has_error_occurred = False
        except AuthenticationError as ae:
            console.print(_authentication_error)
            
        except NotFoundError as nfe:
            console.print(_not_found_error)

        except BadRequestError as bre:
            console.print(_bad_request_error)

        except UnprocessableEntityError as uee:
            console.print(_unprocessable_entity_error)
        
        except Timeout as t:
            console.print(_timeout_error)

        except PermissionDeniedError as pde:
            console.print(_permission_denied_error)

        except RateLimitError as rle:
            console.print(_rate_limit_error)

        except ContextWindowExceededError as cwee:
            console.print(_context_window_exceeded_error)

        except ContentPolicyViolationError as cpve:
            console.print(_content_policy_violation_error)

        except ServiceUnavailableError as sue:
            console.print(_service_unavailable_error)

        except APIError as ae:
            console.print(_api_error)

        except APIConnectionError as ace:
            console.print(_api_connection_error)

        except APIResponseValidationError as arve:
            console.print(_api_response_validation_error)

        except OpenAIError as oae:
            console.print(_openai_error)

        except BudgetExceededError as bee:
            console.print(_budget_exceeded_error)

        except Exception as e:
            console.print(f"[red]{e}[/red]")

        if has_error_occurred:
            raise typer.Exit(1)
        
        return result

    return wrapper
