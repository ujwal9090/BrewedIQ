import streamlit as st
import pandas as pd
import calendar
import visualization as vis

st.set_page_config(layout='wide')
st.title('Dashboard')


@st.cache_data
def load_data(path):
    return pd.read_excel(path, engine='openpyxl')

df = load_data("CoffeeShopSales.xlsx")
df['total_sales'] = df['transaction_qty']* df['unit_price']

df["week_name"]=df["transaction_date"].dt.strftime('%A')
df['transaction_time'] = pd.to_datetime(df['transaction_time'], format='%H:%M:%S')
df['hour']=pd.to_datetime(df.transaction_time).dt.hour

store_selection = st.sidebar.multiselect(
    'Select Store',
    df.store_location.unique().tolist(),
    default=df.store_location.unique().tolist()
)

date_range = st.sidebar.date_input(
    'Select Date Range',
    [df.transaction_date.min(), df.transaction_date.max()]
)

filtered_df = df.loc[
    (df['store_location'].isin(store_selection)) &
    (df['transaction_date'].between(pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])))
]


st.title("BrewedIQ Dashboard")



Total_sales = filtered_df['total_sales'].sum()
a,b,c,d=st.columns(4)
a.metric(label="Total Revenue",value=f'{Total_sales:.2f}')

num_transactions = filtered_df['transaction_id'].nunique()

b.metric(label="Number of Transaction",value=num_transactions)
Avg_Transaction_Value=Total_sales/num_transactions
c.metric(label="Average Transaction Value", value=f'{Avg_Transaction_Value:.2f}')

Avg_transaction_qty=filtered_df.transaction_qty.mean()
d.metric(label="average Transaction Qty",value=f'{Avg_transaction_qty:.2f}')

tab1,tab2,tab3,tab4=st.tabs(["Sales Trend Overtime","Time of Day analysis","top Selling Products","Store Performance"])
with tab1:
    # Radio
    measure = st.radio('Select Measure', ['Sales', 'Transactions'], horizontal=True, key='measure_tab1')

    if measure == 'Sales':  
        ap = filtered_df.groupby(filtered_df["transaction_date"].dt.to_period("M"))["total_sales"].sum()

        sales = filtered_df.groupby(filtered_df.transaction_date.dt.to_period('W'))['total_sales'].sum()
        mov_avg = sales.rolling(window=2).mean()

        sales = filtered_df.groupby(filtered_df.transaction_date.dt.to_period('M'))['total_sales'].sum()
        daily_growth = sales.pct_change() * 100

    if measure == 'Transactions':
        ap = filtered_df.groupby(filtered_df["transaction_date"].dt.to_period("M")).size()

        sales = filtered_df.groupby(filtered_df.transaction_date.dt.to_period('W')).size()
        mov_avg = sales.rolling(window=2).mean()

        sales = filtered_df.groupby(filtered_df.transaction_date.dt.to_period('M')).size()
        daily_growth = sales.pct_change() * 100    

    tab1_columns = st.columns([0.6, 0.4], gap='large')
    with tab1_columns[0]:   
        st.plotly_chart(vis.sales_revenue(ap))

    with tab1_columns[1]:
        st.plotly_chart(vis.mon_growth(daily_growth))
        st.plotly_chart(vis.moving_average(sales , mov_avg))


with tab2:
    # Radio
    measure = st.radio('Select Measure', ['Sales', 'Transactions'], horizontal=True, key='measure_tab2')

    if measure == 'Sales':
        daily_analysis = df.groupby([df['transaction_date'].dt.date,'week_name'])['total_sales'].sum().reset_index()
        avg_daily_analysis = daily_analysis.groupby('week_name')['total_sales'].mean()
        avg_daily_analysis1= avg_daily_analysis.reindex(list(calendar.day_name))

        hourly_analysis = df.groupby([df.transaction_date.dt.date,'hour'])['total_sales'].sum().reset_index()
        avg_hourly_analysis = hourly_analysis.groupby('hour')['total_sales'].mean()
    
    if measure == 'Transactions':
        daily_analysis = df.groupby([df['transaction_date'].dt.date,'week_name']).size()
        avg_daily_analysis = daily_analysis.groupby('week_name').size()
        avg_daily_analysis1= avg_daily_analysis.reindex(list(calendar.day_name))

        hourly_analysis = df.groupby([df.transaction_date.dt.date,'hour']).size()
        avg_hourly_analysis = hourly_analysis.groupby('hour').size()
        

    tab2_columns = st.columns([0.6, 0.4], gap='large')
    with tab2_columns[0]:
        st.plotly_chart(vis.avg_daily_analysis(avg_daily_analysis))

    with tab2_columns[1]:
        st.plotly_chart(vis.avg_hourly_analysis(avg_hourly_analysis))
        st.plotly_chart(vis.avg_hourly_sales(filtered_df))



with tab3:
        # Radio
    measure = st.radio('Select Measure', ['Sales', 'Transactions'], horizontal=True, key='measure_tab3')

    if measure == 'Sales':
        category_sales = filtered_df.groupby('product_category')['total_sales'].sum()
        product_sales = filtered_df.groupby(['product_category', 'product_type'])['total_sales'].sum()

    if measure == 'Transactions': 
        category_sales = filtered_df.groupby('product_category').size()
        product_sales = filtered_df.groupby(['product_category', 'product_type']).size()
        # category_sales2 = df.groupby('product_category')['transaction_qty'].sum().reset_index()
        # category_sales3 = df.groupby(['product_category','product_type'])['total_sales'].sum()

    tab3_columns = st.columns([0.6, 0.4], gap='large')
    with tab3_columns[0]:
        st.plotly_chart(vis.top_selling_products(category_sales), key='bar_chart1')

    with tab3_columns[1]:
        category = st.selectbox('Select Category', filtered_df['product_category'].unique().tolist(), key='selectbox_tab3')
        st.plotly_chart(vis.sales_by_category(product_sales[category]), key='bar_chart2')
        #st.plotly_chart(vis.top_selling_products(category_sales3), key='bar_chart3')


        
with tab4:
    lm = df[df.store_location == 'Lower Manhattan']
    lmstore=lm.groupby(lm["transaction_date"].dt.to_period("M"))["total_sales"].sum()
    hk = df[df.store_location == "Hell's Kitchen"]
    hkstore=hk.groupby(hk["transaction_date"].dt.to_period("M"))["total_sales"].sum()
    As = df[df.store_location == 'Astoria']
    Asstore=As.groupby(As["transaction_date"].dt.to_period("M"))["total_sales"].sum()

    tab4_columns = st.columns([0.66, 0.33], gap='small')
    with tab4_columns[0]:
        st.plotly_chart(vis.store_ranking(lmstore, hkstore, Asstore))

        inner_tab = st.columns(2, gap='small')
        with inner_tab[0]:
            sales = lm.groupby(lm.transaction_date.dt.to_period('M'))['total_sales'].sum()
            daily_growth = sales.pct_change() * 100
            st.plotly_chart(vis.store_growth(daily_growth))

        with inner_tab[1]:
            sales = hk.groupby(hk.transaction_date.dt.to_period('M'))['total_sales'].sum()
            monthly_growth = sales.pct_change() * 100
            st.plotly_chart(vis.store_growth(monthly_growth))

    with tab4_columns[1]:
        with st.container(height=500, border=False):
            st.write('''
            \n\n
                * Lower Manhattan vs. Hell’s Kitchen: Both locations show nearly identical sales trends, reflecting similar demand and operational performance
                * Astoria: Slightly lower sales throughout the period, suggesting possible differences in foot traffic or customer demographics
                * Growth Opportunity: With focused marketing or operational improvements, Astoria could potentially close the gap with the other two stores
            ''')

        sales = As.groupby(As.transaction_date.dt.to_period('M'))['total_sales'].sum()
        monthly_growth = sales.pct_change() * 100
        st.plotly_chart(vis.store_growth(monthly_growth))

