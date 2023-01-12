from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Clase de Django que se permite crear usuarios para la autenticación de forma personalizada
# Se definen en el las funciones que se usarán para crear los usuarios (supersuers y normales)
class MyUserManager(BaseUserManager):

    # Función para crear usuarios normales.
    def create_user(self, username, first_name, last_name, password=None):
        if not username:
            raise ValueError('Users must have a valid username')

        user = self.model(
            username=username,
            first_name=first_name,
            last_name=last_name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    #Función para crear usuarios superuser (administradores de Django, se crean por consola)
    def create_superuser(self, username, first_name, last_name, password=None):
        user = self.create_user(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

# Clase de modelo de usuario
# Se definen los atributos necesarios más los predefinidos necesarios de Django
class User(AbstractBaseUser):
    username = models.CharField(max_length=30, unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=30)

    #Atributos por defecto de ususrios Django
    is_superuser = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name','last_name']

    objects = MyUserManager()

    # Función que sobrescribe la forma en la que se mostrará el usuario
    def __str__(self):
        return self.first_name + ' ' + self.last_name
    
    # Función genérica necesaria para usar AbstractBaseUser
    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    # Función genérica necesaria para usar AbstractBaseUser
    def has_module_perms(self, app_label):
        return True

