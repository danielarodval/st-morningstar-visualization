## Selenium Morningstar Visualization Overview

This project demonstrates the use of Selenium in Python to scrape financial data from Morningstar index funds. The data is then visualized using the Plotly library.

### Key Features

- **Web Scraping**: Implemented using Selenium to navigate and scrape data from Morningstar's index fund webpages.
- **Data Processing**: Extracted data is transformed and stored in pandas dataframes.
- **Visualization**: Utilizing Plotly to create insightful visualizations of the scraped data.

### Dependencies

- Selenium
- BeautifulSoup
- Pandas
- Plotly

### Implementation

#### Web Scraping

1. Selenium WebDriver is initialized to navigate to the Morningstar index fund webpages.
2. The script navigates through the website, accessing different index fund data.
3. Data from the webpage is extracted and loaded into pandas dataframes.

   ```python
   def web_scrape(url):
       # ... (Selenium navigation and data extraction logic)
       return data_frame
   ```

#### Data Processing

1. The scraped data is cleaned and formatted appropriately.
2. Additional functions, like `calculate_yearly_pct_change`, are used for further data manipulation.

   ```python
   def calculate_yearly_pct_change(df, df_name):
       # ... (Data processing logic)
       return processed_df
   ```

#### Visualization with Plotly

1. Data from the processed dataframes is visualized using Plotly.
2. Different types of visualizations are created to represent the data effectively.

### Screenshots/Demo
![Median Home Sale Prices Visualization](link-to-screenshot)

### Dataset

The data includes various financial metrics from Morningstar index funds such as:
- Morningstar US Small Cap
- Morningstar US Large Cap
- Morningstar Developed Markets
- Morningstar Emerging Markets
- Morningstar US Treasury and Corporate Bonds

---

For further information, review the complete Jupyter notebook.