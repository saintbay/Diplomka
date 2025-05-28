from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import UserProfile, Product, Review

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    age = forms.IntegerField(required=False)
    phone = forms.CharField(max_length=15, required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'age', 'phone']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            UserProfile.objects.create(user=user, age=self.cleaned_data['age'], phone=self.cleaned_data['phone'])
        return user

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password and password2 and password != password2:
            raise forms.ValidationError("Пароли не совпадают.")
        return cleaned_data

class ProductFormOnOpen(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['img','name','description','price']

class ProductFormOnSearch(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['img','name','price']

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'text']
        widgets = {
            'rating': forms.RadioSelect(choices=[(i, f'{i} ★') for i in range(1, 6)],
                                        attrs={'class': 'form-check-input'}),
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Напишите свой отзыв...'
            })
        }
