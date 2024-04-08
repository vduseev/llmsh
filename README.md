# LLMsh

[![PyPI](https://img.shields.io/pypi/v/llmsh.svg)](https://pypi.org/project/llmsh/)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/vduseev/llmsh/blob/main/LICENSE)

Command-line tool to use Large Language Models in your shell.
Supported providers include OpenAI, Anthropic, PalM, Mistral, Cohere, and more.

**Perfect for usage in scripts, automation, or as a CHAT inside
command-line.**

*This is an alpha version and a work in progress.*

## Installation

### PyPI installation

```shell
pip install llmsh
```

### Or use install.sh for system-wide installation

#### Clone the repository to your home directory

*Note: It doesn't have to be this directory but it makes the most sense.*

```shell
git clone https://github.com/vduseev/llmsh ~/.llmsh
```

#### (optional) If you are using pyenv

*Temporarily activate the preferred Python version wherever you are.*

```shell
pyenv shell 3.11.7
```

#### Run the installation script

*This will create a virtual environment in `~/.llmsh/.venv`,
install the package, and create a symlink at `~/.local/bin/llmsh`.*

```shell
$ ~/.llmsh/install.sh
```

## Usage

### Configure API keys

```shell
# If you are using OpenAI
export OPENAI_API_KEY="your-api-key"
```

### Prompt mode

```shell
$ llmsh "Translate to Polish: What a good day"
Jaki dobry dzień
```

#### Pipe output to LLM

```shell
$ echo "Translate to Polish: What a good day" | llmsh
Jaki dobry dzień
```

#### Combine pipe and prompt

```shell
$ echo "Translate to Polish:" | llmsh "What a good day"
Jaki dobry dzień
```

#### Use a file as a prompt

```shell
$ echo "Who is Dora?" > prompt.txt
$ llmsh "@prompt.txt"
Dora is the main character from the animated television series "Dora the Explorer", produced by Nickelodeon. Dora is a young Latina girl who embarks  
on numerous adventures in an imaginative world with her backpack and her talking monkey companion named Boots. 
```

#### Specify a system prompt

The system prompt is a prompt that is always present in the conversation.
It is added to the beginning of the conversation before sending it to the model.

```shell
$ llmsh "@prompt.txt" -b "You are Dora the Explorer. Help me learn Spanish"
¡Hola! I'm Dora. I help kids to learn Spanish through fun       
adventures. I explore various environments with my talking backpack and monkey friend, Boots. Do you want to learn some Spanish words with me today? 
```

*System prompt can also be a file: `-s @system.txt`.*

### Interactive chat mode

```shell
$ llmsh -i
> What is the time difference between New York and Gdansk?
New York is typically 6 hours behind Gdansk. However, due to daylight saving
changes, this can occasionally vary.

> It is April. 
In April, Daylight Saving Time is active in both locations. The time
difference remains the same. New York is 6 hours behind Gdansk.

>
# Press Ctrl+D (Ctrl+Z on Windows), or type exit or quit to quit the chat.
```

*You can also use a file as a prompt: `-i @prompt.txt`.*
*As well as a system prompt: `-i -b "You are a helpful assistant."`, which can also be sourced from a file.*

*Piping is not supported in interactive mode.*

## Configuration

### API keys

```shell
# If you are using OpenAI
export OPENAI_API_KEY="your-api-key"

# If you are using Anthropic
export ANTHROPIC_API_KEY="your-api-key"

# If you are using PalM
export PALM_API_KEY="your-api-key"

# If you are using Mistral
export MISTRAL_API_KEY="your-api-key"
```

*See [full list of supported models](https://docs.litellm.ai/docs/providers).*

### Parameters

- `prompt` The prompt to use.
  
  *Positional argument.*

  Interpreted as a path, if it starts with `@`.
  
  *Examples:*
  - Give a prompt directly:
  
    ```shell
    llmsh "Hello"
    ```

  - Read a prompt from a file:
  
    ```shell
    llmsh "@prompt.txt"
    ```

  - Ask to explain a file:

    ```shell
    cat code.py | llmsh "Explain what this code does"
    ```
  
  *As environment variable:*
  - Linux/macOS: `export LLMSH_PROMPT="Hello"`
  - Windows (cmd): `set LLMSH_PROMPT="Hello"`
  - Windows (PowerShell): `$env:LLMSH_PROMPT="Hello"`

- `--before` The system prompt to use.
  
  *Shorthand: `-b`*
  
  Interpreted as a path when starts with @.
  
  *Examples:*
  - Pipe a question to LLM with a system prompt:
  
    ```shell
    echo "Where is John Connor?" | llmsh -b "You are Terminator"
    ```

  - Use a file as a system prompt:
  
    ```shell
    llmsh -b "@terminator.txt"`
    ```
  
  *As environment variable:*
  - Linux/macOS: `export LLMSH_BEFORE_PROMPT="You are Terminator"`
  - Windows (cmd): `set LLMSH_BEFORE_PROMPT="@C:\LLM\terminator.txt"`
  - Windows (PowerShell): `$env:LLMSH_BEFORE_PROMPT="You are Terminator"`

- `--after` The system prompt to be added as last message.
  
  *Shorthand: `-a`*
  
  Interpreted as a path when starts with @.
  
  *Examples:*
  - Ask LLM to write a poem with a system prompt:
  
    ```shell
    llmsh "Write a poem" -a "Use asterisks to emphasize the words"
    ```

  - Use a file as a system prompt:
  
    ```shell
    llmsh "Write a poem" -a "@poet.txt"
    ```
  
  *As environment variable:*
  - Linux/macOS: `export LLMSH_AFTER_PROMPT="You are a poet"`
  - Windows (cmd): `set LLMSH_AFTER_PROMPT="You are a poet"`
  - Windows (PowerShell): `$env:LLMSH_AFTER_PROMPT="You are a poet"`

- `--model` The name of model to use.

  *Shorthand: `-m`*

  **Don't forget to configure the appropriate API key for the
  chosen model.**

  *Examples:*
  - Ask GPT-3.5-turbo to explain what is the moon:

    ```shell
    llmsh "What is moon?" -m "gpt-3.5-turbo"
    ```

  - Ask Mistral 8x7b to write a poem:
  
    ```shell
    llmsh "Write a poem" -m "mistral/mistral-medium"
    ```

  - Pass the prompt from a file to Claude 3 model:
  
    ```shell
    llmsh "@prompt.json" -m "claude-3"
    ```

  *As environment variable:*
  - Linux/macOS: `export LLMSH_MODEL="gpt-3.5-turbo"`
  - Windows (cmd): `set LLMSH_MODEL="gpt-3.5-turbo"`
  - Windows (PowerShell): `$env:LLMSH_MODEL="gpt-3.5-turbo"`

- `--interactive` Enable interactive **chat** mode.

  *Shorthand: `-i`*

  *Examples:*
  - Start an interactive chat:
  
    ```shell
    llmsh -i
    ```

  - Start an interactive chat with a system prompt:
  
    ```shell
    llmsh -i -s "You are a helpful assistant"
    ```

  - Start an interactive role play chat with Mistral 8x7b model:
  
    ```shell
    llmsh -i -m "mistral/mistral-medium" -s "You are a poet and I am a critic"
    ```

  *As environment variable:*
  - Linux/macOS: `export LLMSH_INTERACTIVE="true"`
  - Windows (cmd): `set LLMSH_INTERACTIVE="true"`
  - Windows (PowerShell): `$env:LLMSH_INTERACTIVE="true"`

- `--limit` The maximum number of chat messages to use as context.

  Only works in interactive chat mode. When set, only the last N 
  messages + system prompt will be used to form the context of the
  request to LLM.

  *Examples:*
  - Start an interactive chat with a limit of 10 messages:

    *Only the last 10 messages plus the system prompt will be used 
    as context.*
  
    ```llmsh -i -l 10```
  
  *As environment variable:*
  - Linux/macOS: `export LLMSH_LIMIT="10"`
  - Windows (cmd): `set LLMSH_LIMIT="10"`
  - Windows (PowerShell): `$env:LLMSH_LIMIT="10"`

- `--max-tokens` The maximum number of tokens to generate.

  *Shorthand: `-t`*

  Controls how long the response will be. The higher the number, the longer the response. Default is unlimited.

  *Examples:*
  - `llmsh -t 100`

  *As environment variable:*
  - Linux/macOS: `export LLMSH_MAX_TOKENS="100"`
  - Windows (cmd): `set LLMSH_MAX_TOKENS="100"`
  - Windows (PowerShell): `$env:LLMSH_MAX_TOKENS="100"`

- `--no-stream` Disable streaming mode.

  By default, the response is streamed. This option disables that.

  Streaming mode is useful when you want to see the response as soon as 
  it is available. And streaming works even if you redirect the
  output somewhere else.

  *Examples:*
  - `llmsh --no-stream`
  - `llmsh -i --no-stream`

  *As environment variable:*
  - Linux/macOS: `export LLMSH_NO_STREAM="true"`
  - Windows (cmd): `set LLMSH_NO_STREAM="true"`
  - Windows (PowerShell): `$env:LLMSH_NO_STREAM="true"`

## Roadmap

https://github.com/vduseev/llmsh/labels/feature

## License

Copyright 2024 Vagiz Duseev

Apache 2.0 License.
