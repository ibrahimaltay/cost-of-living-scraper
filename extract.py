from bs4 import BeautifulSoup
import requests
import time
import csv
import pandas as pd
from datetime import datetime
COUNTRY_LIST = ['Afghanistan', 'Aland+Islands', 'Albania', 'Alderney', 'Algeria', 'American+Samoa', 'Andorra', 'Angola', 'Anguilla', 'Antigua+And+Barbuda', 'Argentina', 'Armenia', 'Aruba', 'Australia', 'Austria', 'Azerbaijan', 'Bahamas', 'Bahrain', 'Bangladesh', 'Barbados', 'Belarus', 'Belgium', 'Belize', 'Benin', 'Bermuda', 'Bhutan', 'Bolivia', 'Bonaire', 'Bosnia+And+Herzegovina', 'Botswana', 'Brazil', 'British+Virgin+Islands', 'Brunei', 'Bulgaria', 'Burkina+Faso', 'Burundi', 'Cambodia', 'Cameroon', 'Canada', 'Cape+Verde', 'Cayman+Islands', 'Central+African+Republic', 'Chad', 'Chile', 'China', 'Colombia', 'Comoros', 'Congo', 'Cook+Islands', 'Costa+Rica', 'Croatia', 'Cuba', 'Curacao', 'Cyprus', 'Czech+Republic', 'Denmark', 'Djibouti', 'Dominica', 'Dominican+Republic', 'Ecuador', 'Egypt', 'El+Salvador', 'Equatorial+Guinea', 'Eritrea', 'Estonia', 'Ethiopia', 'Falkland+Islands', 'Faroe+Islands', 'Fiji', 'Finland', 'France', 'French+Guiana', 'French+Polynesia', 'French+Southern+Territories', 'Gabon', 'Gambia', 'Georgia', 'Germany', 'Ghana', 'Gibraltar', 'Greece', 'Greenland', 'Grenada', 'Guadeloupe', 'Guam', 'Guatemala', 'Guernsey', 'Guinea', 'Guinea-Bissau', 'Guyana', 'Haiti', 'Honduras', 'Hong+Kong', 'Hungary', 'Iceland', 'India', 'Indonesia', 'Iran', 'Iraq', 'Ireland', 'Isle+Of+Man', 'Israel', 'Italy', 'Ivory+Coast', 'Jamaica', 'Japan', 'Jersey', 'Jordan', 'Kazakhstan', 'Kenya', 'Kosovo+%28Disputed+Territory%29', 'Kuwait', 'Kyrgyzstan', 'Laos', 'Latvia', 'Lebanon', 'Lesotho', 'Liberia', 'Libya', 'Liechtenstein', 'Lithuania', 'Luxembourg', 'Macao', 'Madagascar', 'Malawi', 'Malaysia', 'Maldives', 'Mali', 'Malta', 'Marshall+Islands', 'Martinique', 'Mauritania', 'Mauritius', 'Mayotte', 'Mexico', 'Micronesia', 'Moldova', 'Monaco', 'Mongolia', 'Montenegro', 'Montserrat', 'Morocco', 'Mozambique', 'Myanmar', 'Namibia', 'Nepal', 'Netherlands', 'New+Caledonia', 'New+Zealand', 'Nicaragua', 'Niger', 'Nigeria', 'North+Korea', 'North+Macedonia', 'Northern+Mariana+Islands', 'Norway', 'Oman', 'Pakistan','Panama', 'Papua+New+Guinea', 'Paraguay', 'Peru', 'Philippines', 'Poland', 'Portugal', 'Puerto+Rico', 'Qatar', 'Republic+Of+Congo', 'Reunion', 'Romania', 'Russia', 'Rwanda', 'Saint+Helena', 'Saint+Kitts+And+Nevis', 'Saint+Lucia', 'Saint+Vincent+And+The+Grenadines', 'Samoa', 'San+Marino', 'Sao+Tome+And+Principe', 'Saudi+Arabia', 'Senegal', 'Serbia', 'Seychelles', 'Sierra+Leone', 'Singapore', 'Sint+Maarten', 'Slovakia', 'Slovenia', 'Solomon+Islands', 'Somalia', 'South+Africa', 'South+Korea', 'South+Sudan', 'Spain', 'Sri+Lanka', 'Sudan', 'Suriname', 'Swaziland', 'Sweden', 'Switzerland', 'Syria', 'Taiwan', 'Tajikistan', 'Tanzania', 'Thailand', 'Timor-Leste', 'Togo', 'Tonga', 'Trinidad+And+Tobago', 'Tunisia', 'Turkey', 'Turkmenistan', 'Turks+And+Caicos+Islands', 'Uganda', 'Ukraine', 'United+Arab+Emirates', 'United+Kingdom', 'United+States', 'Uruguay', 'Us+Virgin+Islands', 'Uzbekistan', 'Vanuatu', 'Vatican+City', 'Venezuela', 'Vietnam', 'Western+Sahara', 'Yemen', 'Zambia', 'Zimbabwe']
ITEMS = ['Meal, Inexpensive Restaurant ', 'Meal for 2 People, Mid-range Restaurant, Three-course ', 'McMeal at McDonalds (or Equivalent Combo Meal) ', 'Domestic Beer (0.5 liter draught) ', 'Imported Beer (0.33 liter bottle) ', 'Cappuccino (regular) ', 'Coke/Pepsi (0.33 liter bottle) ', 'Water (0.33 liter bottle)  ', 'Milk (regular), (1 liter) ', 'Loaf of Fresh White Bread (500g) ', 'Rice (white), (1kg) ', 'Eggs (regular) (12) ', 'Local Cheese (1kg) ', 'Chicken Fillets (1kg) ', 'Beef Round (1kg) (or Equivalent Back Leg Red Meat) ', 'Apples (1kg) ', 'Banana (1kg) ', 'Oranges (1kg) ', 'Tomato (1kg) ', 'Potato (1kg) ', 'Onion (1kg) ', 'Lettuce (1 head) ', 'Water (1.5 liter bottle) ', 'Bottle of Wine (Mid-Range) ', 'Domestic Beer (0.5 liter bottle) ', 'Imported Beer (0.33 liter bottle) ', 'Cigarettes 20 Pack (Marlboro) ', 'One-way Ticket (Local Transport) ', 'Monthly Pass (Regular Price) ', 'Taxi Start (Normal Tariff) ', 'Taxi 1km (Normal Tariff) ', 'Taxi 1hour Waiting (Normal Tariff) ', 'Gasoline (1 liter) ', 'Volkswagen Golf 1.4 90 KW Trendline (Or Equivalent New Car) ', 'Toyota Corolla Sedan 1.6l 97kW Comfort (Or Equivalent New Car) ', 'Basic (Electricity, Heating, Cooling, Water, Garbage) for 85m2 Apartment ', '1 min. of Prepaid Mobile Tariff Local (No Discounts or Plans) ', 'Internet (60 Mbps or More, Unlimited Data, Cable/ADSL) ', 'Fitness Club, Monthly Fee for 1 Adult ', 'Tennis Court Rent (1 Hour on Weekend) ', 'Cinema, International Release, 1 Seat ', 'Preschool (or Kindergarten), Full Day, Private, Monthly for 1 Child ', 'International Primary School, Yearly for 1 Child ', '1 Pair of Jeans (Levis 501 Or Similar) ', '1 Summer Dress in a Chain Store (Zara, H&M, ...) ', '1 Pair of Nike Running Shoes (Mid-Range) ', '1 Pair of Men Leather Business Shoes ', 'Apartment (1 bedroom) in City Centre ', 'Apartment (1 bedroom) Outside of Centre ', 'Apartment (3 bedrooms) in City Centre ', 'Apartment (3 bedrooms) Outside of Centre ', 'Price per Square Meter to Buy Apartment in City Centre ', 'Price per Square Meter to Buy Apartment Outside of Centre ', 'Average Monthly Net Salary (After Tax) ', 'Mortgage Interest Rate in Percentages (%), Yearly, for 20 Years Fixed-Rate ']
CURRENCY = "USD"
SMALL_COUNTRY_LIST = ['Turkey', 'Austria', 'Germany', 'Iran', 'Japan']

COUNTRY_LIST_TEXT = 'countries.txt'

def GetItems():
	URL = f"https://www.numbeo.com/cost-of-living/country_result.jsp?country=Germany&displayCurrency={CURRENCY}" 
	source = requests.get(URL).text
	soup = BeautifulSoup(source,'lxml')
	items = []
	prices = []
	table = soup.find("table", class_="data_wide_table new_bar_table")
	row = table.find_all('tr')
	for x in row:
		try:
			items.append(x.find_all('td')[0].text)
			# print(x.find_all('td')[0].text)
			# prices.append(x.find_all('td')[1].text)
			# print(x.find_all('td')[1].text)
		except Exception as e:
			pass
	return items

def GetCountryPrices(country):
    try:
        COUNTRY = country
        URL = f"https://www.numbeo.com/cost-of-living/country_result.jsp?country={COUNTRY}&displayCurrency={CURRENCY}" 
        source = requests.get(URL).text
        soup = BeautifulSoup(source,'lxml')
        print(f"SELECTED COUNTRY: {COUNTRY}\n")
        items = []
        prices = []
        table = soup.find("table", class_="data_wide_table new_bar_table")
        row = table.find_all('tr')
        for x in row:
            try:
                # items.append(x.find_all('td')[0].text)
                # print(x.find_all('td')[0].text)
                prices.append(x.find_all('td')[1].text.split('$')[0])
                # print(x.find_all('td')[1].text)
            except Exception as e:
                pass
    except Exception as e:
        print(e)
    return prices


def GetCountryList():
	source = requests.get("https://www.numbeo.com/cost-of-living/").text
	soup = BeautifulSoup(source,"lxml")
	table = soup.find("table", class_="related_links")
	anchor = table.find_all("a")
	for x in anchor:
		text = x.text
		text = text.replace(' ',"+")
		COUNTRYLIST.append(text)
	COUNTRYLIST[COUNTRYLIST.index("Kosovo+(Disputed+Territory)")]= "Kosovo+%28Disputed+Territory%29"

def GetCountryListFromText():
	ret = []
	with open('countries.txt', 'r') as file:
		ret = [country.strip().replace(' ', '+') for country in file.readlines()]
		return ret



df = pd.DataFrame()

df['ITEMS'] = GetItems()

country_list_from_text = GetCountryListFromText()
for country in country_list_from_text:
    df[country] = GetCountryPrices(country)

time= datetime.now().strftime('%d-%m-%Y')
df.to_csv(f'{time}.csv', header=True, index=False) 
