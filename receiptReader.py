###Import necessary libraries###
import requests
from bs4 import BeautifulSoup
import pandas as pd



###Fetch URL of receipt and read it###
#Establish url
url = "https://receipt.365retailmarkets.com/receipt/view?transid=VSH603038-230131069590&receipttype=SALES_RECEIPT"

# Send a GET request to fetch the receipt page content
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# Parse the content into list
Data = []
for row in soup.find_all('td'):
    data = row.text.strip()
    if 'Thank' not in data and 'Welcome' not in data and 'Copyright' not in data and 'Payments' not in data:
        Data.append(data)

#Establish important values
Location = Data[0]
TimeNDate = Data[1]
Items = []
Costs = []
Subtotal = 0
TotalTax = 0
Total = 0
PaymentType = ''

#Sort through Data list and add values based off of context
for i in range(len(Data)):
    if (Data[i] == 'Amount'):
        PaymentType = Data[i + 1]
    if (Data[i] == 'Subtotal'):
        Subtotal = float(Data[i + 1][1:])
    if (Data[i] == 'Total Tax'):
        TotalTax = float(Data[i + 1][1:])
    if (Data[i] == 'Total'):
        Total = float(Data[i + 1][1:])

#Start adding items and their respective cost to their lists
#Starting at index 2 since indexes 0 and 1 are the location and time/date
#This list will iterate until 'Subtotal' is found, leaving room to digest smaller and larger receipts
j = 2
while (j < Data.index('Subtotal')):
    if (j % 2 == 0):
        Items.append(Data[j])
    else:
        Costs.append(Data[j])
    j += 1

# Dictionary to capture each datapoint
new_receipt = {
    'Location': Location,
    'Date': TimeNDate,
    'Items Purchased': Items,
    'Price': Costs,
    'Subtotal': Subtotal,
    'Tax': TotalTax,
    'Total Price': Total,
    'Payment Method': PaymentType
}

# Convert dictionary to DataFrame
new_receipt_df = pd.DataFrame([new_receipt])

# Display the updated DataFrame
print(new_receipt_df)