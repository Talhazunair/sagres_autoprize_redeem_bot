# Sagres Bot

Sagres Bot is a Python automation tool that enables users to log in to the Sagres platform, search for products, and attempt to redeem them. It utilizes Selenium for web automation and provides a rich command-line interface using Rich and Colorama libraries.

## Features

- Automated login to the Sagres platform.
- Handles age verification steps.
- Searches for products across multiple pages.
- Attempts to redeem products automatically.
- Rich console interface for better visualization of progress and logs.

## Requirements

Before you begin, ensure you have the following installed on your system:

- Python 3.8+
- Google Chrome (latest version recommended)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/sagres-bot.git
   cd sagres-bot
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. The `chromedriver_autoinstaller` package will automatically download and configure the ChromeDriver for your version of Chrome.

## Usage

1. Run the script:
   ```bash
   python sagres_bot.py
   ```

2. Enter your Sagres account credentials and the product name you want to search for when prompted.

3. The bot will:
   - Handle age verification.
   - Log in to your account.
   - Search for the specified product.
   - Attempt to redeem the product if found.

4. Monitor the console for progress updates.

## Code Structure

- **`WebDriverManager`**: Initializes the WebDriver and manages its lifecycle.
- **`BasePage`**: Contains common web interaction methods (e.g., finding elements, scrolling).
- **`AgeGatePage`**: Handles the age verification process.
- **`LoginPage`**: Manages the login process.
- **`ProductCatalog`**: Fetches and lists available products.
- **`ProductRedeemer`**: Handles the product redemption process.
- **`SagresBot`**: Orchestrates all operations and provides a high-level interface for the bot.

## Configuration

You can modify the following parameters directly in the script:

- **Retry interval**: The time (in seconds) to wait between product search attempts.
- **Maximum retries**: The maximum number of attempts before stopping the product search.

## Libraries Used

- [Selenium](https://pypi.org/project/selenium/): For web automation.
- [chromedriver-autoinstaller](https://pypi.org/project/chromedriver-autoinstaller/): Automatically installs the appropriate ChromeDriver version.
- [Rich](https://pypi.org/project/rich/): For enhanced console outputs.
- [Colorama](https://pypi.org/project/colorama/): For colored terminal text.
- [TQDM](https://pypi.org/project/tqdm/): For progress bars.

## Notes

- Ensure you have a stable internet connection when using the bot.
- The bot assumes that your Sagres account credentials are valid.
- The platform's structure or elements may change over time, which could require updates to the script.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature/bugfix.
3. Submit a pull request with a clear description of your changes.

## Acknowledgments

Thanks to the developers of Selenium, Rich, Colorama, and other libraries that made this project possible.

---

Feel free to reach out with any issues or suggestions. Happy automating!
