import os

from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic

from .forms import ReviewNewForm, ImageUploadForm
from .models import Review, Photo
from accounts.decorators import login_message_required

from accounts.models import User
from trainer.models import Trainer

from PTin import settings


class ReviewListView(generic.ListView):
    model = Review
    paginate_by = 10
    template_name = 'review/review_list.html'
    context_object_name = 'review_list'

    def get_queryset(self):
        trainer_list = Review.objects.order_by('-id')
        self.request.session['trainer_id'] = None
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


def review_detail_view(request, pk):
    review = get_object_or_404(Review, pk=pk)

    # 접속자가 작성자와 일치하는지 확인
    if request.user == review.writer:
        review_auth = True
    else:
        review_auth = False

    context = {
        'review': review,
        'review_auth': review_auth,
    }
    return render(request, 'review/review_detail.html', context)


@login_message_required
def review_new(request):
    if request.method == "POST":
        form = ReviewNewForm(request.POST)
        imgform = ImageUploadForm(request.POST, request.FILES)
        user = request.session['user_id']
        trainer = request.session['trainer_id']
        user_id = User.objects.get(user_id=user)
        if trainer is None:
            pass
        else:
            trainer = Trainer.objects.get(writer_id=trainer)

        if form.is_valid() and imgform.is_valid():
            review = form.save(commit=False)
            review.writer = user_id
            if trainer is None:
                pass
            else:
                review.trainer = trainer
            review.save()
            for img in request.FILES.getlist("image"):
                photo = Photo()
                photo.review = review
                photo.image = img
                photo.save()
            review.hashtag_save()
            review.genre_save()
            return redirect('review:review-detail', review.id)
    else:
        form = ReviewNewForm()
        imgform = ImageUploadForm()
    return render(request, 'review/review_new.html', {'form': form, 'imgform': imgform})


@login_message_required
def review_update(request, review_id):
    review = Review.objects.get(id=review_id)

    if request.method == "POST":
        if review.writer == request.user or request.user.level == '0':
            # reviewimg_change_check = request.POST.get('certimg1Change', False)
            # reviewimg_check = request.POST.get('certimg1-clear', False)
            # if reviewimg_check or reviewimg_change_check:
            #     os.remove(os.path.join(settings.MEDIA_ROOT, review.photo_set.all().path))
            form = ReviewNewForm(request.POST, instance=review)
            imgform = ImageUploadForm(request.POST, request.FILES)

            writer = review.writer
            trainer = review.trainer
            if form.is_valid() and imgform.is_valid():
                review = form.save(commit=False)
                review.writer = writer
                review.trainer = trainer
                review.save()
                for img in request.FILES.getlist("image"):
                    photo = Photo()
                    photo.review = review
                    photo.image = img
                    photo.save()
                review.hashtag_save()
                review.genre_save()
                messages.success(request, "수정되었습니다.")
                return redirect('review:review-detail', review.id)
    else:
        review = Review.objects.get(id=review_id)
        if review.writer == request.user or request.user.level == '0':
            form = ReviewNewForm(instance=review)
            context = {
                'form': form,
                'update': '수정하기',
                'imgform': review.Photo_set.all()
            }
            return render(request, "review/review_new.html", context)
        else:
            messages.error(request, "본인 게시글만 수정할 수 있습니다.")
            return redirect('review-detail', review.id)


@login_message_required
def review_delete(request, review_id):
    review = Review.objects.get(id=review_id)
    if review.writer == request.user or request.user.level =='0':
        review.delete()
        messages.success(request, "삭제되었습니다.")
        return redirect('review:review-list')
    else:
        messages.error(request, "본인 게시글만 삭제할 수 있습니다.")
    return redirect('review-detail', review.id)
