# first_ai_automation
This project is an automation framework for testing the H&M website using Python, Playwright, and pytest. It implements the Page Object Model (POM) approach to organize the code for better maintainability and scalability.

## Project Structure
- **src/pages**: Contains page object classes that represent different pages of the website.
  - `base_page.py`: Base class for all page objects with common methods.
  - `home_page.py`: Home page specific methods.
  - `category_page.py`: Methods for interacting with category pages.
  - `search_results_page.py`: Methods for handling search results.
  - `product_page.py`: Methods for interacting with product details.

- **src/utils**: Utility functions and locators.
  - `locators.py`: Contains locators for various web elements.
  - `helpers.py`: Utility functions for common tasks.

- **tests/uat**: Contains User Acceptance Testing (UAT) test cases.
  - `test_home_navigation.py`: Tests for home page navigation.
  - `test_search_and_filter.py`: Tests for search and filtering functionality.
  - `test_product_details.py`: Tests for viewing product details.
  - `test_add_to_cart_flow.py`: Tests for the add-to-cart functionality.

- **tests**: Contains configuration and fixtures for pytest.
  - `conftest.py`: Configuration for pytest.

- **requirements.txt**: Lists the dependencies required for the project.

- **pytest.ini**: Configuration settings for pytest.

- **.gitignore**: Specifies files and directories to be ignored by Git.

- **scripts/run_tests.sh**: Shell script to run the tests using pytest.

## Setup Instructions
1. Clone the repository.
2. Navigate to the project directory.
3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Run the tests:
   ```
   bash scripts/run_tests.sh
   ```

## Usage Guidelines
- Use the page object classes to interact with the website in a structured manner.
- Write UAT test cases in the `tests/uat` directory to validate the functionality of the website.
- Utilize the utility functions in `src/utils/helpers.py` for common tasks like logging and taking screenshots.