from django.urls import path
from .views import ( 
    home,
    terms,
    works,
    indexView,
    SorryView,
    MessageSent,
    # ContactView,
    my_profile_view, 
    AvailableProfileListView,
    invites_received_view, 
        
    send_invatation,
    remove_from_friends,
    accept_invatation,
    reject_invatation,
    
    WaitingProfilesListView,
    AcceptedProfilesListView,
    ChangePassword,
    PasswordResetDone,
 
    
    ProfileDetailView,

)
from django.conf.urls import include, url
from . import views
from .views import TableListView, BookingListView, TableDetailView, CancelBookingView

app_name = 'profiles'

urlpatterns = [
    path('terms-conditions/', terms, name='terms-conditions'),
    path('how-it-works/', works, name='how-it-works'),
    path('', indexView.as_view(), name='index-view'),
    path('sorry/', SorryView, name='Sorry-view'),
    path('message-sent/', MessageSent, name='message-sent'),
    path('home/', home.as_view(), name='home-view'),
    path('register/', views.registerPage, name="register"),
	path('login/', views.loginPage, name="login"),  
	path('logout/', views.logoutUser, name="logout"),
    path('change-password/', ChangePassword.as_view(), name='ChangePasswordView'),
    path('change-password/done/', PasswordResetDone.as_view(), name='PasswordResetDoneView'),
 
    path('my-profile/', my_profile_view, name='my-profile-view'),
    path('available-profiles/', AvailableProfileListView.as_view(), name='all-available-view'),
    path('waiting-profiles/', WaitingProfilesListView.as_view(), name='all-waiting-view'),
    path('accepted-profiles/', AcceptedProfilesListView.as_view(), name='all-accepted-view'),
    path('my-invites/', invites_received_view, name='my-invites-view'),
    path('send-invite/', send_invatation, name='send-invite'),
    path('remove-friend/', remove_from_friends, name='remove-friend'),
    path('my-invites/acctept/', accept_invatation, name='accept-invite'),
    path('my-invites/reject/', reject_invatation, name='reject-invite'),
    
    path('table-list/', TableListView, name='TableListView'),
    path('booking-list/', BookingListView.as_view(), name='BookingListView'),
    path('booking/cancel/<pk>', CancelBookingView.as_view(), name='CancelBookingView'),
    
    # path('contact/', ContactView, name='contact'),
    # path('contact/', ContactView.as_view(), name='contact'),
    
    
    
    path('table/<category>', TableDetailView.as_view(), name='TableDetailView'),
    path('<slug>/', ProfileDetailView.as_view(), name='profile-detail-view'),
 
]
