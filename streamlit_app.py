
# Import python packages
import streamlit as st

helpful_links = [
    "https://docs.streamlit.io",
    "https://docs.snowflake.com/en/developer-guide/streamlit/about-streamlit",
    "https://github.com/Snowflake-Labs/snowflake-demo-streamlit",
    "https://docs.snowflake.com/en/release-notes/streamlit-in-snowflake"
]

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write(
    f"""Choose the fruits you want in your custom Smoothies!
    """
)

from snowflake.snowpark.functions import col


import requests
smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
#st.text(smoothiefroot_response.json())
sf_df = st.dataframe(data=moothiefroot_response.json(), use_container_width=True)


cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('fruit_name'))
#st.dataframe(data=my_dataframe, use_container_width=True)


import streamlit as st


name_on_order = st.text_input("Name of the Smoothie", "")
st.write("The current Smoothie name", name_on_order)


ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:",
    my_dataframe,
    max_selections = 5
)

ingredients_string = ''

if ingredients_list:
    #st.write("You selected:", ingredients_list)
    #st.text(ingredients_list)
    for ingredients_each in ingredients_list:
        ingredients_string += ingredients_each + ' '
    #st.text(ingredients_string)

my_insert_stmt = """ insert into smoothies.public.orders(ingredients,NAME_ON_ORDER) values ('""" + ingredients_string + """','"""+name_on_order+"""')"""

#st.write(my_insert_stmt)
time_to_insert= st.button("Subtmit orders")

if time_to_insert:
    session.sql(my_insert_stmt).collect()
    st.success('Your Smoothie is ordered!', icon="✅")                                                  
