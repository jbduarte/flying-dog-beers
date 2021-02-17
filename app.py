import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import numpy as np

########### Define your variables
mytitle='Solow Model'
tabtitle='Solow App'
myheading='Solow Model Simulations'
githublink='https://github.com/jbduarte/flying-dog-beers'
sourceurl='https://www.flyingdog.com/beers/'

########### Set up the chart
class Solow:
    r"""
    Implements the Solow growth model with the update rule

        k_{t+1} = [(s z k^α_t) + (1 - δ)k_t] /(1 + n)

    """
    def __init__(self, n=0.05,  # population growth rate
                       s=0.3,  # savings rate
                       δ=0.1,   # depreciation rate
                       α=0.3,   # share of labor
                       z=2.0,   # productivity
                       k=1.0):  # current capital stock

        self.n, self.s, self.δ, self.α, self.z = n, s, δ, α, z
        self.k = k

    def f(self, k):
        return self.z * k**self.α

    def savings(self, k):
        return self.s*self.f(k)/k

    def depreciation(self):
        return self.δ*self.s + self.n
solow = Solow()
solow2 = Solow()
k = np.linspace(1,100,100)

fig = go.Figure()
fig.add_trace(go.Scatter(x=k, y=solow.savings(k), name = 'Savings benchmark',
              line=dict(color='black', width=1)))
fig.add_trace(go.Scatter(x=k, y=solow.depreciation()*np.ones(100), name = 'Depreciation benchmark',
              line=dict(color='black', width=1)))
fig.add_trace(go.Scatter(x=k, y=solow2.savings(k), name = 'Savings',
              line=dict(color='blue', width=2)))
fig.add_trace(go.Scatter(x=k, y=solow2.depreciation()*np.ones(100), name = 'Depreciation',
              line=dict(color='red', width=2)))
fig.update_layout(title='Simulations',
                   xaxis_title='k',
                   yaxis_title='Value')

########### Initiate the app
app = dash.Dash(__name__)
server = app.server
app.title=tabtitle

########### Set up the layout
app.layout = html.Div([
    html.H1(
        children='Solow Model',
        style={
            'textAlign': 'center'
        }
    ),
     html.Label('Savings rate'),
    html.Br(),
    html.Br(),
    dcc.Slider(
        id='s-slider',
        min=0.1,
        max=0.9,
        step=0.1,
        marks={i: str(round(i,1)) for i in np.linspace(0.1,0.9,9)},
        value=0.3
    ),
    html.Label('Depreciation rate'),
    html.Br(),
    html.Br(),
    dcc.Slider(
        id='delta-slider',
        min=0.1,
        max=0.9,
        step=0.1,
        marks={i: str(round(i,1)) for i in np.linspace(0.1,0.9,9)},
        value=0.1
    ),
    html.Label('Population growth rate'),
    html.Br(),
    html.Br(),
    dcc.Slider(
        id='n-slider',
        min=0.01,
        max=0.09,
        step=0.01,
        marks={i: str(round(i,2)) for i in np.linspace(0.01,0.09,9)},
        value=0.05
    ),
    html.Label('Alpha'),
    html.Br(),
    html.Br(),
    dcc.Slider(
        id='alpha-slider',
        min=0.1,
        max=0.9,
        step=0.1,
        marks={i: str(round(i,1)) for i in np.linspace(0.1,0.9,9)},
        value=0.3
    ),
    html.Label('Technology'),
    html.Br(),
    html.Br(),
    dcc.Slider(
        id='tec-slider',
        min=1,
        max=9,
        step=1,
        marks={i: str(round(i,1)) for i in range(1,10)},
        value=2
    ),
    html.Br(),
    html.Br(),
    dcc.Graph(id='graph', figure = fig)
], style={'padding': 40})

# Define callback to update graph
@app.callback(
    Output('graph', 'figure'),
    [Input("s-slider", "value"), Input("delta-slider", "value"),
     Input("n-slider", "value"), Input("alpha-slider", "value"), Input("tec-slider", "value")]
)
def update_figure(selected_s, selected_delta, selected_n, selected_α, selected_z):
    k = np.linspace(1,100,100)
    solow2.s = selected_s
    solow2.δ = selected_delta
    solow2.n = selected_n
    solow2.α = selected_α
    solow2.z = selected_z
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=k, y=solow.savings(k), name = 'Savings benchmark',
                  line=dict(color='black', width=1)))
    fig.add_trace(go.Scatter(x=k, y=solow.depreciation()*np.ones(100), name = 'Depreciation benchmark',
                  line=dict(color='black', width=1)))
    fig.add_trace(go.Scatter(x=k, y=solow2.savings(k), name = 'Savings',
                  line=dict(color='blue', width=2)))
    fig.add_trace(go.Scatter(x=k, y=solow2.depreciation()*np.ones(100), name = 'Depreciation',
                  line=dict(color='red', width=2)))
    fig.update_layout(title='Simulations',
                   xaxis_title='k',
                   yaxis_title='Value')
    fig.update_layout(transition_duration=1000)
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)


