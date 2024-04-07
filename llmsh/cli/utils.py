from pathlib import Path
from typing import Optional

import typer

from llmsh.cli.renderer import console
from llmsh.models.message import Message
from llmsh.settings import settings


def check_file_exists(path: Path) -> None:
    if not path.exists():
        console.print(f"[red]File not found: {path}[/red]")
        raise typer.Exit(1)
    
    if not path.is_file():
        console.print(f"[red]Given path is not a file: {path}[/red]")
        raise typer.Exit(1)


def safe_read_text(path: Path) -> str:
    try:
        with open(path) as f:
            return f.read()
    except Exception as e:
        console.print(f"[red]Error reading file: {path}[/red]")
        console.print(f"[red]{e}[/red]")
        raise typer.Exit(1)


def read_if_path(prompt: str) -> Optional[str]:
    result: str | None = None
    if prompt.startswith("@"):
        path = Path(prompt[1:])
        check_file_exists(path)
        result = safe_read_text(path)
    return result


def prepare_context(
    messages: list[Message],
    system: str,
    limit: Optional[int] = None,
) -> list[str]:
    prepared_messages = messages[-limit:] if limit else messages
    prepared_messages.insert(0, Message(role=settings.system_role, content=system))
    
    contexxt = [m.base() for m in prepared_messages]
    return contexxt


def get_user_prompt(prompt: str) -> str:
    result = ""
    if prompt.startswith("@"):
        prompt_file_path = Path(result[1:])
        check_file_exists(prompt_file_path)
        result = safe_read_text(prompt_file_path)
    return result


def strip_prompt(prompt: Optional[str]) -> str:
    if not prompt:
        return ""
    return prompt.strip().lower()


def quit_on_request(prompt: str) -> None:
    if strip_prompt(prompt) in ("exit", "quit"):
        raise typer.Exit()
