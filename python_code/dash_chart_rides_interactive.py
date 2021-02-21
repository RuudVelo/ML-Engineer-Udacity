import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import plotly.express as px
import pandas as pd
import pickle

# define the dataset here
df_raw_1_1 = pd.read_pickle('df_modelset_rider1.pickle')

df = df_raw_1_1

df = df.groupby(['secs','filename'], as_index=False)['hr','watts'].sum()
df.set_index('secs', inplace=True)
trace1 = go.Line(x=df.index, y=df[('hr')], name='heart rate')
trace2 = go.Line(x=df.index, y=df[('watts')], name='watts')
mgr_options = df["filename"].unique()

app = dash.Dash()

app.layout = html.Div([
    html.H2("Select a ride file"),
    html.Div(
        [
            dcc.Dropdown(
                id="filename",
                options=[{
                    'label': i,
                    'value': i
                } for i in mgr_options],
                value="All filenames"),
        ],
        style={'width': '25%',
               'display': 'inline-block'}),
    dcc.Graph(id='funnel-graph'),
])

@app.callback(
    dash.dependencies.Output('funnel-graph', 'figure'),
    [dash.dependencies.Input('filename', 'value')])
def update_graph(filename):
    if filename == "All filenames":
        df_plot = df.copy()
    else:
        df_plot = df[df['filename'] == filename]

    

    trace1 = go.Line(x=df_plot.index, y=df_plot[('hr')], name='heart rate')
    trace2 = go.Line(x=df_plot.index, y=df_plot[('watts')], name='watts')

    return {
        'data': [trace1, trace2],
        'layout':
        go.Layout(
            title='Ride file {}'.format(filename)
            )
    }

if __name__ == '__main__':
    app.run_server(debug=True)