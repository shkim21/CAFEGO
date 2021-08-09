from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView
#from django.contrib.auth.models import User #회원가입을 구현하는데 있어 장고가 제공해주는 편리함
from django.urls import reverse
from django.contrib import auth
from django.views import View
from django.contrib.auth import authenticate, login, logout
from .models import * #User
from cafe.models import CafeList
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as django_logout
from . import forms
from django.contrib import messages
from django.db.models import Q
# Create your views here.

##allauth 써서 필요 없나??
@login_required
def logout(request):
    django_logout(request)
    return render(request, "accounts/main.html")

def main(request):
    return render(request, 'accounts/main.html')

@login_required
def home(request):
    return render(request,'accounts/home.html')

def badge_list(request):
    badges=Badge.objects.all()
    ctx={'badges':badges}

    return render(request, 'accounts/badge_list.html', context=ctx)

import simplejson as json
def badge_taken(request):
    user=request.user

    jsonDec=json.decoder.JSONDecoder()
    myList=jsonDec.decode(user.badge_taken)
    badges=Badge.objects.all()
    taken_badges=[]
    for badge in badges:
        if badge.badge_name in myList:
            taken_badges.append(badge)   
    

    ctx={'taken_badges':taken_badges}
    return render(request, 'accounts/badge_taken.html', context=ctx)

def badge_untaken(request):
    user=request.user

    jsonDec=json.decoder.JSONDecoder()
    myList=jsonDec.decode(user.badge_taken)
    badges=Badge.objects.all()
    taken_badges=[]
    for badge in badges:
        if not badge.badge_name in myList:
            taken_badges.append(badge) 

    ctx={'taken_badges':taken_badges}
    return render(request, 'accounts/badge_untaken.html', context=ctx)

def user_cafe_map(request):
    return render(request, 'accounts/user_cafe_map.html')

def user_detail(request):
    return render(request, 'accounts/detail.html')

def rank_detail(request):
    return render(request, 'accounts/rank_detail.html')

def rank_list(request):
    users=User.objects.order_by('-total_visit')
    ctx={
        'users':users
    }
    return render(request, 'accounts/rank_list.html', context=ctx)

@login_required
def enroll_home(request):
    return render(request, "accounts/enroll_home.html")

class EnrollNewCafeListView(ListView):
    model = CafeList
    paginate_by = 10
    template_name = 'accounts/enroll_new_cafe.html'
    context_object_name = 'new_cafe_list'
    print("11111111")

    # def get_context_data(self, **kwargs):
    #     context = super(EnrollNewCafeListView, self).get_context_data(**kwargs)
    #     context['form'] = forms.VisitedCafeForm()
    #     return context

    #등록기능?
    def enroll_new_cafe(request):
        cafe_list = VisitedCafe.objects.all() #user id 넣어서 그 값만 가져와야 함
        print("23232323")
        
        if request.method == 'POST':
            form = forms.VisitedCafeForm(request.POST, request.FILES)

            if form.is_valid():
                print("!!!!!!!!!!!!!!")
                ##저장
                cafe = VisitedCafe()
                # cafe.user = form.cleaned_data['user']
                # cafe.cafe_name = form.cleaned_data['cafename']
                # cafe.visit_count = form.cleaned_data['visit_count']
                # cafe.cafe_id = form.cleaned_data['cafe_id']
                #cafe.visit_check = form.cleaned_data['visit_check']
                cafe.save()
        else:
            form = forms.VisitedCafeForm()
        
        return render(request, 'accounts/enroll_new_cafe.html', {
            'cafe_list': cafe_list,
            'form': form,
        })









def enroll_new_cafe2(request):
    cafe_list = CafeList.objects.all()
    print("cafelist출력", cafe_list)
    #cafe_list = VisitedCafe.objects.all() #user id 넣어서 그 값만 가져와야 함
    #print("222222222")
    #print("request.method", request.method)
    
    if request.method == 'POST':
        form = forms.NewCafeForm(request.POST, request.FILES)
        #print("form", form)
        #print("form.cleaned_data['cafe']", form.cleaned_data['visit_check'])
        print("form is valid??", form.is_valid)
        if form.is_valid():
            print("!!!!!!!!!!!!!!")
            ##저장
            visitcafe = VisitedCafe()
            print("1 visitcafe", visitcafe)
            visitcafe.user = form.cleaned_data['user']#로그인 한 유저 연결!
            visitcafe.cafe = form.cleaned_data['cafe']
            visitcafe.visit_count = form.cleaned_data['visit_count']
            visitcafe.visit_check = form.cleaned_data['visit_check']
            visitcafe.save()
    else:
        print("here")
        form = forms.VisitedCafeForm()
    
    return render(request, 'accounts/enroll_new_cafe.html', {
        'cafe_list': cafe_list, #cafe_list
        'form': form,
    })












class EnrollVisitedCafeListView(ListView):
    model = VisitedCafe
    paginate_by = 5
    template_name = 'accounts/enroll_visited_cafe.html'
    context_object_name = 'visited_cafe_list'

    #검색 기능
    def get_queryset(self):
        search_keyword = self.request.GET.get('q', '')
        search_type = self.request.GET.get('type', '') 
        visited_cafe_list = CafeList.objects.order_by('-id')#나중에 ㄱㄴㄷ 순으로 바꿀?

        if search_keyword:
            if len(search_keyword) > 1:
                if search_type == 'name':
                    search_cafe_list = visited_cafe_list.filter(name__icontains=search_keyword)
                elif search_type == 'address':
                    search_cafe_list = visited_cafe_list.filter(address__icontains=search_keyword)
                elif search_type == 'all':
                    search_cafe_list = visited_cafe_list.filter(Q(name__icontains=search_keyword) | Q(address__icontains=search_keyword))
                return search_cafe_list
        else:
            messages.error(self.request, '2글자 이상 입력해주세요.')
        return visited_cafe_list

    #하단부에 페이징 처리
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = context['paginator']
        page_numbers_range = 5
        max_index = len(paginator.page_range)

        page = self.request.GET.get('page')
        current_page = int(page) if page else 1

        start_index = int((current_page - 1) / page_numbers_range) * page_numbers_range
        end_index = start_index + page_numbers_range
        if end_index >= max_index:
            end_index = max_index

        page_range = paginator.page_range[start_index:end_index]
        context['page_range'] = page_range

        search_keyword = self.request.GET.get('q', '')
        search_type = self.request.GET.get('type', '') 

        if len(search_keyword) > 1:
            context['q'] = search_keyword
        context['type'] = search_type

        return context