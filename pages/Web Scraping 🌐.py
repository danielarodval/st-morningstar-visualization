import streamlit as st

st.title('Web Scraping 🌐')

st.subheader('Introduction')
st.write('The functions `web_scrape()`, `calculate_yearly_pct_change()`, and `add_fund_name()` are used to scrape data from a list of URLs, calculate yearly percentage changes, and consolidate the results into a DataFrame. **See below for more details.**')

code_tab1, code_tab2, code_tab3, code_tab4 = st.tabs(["details","web_scrape()", "calculate_yearly_pct_change()", "add_fund_name()"])

with code_tab1:
    st.markdown("""
`web_scrape(url)` - This function navigates a specified webpage, interacts with elements on the page to display relevant data, and then scrapes and processes this data into a DataFrame. It focuses on capturing historical stock data, specifically the `Date`, `Close`, `High`, `Low`, `Open`, and `Volume` values.

`calculate_yearly_pct_change(df, df_name)` - This function calculates the yearly percentage change of stock prices based on the closing prices within a DataFrame. It filters for the last row of December for each year, computes percentage changes, and formats the result into a transposed DataFrame with the DataFrame name as the row index.

`add_fund_name(arr)` - This function takes a list of URLs, extracts fund names from each, scrapes data using `web_scrape`, calculates yearly percentage changes using `calculate_yearly_pct_change`, and returns both a list of data and a consolidated DataFrame with yearly percentage changes across funds.
            """)
with code_tab2:
    st.code('''
    def web_scrape(url):
    # Create a new instance of the Chrome driver
    driver = webdriver.Chrome()
    driver.implicitly_wait(1000)

    # Navigate to the desired webpage
    driver.get(url)
    driver.implicitly_wait(1000)

    # Internally navigate the webpage
    # select overview tab
    select_page = driver.find_element(By.ID, "tab-overview")
    select_page.click()
    driver.implicitly_wait(1000)

    # select time period bar
    select_chart = driver.find_element(By.ID, "chart-container")
    select_chart.click()
    driver.implicitly_wait(1000)

    buttons = driver.find_elements(By.CSS_SELECTOR,'[class="mds-button___markets mds-button--flat___markets markets-ui-button mwc-markets-chart-time-interval__btn"]')

    for button in buttons:
        if button.text == 'MAX':
            button.click()

    select_chart.click()

    # select table format
    table_button = driver.find_element(By.CSS_SELECTOR, '[aria-label="Table"]')
    table_button.click()
    driver.implicitly_wait(150)

    # select volume data
    filter_button = driver.find_element(By.CSS_SELECTOR, '[data-id="priceVolumeDetail"]')
    filter_button.click()
    driver.implicitly_wait(300)
    driver.execute_script("window.scrollBy(0, 600);")

    select_chart.click()

    # select all data
    dropdown_button = driver.find_elements(By.CSS_SELECTOR,'[class="mds-select___markets mds-select--small___markets"]')
    dropdown_button = dropdown_button[1]
    dropdown_button.click()
    driver.implicitly_wait(300)

    dropdown_divs = driver.find_elements(By.CSS_SELECTOR, '.mds-select___markets.mds-select--small___markets')
    dropdown_div = dropdown_divs[1]  # Use the second dropdown as per your code

    select_element = dropdown_div.find_element(By.TAG_NAME, 'select')

    select_object = Select(select_element)

    select_object.select_by_visible_text('All')

    # select table
    driver.execute_script("window.scrollBy(0, 600);")
    select_chart.click()
    driver.implicitly_wait(1000)
    select_chart.click()
    html = driver.page_source

    driver.implicitly_wait(1000)

    driver.quit()

    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('table')
    temp_df = pd.DataFrame(columns=['Date', 'Close', 'High', 'Low', 'Open', 'Volume'])
    table = table.find_all('tr')
    for row in table:
        cols = row.find_all('td')
        row_data = [col.text.strip() for col in cols]
        if len(row_data) != len(temp_df.columns):
            row_data += [''] * (len(temp_df.columns) - len(row_data))
        temp_df.loc[len(temp_df)] = row_data
        
    return temp_df
        ''')
    
with code_tab3:
    st.code('''
    def calculate_yearly_pct_change(df, df_name):
    df['Date'] = pd.to_datetime(df['Date'])
    end_date = df['Date'].max()
    end_row = df.loc[df['Date'] == end_date]
    end_row = end_row.set_index(pd.Index([end_date.year]))

    # Filter DataFrame to only include December dates
    december_df = df[df['Date'].dt.month == 12]

    # Group data by year and select last row for each year
    end_of_year_df = december_df.groupby(december_df['Date'].dt.year).last().loc[2007:]
    final_df = pd.concat([end_of_year_df,end_row])

    final_df['Close'] = pd.to_numeric(final_df['Close'].str.replace(',', ''))
    final_df['Close_pct_change'] = final_df['Close'].pct_change()
    final_df = final_df.iloc[1:]

    final_df['Close_pct_change'] = final_df['Close_pct_change'].apply(lambda x: '{:.1f}'.format(x*100))
    
    # Transpose the DataFrame and set the index to the DataFrame name
    final_df = final_df[['Close_pct_change']].transpose()
    final_df.index = [df_name]
    
    # Set column names to years
    final_df.columns = final_df.columns.astype(str)

    return final_df
    ''')

with code_tab4:
    st.code('''
    def add_fund_name(arr):
    arr_2 = []
    pct_change_df = pd.DataFrame()
    for url in arr:
        # get file name
        title = url.split("details/")[1].split("-FS")[0]
        
        # create dataframes & csv files
        df = web_scrape(url)
        df = df.loc[1:]
        df.to_csv(os.path.dirname(os.path.realpath(__file__))+"/csv_export/"+title+".csv")
        
        # process dataframe 
        pct_change_df = pd.concat([pct_change_df,calculate_yearly_pct_change(df,title)])
        
        arr_2.append([title,url,df])
        
        
    return arr_2, pct_change_df
    ''')

st.subheader("Script in Action")

with st.expander("URLs to Scrape"):
    url_col1, url_col2 = st.columns(2)
    url_col1.markdown("""
    [Morningstar US Small Cap](https://indexes.morningstar.com/our-indexes/details/morningstar-us-small-cap-FSUSA00KGS?currency=USD&variant=TR&tab=performance)\n
    [Morningstar US Large Cap](https://indexes.morningstar.com/indexes/details/morningstar-us-large-cap-FSUSA00KH5?currency=USD&variant=TR&tab=performance)\n
    [Morningstar Developed Markets ex-US](https://indexes.morningstar.com/indexes/details/morningstar-developed-markets-ex-us-FS00009P5R?currency=USD&variant=TR&tab=performance)\n
    [Morningstar Emerging Markets](https://indexes.morningstar.com/indexes/details/morningstar-emerging-markets-FS00009P5Q?currency=USD&variant=TR&tab=performance)
    """) 

    url_col2.markdown("""
    [Morningstar US 5-10 Yr Treasury Bond](https://indexes.morningstar.com/indexes/details/morningstar-us-5-10-yr-treasury-bond-FS0000E728?currency=USD&variant=TR&tab=performance)\n
    [Morningstar US 5-10 Yr Corporate Bond](https://indexes.morningstar.com/indexes/details/morningstar-us-5-10-yr-corporate-bond-FS0000DZER?currency=USD&variant=TR&tab=performance)\n
    [Morningstar US High Yield Bond](https://indexes.morningstar.com/indexes/details/morningstar-us-high-yield-bond-FS0000E18W?currency=USD&variant=TR&tab=performance)\n
    [Morningstar Moderate Target Risk](https://indexes.morningstar.com/indexes/details/morningstar-moderate-target-risk-FSUSA09PYI?currency=USD&variant=TR&tab=performance)
    """)
