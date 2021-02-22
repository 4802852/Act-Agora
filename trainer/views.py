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


class TrainerDetailView(generic.DetailView):
    model = Trainer


class LectureListView(generic.ListView):
    model = Lecture
    paginate_by = 10


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
        search_result = search_result.filter(Q(name__icontains=b) | Q(summary__icontains=b))

    return render(request, 'trainer/trainer_search.html', {'b': b, 'trainers': search_result})


# def trainer_list(request):
#     trainer_list = Trainer.objects.prefetch_related('hashtag').all()
#
#     return render(request, 'trainer/trainer_list.html', {'trainer_list': trainer_list, })
