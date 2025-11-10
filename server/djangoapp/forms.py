# server/djangoapp/forms.py
from django import forms
from .models import CarReview

class ReviewForm(forms.ModelForm):
    purchase_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    car_make = forms.CharField(
        required=False,
        widget=forms.Select(choices=[('', 'Choose Car Make and Model'),
                                     ('Toyota - Corolla', 'Toyota - Corolla'),
                                     ('Honda - Civic', 'Honda - Civic'),
                                     ('Ford - Figo', 'Ford - Figo'),
                                     ('Other', 'Other')],
                           attrs={'class': 'form-control'})
    )
    car_year = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'YYYY'})
    )

    class Meta:
        model = CarReview
        fields = ['review', 'purchase_date', 'car_make', 'car_year']
        widgets = {
            'review': forms.Textarea(attrs={
                'rows': 8,
                'placeholder': 'Write your review here...',
                'class': 'form-control review-textarea'
            }),
        }
