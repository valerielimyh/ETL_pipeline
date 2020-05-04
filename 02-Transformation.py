import pandas as pd
from sqlalchemy import create_engine

#read given user_ip_table
user_ip = pd.read_csv('../Healint_DE/data/user_ip_table.csv')

# load user_ip_table to database
connection_string = f'postgres://Valerie:{params["host"]}@{params["host"]}:{params["port"]}/ip_address_table'
engine = create_engine(connection_string)
user_ip.to_sql('user_ip', engine, index=False)

def ip_to_num(ip):
    ''' Convert ip address to numeric representation
    Parameter:
    Ip address (str). E.g. 1.2.3.4
    
    Output:
    Numeric representation of IP (int). E.g. 16909060
    '''
    # 1.2.3.4 = 4 + (3 * 256) + (2 * 256 * 256) + (1 * 256 * 256 * 256) = 16,909,060
    return sum((np.array(ip.split('.'), dtype='int') * np.array([256**3, 256**2, 256, 1])))

def get_country(num_ip):
    ''' Get country from the Webnet77 IP to Country Database
    Parameter:
    Numeric representation of IP (int). E.g. 16909060
    
    Output:
    COUNTRY (str) if found. Else return "Not Found"
    '''
    try:
        return(ip_df[(num_ip >= ip_df.IP_FROM) & (num_ip <= ip_df.IP_TO)]['COUNTRY'].values[0])
    except:
        return "Not Found"

# step 1. We have to convert the ip address to numeric representation so that we can compare with the Webnet77 IP to Country Database
user_ip['ip_num'] = user_ip.ip_address.apply(ip_to_num)

# Step 2: We have to compare the ip_num with the database's IP_FROM and IP_TO. The number must be within the two columns (inclusive). Then we want to extract them
user_ip['country'] = user_ip.ip_num.apply(get_country)

# keep relevant columns from user_ip 
user_country_df = user_ip[['userid', 'country']]

# load user_country_df to database
user_country_df.to_csv('../Healint_DE/data/user_country_table.csv', index=False)