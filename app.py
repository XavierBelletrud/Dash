import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
from plotly.offline import init_notebook_mode, iplot, plot

# Since we're adding callbacks to elements that don't exist in the app.layout,
# Dash will raise an exception to warn us that we might be
# doing something wrong.
# In this case, we're adding the elements through a callback, so we can ignore
# the exception.
app = dash.Dash(__name__, suppress_callback_exceptions=True)

timesData = pd.read_csv('timesData.csv')
df2016 = timesData[timesData.year == 2016].iloc[:50,:]



# Création de la première trace 
trace1 = go.Bar(
                x = df2016.university_name,
                y = df2016.income,
                name = "Income",
                )

# Création de la deuxième trace 
trace2 = go.Bar(
                x = df2016.university_name,
                y = df2016.international,
                name = "International",
                )
data = [trace1, trace2]
layout = go.Layout(barmode = "group")
fig = go.Figure(data = data, layout = layout)
iplot(fig)


#def get_menu():
    #menu = html.Div([
    #    dcc.Link('page 1  |', href='/apps/page1', className="tab first"),
    #    dcc.Link('page 2  |', href='/apps/page2', className="tab")],
    #className="row")
    #return menu 

index_page = html.Div([
    dcc.Link('Go to Page 1', href='/page-1'),
    html.Br(),
    dcc.Link('Go to Page 2', href='/page-2'),
])

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content'),
    dash_table.DataTable(
        data=df2016.to_dict('records'),
        columns=[{'id': c, 'name': c} for c in df2016.columns],
        fixed_rows={'headers': True},
        style_cell={
            'minWidth': 95, 'maxWidth': 95, 'width': 95
                    }),
    html.A(html.Button('Download Data'),
        id='download-button',
        download='timesData.csv',
        href='/home/helloworld/Bureau/Brief/BriefRendus/Dash/timesData.csv',
        target='_blank')
])


page_1_layout = html.Div([
    html.H1('Page 1'),
    html.Br(),
    dcc.Link('Go to Page 2', href='/page-2'),
    html.Br(),
    dcc.Link('Go back to home', href='/'),
    dcc.Graph(figure=fig),
    html.Br(),


])

@app.callback(dash.dependencies.Output('page-1-content', 'children'),
              [dash.dependencies.Input('page-1-dropdown', 'value')])
def page_1_dropdown(value):
    return 'You have selected "{}"'.format(value)


page_2_layout = html.Div([
    html.H1('Page 2'),
    dcc.RadioItems(
        id='page-2-radios',
        options=[{'label': i, 'value': i} for i in ['Orange', 'Blue', 'Red']],
        value='Orange'
    ),
    html.Div(id='page-2-content'),
    html.Br(),
    dcc.Link('Go to Page 1', href='/page-1'),
    html.Br(),
    dcc.Link('Go back to home', href='/')
])

@app.callback(dash.dependencies.Output('page-2-content', 'children'),
              [dash.dependencies.Input('page-2-radios', 'value')])
def page_2_radios(value):
    return 'You have selected "{}"'.format(value)


# Update the index
@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/page-1':
        return page_1_layout
    elif pathname == '/page-2':
        return page_2_layout
    else:
        return index_page
    # You could also return a 404 "URL not found" page here


if __name__ == '__main__':
    app.run_server(debug=True)