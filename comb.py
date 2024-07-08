from dash import dcc, html, Dash
from dash.dependencies import Input, Output, State
import dash
from datetime import datetime,timedelta
from db_connection import get_db_connection
import pandas as pd
import plotly.express as px


class CombinedDashboard:
    def __init__(self, flask_app):
        self.conn = get_db_connection()
        self.cursor = self.conn.cursor()
        self.analysis_data = self.load_data()
        self.app = Dash(__name__, server=flask_app,
                        url_base_pathname='/analysis_chart/')
        self.layout()
        self.callbacks()

    def load_data(self):
        analysis_sql = """ 
        SELECT analysisreg.*, samplereg.SampleType,samplereg.Date_Time
        FROM analysisreg
        JOIN samplereg ON analysisreg.SampleID = samplereg.SampleID
        ORDER BY samplereg.Date_Time DESC;
        """
        self.cursor.execute(analysis_sql)
        analysis_rows = self.cursor.fetchall()
        analysis_columns = [column[0] for column in self.cursor.description]
        analysis_data = pd.DataFrame(analysis_rows, columns=analysis_columns)
        analysis_data['Date_Time'] = pd.to_datetime(
            analysis_data['Date_Time'])
        analysis_data['SampleType'] = analysis_data['SampleType'].str.upper()
        analysis_data['LabID'] = analysis_data['LabID'].replace(
            "BTE-NIR", "NIR-BTE")
        analysis_data['TestType'] = analysis_data['TestType'].replace(
            "manual", "MANUAL")
        analysis_data['TestType'] = analysis_data['TestType'].replace(
            "nir", "NIR")
        analysis_data = analysis_data[analysis_data['Material'] != 'KGMO']
        self.cursor.close()
        self.conn.close()
        return analysis_data

    def layout(self):
        self.app.layout = html.Div([
            dcc.Location(id='url', refresh=False),
            html.Div([
                html.A('Home', href='/home', style={
                    'fontWeight': 'bold',
                    'textDecoration': 'none',
                    'color': 'black',
                    'border-style': 'solid',
                    'border-color': 'black',
                    'backgroundColor': 'white',
                    'padding': '5px 10px',
                    'borderRadius': '5px',
                    'fontSize': '20px',
                    'display': 'inline-block',
                    'textAlign': 'center'
                }),

                html.H1('M/C Analysis Report',
                        style={'textAlign': 'center', 'fontWeight': 'bold', 'flex': '1'}),

            ], style={'display': 'flex', 'align-items': 'center', 'justify-content': 'space-between', 'width': '100%', 'margin': '10px'}),
            html.Div([
                html.Div([
                    html.Label('Material'),
                    dcc.Dropdown(
                        id='material-dropdown',
                        options=[{'label': mat, 'value': mat}
                                 for mat in self.analysis_data['Material'].unique()],

                        value=self.analysis_data['Material'].unique()[1],
                    )
                ], style={'width': '20%'}),

                html.Div([
                    html.Label('SampleType'),
                    dcc.Dropdown(
                        id='sampletype-dropdown',
                        multi=True,
                        options=[{'label': 'Select All', 'value': 'ALL'}] + [{'label': stype,
                                                                              'value': stype} for stype in self.analysis_data['SampleType'].unique()],
                        value=[
                            stype for stype in self.analysis_data['SampleType'].unique()],
                        placeholder="Select SampleType",
                    )
                ], style={'width': '20%'}),

                html.Div([
                    html.Label('LabID'),
                    dcc.Dropdown(
                        id='LabID-dropdown',
                        multi=True,
                        options=[{'label': 'Select All', 'value': 'ALL'}] + [{'label': lab,
                                                                              'value': lab} for lab in self.analysis_data['LabID'].unique()],
                        value=[lab for lab in self.analysis_data['LabID'].unique()],
                        placeholder="Select LabID",
                    )
                ], style={'width': '20%'}),

                html.Div([
                    html.Label('TestType'),
                    dcc.Dropdown(
                        id='testtype-dropdown',
                        multi=True,
                        options=[{'label': 'Select All', 'value': 'ALL'}] + [{'label': ttype,
                                                                              'value': ttype} for ttype in self.analysis_data['TestType'].unique()],
                        value=[
                            ttype for ttype in self.analysis_data['TestType'].unique()],
                        placeholder="Select TestType",
                    )
                ], style={'width': '20%'}),

                html.Div([
                    html.Label('Date Range'),
                    dcc.DatePickerRange(
                        id='date-picker-range',
                        min_date_allowed=datetime(2023, 1, 1),
                        max_date_allowed=datetime.now(),
                        start_date= datetime.now() - timedelta(days=7),
                        end_date= datetime.now(),
                        display_format='DD-MM-YYYY',
                        style={'font-size': '2px'}
                    )
                ], style={'width': '20%','display': 'flex','flex-direction': 'column'}),
            ], style={'display': 'flex', 'gap': '10px', 'width': '100%', 'fontWeight': 'bold', 'font-size': 'inherit', 'margin': '10px'}),

            html.Button('Reset', id='reset-button', n_clicks=0, style={
                'fontWeight': 'bold',
                'textDecoration': 'none',
                'color': 'black',
                'border-style': 'solid',
                'border-color': 'black',
                'backgroundColor': 'white',
                'padding': '5px 10px',
                'borderRadius': '5px',
                'fontSize': '20px',
                'display': 'inline-block',
                'textAlign': 'center',
                'margin': '10px'}),

            dcc.Graph(id='mc-graph'),

            html.Div([

                html.H1('O/C Analysis Report',
                        style={'textAlign': 'center', 'fontWeight': 'bold', 'flex': '1'}),

            ], style={'display': 'flex', 'align-items': 'center', 'justify-content': 'space-between', 'width': '100%', 'margin': '10px'}),
            html.Div([
                html.Div([
                    html.Label('Material'),
                    dcc.Dropdown(
                        id='oc-material-dropdown',
                        options=[{'label': mat, 'value': mat}
                                 for mat in self.analysis_data['Material'].unique()],

                        value=self.analysis_data['Material'].unique()[1],
                    )
                ], style={'width': '20%'}),

                html.Div([
                    html.Label('SampleType'),
                    dcc.Dropdown(
                        id='oc-sampletype-dropdown',
                        multi=True,
                        options=[{'label': 'Select All', 'value': 'ALL'}] + [{'label': stype,
                                                                              'value': stype} for stype in self.analysis_data['SampleType'].unique()],
                        value=[
                            stype for stype in self.analysis_data['SampleType'].unique()],
                        placeholder="Select SampleType",
                    )
                ], style={'width': '20%'}),

                html.Div([
                    html.Label('LabID'),
                    dcc.Dropdown(
                        id='oc-LabID-dropdown',
                        multi=True,
                        options=[{'label': 'Select All', 'value': 'ALL'}] + [{'label': lab,
                                                                              'value': lab} for lab in self.analysis_data['LabID'].unique()],
                        value=[lab for lab in self.analysis_data['LabID'].unique()],
                        placeholder="Select LabID",
                    )
                ], style={'width': '20%'}),

                html.Div([
                    html.Label('TestType'),
                    dcc.Dropdown(
                        id='oc-testtype-dropdown',
                        multi=True,
                        options=[{'label': 'Select All', 'value': 'ALL'}] + [{'label': ttype,
                                                                              'value': ttype} for ttype in self.analysis_data['TestType'].unique()],
                        value=[
                            ttype for ttype in self.analysis_data['TestType'].unique()],
                        placeholder="Select TestType",
                    )
                ], style={'width': '20%'}),

                html.Div([
                    html.Label('Date Range'),
                    dcc.DatePickerRange(
                        id='oc-date-picker-range',
                        min_date_allowed=datetime(2000, 1, 1),
                        max_date_allowed=datetime.now(),
                        start_date= datetime.now()-timedelta(days=7),
                        end_date= datetime.now(),
                        display_format='DD-MM-YYYY',
                        style={'font-size': '2px'}
                    )
                ], style={'width': '20%','display': 'flex','flex-direction': 'column'}),
            ], style={'display': 'flex', 'gap': '10px', 'width': '100%', 'fontWeight': 'bold', 'font-size': 'inherit', 'margin': '10px'}),

            html.Button('Reset', id='oc-reset-button', n_clicks=0, style={
                'fontWeight': 'bold',
                'textDecoration': 'none',
                'color': 'black',
                'border-style': 'solid',
                'border-color': 'black',
                'backgroundColor': 'white',
                'padding': '5px 10px',
                'borderRadius': '5px',
                'fontSize': '20px',
                'display': 'inline-block',
                'textAlign': 'center',
                'margin': '10px'}),

            dcc.Graph(id='oc-graph'),

            
        ])

    def callbacks(self):
        @self.app.callback(
            Output('sampletype-dropdown', 'options'),
            Output('LabID-dropdown', 'options'),
            Output('testtype-dropdown', 'options'),
            Input('material-dropdown', 'value')
        )
        def update_dropdowns_mc(material):
            if not material:
                material = self.analysis_data['Material'].unique().tolist()

            if isinstance(material, str):
                material = [material]

            filtered_data = self.analysis_data[self.analysis_data['Material'].isin(
                material)]

            sampletype_options = [{'label': 'Select All', 'value': 'ALL'}] + [
                {'label': stype, 'value': stype} for stype in filtered_data['SampleType'].unique()]
            LabID_options = [{'label': 'Select All', 'value': 'ALL'}] + \
                [{'label': lab, 'value': lab}
                    for lab in filtered_data['LabID'].unique()]
            testtype_options = [{'label': 'Select All', 'value': 'ALL'}] + [
                {'label': ttype, 'value': ttype} for ttype in filtered_data['TestType'].unique()]

            return sampletype_options, LabID_options, testtype_options
        @self.app.callback(
            Output('oc-sampletype-dropdown', 'options'),
            Output('oc-LabID-dropdown', 'options'),
            Output('oc-testtype-dropdown', 'options'),
            Input('oc-material-dropdown', 'value')
        )
        def update_dropdowns_oc(material):
            if not material:
                material = self.analysis_data['Material'].unique().tolist()

            if isinstance(material, str):
                material = [material]

            filtered_data = self.analysis_data[self.analysis_data['Material'].isin(
                material)]

            sampletype_options = [{'label': 'Select All', 'value': 'ALL'}] + [
                {'label': stype, 'value': stype} for stype in filtered_data['SampleType'].unique()]
            LabID_options = [{'label': 'Select All', 'value': 'ALL'}] + \
                [{'label': lab, 'value': lab}
                    for lab in filtered_data['LabID'].unique()]
            testtype_options = [{'label': 'Select All', 'value': 'ALL'}] + [
                {'label': ttype, 'value': ttype} for ttype in filtered_data['TestType'].unique()]

            return sampletype_options, LabID_options, testtype_options

        @self.app.callback(
            Output('mc-graph', 'figure'),
            [
                Input('material-dropdown', 'value'),
                Input('sampletype-dropdown', 'value'),
                Input('LabID-dropdown', 'value'),
                Input('testtype-dropdown', 'value'),
                Input('date-picker-range', 'start_date'),
                Input('date-picker-range', 'end_date'),
            ]
        )
        def update_dashboard(material, sampletype, Lab, TestType, start_date, end_date):
            if isinstance(material, str):
                material = [material]
            if isinstance(sampletype, str):
                sampletype = [sampletype]
            if isinstance(Lab, str):
                Lab = [Lab]
            if isinstance(TestType, str):
                TestType = [TestType]

            if 'ALL' in sampletype:
                sampletype = self.analysis_data['SampleType'].unique().tolist()
            if 'ALL' in Lab:
                Lab = self.analysis_data['LabID'].unique().tolist()
            if 'ALL' in TestType:
                TestType = self.analysis_data['TestType'].unique().tolist()

            material = material or self.analysis_data['Material'].unique(
            ).tolist()
            sampletype = sampletype or self.analysis_data['SampleType'].unique(
            ).tolist()
            Lab = Lab or self.analysis_data['LabID'].unique().tolist()
            TestType = TestType or self.analysis_data['TestType'].unique(
            ).tolist()
            start_date = start_date or  datetime.now()-timedelta(days=7)
            end_date = end_date or  datetime.now()

            filtered_data = self.analysis_data[
                (self.analysis_data['Material'].isin(material)) &
                (self.analysis_data['SampleType'].isin(sampletype)) &
                (self.analysis_data['LabID'].isin(Lab)) &
                (self.analysis_data['TestType'].isin(TestType)) &
                (self.analysis_data['Date_Time'] >= pd.Timestamp(start_date)) &
                (self.analysis_data['Date_Time']
                 <= pd.Timestamp(end_date))
            ]

            if 'M_C' not in filtered_data.columns:
                raise KeyError("Column 'M_C' not found in the data")

            average_data = filtered_data.groupby([pd.Grouper(
                key='Date_Time', freq='D'), 'SampleType']).agg({'M_C': 'mean'}).reset_index()

            fig = px.line(average_data, x='Date_Time', y='M_C', color='SampleType',
                          title='M/C and Sample by Date and SampleType', markers=True, height=700)

            fig.update_traces(mode='lines+markers', line_shape='spline')
    
            fig.update_layout(
                title={
                    'text': 'M/C and Sample by Date and SampleType',
                    'y': 0.9,
                    'x': 0.5,
                    'xanchor': 'center',
                    'yanchor': 'top',
                    'font': {'size': 24, 'color': 'black', 'family': 'Arial', 'weight': 'bold'}
                },
                legend=dict(
                    orientation='h',
                    yanchor='bottom',
                    y=1.02,
                    xanchor='center',
                    x=0.5
                ),
                xaxis=dict(
                    title="Date",
                    rangeslider=dict(visible=True),
                ),
                yaxis=dict(
                    title="M/C",
                    fixedrange=False
                ),
                hovermode='x unified',
                hoverlabel=dict(
                    bgcolor="white",
                    font_size=16,
                    font_family="Rmckwell",
                    align='left'
                ),
                
                margin=dict(l=40, r=40, t=40, b=40)
            )
            fig.update_xaxes(rangeslider_thickness=0.02)
            
            return fig
        @self.app.callback(
            Output('oc-graph', 'figure'),
            [
                Input('oc-material-dropdown', 'value'),
                Input('oc-sampletype-dropdown', 'value'),
                Input('oc-LabID-dropdown', 'value'),
                Input('oc-testtype-dropdown', 'value'),
                Input('oc-date-picker-range', 'start_date'),
                Input('oc-date-picker-range', 'end_date'),
            ]
        )
        def update_dashboard_oc(material, sampletype, Lab, TestType, start_date, end_date):
            if isinstance(material, str):
                material = [material]
            if isinstance(sampletype, str):
                sampletype = [sampletype]
            if isinstance(Lab, str):
                Lab = [Lab]
            if isinstance(TestType, str):
                TestType = [TestType]

            if 'ALL' in sampletype:
                sampletype = self.analysis_data['SampleType'].unique().tolist()
            if 'ALL' in Lab:
                Lab = self.analysis_data['LabID'].unique().tolist()
            if 'ALL' in TestType:
                TestType = self.analysis_data['TestType'].unique().tolist()

            material = material or self.analysis_data['Material'].unique(
            ).tolist()
            sampletype = sampletype or self.analysis_data['SampleType'].unique(
            ).tolist()
            Lab = Lab or self.analysis_data['LabID'].unique().tolist()
            TestType = TestType or self.analysis_data['TestType'].unique(
            ).tolist()
            start_date = start_date or datetime.now()-timedelta(days=7)
            end_date = end_date  or datetime.now()

            filtered_data = self.analysis_data[
                (self.analysis_data['Material'].isin(material)) &
                (self.analysis_data['SampleType'].isin(sampletype)) &
                (self.analysis_data['LabID'].isin(Lab)) &
                (self.analysis_data['TestType'].isin(TestType)) &
                (self.analysis_data['Date_Time'] >= pd.Timestamp(start_date)) &
                (self.analysis_data['Date_Time']
                 <= pd.Timestamp(end_date))
            ]

            if 'O_C' not in filtered_data.columns:
                raise KeyError("Column 'O_C' not found in the data")

            average_data = filtered_data.groupby([pd.Grouper(
                key='Date_Time', freq='D'), 'SampleType']).agg({'O_C': 'mean'}).reset_index()

            fig = px.line(average_data, x='Date_Time', y='O_C', color='SampleType',
                          title='O/C and Sample by Date and SampleType', markers=True, height=700)

            fig.update_traces(mode='lines+markers', line_shape='spline')
    
            fig.update_layout(
                title={
                    'text': 'O/C and Sample by Date and SampleType',
                    'y': 0.9,
                    'x': 0.5,
                    'xanchor': 'center',
                    'yanchor': 'top',
                    'font': {'size': 24, 'color': 'black', 'family': 'Arial', 'weight': 'bold'}
                },
                legend=dict(
                    orientation='h',
                    yanchor='bottom',
                    y=1.02,
                    xanchor='center',
                    x=0.5
                ),
                xaxis=dict(
                    title="Date",
                    rangeslider=dict(visible=True),
                ),
                yaxis=dict(
                    title="O/C",
                    fixedrange=False
                ),
                hovermode='x unified',
                hoverlabel=dict(
                    bgcolor="white",
                    font_size=16,
                    font_family="Rmckwell",
                    align='left'
                ),
               
                margin=dict(l=40, r=40, t=40, b=40)
            )
            fig.update_xaxes(rangeslider_thickness=0.02)
            
            return fig

        @self.app.callback(
            Output('material-dropdown', 'value'),
            Output('sampletype-dropdown', 'value'),
            Output('LabID-dropdown', 'value'),
            Output('testtype-dropdown', 'value'),
            Output('date-picker-range', 'start_date'),
            Output('date-picker-range', 'end_date'),
            Input('url', 'pathname'),
            Input('reset-button', 'n_clicks'),
            State('material-dropdown', 'options'),
            State('sampletype-dropdown', 'options'),
            State('LabID-dropdown', 'options'),
            State('testtype-dropdown', 'options')
        )
        def reset_filters_on_page_load_or_button_click(pathname, n_clicks, material_options, sampletype_options, LabID_options, testtype_options):
            if pathname == '/M_C_analysis_report/' or n_clicks > 0:
                return (material_options[1]['value'],
                        [option['value']
                            for option in sampletype_options if option['value'] != 'ALL'],
                        [option['value']
                            for option in LabID_options if option['value'] != 'ALL'],
                        [option['value']
                        for option in testtype_options if option['value'] != 'ALL'],
                        datetime.now()-timedelta(days=7),
                        datetime.now())
            return dash.no_update
        @self.app.callback(
            Output('oc-material-dropdown', 'value'),
            Output('oc-sampletype-dropdown', 'value'),
            Output('oc-LabID-dropdown', 'value'),
            Output('oc-testtype-dropdown', 'value'),
            Output('oc-date-picker-range', 'start_date'),
            Output('oc-date-picker-range', 'end_date'),
            Input('url', 'pathname'),
            Input('oc-reset-button', 'n_clicks'),
            State('oc-material-dropdown', 'options'),
            State('oc-sampletype-dropdown', 'options'),
            State('oc-LabID-dropdown', 'options'),
            State('oc-testtype-dropdown', 'options')
        )
        def reset_filters_on_page_load_or_button_click_oc(pathname, n_clicks, material_options, sampletype_options, LabID_options, testtype_options):
            if pathname == '/analysis_chart/' or n_clicks > 0:
                return (material_options[1]['value'],
                        [option['value']
                            for option in sampletype_options if option['value'] != 'ALL'],
                        [option['value']
                            for option in LabID_options if option['value'] != 'ALL'],
                        [option['value']
                        for option in testtype_options if option['value'] != 'ALL'],
                        datetime.now()- timedelta(days=7),
                        datetime.now())
            return dash.no_update
