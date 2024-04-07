# Copyright 2024 Vagiz Duseev <vagiz@duseev.com>
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

import os
import sys
import threading

import litellm
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
from rich.live import Live
from rich.markdown import Markdown

from llmsh.cli import params, utils
from llmsh.cli.renderer import console
from llmsh.cli.error_handler import handle_exceptions
from llmsh.models.message import Message
from llmsh.settings import settings


litellm.suppress_debug_info = True


@handle_exceptions
def loop(
    prompt: params.prompt = settings.user_prompt,
    model: params.model = settings.model,
    system: params.system = settings.system_prompt,
    limit: params.limit = settings.limit,
    max_tokens: params.tokens = settings.max_tokens,
    no_stream: params.no_stream = settings.no_stream,
    interactive: params.interactive = settings.interactive,
):
    # Determine system prompt
    if text_from_file := utils.read_if_path(system):
        system = text_from_file

    # Determine initial prompt
    if text_from_file := utils.read_if_path(prompt):
        prompt = text_from_file

    is_pipe = not os.isatty(sys.stdin.fileno())
    if is_pipe:
        if interactive:
            # Pipe mode is not supported in chat mode.
            # This is because we can't switch to read user's input after
            # piping the initial input into the command.
            console.print("[red]Pipe mode is not supported in chat mode.[/red]")
            raise typer.Exit()
        
        # Read from pipe if available
        pipe_prompt = ""
        try:
            while True:
                pipe_prompt += input()
        except EOFError:
            pass

        # Append pipe prompt to the user prompt
        prompt += f"\n{pipe_prompt}"

    keyboard_interrupt_event = threading.Event()
    exit_event = threading.Event()
    in_progress_event = threading.Event()

    messages: list[Message] = []
    while True:
        keyboard_interrupt_event.clear()
        exit_event.clear()
        in_progress_event.clear()

        try:
            if not prompt:
                if interactive:
                    prompt = console.input("> ")
                else:
                    console.print("[red]Non-interactive mode requires a prompt.[/red]")
                    raise typer.Exit(1)
                
            # Quit if "exit" or "quit" is entered
            if interactive:
                utils.quit_on_request(prompt)

            # Prepare context
            messages.append(Message(role=settings.client_role, content=prompt))
            context = utils.prepare_context(
                messages=messages,
                system=system,
                limit=limit,
            )

            # Request a response from the model
            in_progress_event.set()
            response = litellm.completion(
                model=model,
                messages=context,
                stream=not no_stream,
                max_tokens=max_tokens,
            )

            if no_stream:
                # Record the arrived response
                content = response.choices[0].message.content or ""
                messages.append(Message(role=settings.server_role, content=content))

                # Render the markdown
                markdown = Markdown(content)
                console.print(markdown)

            else:
                # Record a new empty message
                messages.append(Message(role=settings.server_role, content=""))

                # Keep updating the markdown renderable with the response
                # as it comes in.
                markdown = Markdown(messages[-1].content)
                with Live(
                    markdown,
                    console=console,
                    refresh_per_second=4,
                    vertical_overflow="visible",
                ) as live:
                    try:
                        for chunk in response:
                            if (
                                keyboard_interrupt_event.is_set()
                                or exit_event.is_set()
                            ):
                                break

                            part = chunk.choices[0].delta.content or ""
                            messages[-1].content += part
                            markdown = Markdown(messages[-1].content)
                            live.update(markdown)

                    except KeyboardInterrupt:
                        # If the user presses Ctrl+C, we should stop the current
                        # response and start anew with the next prompt.
                        keyboard_interrupt_event.set()

            # Erase prompt
            prompt = ""
    
        except KeyboardInterrupt:
            # If the user presses Ctrl+C, we should stop the current
            # response and start anew with the next prompt.
            if in_progress_event.is_set():
                console.print("[blue]Press Ctrl+D (or Ctrl+Z on Windows) if you want to quit. Typing 'exit' or 'quit' has the same effect.[/blue]")

            continue

        except EOFError:
            # Quit gracefully on Ctrl+D (or Ctrl+Z on Windows)
            exit_event.set()
            break

        if not interactive:
            # Do not continue in prompt mode
            break
        

def run() -> None:
    typer_app = typer.Typer(add_completion=False)
    typer_app.command(
        "default",
        context_settings={
            "allow_extra_args": True,
            "help_option_names": ["-h", "--help"],
        }
    )(loop)
    typer_app()
