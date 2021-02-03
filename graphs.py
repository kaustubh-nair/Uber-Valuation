import pandas
import plotly.express as px
import numpy as np

def read():
    data = pandas.read_csv('data/data.csv')
    data = data[data['Revenue'] == data['Revenue']]
    data['Yearly Quarter'] = [str(x[0]) + ' ' + x[1] for x in zip(data['Year'], data['Quarter'])]
    print("Loaded")
    print(data)
    return data

def savefig(fig, title):
    fig.write_image("images/" + title + '.jpeg')
df = read()

title = 'Stock price'
fig = px.line(df, x="Yearly Quarter", y="Stock price", title=title)
savefig(fig, title)

title = 'Monthly Active Platform consumers (millions)'
fig = px.line(df, x="Yearly Quarter", y="MAPC", title=title)
savefig(fig, title)

title = 'Gross bookings'
fig = px.line(df, x="Yearly Quarter", y="Total bookings", title=title)
savefig(fig, title)

title = 'Total revenue'
fig = px.line(df, x="Yearly Quarter", y="Total revenue", title=title)
savefig(fig, title)

title = 'Externalities'
fig = px.line(df, x="Yearly Quarter", y="Externalities", title=title)
savefig(fig, title)

fig = px.scatter_matrix(df, dimensions=['Stock price', 'MAPC', 'Total bookings', 'Total revenue',], color="Yearly Quarter", color_discrete_sequence=px.colors.sequential.Burg, title='Scatter matrix')
savefig(fig, 'Scatter matrix')

corr = df[['Stock price', 'MAPC', 'Total revenue', 'Externalities', 'Total bookings',]].corr()
title = 'Correlation matrix'
fig = px.imshow(corr, color_continuous_scale=px.colors.sequential.Cividis_r, title=title)
savefig(fig, title)

corr = df[['Stock price', 'Revenue(Ride)', 'Revenue(Delivery)', 'Revenue(Freight)','Bookings(Ride)', 'Bookings(Delivery)', 'Bookings(Freight)', ]].corr()
title = 'Correlation matrix with streams'
fig = px.imshow(corr, color_continuous_scale=px.colors.sequential.Cividis_r, title=title)
savefig(fig, title)

data = df
data['Revenue(Ride)'] = data['Revenue(Ride)']/100
data['Revenue(Delivery)'] = data['Revenue(Delivery)']/100
data['Revenue(Freight)'] = data['Revenue(Freight)']/100
data['Total revenue'] = data['Total revenue']/100
data['Bookings(Ride)'] = data['Bookings(Ride)']/100
data['Bookings(Delivery)'] = data['Bookings(Delivery)']/100
data['Bookings(Freight)'] = data['Bookings(Freight)']/100
data['Total bookings'] = data['Total bookings']/100
data['Externalities'] = data['Externalities']*25

title = 'Stock and Revenue'
fig = px.line(df, x='Yearly Quarter', y=['Stock price', 'Revenue(Ride)', 'Revenue(Delivery)', 'Revenue(Freight)', 'Total revenue',], title=title)
savefig(fig, 'consolidated/' + title)

title = 'Stock and Bookings'
fig = px.line(df, x='Yearly Quarter', y=['Stock price', 'Bookings(Ride)', 'Bookings(Delivery)', 'Bookings(Freight)', 'Total bookings',], title=title)
savefig(fig, 'consolidated/' + title)

title = 'Stock and Explanatory variables'
fig = px.line(df, x='Yearly Quarter', y=['Stock price', 'Externalities', 'Total revenue', 'MAPC', 'Total bookings',], title=title)
savefig(fig, 'consolidated/' + title)
