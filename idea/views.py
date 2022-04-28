from django.shortcuts import render
from django.urls import reverse_lazy
from django.http import HttpResponse
from . import models
from django.views.decorators.csrf import csrf_exempt
from django.views import generic
import requests

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


@csrf_exempt
def create_idea(request):
    if request.method == 'GET':
        pass
    elif request.method == 'POST':
        print({i: ''.join(j) for i, j in request.POST.items()})
        models.Idea.objects.create(**{i: ''.join(j) for i, j in request.POST.items()})
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
            # if idea.status == 'A':
            #     requests.get(
            #         f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={idea.chat_id}&text={success_message}")
            # elif idea.status == 'R':
            #     requests.get(
            #         f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={idea.chat_id}&text={error_message}")
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
        return context


@csrf_exempt
def change_content(request, content, pk):
    if request.method == 'POST':
        idea = models.Idea.objects.get(pk=pk)
        idea.content = content
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


