from django.shortcuts import render

# Create your views here.
from .models import pgmodel
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import SignupForm, LoginForm, pgform
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.http import JsonResponse
from django.contrib import messages
from django.db.models import Q

from django.contrib.auth import get_user_model
User = get_user_model()


def index(request):
    return render(request,'index.html')

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            message = render_to_string('acc_active_email.html', {
                'user':user,
                'domain':current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'token': account_activation_token.make_token(user),
            })
            mail_subject = 'Activate your blog account.'
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(mail_subject, 
                                 message,
                                  to=[to_email])
            email.send()
            return HttpResponse('Please confirm your email address to complete the registration')

    else:
        form = SignupForm()

    return render(request, 'register.html', {'form': form})

def activate(request, uidb64, token, backend='django.contrib.auth.backends.ModelBackend'):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user =User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user, backend='django.contrib.auth.backends.ModelBackend' )
        return redirect('/login/')
        #return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
       
    else:
        return HttpResponse('Activation link is invalid!')
    
    
def loginview(request):
    	
            if request.method == 'POST':
                login_form = LoginForm(request.POST)
                if login_form.is_valid():

                    email= login_form.cleaned_data['email']
                    password = login_form.cleaned_data['password']

                    user = authenticate(email=email, password=password)
                                    
                    if user is not None:
                        if user.is_active:
                            login(request, user)	
                            return redirect('/pglist/')
                        else:
                            return HttpResponse('Your account is not active')
                    else:
                        return HttpResponse('The Account does not exists')
                else:
                    login_form = LoginForm()
                    return render(request, "login.html",{"form":login_form})
            else:
                login_form = LoginForm()
            return render(request, "login.html",{"form":login_form})
        
        
def payingview(request):
    if request.method=='POST':
        form=pgform(request.POST)
        if form.is_valid():
            
            mobile=form.cleaned_data['mobile']
            city=form.cleaned_data['city']
            location=form.cleaned_data['location']
            available=form.cleaned_data['available']
            occupancy=form.cleaned_data['occupancy']
            balcony=form.cleaned_data['balcony']
            parking=form.cleaned_data['parking']
            food=form.cleaned_data['food']
            amount=form.cleaned_data['amount']
            details=form.cleaned_data['details']
            user_id_id=request.user.id
            
            
            form_object=pgmodel( mobile=mobile, city=city, location=location, available=available, occupancy=occupancy,balcony=balcony, parking=parking,food=food, amount=amount, details=details , user_id_id=user_id_id)
            form_object.save()
        return redirect('/pglist/')
    else:
        form=pgform()       
    return render(request,'pg.html', {'form':form})


def pglistview(request):
    pg_object=pgmodel.objects.all()
    return render(request,'pglist.html',{'pgobject':pg_object})


def pgview(request, id):
    pgobject=pgmodel.objects.get(id=id)
   
    return render(request, 'pgview.html', {'pg':pgobject})



def sample_ajax_view(request, val):  
    blog = pgmodel.objects.filter(id=val).values()
    
    data = list(blog)
   
    return JsonResponse(data,safe=False)




def searchtwo(request):
    
        if request.method=='POST':
            srch=request.POST['srh']
            if srch:
                match=pgmodel.objects.filter(Q(city__icontains=srch) |
                                            Q(location__icontains=srch))
                if match:
                    return render(request, 'pglist.html', {'sr':match})
                else:
                    messages.error(request, 'no result found')
            else:
                return HttpResponseRedirect('/pglist/')
        
        return render(request, 'pglist.html')
    





def editview(request, editid):
    if request.method=='POST':
        
        myform=pgform(request.POST)
        if myform.is_valid():
            myforms=pgmodel.objects.get(id=editid)
           
            myforms.mobile=myform.cleaned_data['mobile']
            myforms.city=myform.cleaned_data['city']
            myforms.location=myform.cleaned_data['location']
            myforms.balcony=myform.cleaned_data['balcony']
            myforms.available=myform.cleaned_data['available']
            myforms.occupancy=myform.cleaned_data['occupancy']
            myforms.parking=myform.cleaned_data['parking']
            myforms.food=myform.cleaned_data['food']
            myforms.details=myform.cleaned_data['details']
            myforms.amount=myform.cleaned_data['amount']
            myforms.save()
           
        
        return redirect('/pgview/'+str(editid) +'/')
        
   
    else:
        myforms=pgmodel.objects.get(id=editid)
        updation=pgform(initial={ 'mobile':myforms.mobile,'city':myforms.city,'location':myforms.location, 'available':myforms.available,'occupancy':myforms.occupancy,'balcony':myforms.balcony, 'parking':myforms.parking,'food':myforms.food,'details':myforms.details,'amount':myforms.amount})
    return render(request, 'edit.html', {'updation':updation, 'id':editid })


def deleteview(request, id):
    de=pgmodel.objects.get(id=id)
    de.delete()
    return redirect('/pgview/'+str(id) +'/')

def logoutview(request):
    logout(request)
    return redirect('/login/')

        

