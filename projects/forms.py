from django import forms
from django.forms import ModelForm, fields, widgets
from .models import Project, Review


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description', 'demo_link','source_link','feature_image'] # how to customize your forms
        #fields = '__all__' # how not to customize your forms
        widgets = {
            'tags': forms.CheckboxSelectMultiple(),
        }
    # for name, field in fields.items():
        # fields.widget.attrs.update({'class': 'input'})
            
    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})

        # how to add css to form in the form model.
        # self.fields['title'].widget.attrs.update({'class': 'input', 'placeholder':'Add Title'})
        # self.fields['description'].widget.attrs.update({'class': 'input'})


class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['value', 'body']
        labels = {
            'value': 'Place your vote',
            'body': 'Add a comment with your vote'
        }

    def __init__(self, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})