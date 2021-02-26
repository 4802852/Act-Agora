from django.contrib import messages
from django.db.models import Q
from django.shortcuts import render, redirect
from .models import Genre, Hashtag, Gym, Trainer, Lecture, LectureInstance
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin


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


class TrainerDetailView(generic.DetailView):
    model = Trainer


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


def trainer_new(request):
    return render(request, 'board/trainer_new.html')


def trainer_new_post(request):
    if request.method == "POST":
        trainer = Trainer()
        trainer.name = request.POST['trainer_name']
        trainer.tagtext = request.POST['tagtext']
        trainer.summary = request.POST['summary']
        trainer.save()
        trainer.hashtag_save()
        return redirect('/trainer/' + str(trainer.id))
    else:
        return render(request, 'board/trainer_new.html')


def trainer_update(request, trainer_id):
    trainer = Trainer.objects.get(id=trainer_id)

    if request.method == "POST":
        trainer.name = request.POST['trainer_name']
        trainer.tagtext = request.POST['tagtext']
        trainer.summary = request.POST['summary']
        trainer.save()
        trainer.hashtag_save()
        return redirect('/trainer/' + str(trainer.id))
    else:
        old = Trainer.objects.get(id=trainer_id)
        return render(request, 'board/trainer_update.html', {'trainer': old})


def trainer_delete(request, trainer_id):
    trainer = Trainer.objects.get(id=trainer_id)
    trainer.delete()
    return redirect('/trainers/')


def trainer_search(request):
    search_result = Trainer.objects.all()
    b = request.GET.get('b', '')
    if b:
        search_result = search_result.filter(Q(writer__icontains=b) |
                                             Q(name__icontains=b) |
                                             Q(genre__icontains=b) |
                                             Q(address__icontains=b) |
                                             Q(place__icontains=b) |
                                             Q(tagtext__icontains=b) |
                                             Q(summary__icontains=b))
    else:
        messages.error(self.request, '검색어를 입력해주세요.')
    return render(request, 'trainer/trainer_search.html', {'b': b, 'trainer_list': search_result})


# def trainer_list(request):
#     trainer_list = Trainer.objects.prefetch_related('hashtag').all()
#
#     return render(request, 'trainer/trainer_list.html', {'trainer_list': trainer_list, })
