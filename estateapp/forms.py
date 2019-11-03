from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import get_user_model

User = get_user_model()

class SignupForm(UserCreationForm):
    username=forms.CharField( label='Username',widget=forms.TextInput(attrs={'class': 'form-control'}))
    email=forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class':'form-control'}))
    password1=forms.CharField(label='Password',widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2=forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={'class':'form-control'}))
    class Meta(UserCreationForm.Meta):
        model=User
        fields=UserCreationForm.Meta.fields + ('email',)
  

    def save(self, commit=True):
        user = super(SignupForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user
    
    
class LoginForm(forms.Form):
	email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))
	password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
 
 
class pgform(forms.Form):
    
    mobile=forms.CharField(label='Mobile',min_length=10, widget=forms.NumberInput(attrs={'class':'form-control','placeholder':'Enter your Mobile Number'}))
    
    city=forms.CharField(label='City',widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter your city'}))
    location=forms.CharField(label='Location', widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter your Location'}))
   
    CHOICES1=(
        ('Female','Female'),
        ('Male','Male'),
        ('Any','Any')
    )
    CHOICES2=(
        ('Single','Single'),
        ('Sharing','Sharing')
        
    )
    balcony= (
    ('yes', 'Yes'),
    ('no', 'No')
    
    )
    parking= (
    ('yes', 'Yes'),
    ('no', 'No')
    
    
    )
    box=(
        
        ('A.C', 'A.C'),
        ('TV', 'TV'),
        ('Fridge', 'Fridge'),
        ('Washing Machine','Washing Machine'),
        ('Wi-fi','Wi-fi')
    )
    food=(
       ('yes', 'Yes') ,
       ('no', 'No')
    )
    
    
   
    available=forms.ChoiceField(widget=forms.Select(attrs={'class':'form-control'}),choices=CHOICES1)
    food=forms.ChoiceField(widget=forms.RadioSelect(attrs={'class':'list-unstyled'}), choices=food)
    occupancy=forms.ChoiceField(widget=forms.Select(attrs={'class':'form-control'}), choices=CHOICES2)
    balcony=forms.ChoiceField( widget=forms.RadioSelect(attrs={'class':'list-unstyled'}),choices=balcony)
    parking=forms.ChoiceField( widget=forms.RadioSelect(attrs={'class':'list-unstyled'}),choices=parking)
    amount=forms.DecimalField(widget=forms.NumberInput(attrs={'class':'form-control','placeholder':'Enter your Rent'}))
    details=forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple(attrs={'class': 'list-unstyled'}), choices=box)
   
    