import pandas as pd
import urllib.request
import gzip
from psycopg2 import connect
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from sqlalchemy import create_engine

# set your own parameters
params = {
    'host': 'localhost',
    'user': 'Valerie',
    'port': 5432
}

# Connect and create database, disconnect, and reconnect to the right database
connection = connect(**params)
connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
connection.cursor().execute('CREATE DATABASE ip_address_table;')
connection.close()

# extract ip address
url = 'http://software77.net/geo-ip/history/' 
# Just like HTTP request, you ask the driver to open a browser and go to the following link
resp = requests.get(url)

# create a soup variable that parses the HTML into a BeautifulSoup object
soup = BeautifulSoup(resp.text, 'html.parser')

# find all 'a' tags with links that start with IpToCountry
ip_address= soup.find_all('a', href = re.compile("^IpToCountry"))

#find the latest timestamp
list_of_epoch_time = []
for address in ip_address:
    link = address['href']
    epoch_time = re.findall(r'\d+', link) #find all epoch time in each link
    list_of_epoch_time.append(epoch_time) #store in a list
    latest_epoch_time = max(list_of_epoch_time)[0] #get the latest (i.e max) timestamp

latest_url = str(url) + "IpToCountry." + str(latest_epoch_time) + ".csv.gz"
out_file = '../Healint_DE/data/external_ip.csv'

# Download archive
try:
  # Read the file inside the .gz archive located at latest_url
    with urllib.request.urlopen(latest_url) as response:
        with gzip.GzipFile(fileobj=response) as uncompressed:
            file_content = uncompressed.read()

  # write to file in binary mode 'wb'
    with open(out_file, 'wb') as f:
        f.write(file_content)

except Exception as e:
    print(e)

# read in Webnet77 IP 
external_ip =  pd.read_csv("../Healint_DE/data/external_ip.csv", comment='#', header=None,
                   names = ['IP_FROM', 'IP_TO', 'REGISTRY', 'ASSIGNED', 'CTRY', 'CNTRY', 'COUNTRY'])


#export to csv    
external_ip.to_csv('../Healint_DE/data/ext_ip_table.csv', index=False)

#  create a database engine with which we can connect
connection_string = f'postgres://Valerie:{params["host"]}@{params["host"]}:{params["port"]}/ip_address_table'
engine = create_engine(connection_string)

# load external_ip to database
external_ip.to_sql('external_ip_address', engine, index=False)
