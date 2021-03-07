from django import forms
from .models import Review, Photo


class ReviewNewForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ReviewNewForm, self).__init__(*args, **kwargs)
        self.fields['title'].label = '제목'
        self.fields['title'].widget.attrs.update({
            'placeholder': '제목을 입력해주세요.',
            'class': 'form-control',
            'autofocus': True,
        })
        self.fields['genretext'].label = '분야'
        self.fields['genretext'].widget.attrs.update({
            'placeholder': '분야를 입력해주세요.(예- PT, 필라테스 등 띄어쓰기로 구분)',
            'class': 'form-control',
        })
        self.fields['tagtext'].label = 'Hashtag'
        self.fields['tagtext'].widget.attrs.update({
            'placeholder': '특징을 입력해주세요. (예 - #차분한 #열정적인, 띄어쓰기로 구분)',
            'class': 'form-control',
        })

    class Meta:
        model = Review
        fields = ['writer', 'trainer', 'title', 'genretext', 'tagtext', 'content']


class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['image']
        widgets = {
            'image': forms.ClearableFileInput(attrs={'multiple': True}),
        }
