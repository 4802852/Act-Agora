from django.contrib import messages
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404

from .forms import TrainerNewForm
from .models import Genre, Hashtag, Trainer, Lecture, LectureInstance, get_file_path
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator

from accounts.decorators import login_message_required
from accounts.models import User
from review.models import Review

import os
from PTin import settings


def index(request):
    """View function for homepage of site."""
    num_trainers = Trainer.objects.all().count()
    num_instances = LectureInstance.objects.all().count()

    num_instances_available = LectureInstance.objects.filter(status__exact='a').count()

    context = {
        'num_trainers': num_trainers,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
    }

    return render(request, 'index.html', context=context)


def aboutus(request):
    return render(request, 'aboutus.html', {})


class TrainerListView(generic.ListView):
    model = Trainer
    paginate_by = 10
    template_name = 'trainer/trainer_list.html'
    context_object_name = 'trainer_list'

    def get_queryset(self):
        trainer_list = Trainer.objects.order_by('-id')
        return trainer_list

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

        return context


def trainer_detail_view(request, pk):
    trainer = get_object_or_404(Trainer, pk=pk)
    request.session['trainer_id'] = trainer.writer_id
    request.session['trainer_name'] = trainer.name

    # 접속자가 작성자와 일치하는지 확인
    if request.user == trainer.writer:
        trainer_auth = True
    else:
        trainer_auth = False

    context = {
        'trainer': trainer,
        'trainer_auth': trainer_auth,
    }

    trainer_review = Review.objects.filter(trainer=trainer)
    if len(trainer_review) > 5:
        context['is_paginated'] = True
    paginator = Paginator(trainer_review, 5)
    page_numbers_range = 5
    max_index = len(paginator.page_range)

    page = request.GET.get('page')
    current_page = int(page) if page else 1

    start_index = int((current_page - 1) / page_numbers_range) * page_numbers_range
    end_index = start_index + page_numbers_range
    if end_index >= max_index:
        end_index = max_index

    page_range = paginator.page_range[start_index:end_index]
    page_obj = paginator.get_page(page)
    context['page_range'] = page_range
    context['page_obj'] = page_obj
    return render(request, 'trainer/trainer_detail.html', context)


class LectureListView(generic.ListView):
    model = Lecture
    paginate_by = 10
    template_name = 'trainer/lecture_list.html'
    context_object_name = 'lecture_list'

    def get_queryset(self):
        lecture_list = Lecture.objects.order_by('-id')
        return lecture_list

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

        return context


class LectureDetailView(generic.DetailView):
    model = Lecture


class LecturesByUserListView(LoginRequiredMixin, generic.ListView):
    """Generic class-based view listing lectures which is occupied by current user."""
    model = LectureInstance
    template_name = 'trainer/lecture_list_by_user.html'
    paginate_by = 10

    def get_queryset(self):
        return LectureInstance.objects.filter(trainee=self.request.user)


class LecturesByTrainerListView(LoginRequiredMixin, generic.ListView):
    model = Lecture
    template_name = 'trainer/lecture_list_by_trainer.html'
    paginate_by = 10

    def get_queryset(self):
        return Lecture.objects.filter(trainer=self.request.user)


@login_message_required
def trainer_new(request):
    if request.method == "POST":
        form = TrainerNewForm(request.POST, request.FILES)
        user = request.session['user_id']
        user_id = User.objects.get(user_id=user)

        if form.is_valid():
            trainer = form.save(commit=False)
            trainer.writer = user_id
            # if request.FILES:
            #     if 'image' in request.FILES.keys():
            #         trainer.imagename = request.FILES['image'].name
            #     if 'upload_files' in request.FILES.keys():
            #         trainer.filename = request.FILES['upload_files'].name
            trainer.save()
            trainer.hashtag_save()
            trainer.genre_save()
            return redirect('trainer-detail', trainer.id)
    else:
        form = TrainerNewForm()
    return render(request, 'trainer/trainer_new.html', {'form': form})


@login_message_required
def trainer_update(request, trainer_id):
    trainer = Trainer.objects.get(id=trainer_id)

    if request.method == "POST":
        if trainer.writer == request.user or request.user.level == '0':
            image_change_check = request.POST.get('imageChange', False)
            image_check = request.POST.get('image-clear', False)
            if image_check or image_change_check:
                os.remove(os.path.join(settings.MEDIA_ROOT, trainer.image.path))

            certimg1_change_check = request.POST.get('certimg1Change', False)
            certimg1_check = request.POST.get('certimg1-clear', False)
            if certimg1_check or certimg1_change_check:
                os.remove(os.path.join(settings.MEDIA_ROOT, trainer.certimg1.path))

            certimg2_change_check = request.POST.get('certimg2Change', False)
            certimg2_check = request.POST.get('certimg2-clear', False)
            if certimg2_check or certimg2_change_check:
                os.remove(os.path.join(settings.MEDIA_ROOT, trainer.certimg2.path))

            certimg3_change_check = request.POST.get('certimg3Change', False)
            certimg3_check = request.POST.get('certimg3-clear', False)
            if certimg3_check or certimg3_change_check:
                os.remove(os.path.join(settings.MEDIA_ROOT, trainer.certimg3.path))

            certimg4_change_check = request.POST.get('certimg4Change', False)
            certimg4_check = request.POST.get('certimg4-clear', False)
            if certimg4_check or certimg4_change_check:
                os.remove(os.path.join(settings.MEDIA_ROOT, trainer.certimg4.path))

            certimg5_change_check = request.POST.get('certimg5Change', False)
            certimg5_check = request.POST.get('certimg5-clear', False)
            if certimg5_check or certimg5_change_check:
                os.remove(os.path.join(settings.MEDIA_ROOT, trainer.certimg5.path))

            certimg6_change_check = request.POST.get('certimg6Change', False)
            certimg6_check = request.POST.get('certimg6-clear', False)
            if certimg6_check or certimg6_change_check:
                os.remove(os.path.join(settings.MEDIA_ROOT, trainer.certimg6.path))

            certimg7_change_check = request.POST.get('certimg7Change', False)
            certimg7_check = request.POST.get('certimg7-clear', False)
            if certimg7_check or certimg7_change_check:
                os.remove(os.path.join(settings.MEDIA_ROOT, trainer.certimg7.path))

            certimg8_change_check = request.POST.get('certimg8Change', False)
            certimg8_check = request.POST.get('certimg8-clear', False)
            if certimg8_check or certimg8_change_check:
                os.remove(os.path.join(settings.MEDIA_ROOT, trainer.certimg8.path))

            certimg9_change_check = request.POST.get('certimg9Change', False)
            certimg9_check = request.POST.get('certimg9-clear', False)
            if certimg9_check or certimg9_change_check:
                os.remove(os.path.join(settings.MEDIA_ROOT, trainer.certimg9.path))

            certimg10_change_check = request.POST.get('certimg10Change', False)
            certimg10_check = request.POST.get('certimg10-clear', False)
            if certimg10_check or certimg10_change_check:
                os.remove(os.path.join(settings.MEDIA_ROOT, trainer.certimg10.path))

            form = TrainerNewForm(request.POST, request.FILES, instance=trainer)
            writer = trainer.writer
            if form.is_valid():
                trainer = form.save(commit=False)
                trainer.writer = writer
                # if request.FILES:
                #     if 'image' in request.FILES.keys():
                #         trainer.imagename = request.FILES['image'].name
                #     if 'upload_files' in request.FILES.keys():
                #         trainer.filename = request.FILES['upload_files'].name
                trainer.save()
                trainer.hashtag_save()
                trainer.genre_save()
                messages.success(request, "수정되었습니다.")
                return redirect('trainer-detail', trainer.id)
    else:
        trainer = Trainer.objects.get(id=trainer_id)
        if trainer.writer == request.user or request.user.level == '0':
            form = TrainerNewForm(instance=trainer)
            context = {
                'form': form,
                'update': '수정하기',
            }
            if trainer.imagename and trainer.image:
                context['imagename'] = trainer.imagename
                context['image_url'] = trainer.image.url
            # if trainer.filename and trainer.upload_files:
            #     context['filename'] = trainer.filename
            #     context['file_url'] = trainer.upload_files.url
            return render(request, "trainer/trainer_new.html", context)
        else:
            messages.error(request, "본인 게시글만 수정할 수 있습니다.")
            return redirect('trainer-detail', trainer.id)


@login_message_required
def trainer_delete(request, trainer_id):
    trainer = Trainer.objects.get(id=trainer_id)
    if trainer.writer == request.user or request.user.level =='0':
        trainer.delete()
        messages.success(request, "삭제되었습니다.")
        return redirect('accounts:mypage')
    else:
        messages.error(request, "본인 게시글만 삭제할 수 있습니다.")
    return redirect('trainer-detail', trainer.id)


def trainer_search(request):
    search_result = Trainer.objects.all()
    b = request.GET.get('b', '')
    if b:
        search_result = search_result.filter(
            Q(writer__name__icontains=b)
            | Q(name__icontains=b)
            | Q(genre__name__icontains=b)
            | Q(address__icontains=b)
            | Q(place__icontains=b)
            | Q(hashtag__name__icontains=b)
            | Q(summary__icontains=b)
            )
    else:
        messages.error(request, '검색어를 입력해주세요.')
    return render(request, 'trainer/trainer_list.html', {'b': b, 'trainer_list': search_result})


def trainer_mylist(request):
    user = request.session['user_id']
    user_id = User.objects.get(user_id=user)
    mylist = Trainer.objects.filter(writer=user_id)
    return render(request, 'trainer/trainer_mylist.html', {'trainer_list': mylist})
