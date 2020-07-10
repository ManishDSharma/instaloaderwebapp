from django.shortcuts import render
from django.http import HttpResponse
import csv
import instaloader
from datetime import datetime
import os
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required
def home(request):
    if request.method == 'POST':
        login_data = request.POST.dict()
        username = login_data.get("username")
        password = login_data.get("password")
        story= login_data.get("story")
        ids= login_data.get("id")
        dp= request.POST.get("dpdn",False)
        ip=request.POST.get("up",False)
        name = []
        n=[]
        for root,dirs ,files in os.walk("C:/"):
            if ip in files:
                a=(root + '\\' + ip )   
                n.append(a)
        with open(n[0], newline='') as f:
            reader = csv.reader(f)
            data = list(reader)           
            for sublist in data:
                for item in sublist:
                    name.append(item)
        if(dp=="STORIES"):
            for i in name:
                L=instaloader.Instaloader(download_comments=False,compress_json=False,save_metadata=False,
                dirname_pattern="C:/"+username+" "+str(datetime.now().date())+" "+story+" "+ids+"/"+i)
                L.login(username,password)
                profile = L.check_profile_id(i)
                L.download_stories(userids=[profile])
        elif(dp=="IGTV"):
            for i in name:
                L=instaloader.Instaloader(download_comments=False,compress_json=False,save_metadata=False,
                dirname_pattern="C:/"+username+" "+str(datetime.now().date())+" "+story+" "+ids+"/"+i)
                L.login(username,password)
                profile = instaloader.Profile.from_username(L.context,i)
                L.download_igtv(profile, fast_update=False, post_filter=None)
        elif(dp=="PROFILES"):
            for i in name:
                L=instaloader.Instaloader(download_comments=False,compress_json=False,save_metadata=False,
                dirname_pattern="C:/"+username+" "+str(datetime.now().date())+" "+story+" "+ids+"/"+i)
                L.login(username,password)
                profile = instaloader.Profile.from_username(L.context,i)
                L.download_profiles(set([profile]), profile_pic=True, posts=True, tagged=False, igtv=False, highlights=False, stories=False,fast_update=False, post_filter=None, storyitem_filter=None, raise_errors=False)
           
        return render(request,'home.html')
    else:
        return render(request,'home.html')

class SignUpView(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('home')


