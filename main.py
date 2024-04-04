import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

#read CSV file
# Function to load data from URL
def load_data():
    return pd.read_csv("https://raw.githubusercontent.com/Natthadon01/test/main/test_data_clean.csv")

# Load initial data
df = load_data()

# Function to update data
def update_data():
    while True:
        new_df = load_data() # Load new data
        df.iloc[:] = new_df.iloc[:] # Update DataFrame
        time.sleep(60)


#Page Setup
st.set_page_config(
    page_title="Restaurant Analytics",
    layout="wide")

st.title('Restaurant Analytics')


## Chart 1 Trend of Food Products Sales

# Adjust datatype and format of the date column.
df[['Day', 'Month', 'Year']] = df['Date'].str.split('/', expand=True)

df['Date'] = pd.to_datetime(df[['Day', 'Month', 'Year']], format='%d/%m/%y')

df.drop(['Day', 'Month', 'Year'], axis=1, inplace=True)


# Create a column for month names.
df["Month Name"] = df["Date"].dt.month_name()\
                             .map(lambda x: x[:3]\
                             .upper())


# Count the number of food orders grouped by Month Name and Menu.
ftrend = df[df["Category"] == "food"]\
    .groupby(["Month Name","Menu"])["Price"]\
    .agg("count")\
    .reset_index()


# Rename column
ftrend = ftrend.rename(columns= {"Price":"Quantity"}) 

# Sort the data by month.
Month = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']

ftrend["Month Name"] = pd.Categorical(ftrend["Month Name"], categories=Month, ordered=True)

ftrend.sort_values("Month Name", inplace=True)


# Create Chart 1
chart1 = go.Figure()

# Add Line Chart
for menu, color in zip(ftrend['Menu'].unique(), px.colors.qualitative.Plotly):
    data = ftrend[ftrend['Menu'] == menu]
    chart1.add_trace(go.Scatter(x=data['Month Name'], 
                                 y=data['Quantity'], 
                                 mode='lines', 
                                 name=menu,
                                 line=dict(color=color)))

# Update layout
chart1.update_layout(title='Trend of Food Products Sales',
                     xaxis_title='',
                     yaxis_title='Quantity',
                     yaxis=dict(range=[0, max(ftrend['Quantity']) + 300]))


## Chart 2 Trend of Beverage Product Sales

# Count the number of drink orders grouped by Month Name and Menu.
dtrend = df[df["Category"] == "drink"]\
        .groupby(["Month Name","Menu"])["Price"]\
        .agg("count").reset_index()

# Sort the data by month.
dtrend["Month Name"] = pd.Categorical(dtrend["Month Name"], categories=Month, ordered=True)

dtrend = dtrend.rename(columns= {"Price":"Quantity"})

dtrend.sort_values("Month Name", inplace=True)

# Create Chart 2
chart2 = go.Figure()

# Add Line Chart
for menu, color in zip(dtrend['Menu'].unique(), px.colors.qualitative.Plotly):
    data = dtrend[dtrend['Menu'] == menu]
    chart2.add_trace(go.Scatter(x=data['Month Name'], 
                                 y=data['Quantity'], 
                                 mode='lines', 
                                 name=menu,
                                 line=dict(color=color)))

# Update layout
chart2.update_layout(title='Trend of Beverage Products Sales',
                     xaxis_title='',
                     yaxis_title='Quantity',
                     yaxis=dict(range=[0, max(dtrend['Quantity']) + 100]))


##Chart 3 Food Product Sales

# Summarize Total Sales.
chart3 = df.query("Category == 'food'")\
        .groupby("Menu")["Price"]\
        .agg("sum").round().reset_index()

# Sort the data.
chart3_data_sort = chart3.sort_values(by='Price', ascending=True)

# Adjust data label formatting.
chart3_data_sort["Price_T"] = (chart3_data_sort["Price"]/1000).round(decimals = 1).astype(str) + "K"


# Create Chart 3
chart3_plot = go.Figure()

# Add bar chart
chart3_plot.add_trace(go.Bar(x=chart3_data_sort['Price'],
                           y=chart3_data_sort['Menu'],
                           orientation='h',
                           text=chart3_data_sort['Price_T'],
                           hoverinfo='text',
                           marker=dict(color=px.colors.qualitative.Plotly)))

# Update layout
chart3_plot.update_layout(title='Food Products Sales',
                     yaxis_title='',
                     xaxis_title='Sales'
                     )



##Chart 4 Beverage Products Sales

# Summarize Total Sales.
chart4 = df.query("Category == 'drink'")\
           .groupby("Menu")["Price"]\
           .agg("sum").round().reset_index()

# Sort the data.
chart4_data_sort = chart4.sort_values(by='Price', ascending=True)

# Adjust data label formatting.
chart4_data_sort["Price_T"] = (chart4_data_sort["Price"]/1000).round(decimals = 1).astype(str) + "K"


# Create Chart
chart4_plot = go.Figure()

# Add bar chart
chart4_plot.add_trace(go.Bar(x=chart4_data_sort['Price'],
                           y=chart4_data_sort['Menu'],
                           orientation='h',
                           text=chart4_data_sort['Price_T'],
                           hoverinfo='text',
                           marker=dict(color=px.colors.qualitative.Plotly)))

# Update layout
chart4_plot.update_layout(title='Beverage Products Sales',
                     yaxis_title='',
                     xaxis_title='Sales')


# Chart 5 Average Sales and Quantity by Day
# Count unique dates and group by day
Unique_Day_name = df.groupby("Day Of Week")["Date"]\
                    .nunique().reset_index(name= "Unique Dates")

# Count the number of food orders
sum_sales_unit = df[["Category","Day Of Week"]]\
                    .groupby("Day Of Week")\
                    .agg("count")\
                    .round()\
                    .reset_index()

# Rename Column
sum_sales_unit = sum_sales_unit.rename(columns={"Category": "Total Unit Sales"})

# Summarize Total Sales.
sum_sales = df[["Category","Day Of Week","Price"]]\
            .groupby("Day Of Week")["Price"]\
            .agg("sum")\
            .round()\
            .reset_index()\

#Rename Column
sum_sales = sum_sales.rename(columns= {"Price":"Total Sales"})


# Merge data
sales_data = pd.merge(sum_sales_unit, Unique_Day_name, on="Day Of Week")

sales_data = pd.merge(sum_sales, sales_data, on="Day Of Week")


# Create new column
sales_data["Avg_Unit_sales"] = (sales_data["Total Unit Sales"] / sales_data["Unique Dates"]).round()

sales_data["Avg_Sales"] = sales_data["Total Sales"] / sales_data["Unique Dates"]

sales_data["Avg_Sales"] = sales_data["Avg_Sales"].round()


# Sort the data
day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

sales_data["Day Of Week"] = pd.Categorical(sales_data["Day Of Week"], 
                                            categories=day_order, 
                                            ordered=True)

sales_data.sort_values("Day Of Week", inplace=True)

# Create Chart 5
chart5 = go.Figure()

# Add bar chart
chart5.add_trace(go.Bar(x=sales_data['Day Of Week'], 
                        y=sales_data['Avg_Sales'], 
                        name='Average Sales', 
                        yaxis='y', 
                        text= sales_data['Avg_Sales']))

# Add line chart
chart5.add_trace(go.Scatter(x=sales_data['Day Of Week'], 
                            y=sales_data['Avg_Unit_sales'], 
                            mode='lines', 
                            name='Average Quantity', 
                            yaxis='y2',
                            line=dict(color='red')))

# Update layout
chart5.update_layout(title='Average Sales and Quantity by Day', 
                     xaxis_title='', 
                     yaxis_title='Sales',
                     yaxis=dict(showgrid=False, 
                                range=[0, max(sales_data['Avg_Sales'])+100]),
                     yaxis2=dict(title='Quantity',
                                 showgrid=False,
                                 overlaying='y', 
                                 side='right', 
                                 position=1,
                                 range=[0, max(sales_data['Avg_Unit_sales'])+50]),
                     legend=dict(x=1.05, 
                                 y=1.0, 
                                 xanchor='left', 
                                 yanchor='top'))


# Chart 6 Average Sales and Quantity by Time

Opened_Day = df["Date"].nunique()
Unit_by_time = df["Order Hour"]\
            .value_counts()\
            .round()\
            .reset_index()

Sales_by_time = df[["Order Hour","Price"]]\
                .groupby("Order Hour")\
                .agg("sum")\
                .round()\
                .reset_index()

# Rename
Unit_by_time = Unit_by_time.rename(columns= {"count":"Sales Unit", "Order Hour": "Hour"})

Sales_by_time = Sales_by_time.rename(columns= {"Order Hour":"Hour","Price":"Sales"})

# Merge data
time_order = pd.merge(Unit_by_time, Sales_by_time, on="Hour")

# Create new columns
time_order["Avg Sales Unit"] = time_order["Sales Unit"]/Opened_Day
time_order["Avg Sales"] = time_order["Sales"]/Opened_Day

# Sort the data
time_order = time_order.round().sort_values(by= "Hour" )

# Create Chart 6
chart6 = go.Figure()

# Add bar chart
chart6.add_trace(go.Bar(x=time_order['Hour'], 
                        y=time_order['Avg Sales'], 
                        name='Average Sales', 
                        yaxis='y', 
                        text= time_order['Avg Sales']))

# Add line chart
chart6.add_trace(go.Scatter(x=time_order['Hour'], 
                            y=time_order['Avg Sales Unit'], 
                            mode='lines', 
                            name='Average Quantity', 
                            yaxis='y2',
                            line= dict(color = 'red')))

# Update layout
chart6.update_layout(title='Average Sales and Quantity by Time', 
                    xaxis_title='Hour', 
                    yaxis_title='Sales',
                    yaxis=dict(showgrid=False, 
                               range = [0,max(time_order['Avg Sales']) + 20]),
                    yaxis2=dict(title=' Quantity',
                                showgrid=False,
                                overlaying='y', 
                                side='right', 
                                position=1,
                                range=[0, max(time_order['Avg Sales Unit'])+5]),
                    legend=dict(x=1.05, 
                                y=1.0, 
                                xanchor='left', 
                                yanchor='top'))


#Chart 7 kitchen Manpower

fstandard = 10

no_kstaff = df[["Day Of Week","Kitchen Staff"]]\
                .groupby("Day Of Week")\
                .agg("mean")\
                .reset_index().round()

df_kstaff = df[df["Category"] == "food"]\
                .groupby(["Day Of Week"])["Waiting Time"]\
                .mean()\
                .reset_index()\
                .round()

# Merge data
df_kstaff = pd.merge(df_kstaff, no_kstaff, on="Day Of Week")

# Sort data
df_kstaff["Day Of Week"] = pd.Categorical(df_kstaff["Day Of Week"],categories=day_order, ordered=True)

df_kstaff.sort_values("Day Of Week", inplace=True)


# Create Chart 7
chart7 = go.Figure()

# Add bar chart
chart7.add_trace(go.Bar(x=df_kstaff['Day Of Week'], 
                        y=df_kstaff['Kitchen Staff'], 
                        name='Avg Staff', 
                        yaxis='y', 
                        text= df_kstaff['Kitchen Staff']))

# Add line chart
chart7.add_trace(go.Scatter(x=df_kstaff['Day Of Week'], 
                            y=df_kstaff['Waiting Time'], 
                            mode='lines', 
                            name='Avg Waiting', 
                            yaxis='y2',
                            line=dict(color='red')))

# Add constant line
chart7.add_trace(go.Scatter(x=df_kstaff['Day Of Week'], 
                            y=[fstandard] * len(df_kstaff),  # Create a list of 10s with the same length as the data
                            mode='lines', 
                            name='Target Time', 
                            yaxis='y2',
                            line=dict(color='yellow', width=2, dash='dashdot')))

# Update layout
chart7.update_layout(title='Kitchen Manpower', 
                     xaxis_title='', 
                     yaxis_title='Kitchen Staff',
                     yaxis=dict(range=[0, max(df_kstaff['Kitchen Staff']) + 5],
                                showgrid=False),  
                     yaxis2=dict(title='Waiting Time (Minutes)',
                                 showgrid=False,
                                 overlaying='y', 
                                 side='right', 
                                 position=1,
                                 range=[0, max(df_kstaff['Waiting Time']) + 10]),
                     legend=dict(x=1.05, 
                                 y=1.0, 
                                 xanchor='left', 
                                 yanchor='top'))


##Chart 8 Drinks Manpower
dstandard = 5

no_dstaff = df[["Day Of Week","Drinks Staff"]]\
        .groupby("Day Of Week")\
        .agg("mean").reset_index().round()

df_dstaff = df[df["Category"] == "drink"]\
                .groupby(["Day Of Week"])["Waiting Time"]\
                .mean()\
                .reset_index()\
                .round()

# Merge data
df_dstaff = pd.merge(df_dstaff, no_dstaff, on="Day Of Week")

# Sort data
df_dstaff["Day Of Week"] = pd.Categorical(df_dstaff["Day Of Week"], categories=day_order, ordered=True)

df_dstaff.sort_values("Day Of Week", inplace=True)



# Create Chart 8

chart8 = go.Figure()

# Add bar chart
chart8.add_trace(go.Bar(x=df_dstaff['Day Of Week'], 
                        y=df_dstaff['Drinks Staff'], 
                        name='Avg Staff', 
                        yaxis='y', 
                        text= df_dstaff['Drinks Staff']))

# Add line chart
chart8.add_trace(go.Scatter(x=df_dstaff['Day Of Week'], 
                            y=df_dstaff['Waiting Time'], 
                            mode='lines', 
                            name='Avg Waiting', 
                            yaxis='y2',
                            line=dict(color='red')))

# Add constant line
chart8.add_trace(go.Scatter(x=df_dstaff['Day Of Week'], 
                            y=[dstandard] * len(df_dstaff),  # Create a list of 10s with the same length as the data
                            mode='lines', 
                            name='Target Time', 
                            yaxis='y2',
                            line=dict(color='yellow', width=2, dash='dashdot')))

# Update layout
chart8.update_layout(title='Drinks Manpower', 
                    xaxis_title='', 
                    yaxis_title='Drink Staff',
                    yaxis=dict(showgrid = False,
                                range=[0, max(df_dstaff['Drinks Staff'])+5]),
                    yaxis2=dict(title='Waiting Time (Minutes)',
                                showgrid = False, 
                                overlaying='y', 
                                side='right', 
                                position=1,
                                range=[0, max(df_dstaff['Waiting Time'])+10]),  # Set the range to start from 0
                    legend=dict(x=1.05, 
                                y=1.0, 
                                xanchor='left', 
                                yanchor='top'))



# Set up Page layout
col1, col2 = st.columns(2)

# Display Chart 1-4 in the first column
with col1:
    st.plotly_chart(chart1, use_container_width=True)
    st.plotly_chart(chart3_plot, use_container_width=True)
    st.plotly_chart(chart5, use_container_width=True)
    st.plotly_chart(chart7, use_container_width=True)

# Display Chart 2-8 in the second column
with col2:
    st.plotly_chart(chart2, use_container_width=True)
    st.plotly_chart(chart4_plot, use_container_width=True)
    st.plotly_chart(chart6, use_container_width=True)
    st.plotly_chart(chart8, use_container_width=True)
