from django.core.exceptions import PermissionDenied, ValidationError
from django.shortcuts import render
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.utils.decorators import method_decorator
from .decorators import *
from django.views.generic import View, CreateView, FormView
from django.contrib import messages
from .forms import *
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.urls import reverse
from .helper import send_mail, email_auth_num
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.contrib.auth.tokens import default_token_generator


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
        self.request.session['register_auth'] = True
        messages.success(self.request, "입력된 Email 주소로 인증 메일이 발송되었습니다.")
        return reverse('accounts:register_success')

    def form_valid(self, form):
        self.object = form.save()

        send_mail(
            '{}님의 회원가입 인증메일 입니다.'.format(self.object.user_id),
            [self.object.email],
            html=render_to_string('accounts/register_email.html', {
                'user': self.object,
                'uid': urlsafe_base64_encode(force_bytes(self.object.pk)).encode().decode(),
                'domain': self.request.META['HTTP_HOST'],
                'token': default_token_generator.make_token(self.object),
            })
        )
        return redirect(self.get_success_url())


class TraineeRegisterView(TrainerRegisterView):
    model = User
    template_name = 'accounts/signup.html'
    form_class = TraineeRegisterForm


def register_success(request):
    if not request.session.get('register_auth', False):
        raise PermissionDenied
    request.session['register_auth'] = False

    return render(request, 'accounts/register_success.html')


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


@login_message_required
def profile_view(request):
    if request.method == 'GET':
        return render(request, 'accounts/profile.html')


@login_message_required
def profile_update_view(request):
    if request.method == 'POST':
        user_change_form = TrainerChangeForm(request.POST, instance=request.user)

        if user_change_form.is_valid():
            user_change_form.save()
            messages.success(request, '회원정보가 수정되었습니다.')
            return render(request, 'user/profile.html')

    else:
        user_change_form = TrainerChangeForm(instance=request.user)

        return render(request, 'accounts/profile_update.html', {'user_change_form': user_change_form})


@login_message_required
def profile_update_view(request):
    if request.method == 'POST':
        user_change_form = TraineeChangeForm(request.POST, instance=request.user)

        if user_change_form.is_valid():
            user_change_form.save()
            messages.success(request, '회원정보가 수정되었습니다.')
            return render(request, 'accounts/profile.html')

    else:
        user_change_form = TraineeChangeForm(instance=request.user)

        return render(request, 'accounts/profile_update.html', {'user_change_form': user_change_form})


@login_message_required
def profile_delete_view(request):
    if request.method == 'POST':
        password_form = CheckPasswordForm(request.user, request.POST)

        if password_form.is_valid():
            request.user.delete()
            logout(request)
            messages.success(request, "회원탈퇴가 완료되었습니다.")
            return redirect('/accounts/login/')

    else:
        password_form = CheckPasswordForm(request.user)

    return render(request, 'accounts/profile_delete.html', {'password_form': password_form})


def activate(request, uid64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uid64))
        current_user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist, ValidationError):
        messages.error(request, '메일 인증에 실패했습니다.')
        return redirect('accounts:login')

    if default_token_generator.check_token(current_user, token):
        current_user.is_active = True
        current_user.save()

        messages.info(request, '메일 인증이 완료되었습니다. 회원가입을 축하드립니다!')
        return redirect('accounts:login')

    messages.error(request, '메일 인증에 실패했습니다.')
    return redirect('accounts:login')


@method_decorator(logout_message_required, name='dispatch')
class RecoveryPwView(View):
    template_name = 'accounts/recovery_pw.html'
    recovery_pw = RecoveryPwForm

    def get(self, request):
        if request.method == 'GET':
            form = self.recovery_pw(None)
            return render(request, self.template_name, {'form': form, })


def ajax_find_pw_view(request):
    user_id = request.POST.get('user_id')
    name = request.POST.get('name')
    email = request.POST.get('email')
    target_user = User.objects.get(user_id=user_id, name=name, email=email)

    if target_user:
        auth_num = email_auth_num()
        target_user.auth = auth_num
        target_user.save()

        send_mail(
            '비밀번호 찾기 인증메일입니다.',
            [email],
            html=render_to_string('accounts/recovery_email.html', {
                'auth_num': auth_num,
            })
        )
    return HttpResponse(json.dumps({ "result": target_user.user_id }, cls=DjangoJSONEncoder), content_type="application/json")


def auth_confirm_view(request):
    user_id = request.POST.get('user_id')
    input_auth_num = request.POST.get('input_auth_num')
    target_user = User.objects.get(user_id=user_id, auth=input_auth_num)
    target_user.auth = ""
    target_user.save()
    request.session['auth'] = target_user.user_id

    return HttpResponse(json.dumps({"result": target_user.user_id}, cls=DjangoJSONEncoder), content_type = "application/json")


@logout_message_required
def auth_pw_reset_view(request):
    if request.method == 'GET':
        if not request.session.get('auth', False):
            raise PermissionDenied

    if request.method == 'POST':
        session_user = request.session['auth']
        current_user = User.objects.get(user_id=session_user)
        login(request, current_user)

        reset_password_form = CustomSetPasswordForm(request.user, request.POST)

        if reset_password_form.is_valid():
            user = reset_password_form.save()
            messages.success(request, "비밀번호 변경완료! 변경된 비밀번호로 로그인하세요.")
            logout(request)
            return redirect('accounts:login')
        else:
            logout(request)
            request.session['auth'] = session_user

    else:
        reset_password_form = CustomSetPasswordForm(request.user)

    return render(request, 'accounts/password_reset.html', {'form': reset_password_form})