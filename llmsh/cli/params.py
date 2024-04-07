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

from typing import Optional
from typing_extensions import Annotated

import typer


prompt = Annotated[
    Optional[str],
    typer.Argument(
        help="Prompt message or a path to file, when started with @.",
        show_default=False,
    ),
]
model = Annotated[
    str,
    typer.Option(
        "--model",
        "-m",
        help="Model name.",
    ),
]
system = Annotated[
    Optional[str],
    typer.Option(
        "--system",
        "-s",
        help="System message or a path to file, when started with @.",
        show_default=False,
    ),
]
limit = Annotated[
    Optional[int],
    typer.Option(
        "--limit",
        "-l",
        help="Limit the number of last messages passed to the context.",
        show_default="unlimited",
    ),
]
tokens = Annotated[
    Optional[int],
    typer.Option(
        "--max-tokens",
        "-t",
        help="Maximum number of tokens to generate.",
        show_default="unlimited",
    ),
]
no_stream = Annotated[
    bool,
    typer.Option(
        "--no-stream",
        help="Disable live streaming.",
    ),
]
interactive = Annotated[
    bool,
    typer.Option(
        "--interactive",
        "-i",
        help="Interactive CHAT mode.",
    ),
]
