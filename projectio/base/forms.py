from django.forms import ModelForm, ModelChoiceField, HiddenInput
from django.urls import reverse
from django import forms

from .models import Project, Task
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Row, Column, Button


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = '__all__'
        widgets = {'user': HiddenInput()}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.add_input(Submit('save_project', 'Save Project', css_class='btn-success', ))
        self.helper.add_input(Button('cancel', 'Cancel', css_class='btn-danger',
                                     onclick="window.location.href = '{}';".format(reverse('home'))))

        self.helper.layout = Layout(
            Row(
                Column('name'),
                Column('start_date'),
                Column('end_date'),
            ),
            Row(
                Column('client'),
                Column('employees'),
                Column('user'),
            ),
            Row(
                Column('invoice'),
                Column('logo'),
                Column('project.tasks.all'),
            ),
            Row('description')
        )


class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = '__all__'
        widgets = {'project': HiddenInput()}


class TaskEdit(ModelForm):
    class Meta:
        model = Task
        fields = '__all__'
        exclude = ('project',)
