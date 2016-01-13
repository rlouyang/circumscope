from django import forms
import localflavor.us.forms as lfforms

class Search(forms.Form):
    first_name = forms.CharField(label='First name', max_length=30, widget=forms.TextInput(attrs={'placeholder': 'First Name'}))
    last_name = forms.CharField(label='Last name', max_length=30, widget=forms.TextInput(attrs={'placeholder': 'Last Name'}))
    high_school = forms.CharField(required=False, label='High School', max_length=30, widget=forms.TextInput(attrs={'placeholder': 'High School'}))
    university = forms.CharField(required=False, label='University', max_length=30, widget=forms.TextInput(attrs={'placeholder': 'University'}))
    hometown = forms.CharField(required=False, label='Hometown', max_length=30, widget=forms.TextInput(attrs={'placeholder': 'Hometown'}))
    current_city = forms.CharField(required=False, label='Current City', max_length=30, widget=forms.TextInput(attrs={'placeholder': 'Current City'}))
    state = lfforms.USStateField(required=False, widget=forms.TextInput(attrs={'placeholder': 'State'}))
    employer = forms.CharField(required=False, label='Employer', max_length=30, widget=forms.TextInput(attrs={'placeholder': 'Employer'}))
    orgs = forms.CharField(required=False, label='Other Organization', max_length=30, widget=forms.TextInput(attrs={'placeholder': 'Other Organizations'}))
    username = forms.CharField(required=False, label='Any Username', max_length=30, widget=forms.TextInput(attrs={'placeholder': 'Any Username'}))