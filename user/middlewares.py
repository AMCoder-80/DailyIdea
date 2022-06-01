from django.shortcuts import redirect

class LoginMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        print(request.get_full_path())
        if not request.get_full_path().endswith('com/'):
            print('Here')
            return self.get_response(request)
        return redirect('idea:login')
