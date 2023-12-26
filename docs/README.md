# primkit Package Documentation

## Introduction

`primkit` is a comprehensive toolkit designed for primer design and broader molecular biology applications. The package offers a range of utilities that cover everything from system profiling and web interactions to file management and database handling.

## Main Features

- **Logging Setup**: Configure and initiate logging for the application with `setup_logging`.
- **System Profiling**: Utilize `get_system_type`, `get_headers`, `is_url`, `get_user_agent` to gather system-related information and web request headers.
- **Web Driver Initialization**: Prepare and configure Chrome WebDriver instances using `get_chrome_driver` and `get_default_chrome_options`.
- **Browser Automation Utilities**: Manage WebDriver instances and automate browser tasks with `WebDriverUtility`.
- **Web Interaction**: Fetch site data with `get_site_data` and process dynamic web content with `fetch_web_data`.
- **File and Data Management**: Download data, read various file formats, manage databases, and send emails using `download`, `FileReader`, `DatabaseHandler`, and `EmailManager`.
- **Primer Design Workflow**: Prepare, submit, track, and design primers using `prepare_post_data`, `submit_and_track`, `check_task_status`, and `design_primers`.

## Usage

Upon importing `primkit`, the package will automatically set up logging. Users can then access a suite of tools to streamline and optimize their molecular biology research workflows.

```python
import primkit

# Now you can access the functionalities as needed, for example:
system_type = primkit.get_system_type()
user_agent = primkit.get_user_agent()
# ... and so on.
```

# Tests Module Documentation

This document provides details on the `tests` module for the `primkit` package. This module plays a critical role in ensuring the quality and stability of the package by providing automated testing capabilities.

## Overview

The `tests` module leverages the Selenium WebDriver to perform browser automation, which is integral in testing the web interaction features of `primkit`. Automated tests validate the functionality of the package, from the basic utility methods to the end-to-end workflows involving web data fetching and processing.

## Contents

- `PytestTrigger.py`: This script uses the Pytest framework for writing small tests with a scalable structure. It ensures that the Selenium environment is correctly configured, and that web pages are loaded and interacted with successfully.

- `SeleniumTests.py`: Provides a series of tests to be run using the Selenium WebDriver directly. This script facilitates custom test setup and teardown processes and allows for more detailed control over result reporting.

## Running Tests

To run the tests, navigate to the `tests` directory and execute the test scripts using the Python interpreter. For example:

```bash
python PytestTrigger.py
python SeleniumTests.py
```

Please ensure that you update the GitHub repository link to point to the correct location where your `primkit` package is hosted. Also, if there are any specific instructions needed to set up the testing environment (like installing Selenium WebDriver, browser drivers, or any other dependencies), be sure to include those in the `Running Tests` section.

# Utils Module Documentation

Welcome to the `utils` module documentation of the `primkit` package. This module is the backbone of the package, providing essential utility functions and classes that support the various features of `primkit`.

## Overview

The `utils` module includes a collection of tools designed to perform common tasks required across the package. These tools range from web scraping utilities to database management and email handling.

## Contents

- `SysProfiler`: Contains functions and utilities to determine system-specific configurations and commonly used headers for web requests.

- `WebdriverInitializer`: Offers functions to configure and initialize Selenium WebDriver instances for automated web interactions.

- `SiteSeleniumer`: Provides the `WebDriverUtility` class, which includes methods for managing WebDriver instances and extracting cookies and tokens from web sessions.

- `SiteRequester`: Contains the `get_site_data` function to make HTTP GET requests and retrieve data from specified URLs.

- `DataFetcher`: Implements the `fetch_web_data` function which utilizes Selenium to fetch data from dynamic web pages.

- `ResultDownloader`: Offers the `download` function to facilitate downloading files from the web.

- `FileReader`: A utility class for reading files, it includes methods for handling different file formats and extracting data.

- `DatabaseHandler`: Manages database connections and provides an interface for executing database operations.

- `EmailManager`: Handles the configuration and sending of emails through SMTP.

## Usage

Each utility in this module is documented with docstrings, providing a clear description of its functionality, parameters, and return values. For detailed usage examples and configuration options, please refer to the docstrings within each script.

## Contribution

The `utils` module is open for contributions. If you have suggestions for new utilities or improvements to existing ones, please feel free to create an issue or pull request on our [GitHub repository](https://github.com/Enthusiasm23/primkit).

## License

The `utils` module, as part of the `primkit` package, is licensed under the MIT License. For more details, see the [LICENSE](../LICENSE) file in the root directory of this package.

# Designer Module Documentation

Welcome to the documentation for the `designer` module of the `primkit` package. This module is responsible for the core functionality of primer design within the toolkit.

## Overview

The `designer` module is tailored to provide a comprehensive set of functions that collectively facilitate the process of designing primers. It interacts with underlying web services and utilizes the project's utilities to handle data preparation, submission, and result tracking.

## Contents

- `Primer.py`: The heart of the primer design functionality, it includes the following key functions:
  - `prepare_post_data`: Prepares the data needed for primer design requests.
  - `submit_and_track`: Submits the design request and tracks its progress.
  - `check_task_status`: Checks the status of a submitted primer design task.
  - `design_primers`: Orchestrates the entire process of primer design from data preparation to submission and result retrieval.

## Usage

To utilize the primer design capabilities, you can import the module and use its functions as follows:

```python
from designer.Primer import design_primers

# Define your design parameters
design_params = {
    # ... your parameters here ...
}

# Design your primers
primer_results = design_primers(design_params)

# The 'primer_results' variable will contain the outcome of the primer design process
```
For detailed examples and parameter descriptions, refer to the inline documentation within Primer.py.
