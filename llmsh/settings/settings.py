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

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


_default_before_prompt = """You are a helpful assistant.
Your goal is to help the user.
"""
_default_after_prompt = """Be concise and clear.
Don't repear what user has said in their last message.
Use markdown to format your answers.
"""
_default_user_prompt = ""


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="llmsh_")

    prompt: Optional[str] = Field(_default_user_prompt)
    before: Optional[str] = Field(_default_before_prompt)
    after: Optional[str] = Field(_default_after_prompt)
    model: str = Field("gpt-4")
    system_role: str = Field("system")
    user_role: str = Field("user")
    llm_role: str = Field("assistant")
    limit: Optional[int] = Field(None)
    max_tokens: Optional[int] = Field(None)
    no_stream: bool = Field(False)
    interactive: bool = Field(False)
    debug: bool = Field(False)
