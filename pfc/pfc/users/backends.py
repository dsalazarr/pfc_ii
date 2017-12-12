from django.contrib.auth.backends import ModelBackend


class MyBackend(ModelBackend):
    def user_can_authenticate(self, user):
        return user.apply_rules()
