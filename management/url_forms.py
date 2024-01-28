from django import forms
from .models import ShortenedURL

class ShortenedURLForm(forms.ModelForm):
    class Meta:
        model = ShortenedURL
        fields = ['long_url','expired_date']  # Add 'slug' or any other fields you want to include

    def clean_slug(self):
        slug = self.cleaned_data.get('slug')
        if ShortenedURL.objects.filter(slug=slug).exists():
            raise forms.ValidationError('This slug is already in use. Please choose another one.')
        return slug

