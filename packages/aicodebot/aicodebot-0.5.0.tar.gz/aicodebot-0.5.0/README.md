# AI Code Bot 🤖

## Your AI-powered coding companion

AICodeBot is a coding assistant designed to make your coding life easier. With capabilities to perform code reviews, manage dependencies, and even suggest improvements, think of it as your AI version of a pair programmer.

⚠️ Status: This project is in its infancy with very limited features. Sometimes it does dumb things.

Even with limited functionality, it will still save you time, and you can look at the Features list below to get an idea of where it is going. Give the project a star and follow along while we build out more of the foundation.

## Setup and Usage

[![PyPI version](https://badge.fury.io/py/aicodebot.svg)](https://badge.fury.io/py/aicodebot)

Follow the steps below to set up AICodeBot on your machine:

`pip install aicodebot`

```bash
> aicodebot --help
Usage: aicodebot [OPTIONS] COMMAND [ARGS]...

Options:
  -V, --version  Show the version and exit.
  -h, --help     Show this message and exit.

Commands:
  alignment  Get a message about Heart-Centered AI Alignment ❤ + 🤖.
  commit     Generate a git commit message and commit changes after you...
  debug      Run a command and get debugging advice if it fails.
  fun-fact   Tell me something interesting about programming or AI.
  version    Print the version number.
```

Note:
The first time you run it, you'll be prompted to enter your OpenAI API Key, which is required, as we use OpenAI language models for the AI. You can get one for free by visiting your [API key settings page](https://platform.openai.com/account/api-keys").

## Features

### Code Workflow Improvements

- [X] **Assisted Git Commit**: Automatically generate a commit message.
- [X] **Assisted Debugging**: Run a command with aicodebot and it captures the log message and tries to figure out what's going on from the error message.  Eventually, it could also suggest fixes for the error and make the changes for you. Try it out with `aicodebot debug $command`
- [ ] **Code Review**: Provides feedback on potential issues in cod, such as style violations, potential bugs, and performance issues. It could also suggest best practices for code improvement. Eventually: FIX the code automatically and notify the team.
- [ ] **Fix the Build**: Check the CI/CD pipeline and fix the build.
- [ ] **Dependency Management**: Updating dependencies to their latest versions with pull requests that run tests.
- [ ] **Documentation Generation**: Generates comprehensive documentation for code, including docstrings, README files, and wiki pages.
- [ ] **Performance Optimization Suggestions**: Suggests potential performance optimizations for code.
- [ ] **Code Formatting**: Automatically formats code according to a specified style guide.
- [ ] **Error Detection**: Detects errors in code and suggests potential fixes.
- [ ] **Test Generation**: Generates unit tests for code.
- [ ] **Code Generation**: Generates boilerplate code for common tasks.
- [ ] **Integration with CI/CD pipelines**: Integrates with CI/CD pipelines to automate tasks like code review, testing, and deployment (via GitHub Actions)
- [ ] **Rubber Ducky Chat Bot**: Helps developers think through design issues by providing a conversational interface to discuss and solve problems
- [ ] **Linting**: Checks code for linting errors and automatically fixes them where possible.
- [ ] **Handle GitHub Issues**: Handles issues that you assign to @aicodebot. It could also suggest labels for new issues based on their content.

### User Interfaces

- [X] **Command-line installable via pip**: aicodebot can be installed as a Python package using `pip install aicodebot`
- [ ] **Chat**: CLI chat interface that knows the context of your codebase and can answer questions about it. No more going back and forth between ChatGPT and command-line.
- [ ] **Callable as a GitHub action**: Can be called as a GitHub action to perform tasks on GitHub repositories.
- [ ] **Slack Bot**: Interacts with aicodebot via slack, sends notifications, performs tasks, and provides real-time assistance to developers.
- [ ] **Bug Report service integrations**: Listen for bug reports from Sentry, Honeybadger, and other bug reporting tools and automatically create issues, assign them to developers, and notify them via Slack. Eventually: FIX the bug automatically and notify the team.

### Repository Management

- [ ] **Project best practices**: Suggest things like pre-commit, linting, license, CI/CD, etc. Eventually: Implement them for you.
- [ ] **Handle Stale Issues**: Automatically detects and handles stale issues on GitHub by nudging the responsible parties.
- [ ] **Triage Incoming Issues**: Provides Level 1 triage of incoming issues on GitHub, including tagging, assigning, and responding with FAQs. It could also escalate issues to human developers when necessary.
- [ ] **Rate the complexity of PRs**: Rates the complexity of pull requests and assigns them to developers based on their skill level and context

### Fun

- [X] **Fun Facts**: Provides fun facts about programming or AI. It could also share interesting news or articles related to AI and programming.
- [X] **Alignment**: Gives a heart-centered inspirational message about how we can build AI in a way that aligns with humanity.
- [ ] **Telling Jokes**: Tells programming jokes. :smiley:
- [ ] **Supportive Encouragement**: High fives and kudos for a job well done
- [ ] **GIF Reactions**: Reacts to messages with relevant and fun gifs. We've gotta figure out how to teach LLMs about humor.

<img src="https://camo.githubusercontent.com/6fc1e79b4aa226b24a756c4c8e20e5b049301a930449a7321d3e45f516e61601/68747470733a2f2f74656e6f722e636f6d2f766965772f6b746f2d6b6f756e6f746f72692d6b6f756e6f746f7269746f6b656e2d6c626f772d73746f726b686f6c646572732d6769662d32353637363438332e676966" width="25%">

## Development / Contributing

### The Stack

#### Test and Build

[![GitHub Build](https://github.com/novara-ai/aicodebot/actions/workflows/build.yml/badge.svg)](https://github.com/novara-ai/aicodebot/actions?query=build)
[![CodeCov](https://codecov.io/gh/novara-ai/aicodebot/branch/main/graph/badge.svg)](https://codecov.io/gh/novara_ai/aicodebot)
[![Pytest](https://img.shields.io/badge/%F0%9F%A7%AA-Pytest-blue)](https://docs.pytest.org/en/stable/contents.html)

#### Code Quality

[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v1.json)](https://github.com/charliermarsh/ruff)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![Super Linter](https://github.com/novara-ai/aicodebot/actions/workflows/linter.yml/badge.svg)](https://github.com/novara-ai/aicodebot/actions/workflows/linter.yml)

#### Infrastructure

[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/release/python-3110/)

[![Open AI](https://img.shields.io/badge/OpenAI-412991.svg?logo=OpenAI&logoColor=white)](https://openai.com)

### Dev Environment

1. Clone the repository

```bash
git clone git@github.com:novara-ai/aicodebot.git
```

2. Set up a virtual environment (I recommend using [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/))

```bash
mkvirtualenv --python=`which python3` aicodebot
```

3. Install the dependencies:

```bash
pip install -r requirements/requirements-dev.txt
```

4. Use aicodebot to build aicodebot 😎

### Testing

Install the test dependencies with
`pip install -r requirements/requirements-test.txt`

We use `pytest` for testing. It will skip some tests if OPENAI_API_KEY is not set.

### Coding Principles

Borrowed from the [zen of python](http://c2.com/cgi/wiki?PythonPhilosophy), with a couple of changes.

```text
1. **Readability is the number 1 code quality metric**.
2. Beautiful is better than ugly.
3. Explicit is better than implicit.
4. Simple is better than complex.
5. Complex is better than complicated.
6. Flat is better than nested.
7. Sparse is better than dense.
8. Special cases aren't special enough to break the rules.
    * Although practicality beats purity.
9. Errors should never pass silently.
    * Unless explicitly silenced.
10. In the face of ambiguity, refuse the temptation to guess.
11. There should be one -- and preferably only one -- obvious way to do it.
12. Now is better than never.
```
