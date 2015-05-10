from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Fieldset, Hidden, HTML
from crispy_forms.bootstrap import FormActions, StrictButton, Field
from django.core.urlresolvers import reverse
from django.contrib.auth.forms import AuthenticationForm

class LoginForm(AuthenticationForm):
    helper = FormHelper()

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-6'
        self.helper.layout = Layout(
            Field('username', placeholder="Username"),
            Field('password', placeholder="Password"),
            Submit('submit', "Zaloguj", css_class='btn btn-primary'),
        )

class LoadFilenameForm(forms.Form):
    #file = forms.FileField(widget=forms.FileInput(attrs={'size':1}) ,required=True)
    file=forms.FileField(label='Select a file')


    helper = FormHelper()

    def __init__(self, *args, **kwargs):
        super(LoadFilenameForm, self).__init__(*args, **kwargs)
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-6'
        self.helper.layout = Layout(
            Field('file'),
            # Field('username', placeholder="Username"),
            # Field('password', placeholder="Password"),
            # Field('filename', placeholder="Filename"),
            #HTML( """<input type=file name="filename" size=30>"""),
            Submit('submit', "Wczytaj", css_class='btn btn-primary'),

        )
