import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

#read CSV file
df = pd.read_csv("https://raw.githubusercontent.com/Natthadon01/test/main/test_data_clean.csv")

#Page Setup
st.set_page_config(
    page_title="Restaurant Analytics",
    layout="wide")

st.title('Restaurant Analytics')



## Chart 1 Food Sales trend

# Adjust datatype and format of the date column.
df[['Day', 'Month', 'Year']] = df['Date'].str.split('/', expand=True)

df['Date'] = pd.to_datetime(df[['Day', 'Month', 'Year']], format='%d/%m/%y')

df.drop(['Day', 'Month', 'Year'], axis=1, inplace=True)


# Create a column for month names.
df["Month Name"] = df["Date"].dt.month_name()\
                             .map(lambda x: x[:3]\
                             .upper())


# Count the number of orders grouped by Month Name and Menu.
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


# Create Chart 1: Food Sales Trend.
chart1 = px.line(ftrend, 
                    x='Month Name', 
                    y='Quantity', 
                    color='Menu', 
                    title= 'Trend of Food Products Sales')

chart1.update_layout(xaxis_title='', 
                     yaxis_title='Quantity')




## Chart 2 Drink trend
dtrend = df[df["Category"] == "drink"].groupby(["Month Name","Menu"])["Price"]\
                                      .agg("count")\
                                      .reset_index()

dtrend["Month Name"] = pd.Categorical(dtrend["Month Name"], categories=Month, ordered=True)

dtrend = dtrend.rename(columns= {"Price":"Quantity"})

#เรียงข้อมูล
dtrend.sort_values("Month Name", inplace=True)


# Create line chart using Plotly Express
chart2 = px.line(dtrend, 
                    x='Month Name', 
                    y='Quantity',
                    color='Menu', 
                    title='Trend of Beverage Products Sales')

# Add axis titles
chart2.update_layout(xaxis_title='',
                         yaxis_title='Quantity')

# Display the line chart using Streamlit




##Chart 3 Food Barchart
#filter data to visualize
chart3 = df.query("Category == 'food'").groupby("Menu")["Price"].agg("sum").round().reset_index()
chart3_data_sort = chart3.sort_values(by='Price', ascending=True)
chart3_data_sort["Price_T"] = (chart3_data_sort["Price"]/1000).round(decimals = 1).astype(str) + "K"

#setting Chart
chart3_plot = px.bar(chart3_data_sort, x='Price', y='Menu', orientation='h', 
    title='Food Products Sales', text = 'Price_T')

chart3_plot.update_layout(yaxis_title='', xaxis_title = 'Sales')

#plot horizontal bar chart










##Chart 4 Drink Barchart
chart4 = df.query("Category == 'drink'").groupby("Menu")["Price"].agg("sum").round().reset_index()
chart4_data_sort = chart4.sort_values(by='Price', ascending=True)

chart4_data_sort["Price_T"] = (chart4_data_sort["Price"]/1000).round(decimals = 1).astype(str) + "K"


#setting Chart
chart4_plot = px.bar(chart4_data_sort, 
                    x='Price', 
                    y='Menu', 
                    orientation='h', 
                    title='Beverage Products Sales', 
                    text = 'Price_T')


chart4_plot.update_layout(yaxis_title='', xaxis_title = 'Sales') #Rename Axix Title
#plot horizontal bar chart



###########################################

#Chart 5 
#Count Date by Day
Unique_Day_name = df.groupby("Day Of Week")["Date"].nunique().reset_index(name= "Unique Dates")

#Sales Data
sum_sales_unit = df[["Category","Day Of Week"]]\
                    .groupby("Day Of Week")\
                    .agg("count")\
                    .round()\
                    .reset_index()

#Rename Column
sum_sales_unit = sum_sales_unit.rename(columns={"Category": "Total Unit Sales"})


sum_sales = df[["Category","Day Of Week","Price"]]\
            .groupby("Day Of Week")["Price"]\
            .agg("sum")\
            .round()\
            .reset_index()\

#Rename Column
sum_sales = sum_sales.rename(columns= {"Price":"Total Sales"})

# Create Sales date with Join unit sales and unique dates table
sales_data = pd.merge(sum_sales_unit, Unique_Day_name, on="Day Of Week")
# Create Avg_Unit_sales column
sales_data["Avg_Unit_sales"] = (sales_data["Total Unit Sales"] / sales_data["Unique Dates"]).round()
#Join unit sales and unique dates table and overwrite sales data
sales_data = pd.merge(sum_sales, sales_data, on="Day Of Week")
# Create Avg_Sales column
sales_data["Avg_Sales"] = sales_data["Total Sales"] / sales_data["Unique Dates"]
sales_data["Avg_Sales"] = sales_data["Avg_Sales"].round() #Round Decimal

# Sort the DataFrame based on the order of days of the week
#สร้าง List day ขึ้มาเพื่อใช้ในการ Sort
day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
#แปลง Day Of Week ให้กลายเป็นข้อมูลประเภท Categorical โดยใช้ day order ในการกำหนดลำดับและจัดเรียง
sales_data["Day Of Week"] = pd.Categorical(sales_data["Day Of Week"], categories=day_order, ordered=True)
#เรียงข้อมูล
sales_data.sort_values("Day Of Week", inplace=True)

#Chart 5 visualize

###########################################
# Create subplots with one row and one column
chart5 = go.Figure()

# Add bar chart for 'Avg Sales' on the primary Y axis
chart5.add_trace(go.Bar(x=sales_data['Day Of Week'], 
                        y=sales_data['Avg_Sales'], 
                        name='Average Sales', 
                        yaxis='y', 
                        text= sales_data['Avg_Sales']))

# Add line chart for 'Avg Unit sales' on the secondary Y axis
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
                     yaxis2=dict(title='Quantity', 
                                 overlaying='y', 
                                 side='right', 
                                 position=1,
                                 range=[0, max(sales_data['Avg_Unit_sales'])]),  # Set the range to start from 0
                     legend=dict(x=1.05, 
                                 y=1.0, 
                                 xanchor='left', 
                                 yanchor='top'))

chart5.update_layout(yaxis=dict(showgrid=False, zeroline=False))
# Display the combo chart using Streamlit



############################################################
# Chart 6
Opened_Day = df["Date"].nunique()
Unit_by_time = df["Order Hour"]\
            .value_counts()\
            .round()\
            .reset_index()

Unit_by_time = Unit_by_time.rename(columns= {"count":"Sales Unit", "Order Hour": "Hour"})


Sales_by_time = df[["Order Hour","Price"]]\
                .groupby("Order Hour")\
                .agg("sum")\
                .round()\
                .reset_index()


Sales_by_time = Sales_by_time.rename(columns= {"Order Hour":"Hour","Price":"Sales"})


time_order = pd.merge(Unit_by_time, Sales_by_time, on="Hour")
time_order["Avg Sales Unit"] = time_order["Sales Unit"]/Opened_Day
time_order["Avg Sales"] = time_order["Sales"]/Opened_Day
time_order = time_order.round().sort_values(by= "Hour" )

#Chart 6 Sales by Time
###################
# Create subplots with one row and one column
chart6 = go.Figure()

# Add bar chart for 'Avg Sales' on the primary Y axis
chart6.add_trace(go.Bar(x=time_order['Hour'], 
                        y=time_order['Avg Sales'], 
                        name='Average Sales', 
                        yaxis='y', 
                        text= time_order['Avg Sales']))

# Add line chart for 'Avg Unit sales' on the secondary Y axis
chart6.add_trace(go.Scatter(x=time_order['Hour'], 
                            y=time_order['Avg Sales Unit'], 
                            mode='lines', 
                            name='Average Quantity', 
                            yaxis='y2',
                            line= dict(color = 'red')))

# Update layout
chart6.update_layout(title='"Average Sales and Quantity by Time"', 
                    xaxis_title='Hour', 
                    yaxis_title='Sales',
                    yaxis2=dict(title=' Quantity', 
                                overlaying='y', 
                                side='right', 
                                position=1,
                                range=[0, max(time_order['Avg Sales Unit'])]),  # Set the range to start from 0
                    legend=dict(x=1.05, 
                                y=1.0, 
                                xanchor='left', 
                                yanchor='top'))

chart6.update_layout(yaxis=dict(showgrid=False, zeroline=False))
# Display the combo chart using Streamlit



#Chart 7 kitchen staff manpower
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

df_kstaff = pd.merge(df_kstaff, no_kstaff, on="Day Of Week")


df_kstaff["Day Of Week"] = pd.Categorical(df_kstaff["Day Of Week"], 
    categories=day_order, ordered=True)

df_kstaff.sort_values("Day Of Week", inplace=True)

###################
# Create subplots with one row and one column
chart7 = go.Figure()

# Add bar chart for 'Avg Sales' on the primary Y axis
chart7.add_trace(go.Bar(x=df_kstaff['Day Of Week'], 
                        y=df_kstaff['Kitchen Staff'], 
                        name='Avg Staff', 
                        yaxis='y', 
                        text= df_kstaff['Kitchen Staff']))

# Add line chart for 'Avg Unit sales' on the secondary Y axis
chart7.add_trace(go.Scatter(x=df_kstaff['Day Of Week'], 
                            y=df_kstaff['Waiting Time'], 
                            mode='lines', 
                            name='Avg Waiting', 
                            yaxis='y2',
                            line=dict(color='red')))

# Add constant line with name 'Standard Time'
chart7.add_trace(go.Scatter(x=df_kstaff['Day Of Week'], 
                            y=[fstandard] * len(df_kstaff),  # Create a list of 10s with the same length as the data
                            mode='lines', 
                            name='Standard Time', 
                            yaxis='y2',
                            line=dict(color='yellow', width=2, dash='dashdot')))

# Update layout
chart7.update_layout(title='Kitchen Manpower', 
                    xaxis_title='', 
                    yaxis_title='Kitchen Staff',
                    yaxis2=dict(title='Waiting Time (Minutes)', 
                                overlaying='y', 
                                side='right', 
                                position=1,
                                range=[0, max(df_kstaff['Waiting Time'])]),  # Set the range to start from 0
                    legend=dict(x=1.05, 
                                y=1.0, 
                                xanchor='left', 
                                yanchor='top'))

# Update layout to remove grid lines and zero lines for y axis
chart7.update_layout(yaxis=dict(showgrid=False, zeroline=False))

# Display the combo chart using Streamlit



##Chart 8 Drink staff manpower
dstandard = 5
no_dstaff = df[["Day Of Week","Drinks Staff"]]\
        .groupby("Day Of Week")\
        .agg("mean").reset_index().round()

df_dstaff = df[df["Category"] == "drink"]\
                .groupby(["Day Of Week"])["Waiting Time"]\
                .mean()\
                .reset_index()\
                .round()

df_dstaff = pd.merge(df_dstaff, no_dstaff, on="Day Of Week")
df_dstaff["Day Of Week"] = pd.Categorical(df_dstaff["Day Of Week"], categories=day_order, ordered=True)
df_dstaff.sort_values("Day Of Week", inplace=True)


###################
# Create subplots with one row and one column
chart8 = go.Figure()

# Add bar chart for 'Avg Sales' on the primary Y axis
chart8.add_trace(go.Bar(x=df_dstaff['Day Of Week'], 
                        y=df_dstaff['Drinks Staff'], 
                        name='Avg Staff', 
                        yaxis='y', 
                        text= df_dstaff['Drinks Staff']))

# Add line chart for 'Avg Unit sales' on the secondary Y axis
chart8.add_trace(go.Scatter(x=df_dstaff['Day Of Week'], 
                            y=df_dstaff['Waiting Time'], 
                            mode='lines', 
                            name='Avg Waiting', 
                            yaxis='y2',
                            line=dict(color='red')))

# Add constant line with name 'Standard Time'
chart8.add_trace(go.Scatter(x=df_dstaff['Day Of Week'], 
                            y=[dstandard] * len(df_dstaff),  # Create a list of 10s with the same length as the data
                            mode='lines', 
                            name='Standard Time', 
                            yaxis='y2',
                            line=dict(color='yellow', width=2, dash='dashdot')))

# Update layout
chart8.update_layout(title='Drinks Manpower', 
                    xaxis_title='', 
                    yaxis_title='Drink Staff',
                    yaxis2=dict(title='Waiting Time (Minutes)', 
                                overlaying='y', 
                                side='right', 
                                position=1,
                                range=[0, max(df_dstaff['Waiting Time'])]),  # Set the range to start from 0
                    legend=dict(x=1.05, 
                                y=1.0, 
                                xanchor='left', 
                                yanchor='top'))

# Update layout to remove grid lines and zero lines for y axis
chart8.update_layout(yaxis=dict(showgrid=False, zeroline=False))





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
