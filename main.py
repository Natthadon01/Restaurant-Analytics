import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

#read CSV file
df = pd.read_csv("https://raw.githubusercontent.com/Natthadon01/test/main/test_data_clean.csv")


st.title('Restaurant Analytics')
st.write('Author: Natthadon Jang')




## Chart 1 Food trend
df[['Day', 'Month', 'Year']] = df['Date'].str.split('/', expand=True)
df['Date'] = pd.to_datetime(df[['Day', 'Month', 'Year']], format='%d/%m/%y')

# ลบคอลัมน์ที่ไม่จำเป็น
df.drop(['Day', 'Month', 'Year'], axis=1, inplace=True)


df["Month Name"] = df["Date"].dt.month_name()
df['Month Name'] = df['Month Name'].map(lambda x: x[:3].upper())

Month = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']
ftrend = df[df["Category"] == "food"].groupby(["Month Name","Menu"])["Price"].agg("count").reset_index()

ftrend = ftrend.rename(columns= {"Price":"Quantity"})
#เรียงข้อมูล
ftrend["Month Name"] = pd.Categorical(ftrend["Month Name"], categories=Month, ordered=True)
ftrend.sort_values("Month Name", inplace=True)


# Create line chart using Plotly Express
line_chart = px.line(ftrend, 
                    x='Month Name', 
                    y='Quantity', 
                    color='Menu', 
                    title='Food Product Movement')

# Add axis titles
line_chart.update_layout(xaxis_title='',
                         yaxis_title='Quantity')

# Display the line chart using Streamlit
st.plotly_chart(line_chart)


## Chart 2 Drink trend
dtrend = df[df["Category"] == "drink"].groupby(["Month Name","Menu"])["Price"].agg("count").reset_index()

dtrend["Month Name"] = pd.Categorical(dtrend["Month Name"], categories=Month, ordered=True)

dtrend = dtrend.rename(columns= {"Price":"Quantity"})

#เรียงข้อมูล
dtrend.sort_values("Month Name", inplace=True)


# Create line chart using Plotly Express
line_chart = px.line(dtrend, 
                    x='Month Name', 
                    y='Quantity', 
                    color='Menu', 
                    title='Drink Product Movement')

# Add axis titles
line_chart.update_layout(xaxis_title='',
                         yaxis_title='Quantity')

# Display the line chart using Streamlit
st.plotly_chart(line_chart)



##Chart 3 Food Barchart
#filter data to visualize
chart3 = df.query("Category == 'food'").groupby("Menu")["Price"].agg("sum").round().reset_index()
chart3_data_sort = chart3.sort_values(by='Price', ascending=True)
#setting Chart
chart3_plot = px.bar(chart3_data_sort, x='Price', y='Menu', orientation='h', 
    title='Total Sales by Food', text = 'Price')

chart3_plot.update_layout(yaxis_title='', xaxis_title = 'Sales') #Rename Axix Title

#plot horizontal bar chart
st.plotly_chart(chart3_plot)


##Chart 4 Drink Barchart
chart4 = df.query("Category == 'drink'").groupby("Menu")["Price"].agg("sum").round().reset_index()
chart4_data_sort = chart4.sort_values(by='Price', ascending=True)
#setting Chart
chart4_plot = px.bar(chart4_data_sort, x='Price', y='Menu', orientation='h', title='Total Sales by Drink', text = 'Price')
chart4_plot.update_layout(yaxis_title='', xaxis_title = 'Sales') #Rename Axix Title
#plot horizontal bar chart
st.plotly_chart(chart4_plot)





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


sales_data = pd.DataFrame(sales_data)


#Chart 5 

# Create a column chart using Plotly Express
chart5 = px.bar(sales_data, x='Day Of Week', y='Avg_Sales', title='Average Sales by Day of Week')
# Add axis titles
chart5.update_layout(xaxis_title='', yaxis_title='Average Sales')
# Add line chart for average unit sales
line_chart = px.line(sales_data, x='Day Of Week', y='Avg_Unit_sales')
line_chart.update_traces(line=dict(color='red'))  # Set the color of the line chart
# Display the combined chart using Streamlit
st.plotly_chart(chart5.add_trace(line_chart.data[0]))




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
# Create a bar chart using Plotly Express
chart6 = px.bar(time_order, x='Hour', y='Avg Sales', title='Average Sales by Hour')
# Add axis titles
chart6.update_layout(xaxis_title='Hour', yaxis_title='Average Sales')
# Display the bar chart using Streamlit
line_chart = px.line(time_order, x='Hour', y='Avg Sales Unit', title='Average Sales Unit by Hour')
line_chart.update_traces(line=dict(color='red'))  # Set the color of the line chart

# Display both bar chart and line chart using Streamlit
st.plotly_chart(chart6.add_trace(line_chart.data[0]))

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




# Create a bar chart using Plotly Express
column_chart7 = px.bar(df_kstaff, x='Day Of Week', y='Kitchen Staff', title='Kitchen Staff by Day of Week')
# Add axis titles
column_chart7.update_layout(xaxis_title='', yaxis_title='Kitchen Staff')
# Create a line chart for Waiting Time using Plotly Express
line_chart = px.line(df_kstaff, x='Day Of Week', y='Waiting Time', title='Waiting Time by Day of Week')
# Set the line color to red
line_chart.update_traces(line=dict(color='red'))
# Add Waiting Time as a line to the bar chart
column_chart7.add_trace(line_chart.data[0])

# Add a constant line at y=10
column_chart7.add_hline(y=fstandard, 
            line_dash="dash", 
            line_color="yellow", 
            annotation_text="standard line", 
            annotation_position="top left")

# Display the combined chart using Streamlit
st.plotly_chart(column_chart7)



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



#Create Chart8
# Create a bar chart using Plotly Express
column_chart8 = px.bar(df_dstaff, x='Day Of Week', y='Drinks Staff', title='Drink Staff Manpower')
# Add axis titles
column_chart8.update_layout(xaxis_title='', yaxis_title='Drinks Staff')
# Create a line chart for Waiting Time using Plotly Express
line_chart = px.line(df_dstaff, x='Day Of Week', y='Waiting Time', title='Waiting Time by Day of Week')
# Set the line color to red
line_chart.update_traces(line=dict(color='red'))

# Add Waiting Time as a line to the bar chart
column_chart8.add_trace(line_chart.data[0])
# Add a constant line at y=10
column_chart8.add_hline(y=dstandard, 
            line_dash="dash", 
            line_color="yellow", 
            annotation_text="standard line", 
            annotation_position="top left")

# Display the combined chart using Streamlit
st.plotly_chart(column_chart8)