from django.urls import path
from . import views
urlpatterns=[
    path('',views.index,name='index'),
    path('signup/',views.signup,name='signup'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('login/',views.Login,name='login'),
    path('logout/',views.Logout,name='logout'),
    path('home',views.home,name='home'),
    path('home/rent', views.rent, name='rent'),
    path('home/profile/', views.profile, name='profile'),
    path('home/profile/edit', views.edit_profile, name='edit_profile'),
    path('home/report/', views.report, name='report'),
    path('home/report_and_reward_table/', views.report_table, name='report_table'),

    #added 26/02/2024
   # path('bookingdetails/<int:id>',views.booking_places_details,name='booking_details'),

    #path('home/rent_places', views.rent_places, name='rent_places'),
path('home/rent_user_details/', views.rent_user_details, name='rent_user_details'),
    path('home/vehicle_and_booking_details',views.vehicle_create_details,name='vehicle_and_booking_details'),
path('home/slot_details',views.edit_slot_details,name='edit_slot_details'),
    path('home/delete/<int:pk>',views.vehicle_delete_details,name='vehicle_delete_details'),
    path('home/book_now/<int:id>',views.book_now,name='book_now'),
    path('payment/<hash_id>/<token>/<id_2>',views.payment,name='payment'),
    path('verify/<int:id>/<int:place_id>',views.verify,name='verify'),
]

'''    path('signup/',views.signup,name='signup'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('login/',views.Login,name='login'),
    path('logout/',views.Logout,name='logout'),
    path('home',views.home,name='home'),
    path('home/rent', views.rent, name='rent'),
    #path(r'^home/book_now/(?P<id>\d+)/$',views.book_now,name='book_now'),
    path('home/book_now/<int:id>',views.book_now,name='book_now'),
    path('payment/<hash_id>/<token>/<id_2>',views.payment,name='payment'),
    path('verify/<int:id>/<int:place_id>',views.verify,name='verify'),
    path('home/profile',views.profile,name='profile'),
    path('home/report',views.report,name='report'),
    path('home/booking_details',views.booking_details,name='booking_details'),
    path('bookingdetails/<int:id>',views.booking_places_details,name='booking_details'),'''
