import pickle

import dill
import joblib
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from catboost import Pool
import base64
from io import BytesIO
"""
requirements
numba==0.51.0
python==3.7
numpy==1.20.2
shap==0.39.0

"""

#Load risk level classifier: CatBoost
#catboost_model = pickle.load(open("C:\\Users\\ASUS\\Downloads\\MamatjanLabFinal-main\\MamatjanLabFinal-main\\model\\model_pkl",'rb'))
catboost_model_h = pickle.load(open("model2/model_cat_heart_pkl",'rb'))

#Load first feature selection model: SHAP
#explainer = joblib.load("C:\\Users\\ASUS\\Downloads\\MamatjanLabFinal-main\\MamatjanLabFinal-main\\model\\explainer.bz2")
explainer = joblib.load(open('model2/explainer_cat_heart.bz2', 'rb'))
 
def get_shap_explanation_scores_df_heart(patient):

    """
    Input: numpy array of patient input data
    Output: dataframe of the 10 features with their respective importance score calculated by SHAP (sorted)
    """

    label = get_risk_level_heart(patient)

    df = pd.DataFrame(np.array(patient)[np.newaxis], columns=['age','sex', 'cp', 'trtbps', 'chol', 'fbs', 'restecg', 'thalachh', 'exng', 'oldpeak', 'slp', 'caa', 'thall'])
    shap_values = explainer.shap_values(df)
    sdf_train = pd.DataFrame({
        'feature_value':  df.values.flatten(),
        'shap_values': shap_values[label].flatten()
    })
    sdf_train.index =df.columns.to_list()
    sdf_train = sdf_train.sort_values('shap_values',ascending=False)
    sdf_train['Feature'] = sdf_train.index

    """Featurelis=[(str(sdf_train['Feature'][0])),(str(sdf_train['Feature'][1])),(str(sdf_train['Feature'][2])) , (str(sdf_train['Feature'][3])), (str(sdf_train['Feature'][4])), (str(sdf_train['Feature'][5])),(str(sdf_train['Feature'][6])),(str(sdf_train['Feature'][7])) , (str(sdf_train['Feature'][8])), (str(sdf_train['Feature'][9]))]
    valuelis=[(str(sdf_train['shap_values'][0])),(str(sdf_train['shap_values'][1])),(str(sdf_train['shap_values'][2])) , (str(sdf_train['shap_values'][3])), (str(sdf_train['shap_values'][4])), (str(sdf_train['shap_values'][5])),(str(sdf_train['shap_values'][6])),(str(sdf_train['shap_values'][7])) , (str(sdf_train['shap_values'][8])), (str(sdf_train['shap_values'][9]))]
​
    return Featurelis ,valuelis"""

    return sdf_train

def get_graph():
    buffer=BytesIO()
    plt.savefig(buffer,format='png')
    buffer.seek(0)
    image_png= buffer.getvalue()
    graph=base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    buffer.close()
    return graph

def plot_SHAP_result_heart(patient_data):
    plt.switch_backend('AGG')
    plt.figure(figsize=(8,7))
     

    colors = {"age":'r', "sex":'c', "cp":'y', "trtbps":'b', "chol":'k', "fbs":'grey', "restecg": 'gold',"thalachh":'lightcoral', "exng":'maroon', "oldpeak":'coral', "slp":'orange', "caa":'skyblue', "thall": 'crimson'}
    df = get_shap_explanation_scores_df_heart(patient_data)
    
    """plt.bar(Featurelis, valuelis,  color=[colors[i] for i in Featurelis])
    plt.title("SHAP Explanation")"""

    df['shap_values'][:12].plot(kind="bar", color=[colors[i] for i in df['Feature']], title="SHAP Explanation")
    plt.show()

    graph = get_graph()
    return graph 


def get_risk_level_heart(patient_data):
    """
    Input: numpy array of patient data
    Output: risk level from 0-1
    """

    prediction = catboost_model_h.predict(patient_data)
    label = np.argmax(prediction, axis=0)

    return(label)

"""test_input = np.array(['63','1' ,'0','145','233','1','0','150','0','2.3','0','0', '1'])
print(get_shap_explanation_scores_df_heart(test_input))
graph = plot_SHAP_result_heart(test_input)

print("The test output")
print(catboost_model.predict(test_input))
"""