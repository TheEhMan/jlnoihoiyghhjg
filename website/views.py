from django.shortcuts import redirect, render
 
from .forms import CreateUserForm
from django.contrib.auth import authenticate , login , logout
from django.contrib import messages
 
from .models import *
 

#pdf display imports 
from django.http import FileResponse
import io

from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter

from model.main import *

def home_page(request):
    context = {}
    return render(request,'website/index.html',context)
 

def about_page(request):
    context = {}
    return render(request,'website/about.html',context)

def collaborators_page(request):
    context = {}
    return render(request,'website/collaborators.html',context)

def projects_page(request):
    context = {}
    return render(request,'website/projects.html',context)

def publications_page(request):
    context = {}
    return render(request,'website/publications.html',context)

def teammembers_page(request):
    context = {}
    return render(request,'website/teammembers.html',context)

def teaching_page(request):
    context = {}
    return render(request,'website/teaching.html',context)

def ieee_page(request):
    context = {}
    return render(request,'website/ieee.html',context)
#################################### Heart Page ###################################

def heart(request):
    context = {}
    return render(request , 'website/heart_attack/heart.html', context)

def heart_login(request):

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username= username, password = password)

        if user != None:
            login(request, user)

            return redirect('heart_form')
        else:
            messages.error(request,'Username or Password is incorrect ')

    context = {}
    return render(request , 'website/heart_attack/heart_login.html', {})

def heart_register(request):
    form = CreateUserForm()

    if request.method== "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, "Account was created for "+user)
            return redirect ('heart_login')

    context = {'form':form}
    return render(request , 'website/heart_attack/heart_register.html', context)
    
def heart_form(request):
    context = {}   
    return render(request, 'website/heart_attack/heart_form.html', context)


def heart_logout(request):
    logout(request)
    return redirect ('heart')


def heart_result(request):

    if request.method == "POST":
        pid= request.POST.get('PID')
        age= int(request.POST.get('age'))
        gender= int(request.POST.get('gender'))
        
        cp= int(request.POST.get('cp'))
        trtbps= int(request.POST.get('trtbps'))
        cholestrol= int(request.POST.get('cholestrol'))
        fbs= int(request.POST.get('fbs'))
        restecg= int(request.POST.get('restecg'))
        
        thalachh= int(request.POST.get('thalachh'))
        exng= int(request.POST.get('exng'))
        thall= int(request.POST.get('thall'))
        
        inplis = [pid,age,gender, cp,trtbps,cholestrol,fbs,restecg,thalachh,exng,thall]

        #testlis = [54,1,5,180,123,233,1,26,225,3 ]

        arr = np.array(inplis)

        sdf_train= get_shap_explanation_scores_df(arr)
        x = get_risk_level(arr) 
        chart= plot_SHAP_result(inplis)

        Featurelis=[(str(sdf_train['Feature'][0])),(str(sdf_train['Feature'][1])),(str(sdf_train['Feature'][2])) , (str(sdf_train['Feature'][3])), (str(sdf_train['Feature'][4]))]
     
 
    context = {"""'chart':chart ,
                'x':x,
                'pid':pid,
                'features':Featurelis,
                'age':age,
                'gender':gender,
                'cp':cp,
                'trtbps': trtbps,
                'chol': cholestrol,
                'fbs': fbs,
                'restecg':restecg,
                'thalachh': thalachh,
                'exng':exng,
                'thall':thall"""} 
    my_context = {'context':context}

    return render(request, 'website/heart_attack/heart_result.html', my_context)


def heart_view_pdf(request):

    buf = io.BytesIO()

    c= canvas.Canvas(buf,pagesize= letter , bottomup=0)

    textob = c.beginText()
    textob.setTextOrigin(inch,inch) 
    textob.setFont("Helvetica",14)

    
    lines=[
        
    ]


    for line in lines:
        textob.textLine(line)

    c.drawText(textob)
    c.showPage()
    c.save()
    buf.seek(0)

    return FileResponse(buf, as_attachment=True , filename = 'Recommender_results.pdf')

#################################### Stroke Page ###################################

def stroke(request):
    context = {}
    return render(request , 'website/stroke/stroke.html', context)

def stroke_register(request):
    form = CreateUserForm()

    if request.method== "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, "Account was created for "+user)
            return redirect ('stroke_login')

    context = {'form':form}
    return render(request , 'website/stroke/stroke_register.html', context)

def stroke_login(request):

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username= username, password = password)

        if user != None:
            login(request, user)

            return redirect('stroke_form')
        else:
            messages.error(request,'Username or Password is incorrect ')

    context = {}
    return render(request , 'website/stroke/stroke_login.html', context)

def stroke_logout(request):
    logout(request)
    return redirect ('stroke')

def stroke_form(request):
    context = {}   
    return render(request, 'website/stroke/stroke_form.html', context)

def stroke_result(request):

    if request.method == "POST":
        pid= request.POST.get('PID')
        age= int(request.POST.get('age'))
        gender= int(request.POST.get('gender'))
        
        mrs= int(request.POST.get('mrs'))
        systolic= int(request.POST.get('systolic'))
        distolic= int(request.POST.get('distolic'))
        glucose= int(request.POST.get('glucose'))
        
        smoking= int(request.POST.get('smoking'))
        bmi= int(request.POST.get('bmi'))
        cholestrol= int(request.POST.get('cholestrol'))
        tos= int(request.POST.get('tos'))
        
        inplis = [age,gender, mrs,systolic,distolic,glucose,smoking,bmi,cholestrol,tos]

        #testlis = [54,1,5,180,123,233,1,26,225,3 ]

        arr = np.array(inplis)

        sdf_train= get_shap_explanation_scores_df(arr)
        x = get_risk_level(arr) 
        chart= plot_SHAP_result(inplis)

        Featurelis=[(str(sdf_train['Feature'][0])),(str(sdf_train['Feature'][1])),(str(sdf_train['Feature'][2])) , (str(sdf_train['Feature'][3])), (str(sdf_train['Feature'][4]))]
     
 
        context = {'chart':chart ,
                    'x':x,
                    'pid':pid,
                    'features':Featurelis,
                    'age':age,
                    'gender':gender,
                    'mrs':mrs,
                    'sys': systolic,
                    'dis': distolic,
                    'glucose':glucose,
                    'smoking': smoking,
                    'bmi':bmi,
                    'chol': cholestrol,
                    'tos':tos} 

    return render(request, 'website/stroke/stroke_result.html', context)

def view_pdf(request):

    buf = io.BytesIO()

    c= canvas.Canvas(buf,pagesize= letter , bottomup=0)

    textob = c.beginText()
    textob.setTextOrigin(inch,inch) 
    textob.setFont("Helvetica",14)

    
    lines=[
        
    ]


    for line in lines:
        textob.textLine(line)

    c.drawText(textob)
    c.showPage()
    c.save()
    buf.seek(0)

    return FileResponse(buf, as_attachment=True , filename = 'Recommender_results.pdf')