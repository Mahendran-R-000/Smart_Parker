import io
from datetime import timedelta

import pandas as pd
import openpyxl
import xlrd
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db.models import F
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect
from django.utils import timezone
from django.core import serializers
from six import StringIO

from .models import *
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.template.loader import render_to_string
from django.utils.encoding import force_str,force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site

from .forms import *
from .tokens import account_activation_token, payment_token
from django.core.mail import send_mail
import qrcode



def index(request):
    return (redirect('login')if not request.user.is_authenticated else redirect('home'))


def signup(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = SignupForm(request.POST)
        print(form.is_valid());
        print(form.errors);
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            print("Form Saved")
            current_site = get_current_site(request)
            mail_subject = 'Activate your account.'
            message = render_to_string('email_template.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })

            to_email = form.cleaned_data.get('email')
            send_mail(mail_subject, message, settings.EMAIL_HOST_USER, [to_email])

            messages.success(request,
                             'An activation link has been sent to your email. Please confirm your email address to complete the registration.')
            return redirect('login')
    else:
        form = SignupForm()

    return render(request, 'signup.html', {'form': form})

def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        b = Booking(customer=user)
        b.save()
        #return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
        #return render(request,'emailverification.html',{'confirm_done': 'Thank you for your email confirmation. Now you can login your account.'})
        messages.success(request,'Thank you for your email confirmation..')
        return redirect('login')
    else:
        return HttpResponse('Activation link is invalid!')

def Login(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method=='POST':
        user=authenticate(request,email=request.POST.get('email'),password=request.POST.get('password'))
        #print(user)
        if user is not None:
            #request.session.set_expiry(600)
            login(request,user)
            return redirect('home')
        messages.error(request,'Invalid Details')
        return redirect('login')
    return render(request,'login.html')

@login_required(login_url='login')
def home(request):

    places=RentRegister.objects.filter(hold=False)
    places= serializers.serialize('json', places)
    try:
        booking_object= Booking.objects.filter(customer=request.user).first()
        data = f'Name: {request.user.first_name} \n Place: {booking_object.booked_place} \n Booking ID: {booking_object.id} \n Slot ID: {booking_object.slot_name} \n Booking Time: \n {booking_object.booked_at} \n Vehicle Number:{booking_object.vehicle} \n Duration: {booking_object.no_of_hours}'
        return render(request, 'home.html', {'places': places, 'data': data})
    except:
        return render(request, 'home.html', {'places': places})
    #struct = json.loads(places)
    #for i in struct:
     #   print(i)
    #data = json.dumps(struct)

    #b=Booking.objects.get(customer=request.user)
    return render(request,'mapdemo.html',{'places':places,'data':data})

    #return render(request, 'home.html')


@login_required(login_url='login')
def rent(request):

    '''
        if RentRegister.objects.filter(user = request.user).exists() :
        return redirect('rent_user_details')
    '''
    name = request.user
    data = UserProfile.objects.get(user=name)
    form = RentImagesform(request.POST or None, request.FILES or None, instance=data)
    files = request.FILES.getlist('images')
    if request.method == 'POST':
        print(form.is_valid())
        #print(form.cleaned_data['address'])
        if form.is_valid():
            user = request.user
            saddress = form.cleaned_data['address']
            splace_name = form.cleaned_data['place_name']
            stotal_transport = form.cleaned_data['total_transport']
            smoney_per_hour = form.cleaned_data['money_per_hour']
            latitude = form.cleaned_data['latitude']
            longitude = form.cleaned_data['longitude']
            # Code for creating getig excel sheet
            read_file = pd.read_excel(request.FILES.get('slots_create'))
            #print(list(read_file['car']))
            obj = SlotsPlace.objects.filter(user=user).first()
            svalue = '1'
            if obj is not None:
             #   print(obj.value)
                svalue = str(int(obj.value) + 1)
             #   print(svalue)

            for slot in list(read_file['car']):
                SlotsPlace.objects.create(user=user, slot_name=slot, place_name=splace_name, value=svalue)
            #print(saddress, stotal_transport, smoney_per_hour)
            obj = RentRegister.objects.create(user=user, place_name=splace_name, address=saddress,
                                              total_transport=stotal_transport, money_per_hour=smoney_per_hour,latitude=latitude,longitude=longitude)
            #print(obj)
            for f in files:
                RentImages.objects.create(rentuser=obj, images=f)
            messages.success(request,'Place added Successfuly')
            return redirect('rent')
    context = {'form': form, 'data': data}
    return render(request, 'rentform.html', context)

def rent_user_details(request):
    name = request.user
    placesUser = RentRegister.objects.filter(user=name)
    booking_value = False
    if request.method == 'POST':
        name_of_place = request.POST.get('places')
        places_id= RentRegister.objects.filter(user=name,place_name=name_of_place).values_list('pk',flat=True)[0]
        print(places_id)
        print(name_of_place)
        booking_value = Booking.objects.filter(booked_place=places_id)
    return render(request, 'rent_place_details.html', {'places': placesUser, 'Booking': booking_value})

@login_required(login_url='login')
def rent_places(request):
    places=RentRegister.objects.filter(user=request.user)
    customers={}
    for place in places:
        booking_object= Booking.objects.filter(booked_place=place.pk)
        print(booking_object)
    return render(request, 'rent_places.html', {'places':places})


@login_required(login_url='login')
def book_now(request,id):
    if request.method=='POST':
        place=RentRegister.objects.get(pk=id)
        print(place.place_name)
        slot_object=SlotsPlace.objects.filter(user=place.user.id,place_name=place.place_name,slot_available=True).first()
        print(slot_object)
        #print(place)
        #print(place.balance_car)
        if place.balance_car !=0:
            total = place.money_per_hour * int(request.POST.get('noofhours'))
            #print(place.occupied_cars)
            #print(place.amount_per_hour * int (request.POST.get('noofhours')))
            #place.save()
            booking_object = Booking.objects.create(customer=request.user)
            booking_object.vehicle=request.POST.get('vehicleno')
            booking_object.no_of_hours = request.POST.get('noofhours')
            booking_object.amount_to_pay = total
            booking_object.slot_name=slot_object.slot_name
            #b = Booking(customer=request.user,no_of_hours=request.POST.get('noofhours'),amount_to_pay=total)
            booking_object.save()
            place.occupied_transport += 1
            slot_object.slot_available=False
            place.save()
            slot_object.save()
            #print(b.pk)
            hash_id_of_place=urlsafe_base64_encode(force_bytes(place.pk))
            hash_id = urlsafe_base64_encode(force_bytes(booking_object.pk))
            token=default_token_generator.make_token(request.user)
            #print(hash_id)
            #print(token)
            #print(b.pk)
            return redirect('payment',hash_id=hash_id,token=token,id_2=hash_id_of_place)
            #b=Booking(customer=request.user)
            print(booking_object)
        messages.error(request,'Booking Failed due to Insuficient Space..')
        return redirect('home')
    v=Vehicle.objects.filter(user=request.user).values('vehicle_no','vehicle_name')
    #print(v['vehicle_no'])
    return render(request,'book_now.html',{'id':id,'vehicle':v})

def payment(request,hash_id,token,id_2):
    try:
        uid = force_str(urlsafe_base64_decode(hash_id))
        place_id = force_str(urlsafe_base64_decode(id_2))
        #print(place_id)
        b=Booking.objects.get(pk=uid)
        user = Myusers.objects.get(pk=request.user.pk)
        #print(token)
    except(TypeError, ValueError, OverflowError) as e:
        #print(e)
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.last_login = timezone.localtime()
        user.save()
        return render(request,'payment.html',{'customer':b,'place':place_id})
    raise Http404('Unauthorized Page')

@login_required(login_url='login')
def verify(request,id,place_id):
    #print(id)
    b=Booking.objects.get(pk=id)
    place = RentRegister.objects.get(pk=place_id)
    money = int(place.money_per_hour) * 0.8
    place.total_money = str(int(money))
    place.save()
    #print(b)
    #print(b.booked)
    b.amount_to_pay=None
#    place.occupied_transport += 1
    #place.save()
    b.booked = True
    b.booked_at=timezone.localtime()
    b.ending_at=b.booked_at+timedelta(hours=b.no_of_hours)
    b.booked_place=place
    b.save()
    #data = f'Name:{request.user.first_name} \n booking time:{b.booked_at} \n vehicle:{b.vehicle} \n booking_time:{b.booked_at} \n total_hours:{b.no_of_hours}'
    #img = qrcode.make(data)
    #img.save(f'media/qrcode/{request.user.first_name}{request.user.last_name}.png')
    #print(img)
    #filename = f'{request.user.first_name}.png'
    #b.qr_code=
    #b.save()
    messages.success(request,'Payment Success')
    return redirect('home')



@login_required(login_url='login')
def vehicle_create_details(request):
 #   b = Booking.objects.filter(customer=request.user).first()
#    data = f'Name: {request.user.first_name} \n Booking Time: \n {b.booked_at} \n Vechicle Number:{b.vehicle} \n Total Duration: {b.no_of_hours}'
    tasks = Vehicle.objects.filter(user=request.user)
    if request.method == 'POST':
        user_vehicle_name=request.POST.get('v_name')
        user_vehicle_no = request.POST.get('v_no')
        Vehicle.objects.create(user=request.user,vehicle_name=user_vehicle_name,vehicle_no=user_vehicle_no)
        messages.success(request,'Added Succesfully')
        return redirect('vehicle_and_booking_details')
    return render(request, 'vehicle_and_booking_details.html', {'tasks': tasks})


@login_required(login_url='login')
def vehicle_delete_details(request,pk):
    data = Vehicle.objects.get(id=pk)
    data.delete()
    messages.success(request,'Deleted Succesfully')
    return redirect('vehicle_and_booking_details')

@login_required(login_url='login')
def edit_profile(request):
    name = request.user
    data = UserProfile.objects.get(user=name)
    form = EditProfileForm(instance=request.user)
    profile_form = ProfileForm(instance=data)
    args = {}
    args['form'] = form
    args['profile_form'] = profile_form
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=data)  # request.FILES is show the selected image or file
        '''
        print(form.is_valid(), profile_form.is_valid())
        print(profile_form.cleaned_data['image'])
        '''
        if form.is_valid() and profile_form.is_valid():

            user_form = form.save()
            custom_form = profile_form.save(False)
            custom_form.user = user_form
            custom_form.save()
            messages.success(request,'Updated Succesfuly')
            return redirect('profile')
        else:
            print("error")
            return redirect('edit_profile')

    return render(request, 'edit_profile.html', args)

@login_required(login_url='login')
def profile(request):
    name = request.user
    data = UserProfile.objects.get(user=name)
    return render(request, 'profile.html', {'data': data})

@login_required(login_url='login')
def report(request):
    name = request.user
    data = UserProfile.objects.get(user=name)
    form = ReportImagesform(request.POST or None, request.FILES or None, instance=data)
    files = request.FILES.getlist('images')
    if request.method == 'POST':
            print(form.is_valid() )
            print(form.cleaned_data['location'])
            if form.is_valid():
                user = request.user
                slocation = form.cleaned_data['location']
                stitle = form.cleaned_data['title']
                stransport_number = form.cleaned_data['transport_number']
                sdescription = form.cleaned_data['description']
                print(slocation, stitle, stransport_number, sdescription)
                data.reward_coins += 10
                data.save()
                obj = Report.objects.create(user=user, location=slocation, title=stitle, transport_number=stransport_number, description=sdescription)
                print(obj)
                for f in files:
                    ReportImages.objects.create(reportuser=obj, images=f)
                messages.success(request,'Succesfully Reported')
                return redirect('report_table')


    context = {'form': form, 'data': data}
    return render(request, 'reporting.html', context)

@login_required(login_url='login')
def edit_slot_details(request):
    user = request.user
    placesUser = RentRegister.objects.filter(user=user)

    new_or_old = placesUser.exists()

    if request.method == 'POST':
        #print("helooooo")
        try:
            read_file = pd.read_excel(request.FILES.get('slots_update'))

            name_of_place = request.POST.get('places')
            #print(name_of_place)
            #print(list(read_file['car']))
            obj = SlotsPlace.objects.filter(user=request.user).first()
            sedited = '1'
            if obj is not None:
                print(obj.edited)
                sedited = str(int(obj.edited) + 1)
                #print(sedited)

                for slot in list(read_file['car']):
                    SlotsPlace.objects.create(user=user,place_name=name_of_place, slot_name=slot, edited=sedited, value=obj.value)
                #messages.success(request,'slots Edited Successfully')
        except Exception as e:
            print(e)
    return render(request, 'slot_details.html', {'places': placesUser, 'new_or_old': new_or_old})


@login_required(login_url='login')
def report_table(request):
    data = Report.objects.filter(user=request.user)
    return render(request, 'reporting_table.html', {'data': data})

def Logout(request):

    logout(request)
    return redirect('/')

