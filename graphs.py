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
title = 'Correlation matrix'
fig = px.imshow(corr, color_continuous_scale=px.colors.sequential.Cividis_r, title=title)
savefig(fig, title)
