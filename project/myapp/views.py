from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from .models import customer, extended
from django.core.mail import EmailMessage
import jwt

# Create your views here.
def index(request):
    if request.method == 'POST':
        name = request.POST['username']
        psd = request.POST['pass']
        user = authenticate(username=name, password=psd)
        if user is not None:
            login(request, user)
            return redirect('main_page')
        else:
            return render(request, 'mylogin.html', {"msg": "Wrong Credential"})
    if request.user.is_authenticated:
        return redirect('main_page')
    else:
        return render(request, 'mylogin.html')


def signup(request):
    if request.method == 'POST':
        name = request.POST['username']
        em = request.POST['email']
        psd = request.POST['password']
        re_psd = request.POST['re_password']
        if psd == re_psd:
            user = User.objects.create_user(username=name, email=em, password=psd, is_active=False)
            try:
                user.save()
                enc = jwt.encode({'myid': str(user.pk)}, key='secret', algorithm='HS256')
                link = request.scheme + '://' + request.META['HTTP_HOST'] + '/activate/' + str(enc) + '/'
                em = EmailMessage('Info', 'Thankyou for signing up ' + link, 'ahsanhafeez0324@gmail.com', [em])
                em.send()
                return redirect('/')
            except:
                render(request, 'mysignup.html', {'message': 'Unable to sign Up'})
        else:
            render(request, 'mysignup.html', {'message': 'password do not match'})
    return render(request, 'mysignup.html')


def logoutt(request):
    logout(request)
    return redirect('/')


def main(request):
    if request.method == 'POST':
        fname = request.POST['firstname']
        lname = request.POST['lastname']
        em = request.POST['email']
        ag = request.POST['age']
        ph = request.POST['phone']
        adr = request.POST['address']
        f = request.FILES['file']
        cx = customer.objects.create(first_name=fname, last_name=lname, email=em, age=ag, phone=ph, address=adr)
        # if cx is None:
        #     return render(request, 'mainpage.html', {'msg': 'Enter Credentials'})
        try:
            cx.save()
            ex = extended()
            ex.id = cx
            ex.img = f
            ex.save()
            return render(request, 'mainpage.html', {'msg': 'Data submit successfully'})
        except:
            return render(request, 'mainpage.html', {'msg': 'Failed to submit :('})
    if request.user.is_authenticated:
        ob = customer.objects.all()
        d = {"obj": ob}
        return render(request, "mainpage.html", d)
    return render(request, 'mainpage.html')


def delete(request, id):
    obj = customer.objects.get(pk=id)
    obj.delete()
    return redirect('main_page')


def update(request, id):
    if request.method == 'POST':
        myId = request.POST['i']
        obj = customer.objects.get(pk=myId)
        obj.first_name = request.POST['fn']
        obj.last_name = request.POST['ln']
        obj.email = request.POST['e']
        obj.age = request.POST['a']
        obj.phone = request.POST['p']
        obj.address = request.POST['add']
        obj.save()
        return redirect('main_page')
    object = customer.objects.get(pk=id)
    d = {'ob': object, 'id': id}
    return render(request, 'updateform.html', d)


def activate(request, id):
    dec = jwt.decode(id, key='secret', algorithms=['HS256'])
    u = User.objects.get(pk=int(dec['myid']))
    u.is_active = True
    u.save()
    return redirect('main_page')