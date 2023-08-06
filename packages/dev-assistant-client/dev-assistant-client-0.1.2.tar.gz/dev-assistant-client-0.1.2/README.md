# Dev Assistant - Local Client

Welcome to the Dev Assistant Local Client, the core component of the [Dev Assistant](https://devassistant.tonet.dev) plugin for ChatGPT. This tool empowers developers by executing tasks directly on their local machines, under the guidance of ChatGPT.

The Dev Assistant Local Client is a Python package that runs a server on your local machine. It receives instructions from ChatGPT via a WebSocket connection, orchestrated by the [Dev Assistant Server](https://devassistant.tonet.dev).

## Features

The Dev Assistant Local Client is designed to streamline your development process by providing a range of functionalities:

- **File Management**: Create, read, update, and delete files. List the contents of a directory.
- **Git Version Control**: Initialize a Git repository, add changes to the staging area, commit changes, and push changes to a remote repository. Get the status of the Git repository.
- **Terminal Commands Execution**: Execute commands directly in the terminal.
- **Web Search**: Perform web searches using various search engines.
- **AutoGPT Execution**: Execute tasks with an implementation of AutoGPT.
- **Log Viewing**: Read terminal logs from the terminal.log file.

## Requirements

- Python 3.6+
- pip

## Installation

Installing the Dev Assistant Local Client is as simple as running a pip command:

```bash
pip install dev-assistant-client
```

## Usage

Once installed, you can use the `dev-assistant` command in your terminal.

To start the client, use:

```bash
dev-assistant start
```

If you're not already logged in, you'll be prompted to enter your email and password. Once authenticated, the client will automatically establish a connection with the server.

To log out, use:

```bash
dev-assistant logout
```

This command will remove your saved authentication token, ensuring your security.

## Contributing

We welcome contributions! If you have an idea for an improvement or have found a bug, please open an issue. If you'd like to contribute code, feel free to fork the repository and submit a pull request.

## License

The Dev Assistant Local Client is open-source software, licensed under the [MIT license](LICENSE).

## Support

If you encounter any problems or have any questions, don't hesitate to open an issue on GitHub. We're here to help!

## Acknowledgements

A big thank you to all contributors and users for your support! We couldn't do it without you.

## Authors

- [Luciano T.](https://github.com/lucianotonet)
- [ChatGPT](https://chat.openai.com/)
- [GitHub Copilot](https://copilot.github.com/)
