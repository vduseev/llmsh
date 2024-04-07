# LLMsh

[![PyPI](https://img.shields.io/pypi/v/llmsh.svg)](https://pypi.org/project/llmsh/)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/vduseev/llmsh/blob/main/LICENSE)

Command-line tool to use Large Language Models in your shell.
Supported providers include OpenAI, Anthropic, PalM, Mistral, Cohere, and more.

**Perfect for usage in scripts, automation, or as a CHAT inside
command-line.**

*This is an alpha version and a work in progress.*

## Installation

```shell
pip install llmsh
```

## Configure

```shell
# Set your OpenAI key in the current shell
export OPENAI_API_KEY="sk-xxxxxx"
```

## Usage

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

```shell
$ llmsh "@prompt.txt" -s "You are Dora the Explorer. Help me learn Spanish"
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
*As well as a system prompt: `-i -s "You are a helpful assistant."`, which can also be sourced from a file.*

*Piping is not supported in interactive mode.*

## Roadmap

https://github.com/vduseev/llmsh/labels/feature

## License

Copyright 2024 Vagiz Duseev

Apache 2.0 License.
