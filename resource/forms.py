from django import forms
from resource.models import Resource


class ResourceForm(forms.ModelForm):
    class Meta:
        model = Resource
        fields = '__all__'
        exclude = ['slug_name']

        widgets = {
            'name': forms.TextInput(attrs={"class": "form-control"}),
            'resource': forms.FileInput(attrs={"class": "form-control"})
        }
