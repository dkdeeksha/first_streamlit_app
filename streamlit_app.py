import streamlit
import pandas as pd
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title("My Mom's New Healthy Diner")

streamlit.header('Breakast Favourites')

streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Eggs')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

# import pandas as pd
my_fruit_list = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")

my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
# streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index))

# choose a few fruits to set a few example
# streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado', 'Strawberries'])

# choose fruits and pass selection into the table
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado', 'Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]


# Display the table on the page.
streamlit.dataframe(fruits_to_show)

# new section to display fruityvice api response
streamlit.header('Fruityvice Fruit Advice!')

# Move the Fruityvice Code into a Try-Except (with a nested If-Else)

try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
  if not fruit_choice:
    streamlit.error("Please select a fruit to get information.")
  else:
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
    fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
    streamlit.dataframe(fruityvice_normalized)
    
 except URLError as e:
  streamlit.error()
  

  # fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
  # streamlit.write('The user entered ', fruit_choice)

  # # import requests
  # fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
  # # streamlit.text(fruityvice_response.json())    commented -- just writes data to the screen

  # # take json version of response and normalize it  
  # fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
  # streamlit.dataframe(fruityvice_normalized)

# dont run anything past this line while we troubleshoot
streamlit.stop()

#import snowflake.connector

my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("select * from fruit_load_list")

#my_data_row = my_cur.fetchone() # fetches one record
my_data_rows = my_cur.fetchall()
streamlit.text("The fruit load list contains")
streamlit.dataframe(my_data_rows)

# allow user to add fruit to the list
add_my_fruit = streamlit.text_input('What fruit would you like to add?','jackfruit')
streamlit.write('Thanks for adding ', add_my_fruit)

#testing what will happen
my_cur.execute("insert into fruit_load_list values ('from Streamlit')")
