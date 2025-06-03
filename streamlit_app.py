import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col 
import requests
import pandas as pd
from PIL import Image
 
# Set title
st.title("Zena's Amazing Athleisure Catalog")

# Get Snowflake session
cnx = st.connection("snowflake")
session = cnx.session()

# Read the table and select the required column
my_dataframe = session.table("ZENAS_ATHLEISURE_DB.PRODUCTS.catalog_for_website").select(col('COLOR_OR_STYLE'))

# Convert to pandas for Streamlit
pd_df = my_dataframe.to_pandas()

# Drop duplicates and NA just to be safe
pd_colors = pd_df['COLOR_OR_STYLE'].dropna().unique()

# Create drop-down
option = st.selectbox('Pick a sweatsuit color or style:', pd_colors)

# Display the selection
st.write("You selected:", option)

# We'll build the image caption now, since we can
product_caption = 'Our warm, comfortable, ' + option + ' sweatsuit!'

# use the color selected to go back and get all the info from the database
table_prod_data = session.sql("select file_name, price, size_list, upsell_product_desc, file_url from ZENAS_ATHLEISURE_DB.PRODUCTS.catalog_for_website where color_or_style = '" + option + "';")
pd_prod_data = table_prod_data.to_pandas() 

# assign each column of the row returned to its own variable 
price = '$' + str(pd_prod_data['PRICE'].iloc[0])+'0'
file_name = pd_prod_data['FILE_NAME'].iloc[0]
size_list = pd_prod_data['SIZE_LIST'].iloc[0]
upsell = pd_prod_data['UPSELL_PRODUCT_DESC'].iloc[0]
url = pd_prod_data['FILE_URL'].iloc[0]

###****** This is  to prinit the url for download.
#  st.write(file_name)
#  st.write(url)
###****** no need to prinit the url for download.

# display the info on the page
#image = Image.open(url)
#st.image(image, width=400, caption=product_caption)
st.image(image=url, width=400, caption=product_caption)
st.markdown('**Price:** '+ price)
st.markdown('**Sizes Available:** ' + size_list)
st.markdown('**Also Consider:** ' + upsell)


#st.write(url)
