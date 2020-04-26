import logging
logger = logging.getLogger(__name__)

from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in
from django.db.models.signals import pre_save

from .models import User
from django.contrib.auth.models import User as BaseUser


@receiver(user_logged_in)
def post_login(sender, user, request, **kwargs):
    logger.info(f"#### {user} LOGGED IN ####")

@receiver(pre_save, sender=User)
def user_updated(sender, **kwargs):
    user = kwargs.get('instance', None)
    logger.info(f"#### {user} user ####")
    
    # if user:
    #     new_password = user.password
    #     try:
    #         old_password = User.objects.get(pk=user.pk).password
    #     except User.DoesNotExist:
    #         old_password = None
    #     if new_password != old_password:
    #         pass

@receiver(pre_save, sender=BaseUser)
def base_user_updated(sender, **kwargs):
    user = kwargs.get('instance', None)
    logger.info(f"#### {user} base ####")