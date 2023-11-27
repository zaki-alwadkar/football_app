import streamlit as st
import pandas as pd
import base64
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

st.title('NFL Football Stats (Rushing) Explorer')

st.markdown("""
This app performs simple webscraping of NFL Football player stats data (focusing on Rushing)!
* **Python libraries:** base64, pandas, streamlit, numpy, matplotlib, seaborn
* **Data source:** [pro-football-reference.com](https://www.pro-football-reference.com/).
""")

st.sidebar.header('User Input Features')
selected_year = st.sidebar.selectbox('Year', list(reversed(range(1990, 2020))))

# Web scraping of NFL player stats
# https://www.pro-football-reference.com/years/2019/rushing.htm
@st.cache
def load_data(year):
    url = "https://www.pro-football-reference.com/years/" + str(year) + "/rushing.htm"
    html = pd.read_html(url, header=1)
    df = html[0]
    raw = df.drop(df[df.Age == 'Age'].index)  # Deletes repeating headers in content
    raw = raw.fillna(0)
    playerstats = raw.drop(['Rk'], axis=1)
    return playerstats

playerstats = load_data(selected_year)

# Sidebar - Team selection
sorted_unique_team = sorted(playerstats.Tm.unique())
selected_team = st.sidebar.multiselect('Team', sorted_unique_team, sorted_unique_team)

# Sidebar - Position selection
unique_pos = ['RB', 'QB', 'WR', 'FB', 'TE']
selected_pos = st.sidebar.multiselect('Position', unique_pos, unique_pos)

# Filtering data
df_selected_team = playerstats[(playerstats.Tm.isin(selected_team)) & (playerstats.Pos.isin(selected_pos))]

st.header('Display Player Stats of Selected Team(s)')
st.write('Data Dimension: ' + str(df_selected_team.shape[0]) + ' rows and ' + str(df_selected_team.shape[1]) + ' columns.')
st.dataframe(df_selected_team)

# Download NBA player stats data
# https://discuss.streamlit.io/t/how-to-download-file-in-streamlit/1806
def filedownload(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
    href = f'<a href="data:file/csv;base64,{b64}" download="playerstats.csv">Download CSV File</a>'
    return href

st.markdown(filedownload(df_selected_team), unsafe_allow_html=True)

# Bar Graph
if st.button('Bar Graph - Total Rushing Yards'):
    st.header('Bar Graph - Total Rushing Yards')
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Convert 'Yds' column to numeric values
    df_selected_team['Yds'] = pd.to_numeric(df_selected_team['Yds'], errors='coerce')
    
    total_rushing_yards = df_selected_team.groupby('Tm')['Yds'].sum().sort_values(ascending=False)
    total_rushing_yards.plot(kind='bar', ax=ax, color='skyblue')
    ax.set_ylabel('Total Rushing Yards')
    ax.set_xlabel('Team')
    st.pyplot(fig)


# Scatter Plot
if st.button('Scatter Plot - Total Rushing Yards vs Attempts'):
    st.header('Scatter Plot - Total Rushing Yards vs Attempts')
    fig, ax = plt.subplots(figsize=(10, 6))

    # Convert numeric columns to numeric types
    numeric_columns = ['Att', 'Yds', 'TD', 'Lng', '1D', 'Y/A', 'Y/G', 'Fmb']
    for col in numeric_columns:
        df_selected_team[col] = pd.to_numeric(df_selected_team[col], errors='coerce')

    # Plot scatter plot
    sns.scatterplot(data=df_selected_team, x='Att', y='Yds', hue='Tm', s=100, ax=ax)
    
    ax.set_ylabel('Total Rushing Yards')
    ax.set_xlabel('Total Rushing Attempts')
    ax.set_title('Scatter Plot - Total Rushing Yards vs Attempts')
    st.pyplot(fig)

# Pie Chart
if st.button('Pie Chart - Total Rushing Yards by Team'):
    st.header('Pie Chart - Total Rushing Yards by Team')
    fig, ax = plt.subplots(figsize=(10, 6))

    # Convert 'Yds' column to numeric values
    df_selected_team['Yds'] = pd.to_numeric(df_selected_team['Yds'], errors='coerce')

    total_rushing_yards = df_selected_team.groupby('Tm')['Yds'].sum().sort_values(ascending=False)
    
    # Plot pie chart
    total_rushing_yards.plot(kind='pie', autopct='%1.1f%%', startangle=90, ax=ax)
    
    ax.set_ylabel('')
    ax.set_title('Pie Chart - Total Rushing Yards by Team')
    st.pyplot(fig)


# 3D Scatter Plot
if st.button('3D Scatter Plot - Rushing Stats'):
    st.header('3D Scatter Plot - Rushing Stats')
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')

    # Convert numeric columns to numeric types
    numeric_columns = ['Att', 'Yds', 'TD']
    for col in numeric_columns:
        df_selected_team[col] = pd.to_numeric(df_selected_team[col], errors='coerce')

    # Scatter plot
    scatter = ax.scatter(df_selected_team['Att'], df_selected_team['Yds'], df_selected_team['TD'], c=df_selected_team['Yds'], cmap='viridis', s=50)

    # Colorbar
    cbar = fig.colorbar(scatter)
    cbar.set_label('Total Rushing Yards')

    ax.set_xlabel('Total Rushing Attempts')
    ax.set_ylabel('Total Rushing Yards')
    ax.set_zlabel('Total Touchdowns')
    ax.set_title('3D Scatter Plot - Rushing Stats')

    st.pyplot(fig)
    
    
    


 

