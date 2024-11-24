import streamlit as st
import pandas as pd # type: ignore
import os
import plotly.express as px
import matplotlib.pyplot as plt
import numpy as np

st.title('Visualization 📊')

df = pd.read_csv(os.path.join('static_data','df.csv'), index_col=0)

st.subheader('Introduction')
st.write('The DataFrame below displays the yearly percentage changes of stock prices based on the closing prices within a DataFrame. It filters for the last row of December for each year, computes percentage changes, and formats the result into a transposed DataFrame with the DataFrame name as the row index.')

with st.expander('DataFrame'):
    st.write(df)

st.subheader('Graphing')

# Convert percentage strings to float
df_float = df.applymap(lambda x: float(x) if isinstance(x, str) else x)
# Prepare data
#print(df_float)
years = df_float.columns
asset_classes = df_float.index

# Create a custom colormap
cmap = plt.get_cmap("copper")
cmap.set_bad(color="white")

# Prepare the data as a masked array
masked_data = np.ma.masked_invalid(df_float.to_numpy())

# Set up the figure and axis
fig, ax = plt.subplots(figsize=(24, 12))

# Display the data as blocks
cax = ax.imshow(masked_data, cmap=cmap, aspect='auto')

# Set labels and ticks
ax.set_xticks(range(len(years)))
ax.set_xticklabels(years)
ax.set_yticks(range(len(asset_classes)))
ax.set_yticklabels(asset_classes)

# Add a colorbar
cbar = fig.colorbar(cax, ax=ax)


# Loop through rows and columns of the normalized dataframe
for i in range(len(asset_classes)):
    for j in range(len(years)):
        # Add the value as text at the center of the cell
        ax.annotate(df_float.iloc[i, j], xy=(j, i),
                    ha='center', va='center', color='white')

ax.set_title('Asset Class Winners and Losers',fontfamily='Franklin Gothic Demi Cond',fontsize=24,loc='left')
        
# Show the plot
st.pyplot(fig)

del years, asset_classes, cmap, masked_data, fig, ax, cax, cbar, i, j

# plotly graphs
# Create the heatmap plot
fig = px.imshow(df,
                labels=dict(x="Years", y="Asset Class", color="Percentage"),
                x=df.columns,
                y=df.index,
               )

# Update the layout and x-axis
fig.update_xaxes(side="top")
fig.update_layout(title="Asset Class Winners and Losers")

# Add percentage values to the heatmap
for i, row in enumerate(df.index):
    for j, col in enumerate(df.columns):
        value = df.loc[row, col]
        fig.add_annotation(dict(x=j, y=i, text=value, ax=0, ay=0, xref="x", yref="y", 
                                showarrow=False, font=dict(size=12, color="white")))

# Show the plot
st.plotly_chart(fig)

del fig, i, row, j, col, value