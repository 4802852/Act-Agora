from django import forms
from .models import Trainer


class TrainerNewForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(TrainerNewForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = '이름'
        self.fields['name'].widget.attrs.update({
            'placeholder': '이름을 입력해주세요.',
            'class': 'form-control',
            'autofocus': True,
        })
        self.fields['genretext'].label = '분야'
        self.fields['genretext'].widget.attrs.update({
            'placeholder': '분야를 입력해주세요.(예- PT, 필라테스 등 띄어쓰기로 구분)',
            'class': 'form-control',
        })
        self.fields['address'].label = '지역'
        self.fields['address'].widget.attrs.update({
            'placeholder': '지역을 입력해주세요. (예- 서울시 동작구)',
            'class': 'form-control',
        })
        self.fields['place'].label = '장소'
        self.fields['place'].widget.attrs.update({
            'placeholder': '장소를 입력해주세요. (예- 홍길동체육관)',
            'class': 'form-control',
        })
        self.fields['tagtext'].label = 'Hashtag'
        self.fields['tagtext'].widget.attrs.update({
            'placeholder': '특징을 입력해주세요. (예 - #차분한 #열정적인, 띄어쓰기로 구분)',
            'class': 'form-control',
        })

    class Meta:
        model = Trainer
        fields = ['writer', 'name', 'genretext', 'address', 'place', 'tagtext', 'summary']
