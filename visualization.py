import plotly.graph_objects as go
import plotly.express as px
    
def sales_revenue(data):
    fig = go.Figure()

    fig.add_trace(
    go.Scatter(
        x = data.index.astype(str),
        y = data.values,
         mode = 'lines',
         name = 'lines'
    ))
    fig.update_layout(
    title="Sales Revenue",
    xaxis_title="Monthly",
    yaxis_title="Total sales",
    showlegend=False,
    width=1200,
    height=700
    )

    return fig
   
def moving_average(data, data1):
    fig = go.Figure()

    # Sales line
    fig.add_trace(go.Scatter(
        x=data.index.astype(str),
        y=data.values,
        mode='lines',
        name="Sales"
    ))

    # Moving Average line
    fig.add_trace(go.Scatter(
        x=data1.index.astype(str),
        y=data1.values,
        mode='lines',
        name="Moving Average"
    ))

    # Adjust figure size here
    fig.update_layout(
        width=700,   # adjust width
        height=350   # adjust height
    )

    return fig


def mon_growth(data):
    fig = px.bar(
        x=data.index.astype(str),
        y=data.values,
        title="Monthly Sales Growth",
        width=600,   # adjust width here
        height=300   # adjust height here
    )
    return fig

def avg_daily_analysis(data):
    fig = px.bar(
        x=data.index,
        y=data.values,
        title="Avg_Daily_analysis",
        width=600,   # length
        height=600   # width
    )
    return fig

def avg_hourly_analysis(data):
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=data.index,
            y=data.values,
            mode='lines',
            name='lines'
        )
    )

    fig.update_layout(
        title="Avg_hourly_analysis",
        xaxis_title="Hours",
        yaxis_title="total_sales",
        showlegend=False,
        width=500,   # length of the figure
        height=300   # height of the figure
    )

    return fig

def avg_hourly_sales(data):
    fig = go.Figure()

    for category in data['product_category'].unique():
        cat_df = data[data['product_category'] == category]
        hourly_sales = cat_df.groupby(
            [cat_df['transaction_date'].dt.date, 'hour']
        )['total_sales'].sum().reset_index()

        average_hourly_sales = hourly_sales.groupby('hour')['total_sales'].mean()

        fig.add_trace(
            go.Scatter(
                x=average_hourly_sales.index,
                y=average_hourly_sales.values,
                mode='lines',
                name=category
            )
        )

    fig.update_layout(
        title="Average Sales by Hour of Day (Product Category Wise)",
        xaxis_title="Hour of Day",
        yaxis_title="Average Sales by Hour",
        legend_title="Product Category",
        width=650,   # set figure width (length)
        height=400   # set figure height
    )    
    
    return fig


def top_selling_products(data):
    fig = px.bar(
        x=data.index.astype(str),
        y=data.values,
        title="Product Category Distribution (by Sales)",
        color_discrete_sequence=["darkviolet"],
        # Optional: width and height can also be added here
        width=560,
        height=700
    )

    fig.update_layout(
        xaxis_title="Product Category",
        yaxis_title="Total Sales"
    )

    fig.update_xaxes(tickangle=45)

    return fig

def store_performance(data):
    fig = px.bar(
        data,
        x='product_category',
        y='transaction_qty',
        title="Product Category Distribution (By Transaction)",
        labels={
            "product_category": "Product Category",
            "transaction_qty": "Total Sales"
        },
        color_discrete_sequence=["darkviolet"],
        width=500,  # figure width
        height=400  # figure height
    )

    fig.update_layout(
        xaxis_tickangle=45
    )

    return fig

def sales_by_category(data):
    fig = px.pie(
        values=data.values,
        names=data.index.astype(str),
        labels=data.index.astype(str),
        title="Product Category (Tea) Distribution by Sales",
        color_discrete_sequence=px.colors.sequential.RdBu,
        width=600,   # set figure width
        height=350   # set figure height
    )
    return fig

def store_ranking(lmstore, hkstore, Asstore):
    fig = go.Figure()

    fig.add_trace(go.Scatter(
    x=lmstore.index.astype(str),
    y=lmstore.values,
    mode="lines",
    name="Lower Manhattan"
   ))

    fig.add_trace(go.Scatter(
    x=hkstore.index.astype(str),
    y=hkstore.values,
    mode="lines",
    name="Hell's Kitchen"
    ))

    fig.add_trace(go.Scatter(
    x=Asstore.index.astype(str),
    y=Asstore.values,
    mode="lines",
    name="Astoria"
    ))

    fig.update_layout(
    title="Sales Revenue",
    xaxis_title="Weekly",
    yaxis_title="Total Sales",
    legend_title="Stores",
    xaxis=dict(tickangle=90),
    template="plotly_white",
    width=900,
    height=500
   )

    return fig

def store_growth(data):
    fig = px.bar(x=data.index.astype(str),y=data.values,title="Monthly sales Growth")
    return fig

def hk_growth(data):
    fig = px.bar(x=data.index.astype(str),y=data.values,title="Store Ranking")
    return fig

def sales_growth(data):
    fig = px.bar(x=data.index.astype(str),y=data.values,title="Store Ranking")
    return fig
