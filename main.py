import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load the data
file_path = '/mnt/data/202406_202406_연령별인구현황_월간.csv'
data = pd.read_csv(file_path, encoding='euc-kr')

# Preprocess the data
data['Total_Population'] = data['2024년06월_계_총인구수'].str.replace(',', '').astype(int)
data['2015_Population'] = data['2024년06월_계_9세'].str.replace(',', '').astype(int)
data['2015_Ratio'] = data['2015_Population'] / data['Total_Population']
top_10_regions = data.nlargest(10, '2015_Ratio')

# Extract necessary columns for plotting
columns_to_plot = [col for col in data.columns if '세' in col and '계' in col]

# Create the Streamlit app
st.title('Population Structure of Top 10 Regions with Highest Ratio of People Born in 2015')

for _, row in top_10_regions.iterrows():
    region_name = row['행정구역']
    st.subheader(region_name)
    
    # Extract the population data for the region
    region_data = data[data['행정구역'] == region_name][columns_to_plot].T
    region_data.columns = ['Population']
    region_data.index = region_data.index.str.extract(r'(\d+세)')[0]
    
    # Plot the population structure
    fig, ax = plt.subplots()
    region_data.plot(kind='bar', ax=ax, legend=False)
    ax.set_title(f'Population Structure of {region_name}')
    ax.set_xlabel('Age Group')
    ax.set_ylabel('Population')
    st.pyplot(fig)
