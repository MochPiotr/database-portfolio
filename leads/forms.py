from django import forms 
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UsernameField
from .models import Lead, Agent, Deal, Contact

User = get_user_model()

class LeadModelForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = ('name', 'organisation', 'agent', 'status', 'primary_contact', 'contacts')
        exclude = ("organisation",)

class DealModelForm(forms.ModelForm):
    class Meta:
        model = Deal
        fields = ('name','lead', 'value', 'close_date','agent','probability', 'status','contact')
        widgets = {
            'close_date': forms.DateInput(attrs={
                'type': 'date',      
                'class': 'input',     
                'placeholder': 'Select a date',
            }),
        }

class ContactModelForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ('first_name', 'last_name', 'phone','email','job_position', 'organisation','name', 'agent')
        exclude = ("organisation",)

class LeadForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    phone = forms.CharField()

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", )
        field_classes = {'username': UsernameField}

class AssignAgentForm(forms.Form):
    agent = forms.ModelChoiceField(queryset=Agent.objects.none())

    def __init__(self, *args, **kwargs):
        request = kwargs.pop("request")
        agents = Agent.objects.filter(organisation=request.user.userprofile)
        super(AssignAgentForm, self).__init__(*args, **kwargs)
        self.fields["agent"].queryset = agents

class LeadCategoryUpdateForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = (
            'status',
        )