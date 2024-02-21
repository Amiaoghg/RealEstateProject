import pandas as pd
import numpy as np
import plotly.express as px
pd.options.plotting.backend = "plotly"
import plotly.graph_objects as go
import json
import streamlit as st
from streamlit_option_menu import option_menu
import geopandas as gpd
import plotly.io as pio
pio.renderers.default='browser'
mypath = ""
counta = gpd.read_file(mypath + "geojson-counties-fips.json")  
counta = counta.rename(columns={'COUNTY':"countyfips", "STATE":"state_fips"})
gdf = gpd.read_file(mypath + "data.geojson")
fixed_fips = pd.read_csv(mypath + "state_and_county_fips_master.csv").dropna()
fixed_fips.name = fixed_fips["name"].str.split().str[0]
fixed_fips = fixed_fips.rename(columns = {'name' : 'county'})
df = pd.read_csv(mypath + "cleaned.csv")
county_pop = pd.read_csv(mypath + "pop.csv").dropna()
## upload pop.csv






from urllib.request import urlopen
import json
with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    desired = json.load(response)








df = df[~df.isin(['Puerto Rico']).any(axis=1)]
df = df[~df.isin(['Wyoming']).any(axis=1)]
df = df[~df.isin(['Puerto Rico']).any(axis=1)]
df = df[~df.isin(['New Jersey']).any(axis=1)]


b = [
    df.price < 10000,
    (df.price >= 10000) & (df.price < 100000),
    (df.price >= 100000) & (df.price < 200000),
    (df.price >= 200000) & (df.price < 300000),
    (df.price >= 300000) & (df.price < 400000),
    (df.price >= 400000) & (df.price < 500000),
    (df.price >= 500000) & (df.price < 600000),
    (df.price >= 600000) & (df.price < 700000),
    (df.price >= 700000) & (df.price < 800000),
    (df.price >= 800000) & (df.price < 900000),
    (df.price >= 900000) & (df.price < 1000000),
    (df.price >= 1000000) & (df.price < 1100000),
    (df.price >= 1100000) & (df.price < 1200000),
    (df.price >= 1200000)
]




choices = ['Below 10k', 'Below 100k', '100k', '200k', '300k', '400k', '500k', '600k', '700k','800k','900k','1m','1.1m','Over1.2m']


df['price_range'] = np.select(b, choices, default='Unknown')






size = [
    df.house_size < 1000,
    (df.house_size >= 1000) & (df.house_size < 2000),
    (df.house_size >= 2000) & (df.house_size < 3000),
    df.house_size >= 3000
]




size_type = ['Small',"Medium","Large","Huge"]
df['size_range'] = np.select(size, size_type)




bath1 = [


    (df.bath >= 1) & (df.bath < 3),
    (df.bath >= 3) & (df.bath < 10),
    df.bath >= 10
]




bath_type = ['Regular',"Mansion","Hotel"]
df['bath_type'] = np.select(bath1, bath_type)


bed1 = [


    (df.bed >= 1) & (df.bed < 3),
    (df.bed >= 3) & (df.bed < 10),
    df.bed >= 10
]




bed_type = ['Regular',"Mansion","Hotel"]
df['bed_type'] = np.select(bed1, bed_type, default='Unknown')


test = gdf[gdf["name"] == "Winchester"]


uc = df.city.unique()
us = ["VI","MA","CT","NY","NH","VT","RI","ME"]


dfstate = {"Massachusetts": 'MA', "New Hampshire": "NH", "Rhode Island": "RI", "Connecticut":"CT", "Maine":"ME", "Vermont": "VT", "New York": "NY", "Virgin Islands":"VI"}






df['state'] = df.state.replace(dfstate)
target = gdf['name'].isin(uc) & gdf['state'].isin(us)
target1 = gdf[target].copy()
target1.rename(columns = {'name' : 'city'}, inplace = True)


num_cols = df.select_dtypes(include=['int', 'float']).columns


test2 = df[df.duplicated(subset = ("city","state"))]
test3= target1[target1.duplicated(subset = ["city" , "state"])]
test4 = target1[target1.duplicated()]
test5 = target1[(target1["city"].isin(test3.city)&(target1["state"].isin(test3.state)))]
dc = ["Washington","Greene","Orange","Cattaraugus","Ulster","Erie","Herkimer","Oxford"]
droped = target1[(target1["city"].isin(test5.city)&(target1["state"].isin(test5.state))
                &target1["county"].isin(dc))]
target2 = target1[~ target1.id.isin(droped.id)]




merged = pd.merge(df, target2, how="left", on= ['city','state'])
merged = merged[merged['state'] != 'VI']




null = merged[merged.latitude.isnull()]


cat_cols = df.select_dtypes(include=['object']).columns
box_cols = ['price_range','size_rang','bath_type','bed_type']
hover1 = ['price_range', 'size_range', 'bed_type', 'city', 'state', 'bed', 'bath', 'house_size', 'price' ]


center = {"lat": 41, "lon": 74}




county_pop['county'] = county_pop['county'].str[1:]


county1 = county_pop['county'].str.split(",", expand = True).rename({ 0:"countytest", 1 : "state"}, axis = 1)
county_pop = pd.concat([county_pop,county1 ], axis = 1)
county_pop["county"] = county_pop["countytest"].str.replace(" County", "")
county_pop = county_pop.drop("countytest", axis = 1)
county_pop["2022"] = county_pop["2022"].str.replace(",", "").astype(int)
county_pop = county_pop.rename({"2022":"population"},axis = 1)
county_pop["state"] = county_pop['state'].str.strip().replace(dfstate)
merged = pd.merge(merged, county_pop, how = "left", on = ['county', 'state'])


merged = pd.merge(merged.drop("geometry", axis = 1), counta[["countyfips","geometry","state_fips"]], how = "left", on = ['countyfips','state_fips'])




merged["fips"] = merged["state_fips"]+merged["countyfips"]


gdf1 = gpd.GeoDataFrame(merged, geometry='geometry')


geojson_data = gdf1.drop_duplicates(subset="fips").to_json()










num_cols = merged.select_dtypes(include=['int', 'float']).columns


merged = merged.drop(["status","id","gnis_id","feature","pop_2010","feature2","elev_in_ft","fips","countyfips","state_fips"],axis = 1)
merged=pd.merge(merged, fixed_fips, how = "left", on = ['county','state'])




fig = px.choropleth(merged.groupby(['fips','state','county'])['price'].mean().reset_index(), geojson=desired,color='price',locations = "fips",
                           color_continuous_scale="Pinkyl",
                           scope="usa",
                           range_color=(0, 1000000),
                           labels={'unemp':'unemployment rate'},
                           hover_name='county',
                           hover_data=["state", "county"]


                           
                          )
fig.update_geos(fitbounds="locations", visible=False)
  






with st.sidebar: 
	selected = option_menu(
		menu_title = 'Navigation Pane',
		options = ['Abstract', 'Background Information', 'Data Cleaning','Exploratory Analysis', 'Analysis', 'Conclusion', 'Bibliography'],
		menu_icon = 'arrow-down-right-circle-fill',
		icons = ['bookmark-check', 'book', 'box', 'map', 'boxes', 'bar-chart'],
		default_index = 0,
		)


if selected=='Abstract':
    
    st.markdown("In this case study, we will be exploring the different effects that factors have on the housing prices on the east coast. Although many factors will effect the housing market, some have a larger role than others. Here, I will be going in-depth about the different factors that affect the pricing.")
    




if selected=="Background Information":
    st.title("Background Information")
    st.markdown("Purchasing a house is a matter that everyone has to go through at some point, and the value of  the house will often fluctuate based on certain factors about the house. Figuring out what makes a house expensive is useful to everyone. Below are 10 of the factors that experts have concluded:")


    st.markdown("Location:")
    st.markdown("")
    st.markdown("According to experts, the location of the house is most important. A mansion in a middle of a desert will cost less than if it were in the city. ")
    st.markdown("Size:")
    st.markdown("")
    st.markdown("The size of the house is no doubt a factor; in 9 out of 10 cases, a bigger house beats a smaller one")
    st.markdown("")
    st.markdown("Features in the house")
    st.markdown("")
    st.markdown("Amount of bedrooms, bathrooms, etc; based on the amount of features in the house’s value could rise and fall.")
    st.markdown("")
    st.markdown(" Other factors that are unrelated to the house also effect housing prices, such as interest rates, inflation, and overall housing markets. These factors will not be put into consideration in this case study.")






    
if selected=="Data Cleaning":
    st.title('Data Cleaning')
    st.markdown(df.info())
    st.markdown("My set of data has lots of missing values within it, with only a few sections having a full 306000 datapoints. To start with,I have to identify the least important parts of my data.In this case, zip_code , prev_sold_date and status are the least important. zip_code will not be used throughout my data analyzation.")
    st.markdown("For the status, I only want to analyze houses that are already built.")
    st.code("a = 'ready_to_build' built = df[df['status'] != a] built.status.value_counts()")


   
        
    st.markdown("Now, everything left in the dataset has already been built")
    st.markdown("Looking through data points one by one, I will be filling in all NA's in bed and bath with 1's, as each house would at least have a bedroom and a bathroom.")
    st.code("built.bed.fillna(1, inplace=True) built.bath.fillna(1, inplace=True) built.info()")
    st.markdown("With bed and bath fixed, we move o to acre_lot. Acre_lot would not be relevant to almost any conclusion I could have used, so I entirely removed it.")


    st.markdown("Finally, dropping all values with a NAN in city, state or house_size, because those 3 are the most important values")
    st.markdown("Now that the dataset is finally clean, the next step is to add geometry for each of the counties. I first had to rename each of the states into its abbreviations")
    st.code('''dfstate = {"Massachusetts": 'MA', "New Hampshire": "NH", "Rhode Island": "RI", "Connecticut":"CT", "Maine":"ME", "Vermont": "VT", "New York": "NY", "Virgin Islands":"VI"}


df['state'] = df.state.replace(dfstate)''')
    st.markdown("In order to combine a county dataframe with my original dataframe, I had to match each state and county. During this process, I found out that multiple states have the same county names, so I had to test and remove each of them.")


    st.code('''target1 = gdf[target].copy()
target1.rename(columns = {'name' : 'city'}, inplace = True)


num_cols = df.select_dtypes(include=['int', 'float']).columns


test2 = df[df.duplicated(subset = ("city","state"))]
test3= target1[target1.duplicated(subset = ["city" , "state"])]
test4 = target1[target1.duplicated()]
test5 = target1[(target1["city"].isin(test3.city)&(target1["state"].isin(test3.state)))]
dc = ["Washington","Greene","Orange","Cattaraugus","Ulster","Erie","Herkimer","Oxford"]
droped = target1[(target1["city"].isin(test5.city)&(target1["state"].isin(test5.state))
                &target1["county"].isin(dc))]
target2 = target1[~ target1.id.isin(droped.id)]''')


    st.markdown("After finding out each of the duplicated city and removing them, I had to merge my dataframes. While merging however, the geo-data frame will not match up exactly with my old one, so I had to match county-fips(and ID assigned to each county by the government), and combine them like that")


    st.code('''county_pop['county'] = county_pop['county'].str[1:]


county1 = county_pop['county'].str.split(",", expand = True).rename({ 0:"countytest", 1 : "state"}, axis = 1)
county_pop = pd.concat([county_pop,county1 ], axis = 1)
county_pop["county"] = county_pop["countytest"].str.replace(" County", "")
county_pop = county_pop.drop("countytest", axis = 1)
county_pop["2022"] = county_pop["2022"].str.replace(",", "").astype(int)
county_pop = county_pop.rename({"2022":"population"},axis = 1)
county_pop["state"] = county_pop['state'].str.strip().replace(dfstate)
merged = pd.merge(merged, county_pop, how = "left", on = ['county', 'state'])


merged = pd.merge(merged.drop("geometry", axis = 1), counta[["countyfips","geometry","state_fips"]], how = "left", on = ['countyfips','state_fips'])




merged["fips"] = merged["state_fips"]+merged["countyfips"]


gdf1 = gpd.GeoDataFrame(merged, geometry='geometry')


geojson_data = gdf1.drop_duplicates(subset="fips").to_json()
merged = merged.drop(["status","id","gnis_id","feature","pop_2010","feature2","elev_in_ft","fips","countyfips","state_fips"],axis = 1)
merged=pd.merge(merged, fixed_fips, how = "left", on = ['county','state'])
''')






    
if selected=="Exploratory Analysis":
    st.title('Exploratory Analysis')
    
   
            
        


    col11,col12 = st.columns([11,12])
    with st.form("Select what to compare"):
        num_col11 = col11.selectbox("Select for color", num_cols, key=13)
        check1 = col11.checkbox(label = "check for custom range")
        submitted = st.form_submit_button("Make graph")
        if submitted: 
            notmerged = (merged.groupby(['fips','state','county'])[num_col11].mean().reset_index())
            sliderrange = None
            if check1:
                slider1 = col11.slider("Select color range", min_value= notmerged[num_col11].min(), max_value = notmerged[num_col11].max())
                sliderrange = (notmerged[num_col11].min(),slider1)
            
            fig1 = px.choropleth(notmerged, geojson=desired,color=num_col11,locations = "fips",
                                       color_continuous_scale="Pinkyl",
                                       scope="usa",
                                       labels={'unemp':'unemployment rate'},
                                       hover_name='county',
                                       hover_data=["state", "county"],
                                       range_color= sliderrange


                                       
                                      )
            fig1.update_geos(fitbounds="locations", visible=False)
            
              
            
            col12.plotly_chart(fig1)


    


     
        
    
    
if selected=="Analysis":
    st.title("Analysis")
    
    st.title("Population")
    st.markdown("The population of an area can often decide the regions housing prices. Having a high population density generally means that the housing prices will be higher, due to more demand of housing, even if on average, the house will lack features.")
    fig = px.choropleth(merged.groupby(['fips','state','county'])[['population','price']].mean().reset_index(), geojson=desired,color='population',locations = "fips",
                               color_continuous_scale="Pinkyl",
                               scope="usa",
                               range_color=(0, 1000000),
                               labels={''},
                               hover_name='county',
                               hover_data=["state", "county", "price"]


                               
                              )
    fig.update_geos(fitbounds="locations", visible=False)
    st.plotly_chart(fig)
    st.title("House features")
    st.markdown("Housing prices are also in part, influenced by it’s own features. In the case study, the average amount of features such as bathrooms or bedroom that are present in each county is taken into consideration.")
    fig11 = px.choropleth(merged.groupby(['fips','state','county'])[['bed','price']].mean().reset_index(), geojson=desired,color='bed',locations = "fips",
                               color_continuous_scale="Pinkyl",
                               scope="usa",
                               range_color=(0, 10),
                               labels={''},
                               hover_name='county',
                               hover_data=["state", "county", "price"]


                               
                              )
    fig11.update_geos(fitbounds="locations", visible=False)
    st.plotly_chart(fig11)
    st.title("House size")
    st.markdown("Similar to the features in a house, the size of a house is often also a deciding factor to it’s price. While it shares great overlap with housing-features, it also has unique interactions when population and location is taken into account.")
    fig12 = px.choropleth(merged.groupby(['fips','state','county'])[['house_size','price']].mean().reset_index(), geojson=desired,color='house_size',locations = "fips",
                               color_continuous_scale="Pinkyl",
                               scope="usa",
                               range_color=(0, 6000),
                               labels={''},
                               hover_name='county',
                               hover_data=["state", "county", "price"]


                               
                              )
    fig12.update_geos(fitbounds="locations", visible=False)
    st.plotly_chart(fig12)
    st.title("Location & climate")
    st.markdown("Many people have preferences on the local climate of their environment. When latitude and temperature is put into consideration, it can reveal the preferences of where people of different wealths prefer to live. ")
   


        
    
if selected=="Conclusion":
    st.title("Conclusion")
    
    st.markdown("	After comparing the effect that each common factor has, a lot of relevant information was collected, such as on average, rich people tend to populate coastal counties and cities more than inland ones. Below is a graph that shows the specifics of how much each factor had effected the housing price of the area. ")
    st.button("Show process", help = "In order to make the graph, I compared what a 10% change on each relevant factor had increased the housing price by (in percentages) across all counties")
   
    effects = ["bed","bath","house_size","population","population in previous years", "Longitude", "Latitude"]
    values = [7.1,3.2,32.3,36.7,18.7,11.9,-13.2]
    effects2 = pd.DataFrame(zip(effects,values),columns = ["effects","values"])
    fig111 = px.bar(effects2, x= "effects", y="values", title="Different effects on housing price")
    st.plotly_chart(fig111)


    st.markdown("As seen in the graph, the population of a county has the greatest impact overall, with house size coming in as a close second. However, there seems to also be some factors that negatively impact a house’s price, primarily it’s latitude. This can mainly be attributed to the fact that at higher altitudes in the region of study, the weather most likely would be lower. ")
    
if selected=="Bibliography":
    st.title("Bibliography")
    
    
    
    
    
    
    
    
    
    
    
    