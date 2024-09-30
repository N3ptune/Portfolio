import pandas as pd
from bs4 import  BeautifulSoup
from selenium import webdriver

driver = webdriver.Chrome()

driver.get('https://sandbox.oxylabs.io/products')

# Object is "results", brackets make the object an empty list
# We will store data here
# other results will store other data
results = []
other_results = []

# add the page source to the variable
content = driver.page_source

# load the contents of the page, its source, in bs
# class, which analyzes the html as a nested data structure and allows
# selection of elements using selectors
soup = BeautifulSoup(content, 'html.parser')

# loop over all elements returned by findAll. It has filter attrs given
# to it, so it will only return elements with a certain class
for element in soup.find_all(attrs={'class': 'product-card'}):
    name = element.find('h4')
    if name not in results:
        results.append(name.text)

for element in soup.find_all(attrs={'class': 'product-card'}):
    name2 = element.find(attrs={'class': 'price-wrapper'})
    if name2 not in other_results:
        other_results.append(name2.text)

# create 2d data table "df"
# mofe df to a Excel
df = pd.DataFrame({'Names': results, 'Prices': other_results})
df.to_excel('names.xlsx', index=False)
