# UbuntuBoost

Welcome to **UbuntuBoost** – your all-in-one solution to optimize, secure, and maintain your Ubuntu system. Developed by [Kevin Marville](https://github.com/kvnbbg), this tool is designed to make your Ubuntu experience smoother, faster, and more secure.

## Features

- **Update and Upgrade**: Keep your system up to date with the latest packages.
- **System Optimization**: Optimize CPU, memory, and other system settings for enhanced performance.
- **Security Enhancements**: Strengthen your system's security by configuring firewalls, updating software, and more.
- **System Cleaning**: Clean old kernels and unnecessary files to free up space.
- **Custom Configuration**: Easily configure swap space, cache settings, and more.

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/kvnbbg/UbuntuBoost.git
   cd UbuntuBoost
   ```

2. **Install the required dependencies**:
   ```bash
   sudo apt-get update
   sudo apt-get install -y python3 python3-pip
   pip3 install -r requirements.txt
   ```

3. **Create a virtual environment (optional but recommended)**:
   ```bash
   python3 -m venv my_venv
   source my_venv/bin/activate
   ```

## Usage

### Optimizer

To optimize your Ubuntu system, simply run:

```bash
python3 run.py
```

You'll be prompted with a menu where you can choose the following options:

1. **Update and Upgrade System**: Ensure your system is up to date.
2. **Install System Packages**: Install necessary packages for system optimization.
3. **Clean Old Kernels**: Remove old kernels to free up space.
4. **Optimize System Performance**: Optimize CPU and memory settings.
5. **Enhance System Security**: Improve the security of your system.
6. **Configure Swap Space**: Set up and optimize swap space.
7. **Clean System**: Clean up unnecessary files.
8. **Full Optimization**: Run all tasks in sequence for a full system optimization.
9. **Exit**: Exit the tool.

### Sonic Pi & Other Programs

You can also initialize Sonic Pi and other programs using the same interface. Simply follow the prompts after selecting the appropriate option from the menu.

## Credits

Developed by [Kevin Marville](https://github.com/kvnbbg).

- [GitHub](https://github.com/kvnbbg)
- [Blog](https://kvnbbg.fr)
- [Portfolio](https://kvnbbg-creations.io)
- [Instagram](https://www.instagram.com/techandstream/)
- [LinkedIn](https://linkedin.com/in/kevin-marville)

## Contributing

Contributions are welcome! If you'd like to contribute, please fork the repository and use a feature branch. Pull requests are warmly welcome.

1. Fork the project.
2. Create your feature branch (`git checkout -b feature/AmazingFeature`).
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4. Push to the branch (`git push origin feature/AmazingFeature`).
5. Open a pull request.

## License

This project is licensed under the License - see the [LICENSE](LICENSE) file for details.

## Contact

For any inquiries or support, please reach out via [LinkedIn](https://linkedin.com/in/kevin-marville) or [email](mailto:contact@kvnbbg.fr).

## Acknowledgements

Special thanks to the Ubuntu community and all contributors to open-source projects that make tools like UbuntuBoost possible.

## Like This Project?

If you like this project and want to support it, please consider following me on [Instagram](https://www.instagram.com/techandstream/) or visiting my [portfolio](https://kvnbbg-creations.io).
