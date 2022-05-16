from django.shortcuts import redirect

class LoginMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        print(request.get_full_path())
        if request.user.is_authenticated or '/login' in request.get_full_path() or '/create' in request.get_full_path():
            print('Here')
            return self.get_response(request)
        return redirect('idea:login')
