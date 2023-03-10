import altair as alt
import pandas as pd
import streamlit as st 
import matplotlib.pyplot as plt
import plotly.express as px

alt.data_transformers.disable_max_rows()
st.title('Data Analized')


playStore = pd.read_csv('assignment/googleplaystore.csv')
playStore['Price'] = playStore['Price'].str.replace('$', '')
playStore['Price'] = playStore['Price'].str.replace('Everyone', '0')
playStore['Reviews'] = playStore['Reviews'].str.replace('M', '')
playStore = playStore.astype({'Price':float,'Reviews':float})
playStore.drop(playStore[playStore['Rating'] == 19. ].index, inplace=True)
playStore.dropna(inplace=True)
playStore["Last Updated"] = pd.to_datetime(playStore["Last Updated"], format="%B %d, %Y")
playStore["Year"] = playStore["Last Updated"].dt.year
playStoreApp = st.selectbox("Select app Category of the App", playStore['Category'].unique())
scatter_plot = st.checkbox("scatter plot")
line_plot = st.checkbox("line plot")
histogram_plot = st.checkbox("histogram plot")
bar_plot = st.checkbox("bar plot")
heatmap_plot = st.checkbox("heatmap plot")
years = playStore["Year"].unique()

# Create a slider for the year

plots = []

if scatter_plot:
    plots.append(alt.Chart(playStore[playStore['Category'] == playStoreApp],width=800, height=600).mark_circle().encode(
      x = 'Installs',
      y = 'Reviews',
      color='App:N',
      tooltip = ['Reviews','Installs','App','Year','Last Updated']
  ).interactive())

if line_plot:
    plots.append(alt.Chart(playStore[playStore['Category'] == playStoreApp],width=800, height=600).mark_line().encode(
      x = 'Reviews',
      y = 'Installs',
      color='Content Rating:N',
      tooltip = ['Reviews','Installs','App']
  ).interactive())

if histogram_plot:
    plots.append(alt.Chart(playStore[playStore['Category'] == playStoreApp],width=800, height=600).mark_bar().encode(
      x = 'Reviews',
      y = 'count()',
       color='App:N',
      tooltip = ['Reviews','App']
  ).interactive())

if bar_plot:
    plots.append(alt.Chart(playStore[playStore['Category'] == playStoreApp],width=800, height=600).mark_bar().encode(
      y = 'Reviews',
      x = 'App',
       color='App:N',
      tooltip = ['Reviews','App']
  ).interactive())

if heatmap_plot:
    plots.append(alt.Chart(playStore[playStore['Category'] == playStoreApp],width=800, height=600).mark_rect().encode(
    alt.X('Rating:Q', bin=alt.Bin(maxbins=60)),
    alt.Y('Reviews:Q', bin=alt.Bin(maxbins=40)),
    alt.Color('Rating:Q', scale=alt.Scale(scheme='greenblue')),
      tooltip=['App','Rating','Genres']
).interactive())

if plots:
    st.altair_chart(alt.vconcat(*plots))
    #combined_plot = alt.layer(*plots)  combine all in one chart
    #st.altair_chart(combined_plot)


st.subheader('Pie plot of a sample data of 10 apps and their price')
sampledata  = playStore.head(10).copy()
fig, ax = plt.subplots()
explode = (0, 0, 0.4, 0,0,0,0,0,0,0.4)  
ax.pie(sampledata['Rating'], labels=sampledata['App'],explode=explode,
        shadow=True, startangle=90,autopct='%1.1f%%')


st.pyplot(fig)
st.subheader('Area chart of 100 App')
sampledataArea  = playStore.head(100).copy()
st.area_chart(data=sampledata, x='Last Updated', y=['Reviews','Installs','Rating','App'], width=0, height=0, use_container_width=True)

# @st.cache
# def convert_df(df):
#     # IMPORTANT: Cache the conversion to prevent computation on every rerun
#     return df.to().encode('utf-8')

# jpegg = convert_df(my_large_df)

# st.download_button(
#     label="Download data as Jpeg",
#     data=jpegg,
#     file_name='large_df.jpeg',
#     mime='image/jpeg',
# )
fig = px.scatter(
    playStore.head(30),
    x="Reviews",
    y="Installs",
    size="Reviews",
    color="App",
    hover_name="App",
    log_x=True,
    size_max=60,
)
fig
st.balloons()
