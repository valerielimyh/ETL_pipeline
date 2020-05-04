-- if you're executing this within a Python IDE
# import relevant libraries
from psycopg2 import connect
from sqlalchemy import create_engine

# set your own parameters
params = {
    'host': 'localhost',
    'user': 'Valerie',
    'port': 5432
}

# connect to database engine 
connection_string = f'postgres://Valerie:{params["host"]}@{params["host"]}:{params["port"]}/ip_address_table'
engine = create_engine(connection_string)
connection = connect(**params, dbname='ip_address_table')
cursor = connection.cursor()

query="""
rollback;
SELECT countries, COUNT(userid) as num_users
FROM (SELECT userid, CASE WHEN (country IN ( 
                                    SELECT country 
                                    FROM ( SELECT country, COUNT(userid) as num_users
                                            FROM user_country_table
                                            GROUP BY country
                                            ORDER BY num_users DESC
                                            LIMIT 10 )top10 )) 
                                    THEN country ELSE 'Others' END AS countries
      FROM user_country_table) sub
GROUP BY countries
ORDER BY num_users DESC;
"""
cursor.execute(query)
cursor.fetchall()

-- if you're executing this within command line

# navigate to your local repo directory
$ cd [local_repo_directory]

# connect to database in psql 
$ psql
\connect ip_address_table

SELECT countries, COUNT(userid) as num_users
FROM (SELECT userid, CASE WHEN (country IN ( 
                                    SELECT country 
                                    FROM ( SELECT country, COUNT(userid) as num_users
                                            FROM user_country_table
                                            GROUP BY country
                                            ORDER BY num_users DESC
                                            LIMIT 10 )top10 )) 
                                    THEN country ELSE 'Others' END AS countries
      FROM user_country_table) sub
GROUP BY countries
ORDER BY num_users DESC;

-- Output
-- [('United States', 574),
--  ('United Kingdom', 95),
--  ('Others', 88),
--  ('France', 69),
--  ('Canada', 58),
--  ('Japan', 37),
--  ('Spain', 22),
--  ('Australia', 20),
--  ('Ireland', 13),
--  ('Germany', 12),
--  ('Netherlands', 12)]