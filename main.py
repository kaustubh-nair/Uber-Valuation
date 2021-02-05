import pandas
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import Ridge, LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import MinMaxScaler
import plotly.express as px
import numpy as np

def read():
    data = pandas.read_csv('data/data.csv')

    #remove null
    data = data[data['Revenue'] == data['Revenue']]

    data = data[string_columns + columns]

    data['Yearly Quarter'] = [str(x[0]) + ' ' + x[1] for x in zip(data['Year'], data['Quarter'])]

    # convert millions to dollars
    for row in ['MAPC', 'Revenue(Ride)', 'Revenue(Delivery)', 'Revenue(Freight)', 'Total revenue', 'Bookings(Ride)', 'Bookings(Delivery)', 'Bookings(Freight)', 'Total bookings', 'Externalities']:
        data[row] = data[row] * 1000000

    scaler = MinMaxScaler()
    data[columns] = scaler.fit_transform(data[columns])

    print("Loaded")
    print(data)
    return data

def savefig(fig, title):
    fig.write_image("images/" + title + '.jpeg')

def drawgraphs():

    title = 'Valuation'
    fig = px.line(df, x="Yearly Quarter", y="Valuation", title=title)
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

    fig = px.scatter_matrix(df, dimensions=['Valuation', 'MAPC', 'Total bookings', 'Total revenue',], color="Yearly Quarter", color_discrete_sequence=px.colors.sequential.Burg, title='Scatter matrix')
    savefig(fig, 'Scatter matrix')

    corr = df[['Valuation', 'MAPC', 'Total revenue', 'Externalities', 'Total bookings',]].corr()
    title = 'Correlation matrix'
    fig = px.imshow(corr, color_continuous_scale=px.colors.sequential.Cividis_r, title=title)
    savefig(fig, title)

    corr = df[['Valuation', 'Revenue(Ride)', 'Revenue(Delivery)', 'Revenue(Freight)','Bookings(Ride)', 'Bookings(Delivery)', 'Bookings(Freight)', ]].corr()
    title = 'Correlation matrix with streams'
    fig = px.imshow(corr, color_continuous_scale=px.colors.sequential.Cividis_r, title=title)
    savefig(fig, title)


    title = 'Stock and Revenue'
    fig = px.line(df, x='Yearly Quarter', y=['Valuation', 'Revenue(Ride)', 'Revenue(Delivery)', 'Revenue(Freight)', 'Total revenue',], title=title)
    savefig(fig, 'consolidated/' + title)

    title = 'Stock and Bookings'
    fig = px.line(df, x='Yearly Quarter', y=['Valuation', 'Bookings(Ride)', 'Bookings(Delivery)', 'Bookings(Freight)', 'Total bookings',], title=title)
    savefig(fig, 'consolidated/' + title)

    title = 'Stock and Explanatory variables'
    fig = px.line(df, x='Yearly Quarter', y=['Valuation', 'Externalities', 'Total revenue', 'MAPC', 'Total bookings',], title=title)
    savefig(fig, 'consolidated/' + title)


def model(x_poly, title):
    print(x_poly)

    y = df['Valuation']
    model = LinearRegression()
    model.fit(x_poly, y)
    y_poly_pred = model.predict(x_poly)

    df['Fitted valuation'] = y_poly_pred
    print(df)
    print(df['Fitted valuation'])
    df['Actual valuation'] = df['Valuation']

    fig = px.line(df, x='Yearly Quarter', y=['Actual valuation', 'Fitted valuation'], title=title)
    savefig(fig, 'model/' + title)

    rmse = np.sqrt(mean_squared_error(y,y_poly_pred))
    print(rmse)

string_columns = ['Year', 'Quarter']
columns = ['Valuation','Externalities', 'MAPC', 'Revenue(Ride)', 'Revenue(Delivery)', 'Revenue(Freight)', 'Total revenue', 'Bookings(Ride)', 'Bookings(Delivery)', 'Bookings(Freight)', 'Total bookings']
df = read()

polynomial_features= PolynomialFeatures(degree=2)
x_poly = polynomial_features.fit_transform(df[[x for x in columns if x != 'Valuation']])
title = 'Quadratic Regression all features'
model(x_poly, title)

x_poly = polynomial_features.fit_transform(df[['Externalities', 'MAPC', 'Total revenue', 'Total bookings']])
title = 'Quadratic Regression aggregated features'
model(x_poly, title)

polynomial_features= PolynomialFeatures(degree=1)
x_poly = polynomial_features.fit_transform(df[[x for x in columns if x != 'Valuation']])
title = 'Linear Regression all features'
model(x_poly, title)

x_poly = polynomial_features.fit_transform(df[['Externalities', 'MAPC', 'Total revenue', 'Total bookings']])
title = 'Linear Regression aggregated features'
model(x_poly, title)
