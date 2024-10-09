from django.shortcuts import render
from django.shortcuts import redirect
#from django.views.generic import TemplateView
from django.views.generic import TemplateView, CreateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
#from .forms import SignUpForm
from django.urls import reverse_lazy
from .forms import SignUpForm, UserForm, ProfileForm
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.core.mail import send_mail, send_mass_mail
from django.conf import settings
from bdmapp.doner_profile.models import Profile
from django.db.models import Q
#from .models import Profile

class HomeView(TemplateView):
    template_name = 'common/home.html' 

class AboutView(LoginRequiredMixin, TemplateView):
    template_name = 'common/about.html'
    login_url = reverse_lazy('home')

class ContactView(CreateView):
    form_class = SignUpForm
    template_name = 'common/contact.html'
    success_url = reverse_lazy('home')

    def contact(request):
        post = Profile.objects.all()
        search = request.GET.get('q')
        if search:
            post = post.filter(
                Q(Blood_Group__icontains=search)
            )
           # return render(request, 'common/don_req.html',{'post':post})




def get_context_data(self, **kwargs):
     # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        print(self.request.user.id)
        context['book_list'] = self.request.user
        return context


class SignUpView(CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('login')
    template_name = 'common/register.html' 

class PasswordChangeView(CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('home')
    template_name = 'common/change-password.html' 


class ResetPasswordView(CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('home')
    template_name = 'common/change-password.html' 

    
class DonationView(LoginRequiredMixin, ListView):
    #profile_form = ProfileForm
    template_name = 'common/don_req.html'
    #login_url = reverse_lazy('home')

    def get_queryset(self):
        return Profile.objects.all()  


    def donation(request):
        post = Profile.objects.all()
        search = request.GET.get('q')
        if search:
            post = post.filter(
                Q(Blood_Group__icontains=search)
            )
            return render(request, 'common/don_req.html',{'post':post})
        
        
       

class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'common/profile.html'

class ProfileUpdateView(LoginRequiredMixin, TemplateView):
    user_form = UserForm
    profile_form = ProfileForm
    template_name = 'common/profile-update.html'

    def post(self, request):

        post_data = request.POST or None
        file_data = request.FILES or None

        user_form = UserForm(post_data, instance=request.user)
        profile_form = ProfileForm(post_data, file_data, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.error(request, "Your profile is updated successfully!")
            return HttpResponseRedirect(reverse_lazy('profile'))

        context = self.get_context_data(
                                        user_form=user_form,
                                        profile_form=profile_form
                                    )

        return self.render_to_response(context)     

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class ExcelPageView(TemplateView):
    template_name = "common/excel_home.html"


    # excel_app/views.py

import xlwt
from django.http import HttpResponse
from django.contrib.auth.models import User
from bdmapp.doner_profile.models import Profile

def export_users_xls(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="profiles.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Profiles Data') # this will make a sheet named Users Data

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Username', 'Blood Group', 'Gender', 'Age', 'Profession', ' Home District', 'Present Address', 'Contact Number', 'Email Address', ]

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style) # at 0 row 0 column 

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    rows = Profile.objects.all().values_list('Full_Name', 'Blood_Group', 'Gender','Age','Profession','Home_District', 'Present_Address', 'Phone_Number', 'Email',)
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)

    return response

# excel_app/views.py
import xlwt
from django.http import HttpResponse

def export_styling_xls(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="profiles.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Styling Data') # this will make a sheet named Users Data - First Sheet
    styles = dict(
        bold = 'font: bold 1',
        italic = 'font: italic 1',
        # Wrap text in the cell
        wrap_bold = 'font: bold 1; align: wrap 1;',
        # White text on a blue background
        reversed = 'pattern: pattern solid, fore_color blue; font: color white;',
        # Light orange checkered background
        light_orange_bg = 'pattern: pattern fine_dots, fore_color white, back_color orange;',
        # Heavy borders
        bordered = 'border: top thick, right thick, bottom thick, left thick;',
        # 16 pt red text
        big_red = 'font: height 320, color red;',
    )

    for idx, k in enumerate(sorted(styles)):
        style = xlwt.easyxf(styles[k])
        ws.write(idx, 0, k)
        ws.write(idx, 1, styles[k], style)

    wb.save(response)

    return response

    # excel_app/views.py

from xlutils.copy import copy # http://pypi.python.org/pypi/xlutils
from xlrd import open_workbook # http://pypi.python.org/pypi/xlrd
import xlwt
from django.http import HttpResponse
from datetime import datetime
import os

def export_write_xls(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="profiles.xls"'

    # EG: path = excel_app/sample.xls
    path = os.path.dirname(__file__)
    file = os.path.join(path, 'sample.xls')

    rb = open_workbook(file, formatting_info=True)
    r_sheet = rb.sheet_by_index(0)

    wb = copy(rb)
    ws = wb.get_sheet(0)

    #font_style = xlwt.XFStyle()
    #font_style.font.bold = True

    style=xlwt.XFStyle()
    style.num_format_str = "D-MMMM-YY"
   # style.font = font_style

    ws.write(3,5,datetime.now(),style)

    row_num = 2 # index start from 0
    rows = Profile.objects.all().values_list('Full_Name', 'Blood_Group', 'Gender','Age','Profession', 'Last_Donation_Date','Home_District', 'Present_Address', 'Phone_Number', 'Email',)
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num])
    
    # wb.save(file) # will replace original file
    # wb.save(file + '.out' + os.path.splitext(file)[-1]) # will save file where the excel file is
    wb.save(response)
    return response