from django.shortcuts import render
from django.urls import reverse_lazy
from django.http import HttpResponse
from . import models
from django.db.models.aggregates import Count
from user.models import User
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.views import LoginView
from django.views import generic
import json, requests
from random import choice

# Create your views here.

success_message = """
به به!😍
مژده بدید🎉
ایده شما توسط ادمین تایید شد و در کانال زیر قرار گرفت😊
@DailyIdea
💖هر هفته به بهترین ایده جایزه میدیم🎁
برای گروه ها و مخاطب هاتون بفرستید😉
بلکه ایده تون رو لایک کنند و جایزه بگیرید🏆
"""

error_message = """
سلام دوست عزیز🙋‍
متاسقانه ایده شما توسط ادمین تایید نشد
مبتونید برای مشاهده نمونه ایده های بیشتر به کانال زیر بپیوندید
@DailyIdea
"""

TOKEN = "5178760524:AAHwUq8bPzxmkDmO0dXaUqbyAhKC9Fev1pM"


def get_user(idea):
    adj = ['ایده پرداز', 'خلاق', 'آفرینشگر', 'مبتکر', 'دانا', 'اندیشمند', 'خوش فکر', 'مدبر', 'مبدع', 'نیک اندیش',
           'هنرمند', 'آرتیست', 'خبره', 'اندیشگر', 'آنده نگر', 'آفریننده']
    if idea.user != 'None':
        text = f'💡{choice(adj)}: '
        return text + f"{idea.user}"
    return ''


@csrf_exempt
def create_idea(request):
    if request.method == 'GET':
        pass
    elif request.method == 'POST':
        try:
            user_id = request.POST.get('chat_id')
            idea = models.Idea(content=request.POST['content'], status=request.POST['status'],
                               chat_id=user_id)

            user, created = User.objects.get_or_create(chat_id=user_id)
            user.name = request.POST.get('name')
            idea.user = user
            idea.save()
        except Exception as e:
            return HttpResponse(e)
        return HttpResponse("OK")


def index(request):
    ideas = models.Idea.objects.all()
    print(request.resolver_match)
    return render(request, 'adminPanel/index.html', {'ideas': ideas, 'res': request.resolver_match})


def idea(request, status=None):
    print(status)
    if status:
        ideas = models.Idea.objects.filter(status=status)
    else:
        ideas = models.Idea.objects.all()
    status_ref = status if status else 'null'
    print(request.resolver_match)
    return render(request, 'adminPanel/table.html',
                  {'ideas': ideas, 'status_ref': status_ref, 'res': request.resolver_match})


@csrf_exempt
def change_status(request, state, pk):
    idea = models.Idea.objects.get(pk=pk)
    if request.method == 'POST':
        if idea.status == 'P':
            idea.status = state
            idea.save()
            if idea.status == 'A':
                markup = json.dumps({"inline_keyboard": [[
                    {"text": "من اولین مشتریش هستم",
                     "callback_data": "buyer"},
                    {"text": "من ایده بهتری دارم",
                     "callback_data": "improve"}
                ],
                    [
                        {"text": "من مشتریش رو دارم",
                         "callback_data": "customer"},
                        {"text": "من سرمایه گذاری میکنم",
                         "callback_data": "invest"},
                    ]]})
                data = {
                    "chat_id": "@IdeaDaily",
                    "text": f"{idea.content}\n\n{get_user(idea)}\n\n@IdeaDaily|[هر روز یک ایده بده](https://t.me/IdeaDailybot/start)",
                    "reply_markup": markup,
                    "parse_mode": "Markdown"
                }
                data2 = {
                    "chat_id": idea.chat_id,
                    "text": success_message,
                }
                requests.get(
                    f"https://api.telegram.org/bot{TOKEN}/sendMessage", data=data
                )
                requests.get(
                    f"https://api.telegram.org/bot{TOKEN}/sendMessage", data=data2
                )
            elif idea.status == 'R':
                data = {
                    "chat_id": idea.chat_id,
                    "text": error_message,
                }
                requests.get(
                    f"https://api.telegram.org/bot{TOKEN}/sendMessage", data=data)
            return HttpResponse(idea.get_status())
        return HttpResponse('Failed')
    else:
        return HttpResponse("Method not allowed")


@csrf_exempt
def change_cat(request, id, pk):
    idea = models.Idea.objects.get(pk=pk)
    category = models.Category.objects.get(id=id)
    if request.method == 'POST':
        idea.category_id = category.id
        idea.save()
        return HttpResponse("OK")
    else:
        return HttpResponse("Method not allowed")


class IdeaDetail(generic.DetailView):
    model = models.Idea
    # fields = ['content', 'category', 'status']
    template_name = 'adminPanel/detail.html'

    def get_context_data(self, **kwargs):
        context = super(IdeaDetail, self).get_context_data(**kwargs)
        context['cats'] = models.Category.objects.all()
        context['investors'] = models.Requester.objects.filter(idea__pk=self.kwargs['pk'], type='I')
        context['customers'] = models.Requester.objects.filter(idea__pk=self.kwargs['pk'], type='C')
        context['buyers'] = models.Requester.objects.filter(idea__pk=self.kwargs['pk'], type='B')
        return context


@csrf_exempt
def change_content(request, content, user, pk):
    if request.method == 'POST':
        idea = models.Idea.objects.get(pk=pk)
        user = models.User.objects.get(chat_id=idea.chat_id)
        idea.content = content
        user.name = user
        idea.save()
        return HttpResponse("OK")
    else:
        return HttpResponse("Failed")


class CategoryList(generic.ListView):
    model = models.Category
    template_name = 'adminPanel/cat_table.html'
    context_object_name = 'cats'


class CreateCategory(generic.CreateView):
    model = models.Category
    fields = ['name']
    success_url = reverse_lazy('idea:cat_views')
    template_name = 'adminPanel/create_cat.html'
    context_object_name = 'cat'


def get_idea(request, pk):
    try:
        idea = models.Idea.objects.get(id=pk)
        return HttpResponse(f"{idea.user}-{idea.content}-{idea.chat_id}")
    except Exception as e:
        return HttpResponse(e)


@csrf_exempt
def save_req(request):
    try:
        idea = models.Idea.objects.get(content__icontains=request.POST['content'])
        req = models.Requester.objects.create(user=request.POST['user'], phone_number=request.POST['phone'],
                                              type=request.POST['type'])
        idea.requester.add(req)
    except Exception as e:
        return HttpResponse(e)
    return HttpResponse("OK")


class LoginUser(LoginView):
    template_name = 'adminPanel/login.html'
    redirect_authenticated_user = reverse_lazy('idea:test')


def user_table(request, filter=None):
    users = User.objects.all().annotate(idea_count=Count('ideas'))
    if filter == 'recent':
        users = users.order_by('-id')
    elif filter == 'active':
        users = users.order_by('-idea_count')
    return render(request, 'adminPanel/user_table.html', {'users': users})
