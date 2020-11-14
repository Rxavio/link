from django.shortcuts import render, redirect, get_object_or_404
from .models import Profile, Relationship
from .forms import UserUpdateForm, ProfileUpdateForm
from django.views.generic import ListView, DetailView, DeleteView, CreateView

from django.contrib.auth.models import User
from django.db.models import Q

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CreateUserForm

from django.shortcuts import render, HttpResponse
from django.views.generic import ListView, FormView, View
from .models import Table, Booking, Contact
from .forms import AvailabilityForm
from profiles.booking_functions.availability import check_availability
from django.urls import reverse, reverse_lazy
from django.contrib.auth.views import PasswordChangeView,PasswordResetDoneView
from .models import Video

from django.contrib.auth.models import Group
from .decorators import unauthenticated_user, allowed_users, admin_only

from django.conf import settings


# Create your views here.

def terms(request):
    context = {}
    return render(request, 'profiles/terms.html',context)

def works(request):
    context = {}
    return render(request, 'profiles/works.html',context)

class indexView(CreateView):
    model = Contact
    template_name = 'profiles/index.html' 
    success_url= reverse_lazy('profiles:message-sent')
    fields = ['subject', 'message']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form) 
    
def MessageSent(request):
   
    return render(request, 'profiles/message_sent.html') 

class home(LoginRequiredMixin, ListView):
    model = Profile
    template_name = 'profiles/home.html' 
    paginate_by = 20

    def get_queryset(self):
        qs = Profile.objects.get_all_profiles(self.request.user).order_by('-created')
       
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #  user = User.objects.get(username__iexact=self.request.user)
        user = User.objects.get(username=self.request.user)
        profile = Profile.objects.get(user=user)
        rel_r = Relationship.objects.all()
        rel_s = Relationship.objects.all()
        rel_receiver = []
        rel_sender = []
        for item in rel_r:
            rel_receiver.append(item.receiver.user)
        for item in rel_s:
            rel_sender.append(item.sender.user)
        context["rel_receiver"] = rel_receiver
        context["rel_sender"] = rel_sender
        context['is_empty'] = False
        if len(self.get_queryset()) == 0:
            context['is_empty'] = True

        return context   
  

# def registerPage(request):
# 	if request.user.is_authenticated:
#             return redirect('profiles:home-view')   
# 	else:
# 		form = CreateUserForm()
# 		if request.method == 'POST':
# 			form = CreateUserForm(request.POST)
# 			if form.is_valid():
# 				form.save()
# 				user = form.cleaned_data.get('username')
# 				messages.success(request, user + ' Your Account created ')

# 				return redirect('profiles:login')
                
# 		context = {'form':form}
# 		return render(request, 'profiles/register.html', context)

# def loginPage(request):
# 	if request.user.is_authenticated:
# 		return redirect('profiles:home-view')
# 	else:
# 		if request.method == 'POST':
# 			username = request.POST.get('username')
# 			password =request.POST.get('password')

# 			user = authenticate(request, username=username, password=password)

# 			if user is not None:
# 				login(request, user)
# 				return redirect('profiles:home-view')
# 			else:
# 				messages.info(request, 'Username and assword Does not Match')

# 		context = {}
# 		return render(request, 'profiles/login.html', context)




@unauthenticated_user
def registerPage(request):

	form = CreateUserForm()
	if request.method == 'POST':
		form = CreateUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			username = form.cleaned_data.get('username')
			# group = Group.objects.get(name='available')
			# user.groups.add(group)
			messages.success(request, 'Account was created for ' + username)

			return redirect('profiles:login')
		

	context = {'form':form}
	return render(request, 'profiles/register.html', context)

@unauthenticated_user
def loginPage(request):

	if request.method == 'POST':
		username = request.POST.get('username')
		password =request.POST.get('password')

		user = authenticate(request, username=username, password=password)

		if user is not None:
			login(request, user)
			return redirect('profiles:home-view')
		else:
			messages.info(request, 'Username and password does not Match')

	context = {}
	return render(request, 'profiles/login.html', context)


def logoutUser(request):
	logout(request)
	return redirect('profiles:login')


# @login_required(login_url='profiles:login')
# def my_profile_view(request):
#     profile = Profile.objects.get(user=request.user)
#     form = ProfileModelForm(request.POST or None, request.FILES or None, instance=profile)
#     confirm = False

#     if request.method == 'POST':
#         if form.is_valid():
#             form.save()
#             messages.success(request, f'Your account has been updated!')
#             confirm = True

#     context = {
#         'profile': profile,
#         'form': form,
#         'confirm': confirm,
#     }
#     return render(request, 'profiles/my_account.html', context)

@login_required(login_url='profiles:login')
def my_profile_view(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profiles:my-profile-view')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'profiles/my_account.html', context)



class AvailableProfileListView(LoginRequiredMixin, ListView):
    model = Profile
    template_name = 'profiles/available-profiles.html'
    paginate_by = 20
  
    def get_queryset(self):
        qs = Profile.objects.get_all_profiles(self.request.user).order_by('-created')
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # user = User.objects.get(username__iexact=self.request.user)
        user = User.objects.get(username=self.request.user)
        profile = Profile.objects.get(user=user)
        rel_r = Relationship.objects.all()
        rel_s = Relationship.objects.all()
        rel_receiver = []
        rel_sender = []
        for item in rel_r:
            rel_receiver.append(item.receiver.user)
        for item in rel_s:
            rel_sender.append(item.sender.user)
        context["rel_receiver"] = rel_receiver
        context["rel_sender"] = rel_sender
        context['is_empty'] = False
        if len(self.get_queryset()) == 0:
            context['is_empty'] = True

        return context    
    
class WaitingProfilesListView(LoginRequiredMixin, ListView):
    model = Profile
    template_name = 'profiles/waiting_profiles.html'

    def get_queryset(self):
        qs = Profile.objects.get_all_profiles(self.request.user)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # user = User.objects.get(username__iexact=self.request.user)
        user = User.objects.get(username=self.request.user)
        profile = Profile.objects.get(user=user)
        rel_r = Relationship.objects.filter(sender=profile)
        rel_s = Relationship.objects.filter(receiver=profile)
        rel_receiver = []
        rel_sender = []
        for item in rel_r:
            rel_receiver.append(item.receiver.user)
        for item in rel_s:
            rel_sender.append(item.sender.user)
        context["rel_receiver"] = rel_receiver
        context["rel_sender"] = rel_sender
        context['is_empty'] = False
        if len(self.get_queryset()) == 0:
            context['is_empty'] = True

        return context
    
class AcceptedProfilesListView(LoginRequiredMixin, ListView):
    model = Profile
    template_name = 'profiles/accepted_profiles.html'
   
    def get_queryset(self):
        qs = Profile.objects.get_all_profiles(self.request.user)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # user = User.objects.get(username__iexact=self.request.user)
        user = User.objects.get(username=self.request.user)
        profile = Profile.objects.get(user=user)
        rel_r = Relationship.objects.filter(sender=profile)
        rel_s = Relationship.objects.filter(receiver=profile)
        rel_receiver = []
        rel_sender = []
        for item in rel_r:
            rel_receiver.append(item.receiver.user)
        for item in rel_s:
            rel_sender.append(item.sender.user)
        context["rel_receiver"] = rel_receiver
        context["rel_sender"] = rel_sender
        context['is_empty'] = False
        if len(self.get_queryset()) == 0:
            context['is_empty'] = True

        return context  
    
class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'profiles/profile_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # user = User.objects.get(username__iexact=self.request.user)
        user = User.objects.get(username=self.request.user)
        profile = Profile.objects.get(user=user)
        rel_r = Relationship.objects.filter(sender=profile)
        rel_s = Relationship.objects.filter(receiver=profile)
        rel_receiver = []
        rel_sender = []
        for item in rel_r:
            rel_receiver.append(item.receiver.user)
        for item in rel_s:
            rel_sender.append(item.sender.user)
        context["rel_receiver"] = rel_receiver
        context["rel_sender"] = rel_sender
        return context   
    
    
    
        
@login_required(login_url='profiles:login')     
def invites_received_view(request):
    profile = Profile.objects.get(user=request.user)
    qs = Relationship.objects.invatations_received(profile)
    results = list(map(lambda x: x.sender, qs))
    is_empty = False
    if len(results) == 0:
        is_empty = True

    context = {
        'qs': results,
        'is_empty': is_empty,
    }
    return render(request, 'profiles/my_invite.html', context)

@login_required(login_url='profiles:login')
def accept_invatation(request):
    if request.method=="POST":
        pk = request.POST.get('profile_pk')
        sender = Profile.objects.get(pk=pk)
        receiver = Profile.objects.get(user=request.user)
        rel = get_object_or_404(Relationship, sender=sender, receiver=receiver)
        
        if rel.status == 'send':
            rel.status = 'accepted'
            rel.save()
            # group = Group.objects.get(name='coupled')
            # rel.user.groups.add(group)
    return redirect('profiles:my-invites-view')

@login_required(login_url='profiles:login')
def reject_invatation(request):
    if request.method=="POST":
        pk = request.POST.get('profile_pk')
        receiver = Profile.objects.get(user=request.user)
        sender = Profile.objects.get(pk=pk)
        rel = get_object_or_404(Relationship, sender=sender, receiver=receiver)
        rel.delete()
    return redirect('profiles:my-invites-view')


@login_required(login_url='profiles:login')  
def send_invatation(request):
    if request.method=='POST':
        pk = request.POST.get('profile_pk')
        user = request.user
        sender = Profile.objects.get(user=user)
        receiver = Profile.objects.get(pk=pk)

        rel = Relationship.objects.create(sender=sender, receiver=receiver, status='send')

        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('profiles:my-profile-view')

@login_required(login_url='profiles:login')
def remove_from_friends(request):
    if request.method=='POST':
        pk = request.POST.get('profile_pk')
        user = request.user
        sender = Profile.objects.get(user=user)
        receiver = Profile.objects.get(pk=pk)

        rel = Relationship.objects.get(
            (Q(sender=sender) & Q(receiver=receiver)) | (Q(sender=receiver) & Q(receiver=sender))
        )
        rel.delete()
        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('profiles:my-profile-view')  
 






@login_required(login_url='profiles:login')
def invite_profiles_list_view(request):
    user = request.user
    qs = Profile.objects.get_all_profiles_to_invite(user)

    context = {'qs': qs}

    return render(request, 'profiles/to_invite_list.html', context)


class BookingListView(LoginRequiredMixin, ListView):
    model = Booking
    template_name = 'profiles/booking_list.html'
    
    def get_queryset (self, *args, **kwargs):
        if self.request.user.is_staff:
            booking_list=Booking.objects.all()
            return booking_list
        
        else:
            booking_list=Booking.objects.filter(user=self.request.user)
            return booking_list

@login_required(login_url='profiles:login')
def TableListView(request):
    table = Table.objects.all()[0]
    table_categories = dict(table.TABLE_CATEGORIES)
    # print('Categories', table_categories)
    table_values = table_categories.values()
    # print('Category', table_values)
    table_list = []

    for table_category in table_categories:
        table = table_categories.get(table_category)
        # print(table)
        table_url = reverse('profiles:TableDetailView', kwargs={
                           'category': table_category})
        # print(table, table_url)
        table_list.append((table, table_url))
        
    context = {
        "table_list": table_list,
    }
    # print(table_list)
    return render(request, 'profiles/table_list.html', context) 



class TableDetailView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        # print(self.request.user)
        category = self.kwargs.get('category', None)
        form = AvailabilityForm()
        table_list = Table.objects.filter(category=category)

        if len(table_list) > 0:
            table = table_list[0]
            table_category = dict(table.TABLE_CATEGORIES).get(table.category, None)
            context = {
                'table_category': table_category,
                'form': form,
            }
            return render(request, 'profiles/table_detail.html', context)
        else:
            return HttpResponse('Category does not exist')

    def post(self, request, *args, **kwargs):
        category = self.kwargs.get('category', None)
        table_list = Table.objects.filter(category=category)
        form = AvailabilityForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data

        available_tables = []
        for table in table_list:
            if check_availability(table, data['check_in'], data['check_out']):
                available_tables.append(table)

        if len(available_tables) > 0:
            table = available_tables[0]
            booking = Booking.objects.create(
                user=self.request.user,
                table=table,
                check_in=data['check_in'],
                check_out=data['check_out']
            )
            booking.save()
            # return HttpResponse(booking)
            return redirect('profiles:BookingListView') 
            
        else:
            # return HttpResponse('All of this category of tables are booked!! Try another one')
            return redirect('profiles:Sorry-view') 
           
        
class CancelBookingView(LoginRequiredMixin, DeleteView):
    model = Booking
    template_name = 'profiles/booking_cancel_view.html'     
    success_url= reverse_lazy('profiles:BookingListView')  
    
def SorryView(request):
   
    return render(request, 'profiles/sorry_view.html')


class ChangePassword(PasswordChangeView):
    template_name = 'profiles/change_password.html'  
    success_url= reverse_lazy('profiles:PasswordResetDoneView') 
    
class PasswordResetDone(PasswordResetDoneView):
    template_name = 'profiles/change_password_done.html'     
        
 
    
                 
        

