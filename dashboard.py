import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

data = pd.read_csv('finaldata.csv', sep=",")

st.title("🌴 Hotel Booking Dashboard")
st.markdown("Explore hotel reservations between 2015 and 2017 in detail.")
st.sidebar.subheader('Filters')
selected_category = st.sidebar.selectbox('Hotel', data['hotel'].unique())
selected_years = st.sidebar.multiselect('Year', data['arrival_date_year'].unique(), default= data['arrival_date_year'].unique())
selected_countries = st.sidebar.multiselect('Country', data['country'].unique(), default=['TUR','ITA','RUS'])
type_of_customer = st.sidebar.multiselect('Customer Type', data['customer_type'].unique(), default=['Transient','Contract','Transient-Party','Group'])

filtered_data = data[
    (data['hotel'] == selected_category) &
    (data['arrival_date_year'].isin(selected_years)) &
    (data['country'].isin(selected_countries)) &
    (data['customer_type'].isin(type_of_customer)) 
]

st.write(f"Total reservation: {len(filtered_data)}")

figure_size = (900, 600)

custom_month_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
monthly_data = filtered_data.groupby('arrival_date_month')['arrival_date_month'].count().reindex(custom_month_order)
monthly_data.index = pd.Categorical(monthly_data.index, categories=custom_month_order, ordered=True)

#figure1
fig1 = go.Figure()
fig1.add_trace(go.Scatter(x=monthly_data.index, y=monthly_data.values, mode='lines', line=dict(color='#3A98B9')))
fig1.update_xaxes(showgrid=False)
fig1.update_yaxes(showgrid=False)
fig1.update_layout(title='Reservation by Month', width=figure_size[0], height=figure_size[1])
st.plotly_chart(fig1)

#figure2
fig2 = px.pie(
    filtered_data.replace({'is_canceled': {0: 'No', 1: 'Yes'}}),
    names='is_canceled',
    title='Cancellation',
    width=figure_size[0],
    height=figure_size[1],
    color_discrete_sequence=['#3A98B9', '#C51605']
)
st.plotly_chart(fig2)

#figure3
country_data = filtered_data.groupby('country')['country'].count().reset_index(name='count')
country_data = country_data.sort_values(by='count', ascending=False)
fig3 = go.Figure()
fig3.add_trace(go.Bar(x=country_data['country'], y=country_data['count'], marker_color='#3A98B9'))
fig3.update_xaxes(categoryorder='total descending')
fig3.update_layout(title='Guests by Country', width=figure_size[0], height=figure_size[1])
fig3.update_xaxes(showgrid=False)
fig3.update_yaxes(showgrid=False)
st.plotly_chart(fig3)

#figure4
family_data = filtered_data[['adults', 'children', 'babies', 'adr']]
family_data['family'] = family_data['adults'] + family_data['children'] + family_data['babies']
fig4 = px.box(family_data, x='family', y='adr', title='ADR by Family Size')
fig4.update_xaxes(title='Family Size')
fig4.update_yaxes(title='Average Daily Rate')
fig4.update_traces(marker_color='#3A98B9')
fig4.update_layout(width=figure_size[0], height=figure_size[1])
fig4.update_xaxes(showgrid=False)
fig4.update_yaxes(showgrid=False)
st.plotly_chart(fig4)

#figure5
weekend_stays = filtered_data['stays_in_weekend_nights'].sum()
weeknight_stays = filtered_data['stays_in_week_nights'].sum()
fig5 = go.Figure()
fig5.add_trace(go.Bar(x=['Weekend Stays', 'Week Night Stays'], y=[weekend_stays, weeknight_stays], marker_color='#3A98B9'))
fig5.update_layout(title='Weekend and Week Night Stays Distribution', width=figure_size[0], height=figure_size[1])
fig5.update_xaxes(title='Stay Type')
fig5.update_yaxes(title='Stay Count')
fig5.update_xaxes(showgrid=False)
fig5.update_yaxes(showgrid=False)
st.plotly_chart(fig5)

st.markdown("[Github](https://github.com/busekcoban/HotelBookingDataAnalysis)")
