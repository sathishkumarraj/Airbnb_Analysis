import streamlit as st
from streamlit_option_menu import option_menu
import plotly.express as px
import pandas as pd
import plotly.figure_factory as ff
from PIL import Image
import warnings
import os
warnings.filterwarnings('ignore')


# Set page configuration
st.set_page_config(
    page_title="AirBnb-Analysis by SATHISH KUMAR R!!!",
    page_icon=":bar_chart:",
    layout="wide"
)

def setting_bg():
    st.markdown(f""" <style>.stApp {{
                        # background:url("https://images.pexels.com/photos/1631677/pexels-photo-1631677.jpeg?auto=compress&cs=tinysrgb&w=600");
                        background-size: cover;
                        backdrop-filter: blur(50px)}}
                     </style>""" ,unsafe_allow_html=True)

setting_bg()

# Set the background color and padding for better aesthetics
st.markdown("<style>body { background-color: #f8f9fa; }</style>", unsafe_allow_html=True)
st.markdown("<style>.block-container { padding: 1rem; }</style>", unsafe_allow_html=True)

# Set the title with custom styling
st.title("AirBnb-Analysis")
st.markdown("<style>h1 { color: #FF385C; font-size: 36px; }</style>", unsafe_allow_html=True)

with st.sidebar:
    SELECT = option_menu(
        menu_title=None,
        options=["Home", "Explore Data", "Contact"],
        icons=["house", "bar-chart", "at"],
        default_index=2,
        orientation="vertical",
        styles={
            "container": {
                "padding": "20px",
                "background-color": "white",
                "width": "300px",
                },
            "icon": {
                "color": "#FF385C",
                "font-size": "20px",
            },
            "nav-link": {
                "font-size": "18px",
                "text-align": "center",
                "margin": "20px 0",
                "--hover-color": "white",
                "color": "#FF385C",
                
            },
            "nav-link-selected": {
                "background-color": "black",
                "color": "#FF385C",
            },
        }
    )
    
# ----------------Home----------------------#

if SELECT == "Home":
        col1, col2 = st.columns([3,1])
        with col1:
            st.subheader("Airbnb is an American San Francisco-based company operating an online marketplace for short- and long-term homestays and experiences. The company acts as a broker and charges a commission from each booking. The company was founded in 2008 by Brian Chesky, Nathan Blecharczyk, and Joe Gebbia. Airbnb is a shortened version of its original name, AirBedandBreakfast.com. The company is credited with revolutionizing the tourism industry, while also having been the subject of intense criticism by residents of tourism hotspot cities like Barcelona and Venice for enabling an unaffordable increase in home rents, and for a lack of regulation.")
            st.subheader('Skills take away From This Project:')
            st.subheader('Python Scripting, Data Preprocessing, Visualization, EDA, Streamlit, MongoDb, PowerBI or Tableau')
            st.subheader('Domain:')
            st.subheader('Travel Industry, Property management and Tourism')
            
        with col2:    
            st.image("https://cdn.dribbble.com/users/1815739/screenshots/4740027/airbnbexp_gif1.gif", use_column_width=True, width=100)

# ----------------Explore Data----------------------#

if SELECT == "Explore Data":
    fl = st.file_uploader(":file_folder: Upload a file", type=(["csv", "txt", "xlsx", "xls"]))
    if fl is not None:
        filename = fl.name
        st.write(filename)
        df = pd.read_csv(filename, encoding="ISO-8859-1") 
    else:
        os.chdir(r"C:\Users\sathi\OneDrive\Desktop\Guvi Capstone projects\Airbnb_Analysis_Project")
        df = pd.read_csv("Airbnb NYC 2019.csv", encoding="ISO-8859-1")

    st.sidebar.header("Choose your filter: ")

    # Create for neighbourhood_group
    neighbourhood_group = st.sidebar.multiselect("Pick your neighbourhood_group", df["neighbourhood_group"].unique())
    if not neighbourhood_group:
        df2 = df.copy()
    else:
        df2 = df[df["neighbourhood_group"].isin(neighbourhood_group)]

    # Create for neighbourhood
    neighbourhood = st.sidebar.multiselect("Pick the neighbourhood", df2["neighbourhood"].unique())
    if not neighbourhood:
        df3 = df2.copy()
    else:
        df3 = df2[df2["neighbourhood"].isin(neighbourhood)]

    # Filter the data based on neighbourhood_group, neighbourhood
    if not neighbourhood_group and not neighbourhood:
        filtered_df = df
    elif not neighbourhood:
        filtered_df = df[df["neighbourhood_group"].isin(neighbourhood_group)]
    elif not neighbourhood_group:
        filtered_df = df[df["neighbourhood"].isin(neighbourhood)]
    elif neighbourhood:
        filtered_df = df3[df["neighbourhood"].isin(neighbourhood)]
    elif neighbourhood_group:
        filtered_df = df3[df["neighbourhood_group"].isin(neighbourhood_group)]
    elif neighbourhood_group and neighbourhood:
        filtered_df = df3[df["neighbourhood_group"].isin(neighbourhood_group) & df3["neighbourhood"].isin(neighbourhood)]
    else:
        filtered_df = df3[df3["neighbourhood_group"].isin(neighbourhood_group) & df3["neighbourhood"].isin(neighbourhood)]

    room_type_df = filtered_df.groupby(by=["room_type"], as_index=False)["price"].sum()

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Room Type ViewData")
        fig = px.bar(room_type_df, x="room_type", y="price", text=['${:,.2f}'.format(x) for x in room_type_df["price"]],
                     template="seaborn")
        st.plotly_chart(fig, use_container_width=True, height=200)

    with col2:
        st.subheader("Neighbourhood Group ViewData")
        fig = px.pie(filtered_df, values="price", names="neighbourhood_group", hole=0.5)
        fig.update_traces(text=filtered_df["neighbourhood_group"], textposition="outside")
        st.plotly_chart(fig, use_container_width=True)

    cl1, cl2 = st.columns((2))
    with cl1:
        with st.expander("Room Type wise Price"):
            st.write(room_type_df.style.background_gradient(cmap="Blues"))
            csv = room_type_df.to_csv(index=False).encode('utf-8')
            st.download_button("Download Data", data=csv, file_name="room_type.csv", mime="text/csv",
                               help='Click here to download the data as a CSV file')

    with cl2:
        with st.expander("Neighbourhood Group wise Price"):
            neighbourhood_group = filtered_df.groupby(by="neighbourhood_group", as_index=False)["price"].sum()
            st.write(neighbourhood_group.style.background_gradient(cmap="Oranges"))
            csv = neighbourhood_group.to_csv(index=False).encode('utf-8')
            st.download_button("Download Data", data=csv, file_name="neighbourhood_group.csv", mime="text/csv",
                               help='Click here to download the data as a CSV file')

    # Create a scatter plot
    data1 = px.scatter(filtered_df, x="neighbourhood_group", y="neighbourhood", color="room_type")
    data1['layout'].update(title="Room_type in the Neighbourhood and Neighbourhood_Group wise data using Scatter Plot.",
                            titlefont=dict(size=20), xaxis=dict(title="Neighbourhood_Group", titlefont=dict(size=20)),
                            yaxis=dict(title="Neighbourhood", titlefont=dict(size=20)))
    st.plotly_chart(data1, use_container_width=True)

    with st.expander("Detailed Room Availability and Price View Data in the Neighbourhood"):
        st.write(filtered_df.iloc[:500, 1:20:2].style.background_gradient(cmap="Oranges"))

    # Download original DataSet
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button('Download Data', data=csv, file_name="Data.csv", mime="text/csv")

    import plotly.figure_factory as ff

    st.subheader(":point_right: Neighbourhood Group wise Room Type and Minimum stay nights")
    with st.expander("Summary_Table"):
        df_sample = df[0:5][["neighbourhood_group", "neighbourhood", "reviews_per_month", "room_type", "price", "minimum_nights", "host_name"]]
        fig = ff.create_table(df_sample, colorscale="Cividis")
        st.plotly_chart(fig, use_container_width=True)

    # map function for room_type

    # If your DataFrame has columns 'Latitude' and 'Longitude':
    st.subheader("Airbnb Analysis in Map view")
    df = df.rename(columns={"Latitude": "lat", "Longitude": "lon"})

    st.map(df)

# ----------------------Contact---------------#

if SELECT == "Contact":
    Name = (f'{"Name :"}  {"SATHISH KUMAR R"}')
    mail = (f'{"Mail :"}  {"sathishkumarraj7@gmail.com"}')
    description = "An Aspiring DATA-SCIENTIST..!"
    social_media = {
        "GITHUB": "https://github.com/sathishkumarraj",
        "LINKEDIN": "https://www.linkedin.com/in/sathishkumarraj/"
    }

    col1, col2 = st.columns(2)
    with col1:
        st.image("https://mir-s3-cdn-cf.behance.net/project_modules/hd/699e4762225981.5a89af14d87a9.gif", use_column_width=True, width=300)    

    with col2:
        # st.header('Airbnb Analysis')
        st.subheader(
            "This project aims to analyze Airbnb data using MongoDB Atlas, perform data cleaning and preparation, develop interactive geospatial visualizations, and create dynamic plots to gain insights into pricing variations, availability patterns, and location-based trends.")
        st.write("---")
        st.subheader(Name)
        st.subheader(mail)

    st.write("#")
    cols = st.columns(len(social_media))
    for index, (platform, link) in enumerate(social_media.items()):
        cols[index].write(f"[{platform}]({link})")
