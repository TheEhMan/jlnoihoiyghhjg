from dash import Dash, html, dcc, callback, Output, Input, State
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
import pickle
import joblib
import numpy as np
from dash.exceptions import PreventUpdate
from django_plotly_dash import DjangoDash



catboost_model = pickle.load(open("website/dash/model_pkl", 'rb'))
explainer = joblib.load('website/dash/explainer.bz2')
def get_shap_explanation_scores_df(patient):
 
    """
    Input: numpy array of patient input data
    Output: dataframe of the 10 features with their respective importance score calculated by SHAP (sorted)
    """

    label = get_risk_level(patient)

    df = pd.DataFrame(np.array(patient)[np.newaxis],
        columns=['age',	'gender', 'polyuria', 'polydipsia', 'sudden_weight_loss', 'weakness', 'polyphagia', 'genital_thrush', 'visual_blurring', 'itching', 'irritability', 'delayed_healing', 'partial_paresis', 'muscle_stiffness', 'alopecia', 'obesity']
        )
    shap_values = explainer.shap_values(df)
    sdf_train = pd.DataFrame({
        'feature_value':  df.values.flatten(),
        'shap_values': shap_values[label].flatten()
    })
    sdf_train.index =df.columns.to_list()
    sdf_train = sdf_train.sort_values('shap_values',ascending=False)
    sdf_train['Feature'] = sdf_train.index


    return sdf_train

def get_risk_level(patient_data):
    """
    Input: numpy array of patient data
    Output: risk level from 0-1
    """

    prediction = catboost_model.predict(patient_data)
    label = np.argmax(prediction, axis=0)

    return(label)

app = DjangoDash("DashApp", external_stylesheets=[dbc.themes.COSMO])


app.layout = dbc.Container([

    dbc.Navbar(
        dbc.Container([
            html.A(
                dbc.Row([
                        (dbc.NavbarBrand("An Explainable Recommendation Framework for line Stratification of Diabetes Risk", className="text-center")),
                    ]
                ,align="center",
                ),
                href="/",
            ),
        ]),
    color="primary",
    dark=True,
    className="mb-5 text-center",
    ),

    dbc.Container([
        dbc.Row([
            dbc.Col([
                dbc.Row([
                    html.Label('Age', className = 'text-center'),
                    dbc.Input(
                    type= 'number',
                    id = 'age',
                    size = 'sm',
                    className = 'mb-2'
                    ),
                ]),


                dbc.Row([
                    html.Label("Sex", className= 'text-center'),
                    dbc.RadioItems(
                        options= [{'label':'Male', 'value': 1}, {'label':'Female', 'value': 0}],
                        inline= True,
                        id = 'sex',
                        style = {'text-align': 'center'},
                        className = 'mb-3'),
                ]),

                dbc.Row([
                    dbc.Label("Polyuria", className = 'text-center', id = 'polyuria-label', style= {"cursor": "pointer"}),
                    dbc.Tooltip("The body urinates more than usual and passes excessive or abnormally large amounts of urine each time you urinate", target="polyuria-label", placement="top"),
                    dbc.RadioItems(
                        options = [{'label': "Yes", 'value': 1},{'label': 'No', 'value': 0}],
                        inline= True,
                        id = 'polyuria',
                        style = {'text-align': 'center'},
                        className = 'mb-3'),
                ]),

                dbc.Row([
                html.Label("Polydipsia", className = 'text-center', id = 'polydipsia-label', style= {"cursor": "pointer"}),
                dbc.Tooltip("Excessive thirst or excess drinking", target="polydipsia-label", placement="top"),

                dbc.RadioItems(
                    options = [{'label': "Yes", 'value': 1},{'label': 'No', 'value': 0}],
                    inline= True,
                    id = 'polydipsia',
                    style = {'text-align': 'center'}),
                ]),


            ]
            ),
            dbc.Col([
                dbc.Row([
                html.Label("Sudden Weight Loss", className = 'text-center', id = 'swl-label', style= {"cursor": "pointer"}),
                dbc.Tooltip("Losing weight without changing your diet or exercise routine", target="swl-label", placement="top"),
                dbc.RadioItems(
                    options = [{'label': "Yes", 'value': 1},{'label': 'No', 'value': 0}],
                    inline= True,
                    className = 'mb-3',
                    id = 'swl',
                    style = {
                    'text-align': 'center'
                    }),
                ]),

                dbc.Row([
                html.Label("Weakness", className='text-center', id = 'weakness-label', style= {"cursor": "pointer"}),
                dbc.Tooltip("Lack of strength, firmness, vigor", target="weakness-label", placement="top"),
                dbc.RadioItems(
                    options = [{'label': "Yes", 'value': 1},{'label': 'No', 'value': 0}],
                    inline= True,
                    id = 'weakness',
                    style = {'text-align': 'center'},
                    className = 'mb-3'),
                ]),

                dbc.Row([
                html.Label("Polyphagia", className='text-center', id = 'polyphagia-label', style= {"cursor": "pointer"}),
                dbc.Tooltip("Excessive hunger or appetite", target="polyphagia-label", placement="top"),
                dbc.RadioItems(
                    options = [{'label': "Yes", 'value': 1},{'label': 'No', 'value': 0}],
                    inline= True,
                    id = 'polyphagia',
                    style = {'text-align': 'center'},
                    className = 'mb-3'),
                ]),

                dbc.Row([
                html.Label("Genital Thrush", className='text-center', id = 'gt-label', style= {"cursor": "pointer"}),
                dbc.Tooltip("Ithicng or burning in the genital area", target="gt-label", placement="top"),
                dbc.RadioItems(
                    options = [{'label': "Yes", 'value': 1},{'label': 'No', 'value': 0}],
                    inline= True,
                    id = 'genital_thrush',
                    style = {'text-align': 'center'},
                    className = 'mb-3'),
                ])
            ]),
            dbc.Col([
                dbc.Row([
                html.Label("Visual Blurring", className = 'text-center', id = 'vb-label', style= {"cursor": "pointer"}),
                dbc.Tooltip("Vision is not sharp and clear", target="vb-label", placement="top"),
                dbc.RadioItems(
                    options = [{'label': "Yes", 'value': 1},{'label': 'No', 'value': 0}],
                    inline= True,
                    id = 'visual_blurring',
                    style = {'text-align': 'center'},
                    className = 'mb-3'),
                ]),

                dbc.Row([
                html.Label("Itching on the skin", className = 'text-center'),
                dbc.RadioItems(
                    options = [{'label': "Yes", 'value': 1},{'label': 'No', 'value': 0}],
                    inline= True,
                    id = 'itching',
                    style = {'text-align': 'center'},
                    className = 'mb-3'),
                ]),

                dbc.Row([
                html.Label("Irritability", className = 'text-center' ,id = 'irritability-label', style= {"cursor": "pointer"}),
                dbc.Tooltip("Quick excitability to annoyance, impatience, or anger", target="irritability-label", placement="top"),


                dbc.RadioItems(
                    options = [{'label': "Yes", 'value': 1},{'label': 'No', 'value': 0}],
                    inline= True,
                    id = 'irritability',
                    style = {'text-align': 'center'},
                    className = 'mb-3'),
                ]),

                dbc.Row([
                html.Label("Delayed Healing", className = 'text-center', id = 'dh-label', style= {"cursor": "pointer"}),
                dbc.Tooltip("The wound has trouble healing or staying closed", target="dh-label", placement="top"),
                dbc.RadioItems(
                    options = [{'label': "Yes", 'value': 1},{'label': 'No', 'value': 0}],
                    inline= True,
                    id = 'delayed_healing',
                    style = {'text-align': 'center'},
                    className = 'mb-3'),
                ]),
            ]),
            dbc.Col([
                dbc.Row([
                html.Label("Partial Paresis", className = 'text-center', id = 'pp-label', style= {"cursor": "pointer"}),
                dbc.Tooltip("the weakening of a muscle or group of muscles", target="pp-label", placement="top"),
                dbc.RadioItems(
                    options = [{'label': "Yes", 'value': 1},{'label': 'No', 'value': 0}],
                    inline= True,
                    id = 'partial_paresis',
                    style = {'text-align': 'center'},
                    className = 'mb-3'),
                ]),

                dbc.Row([
                html.Label("Muscle stiffness", className = 'text-center', id = 'mf-label', style= {"cursor": "pointer"}),
                dbc.Tooltip("Tight feeling in the muscles, which can be accompanied by pain and difficulty moving", target="mf-label", placement="top"),
                dbc.RadioItems(
                    options = [{'label': "Yes", 'value': 1},{'label': 'No', 'value': 0}],
                    inline= True,
                    id = 'muscle_stiffness',
                    style = {'text-align': 'center'},
                    className = 'mb-3'),
                ]),

                dbc.Row([
                html.Label("Alopecia", className = 'text-center', id = 'alopecia-label', style= {"cursor": "pointer"}),
                dbc.Tooltip("Hair loss", target="alopecia-label", placement="top"),
                dbc.RadioItems(
                    options = [{'label': "Yes", 'value': 1},{'label': 'No', 'value': 0}],
                    inline= True,
                    id = 'alopecia',
                    style = {'text-align': 'center'},
                    className = 'mb-3'),
                ]),

                dbc.Row([
                html.Label("Obesity", className = 'text-center', id = 'obesity-label', style= {"cursor": "pointer"}),
                dbc.Tooltip("Abnormal or excessive fat accumulation that presents a risk to health, when body mass index (BMI) is over 25", target="obesity-label", placement="top"),


                dbc.RadioItems(
                    options = [{'label': "Yes", 'value': 1},{'label': 'No', 'value': 0}],
                    inline= True,
                    id = 'obesity',
                    style = {'text-align': 'center'},
                    className = 'mb-3'),
                ])
            ]),

        ]),

        dbc.Row([
            dbc.Button("Submit", color = 'primary', id = 'submit_button')
        ]),

        dbc.Row([
            dbc.Label('hello',
                      id = 'output_label',
                      className = 'text-center',
                      ),
        ])



    ]),

    dbc.Container([
        dbc.Row([
            dcc.Graph(
                figure = {},
                id = 'shap_explanation',

            )
        ])
    ])
])

@app.callback(
    Output(component_id = 'output_label', component_property= 'children'),
    Output(component_id = 'shap_explanation', component_property= 'figure'),

    [Input(component_id = 'submit_button', component_property= 'n_clicks')],

    [State(component_id= 'age', component_property= 'value'),
     State(component_id = 'sex', component_property = 'value'),
     State(component_id= 'polyuria', component_property= 'value'),
    State(component_id= 'polydipsia', component_property= 'value'),
    State(component_id= 'swl', component_property= 'value'),
     State(component_id= 'weakness', component_property= 'value'),
    State(component_id= 'polyphagia', component_property= 'value'),
    State(component_id= 'genital_thrush', component_property= 'value'),
    State(component_id= 'visual_blurring', component_property= 'value'),
    State(component_id= 'itching', component_property= 'value'),
    State(component_id= 'irritability', component_property= 'value'),
    State(component_id= 'delayed_healing', component_property= 'value'),
    State(component_id= 'partial_paresis', component_property= 'value'),
    State(component_id= 'muscle_stiffness', component_property= 'value'),
    State(component_id= 'alopecia', component_property= 'value'),
    State(component_id= 'obesity', component_property= 'value')],
)
def update_label(n, age,sex, polyuria, polydopsia, swl, weakness, polyphagia, genital_thrush, visual_blurring, itching, irritability, delayed_healing, partial_paresis, muscle_stiffness, alopecia, obesity):
    patient_input = np.array([age,sex, polyuria, polydopsia, swl, weakness, polyphagia, genital_thrush, visual_blurring, itching, irritability, delayed_healing, partial_paresis, muscle_stiffness, alopecia, obesity])


    patient_input = np.array([age,sex, polyuria, polydopsia, swl, weakness, polyphagia, genital_thrush, visual_blurring, itching, irritability, delayed_healing, partial_paresis, muscle_stiffness, alopecia, obesity])

    if None in patient_input:
        raise PreventUpdate

    else:
        prediction  = catboost_model.predict(patient_input)
        fx = get_shap_explanation_scores_df(patient_input)
        if prediction == 0:
            text = "You don't have diabetes risk"
        else:
            text = "You have diabetes risk"
        figure = px.histogram(fx, x= 'Feature', y = 'shap_values', title= 'SHAP Explanation ')

        return text, figure
    

    