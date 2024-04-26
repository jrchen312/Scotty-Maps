from django import forms

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

# Kind of like a modelform? but it would need to inherit both a User class
# and the Profile class, which is weird, so let's leave it hanging in the air.
class SpecialUserCreationForm(UserCreationForm):
    name = forms.CharField(max_length=100, required=True)
    tag_id = forms.CharField(max_length=200, required=False, help_text="Optional")

    def save(self, commit=True):
        if not commit:
            raise NotImplementedError("cannot do this")
        
        # call the parent 
        user = super(UserCreationForm, self).save(commit=True)

        profile = Profile(user=user, 
                          name=self.cleaned_data['name'],
                          tag_id=self.cleaned_data['tag_id'],
                          )
        profile.save()
        return user, profile
    

class ProfileEditForm(forms.Form):
    name = forms.CharField(max_length=100)
    tag_id = forms.CharField(max_length=200)
