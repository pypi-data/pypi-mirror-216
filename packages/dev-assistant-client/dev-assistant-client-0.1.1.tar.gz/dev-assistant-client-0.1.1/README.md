# Dev Assistant Client

Dev Assistant is a plugin for ChatGPT designed to assist developers with their tasks directly from their local machine. The Dev Assistant Client is a Python-based command-line tool that interacts with the Dev Assistant API, serving as a local extension of the ChatGPT plugin.

The Dev Assistant Client communicates with the [DevAssistant](https://devassistant.tonet.dev) server, a centralized API gateway built with Laravel. This setup allows developers to interact with ChatGPT directly from their local machines, providing a seamless and efficient development experience.

## Installation

You can install the Dev Assistant Client using pip:

```bash
pip install dev-assistant-client
```

## Usage

After installing the Dev Assistant Client, you can use the `dev-assistant` command in your terminal.

To start the client:

```bash
dev-assistant start
```

If you are not already logged in, you will be prompted to enter your email and password to log in. Once logged in, the client will automatically connect to the server.

To log out:

```bash
dev-assistant logout
```

This will remove your saved authentication token.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License
Dev Assistant Client is open-source software licensed under the [MIT license](LICENSE).

## Support

If you encounter any problems or have any questions, please open an issue on GitHub.

## Acknowledgements

Thanks to all contributors and users for your support!
