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

title = 'Monthly Active Platform consumers'
fig = px.line(df, x="Yearly Quarter", y="MAPC", title=title)
savefig(fig, title)
