from django.core.exceptions import PermissionDenied
from django.shortcuts import render
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.utils.decorators import method_decorator
from .decorators import *
from django.views.generic import View, CreateView, FormView
from django.contrib import messages
from .forms import *
import json
from django.core.serializers.json import DjangoJSONEncoder


@method_decorator(logout_message_required, name='dispatch')
class AgreementView(View):
    def get(self, request, *args, **kwargs):
        request.session['agreement'] = False
        return render(request, 'accounts/agreement.html')

    def post(self, request, *args, **kwargs):
        if request.POST.get('agreement1', False) and request.POST.get('agreement2', False):
            request.session['agreement'] = True

            # Check whether Trainer or Trainee register.
            if request.POST.get('signup_t') == 'signup_t':
                return redirect('/accounts/signup_t/')
            else:
                return redirect('/accounts/signup/')

        else:
            messages.info(request, "약관에 모두 동의해주세요.")
            return render(request, 'accounts/agreement.html')


class TrainerRegisterView(CreateView):
    model = User
    template_name = 'accounts/signup_t.html'
    form_class = TrainerRegisterForm

    def get(self, request, *args, **kwargs):
        if not request.session.get('agreement', False):
            raise PermissionDenied
        request.session['agreement'] = False
        return super().get(request, *args, **kwargs)

    def get_success_url(self):
        messages.success(self.request, "회원가입 성공")
        return settings.LOGIN_URL

    def form_valid(self, form):
        self.object = form.save()
        return redirect(self.get_success_url())


class TraineeRegisterView(CreateView):
    model = User
    template_name = 'accounts/signup.html'
    form_class = TraineeRegisterForm

    def get(self, request, *args, **kwargs):
        if not request.session.get('agreement', False):
            raise PermissionDenied
        request.session['agreement'] = False
        return super().get(request, *args, **kwargs)

    def get_success_url(self):
        messages.success(self.request, "회원가입 성공")
        return settings.LOGIN_URL

    def form_valid(self, form):
        self.object = form.save()
        return redirect(self.get_success_url())


@method_decorator(logout_message_required, name='dispatch')
class LoginView(FormView):
    template_name = 'accounts/login.html'
    form_class = LoginForm
    success_url = '/'


    def form_valid(self, form):
        user_id = form.cleaned_data.get('user_id')
        password = form.cleaned_data.get('password')
        user = authenticate(self.request, username=user_id, password=password)

        if user is not None:
            self.request.session['user_id'] = user_id
            login(self.request, user)
            remember_session = self.request.POST.get('remember_session', False)
            if remember_session:
                settings.SESSION_EXPIRE_AT_BROWSER_CLOSE = False

        return super().form_valid(form)


def logout_view(request):
    logout(request)
    return redirect('/')


def mypage(request):
    return render(request, 'accounts/mypage.html')


@method_decorator(logout_message_required, name='dispatch')
class RecoveryIdView(View):
    template_name = 'accounts/recovery_id.html'
    form = RecoveryIdForm

    def get(self, request):
        if request.method == 'GET':
            form = self.recovery_id(None)
            return render(request, self.template_name, {'form': form})


def ajax_find_id_view(request):
    name = request.POST.get('name')
    email = request.POST.get('email')
    result_id = User.objects.get(name=name, email=email)

    return HttpResponse(json.dumps({"result_id": result_id.user_id}, cls=DjangoJSONEncoder),
                        content_type="application/json")


@login_message_required
def password_edit_view(request):
    if request.method == 'POST':
        password_change_form = CustomPasswordChangeForm
        if password_change_form.is_valid():
            user = password_change_form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "비밀번호를 성공적으로 변경하셨습니다.")
            return redirect('accounts:mypage')
    else:
        password_change_form = CustomPasswordChangeForm(request.user)

    return render(request, 'accounts/password_change.html', {'password_change_form': password_change_form})

