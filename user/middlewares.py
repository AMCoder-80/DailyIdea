from django.urls import reverse_lazy
from django.shortcuts import redirect

class LoginMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        print(request.get_full_path())
        if request.user.is_authenticated or request.get_full_path() == '/login':
            print('Here')
            return self.get_response(request)
        return redirect('idea:login')
