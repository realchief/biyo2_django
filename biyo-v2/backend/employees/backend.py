from django.contrib.auth import get_user_model
User = get_user_model()


class OwnerAuthModelBackend(object):

    def authenticate(self, username=None, password=None):
        # if '@' in username:
        #     kwargs = {'email': username}
        # else:
        kwargs = {'email': username}
        try:
            user = User.objects.get(**kwargs)

            if user.check_is_owner():
                if user.check_password(password):
                    return user
            else:
                return None

        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
