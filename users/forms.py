from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.core import validators

User = get_user_model()

# Clase para el formulario de inicio de sesión de usuarios
class UserLoginForm(forms.Form):
    email = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label='Username') #Campo de nombre de usuario
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label='Password') #Campo de contraseña

    # Función donde se recogen los valores y se comprueba si los datos introducidos son correctos o no
    # En caso de que no lo sean se da un error de validación (ValidationError)
    def clean(self, *args, **kwargs):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if email and password:
            user = authenticate(username=email, password=password)

            if not user:
                raise forms.ValidationError('Wrong Credentials')
            if not user.is_active:
                raise forms.ValidationError('User inactive')
            
        return super(UserLoginForm, self).clean(*args, **kwargs)

# Clase para el formulario de registro de usuarios
class UserRegisterForm(forms.ModelForm):
    #Se definen los campos que el usuario tendrá que introducir en el formulario para crear el usuario
    email = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label='Email')
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label='First Name')
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label='Last Name')
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label='Password', validators=[
        validators.MinLengthValidator(5, "Please enter 5 or more characters") # Se incluye una validacion de 5 caracteres mínimos que tiene que tener la contraseña
    ])    
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label='Confirm Password', validators=[
        validators.MinLengthValidator(5, "Please enter 5 or more characters")
    ])

    # Se define la clase a la que se le van a aplicar los campos rellenados en el formulario.
    # En este caso el usuario (User)
    class Meta:
        model = User
        fields = [
            'email',
            'first_name',
            'last_name',
            'password',
        ]

    # Se recogen los datos introducidos en el formulario y se realiza la validación.
    # Comprueba si el usuario existe y si las dos contraseñas introducidas son iguales o no.
    def clean(self, *args, **kwargs):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')

        email_qs = User.objects.filter(email=email)
        if email_qs.exists():
            raise forms.ValidationError("This email has already been registered")
        if password != password2:
            raise forms.ValidationError("Passwords must match")
        
        return super(UserRegisterForm, self).clean(*args, **kwargs)
