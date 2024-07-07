# School Test Results Scraper

This project is a web scraper for extracting school test results from the NECTA website. The scraper collects data from nested links on a specified page and consolidates the results into an Excel spreadsheet.

## Prerequisites

Ensure you have Python installed. You will also need to install the following Python libraries:

- `requests`
- `beautifulsoup4`
- `pandas`
- `openpyxl`

You can install these libraries using pip:

```sh
pip install requests beautifulsoup4 pandas openpyxl
```
## Usage

1. **Clone the Repository**

    ```sh
    git clone https://github.com/yourusername/school-test-results-scraper.git
    cd school-test-results-scraper
    ```

2. **Edit the Script (if necessary)**

    Update the `url` variable in `scraper.py` if you want to scrape a different page.

3. **Run the Script**

    ```sh
    python scraper.py
    ```

4. **Check the Output**

    The results will be saved in an Excel file named `school_test_results.xlsx` in the same directory.



## Notes

- Ensure the structure of the scraped data matches the defined schema. Adjust the `columns` list if necessary.
- This script currently assumes that the second table on each page contains the desired data. Modify the script as needed for different structures.

## License

This project is licensed under the MIT License.

Feel free to adjust the instructions or content based on your specific requirements or preferences.
