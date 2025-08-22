from django.shortcuts import render

# Create your views here.
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from rest_framework import permissions, views, response, status
from .serializers import SignupSerializer
from .forms import SignupForm, LoginForm

# API: signup
class SignupAPI(views.APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return response.Response({"message": "User created"}, status=status.HTTP_201_CREATED)

# HTML: signup
def signup_page(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.cleaned_data.pop('password')  # we’ll set via set_password below
            user = form.save(commit=False)
            user.set_password(request.POST['password'])
            user.save()
            return redirect('accounts:login')
    else:
        form = SignupForm()
    return render(request, 'accounts/signup.html', {'form': form})

# HTML: login
def login_page(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)  # Django session login
            return redirect('products:list')
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})

@login_required
def logout_page(request):
    logout(request)
    return redirect('accounts:login')
