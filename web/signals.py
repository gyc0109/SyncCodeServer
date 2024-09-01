from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import Admin

@receiver(post_migrate)
def create_default_admin(sender, **kwargs):
    if not Admin.objects.filter(username='admin').exists():
        Admin.objects.create(
            username='admin',
            password='b5e2b41d95d9cff78164e375ae72a7df',
            phone='12345678900',
            email='admin@123.com'
        )
