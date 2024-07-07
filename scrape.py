import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL of the main page
# url = "https://matokeo.necta.go.tz/results/2023/sfna/SFNA2023/distr_ps2501.htm"
url = "https://matokeo.necta.go.tz/results/2023/sfna/sfna.htm"

response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# Extract all nested links from the page
links = []
for a_tag in soup.find_all('a', href=True):
    h_url = a_tag['href']
    link=[]
    if h_url.startswith("https"):
        link.append(h_url)
    else:
        link.append(url.rsplit('/', 1)[0] + '/' + h_url)
    link.append( a_tag.get_text(strip=True))
    links.append(link)
    
def scrape_region(linkurl):
    # reg_links = []
    print(f"region link: {linkurl}")
    response = requests.get(linkurl[0])
    soup = BeautifulSoup(response.content, 'html.parser')
    
    for a_tag in soup.find_all('a', href=True):
        h_url = a_tag['href']
        link=[]
        if h_url.startswith("https"):
            link.append(h_url)
        else:
            link.append(linkurl[0].rsplit('/', 1)[0] + '/' + h_url)
        link.append(linkurl[1])
        link.append( a_tag.get_text(strip=True))
        # reg_links.append(link)
        scrape_school(link)

def scrape_school(linkurl):
    print(f"school link: {linkurl}")
    response = requests.get(linkurl[0])
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # print(f"school table link: {soup}")
    
    for a_tag in soup.find_all('a', href=True):
        h_url = a_tag['href']
        link=[]
        if h_url.startswith("https"):
            link.append(h_url)
        else:
            link.append(linkurl[0].rsplit('/', 1)[0] + '/' + h_url)
        link.append(linkurl[1])
        link.append(linkurl[2])
        link.append( a_tag.get_text(strip=True))
        # links.append(link)
        
        print(f"school table link: {link}")
        
        scraped_data = scrape_table(link)
        if scraped_data:
            data.extend(scraped_data)

# Initialize an empty list to store the data
data = []

# Function to scrape data from a single link
def scrape_table(linkurl):
    print(f"table link: {linkurl}")
    response = requests.get(linkurl[0])
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find all tables on the page
    tables = soup.find_all('table')
    print(f"tables: {len(tables)}")
    
    if len(tables) < 3:
        print(f"Warning: Expected at least 3 tables on {linkurl[0]}, found {len(tables)}. Skipping this link.")
        return None

    # The second table
    table = tables[2]
    rows = table.find_all('tr')

    # Print the number of columns for debugging purposes
    if rows:
        num_columns = len(rows[0].find_all('th'))
        print(f"URL: {linkurl[0]} - Number of columns: {num_columns}")

    scraped_data = []
    for row in rows[1:]:  # Skip the header row
        cells = row.find_all('td')
        row_data = []
        row_data.append(linkurl[1])
        row_data.append(linkurl[2])
        row_data.append(linkurl[3])
        # row_data = [cell.get_text(strip=True) for cell in cells]
        for cell in cells:
            row_data.append(cell.get_text(strip=True))
        scraped_data.append(row_data)

    return scraped_data

# Loop through each link and scrape data
# for link in links:
    # scraped_data = scrape_region(link)
    # if scraped_data:
    #     data.extend(scraped_data)
    # scrape_region(link)
scrape_region(links[0])

# Check the structure of the scraped data
if data:
    print("Sample of the scraped data:", data[0])

# Define the schema based on the actual data
# Adjust this based on the actual number of columns in the scraped data
columns = ['District', 'Region', 'School', 'Cand. No', 'Prem No', 'Gender', 'Candidate Name', 'Subjects'][:len(data[0])]

# Create a DataFrame from the scraped data
df = pd.DataFrame(data, columns=columns)

try:
    df.to_excel('school_test_results.xlsx', index=False)
    print("Data has been consolidated and saved to 'school_test_results.xlsx'")
except Exception as e:
    print(f"Error saving data to Excel file: {e}")
