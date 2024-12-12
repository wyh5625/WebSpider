import openpyxl
import pandas as pd
from DrissionPage import ChromiumPage, ChromiumOptions

# Load the Excel workbook
workbook = openpyxl.load_workbook('data.xlsx')
sheet = workbook.active

# Set up Chromium options
co = ChromiumOptions()
co.headless(False)  # Set to True for headless mode
co.set_argument('--start-maximized')
co.set_user_agent(
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36')

# Initialize the ChromiumPage
page = ChromiumPage(co)

# Navigate to the initial URL
page.get('https://subhd.tv/a/573702')
page.listen.start('ajax/down1_ajax')  # Start listening for specific AJAX requests

lists = []
for row in sheet.iter_rows(values_only=True, min_row=2):
    try:
        url = row[0]
        name = row[1]
        page.get(url)  # Navigate to the URL from the Excel sheet
        page.wait(3)  # Adjust wait time as necessary (consider using dynamic waits)

        # Click the button to get the subtitle link
        page.ele('xpath:/html/body/div[5]/div/div/div/div[1]/div[3]/div[1]/button').click()

        # Wait for the AJAX response
        data = page.listen.wait()
        caption_url = data.response.body['url']

        # Append the results to the list
        lists.append([name, caption_url])
        print([name, caption_url])

    except Exception as e:
        print(f"Error processing {name}: {e}")

# Convert the list to a DataFrame
df = pd.DataFrame(lists, columns=['电影名字', '资源网址'])

# Save the DataFrame to an Excel file
df.to_excel('电影url数据.xlsx', index=False, engine='openpyxl')

# Optionally, close the page/browser
page.close()