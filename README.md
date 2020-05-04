ETL pipeline 
============
To identify the country of a user based on the IP address, by replicating an external IP database into the data warehouse.

# Prerequisites
In Python, make sure to have postgresql, psycopy and sqlalchemy installed. if not do execute the steps below

brew install postgresql

pip install psycopg2

pip install sqlalchemy


# Deployment
Step 1. Run the clone_repo.py file to clone this repo to your local directory (../Healint_DE). The script will ask you to input the url of the github repo you want to download, as well as the path of the local directory where you want to clone to.


Step 2. Run 01-Extraction.py - This script downloads the ​latest​ IP address table ('external_ip_address'), creates a database ('ip_address_table') and load it into 'ip_address_table'.


Step 3. Run 02-Transformation.py - This script joins the 'ip_address_table' with the given user information ('user_ip'). The final table ('user_country_table') contains `userid` and `country` name. 


Step 4. Run 03-validation.sql - This query returns the number of unique users in the top 10 countries, and the number of users from other countries that are grouped under a self-defined country code `Others`
