from django.contrib.auth import authenticate
from oauth2_provider.oauth2_validators import OAuth2Validator


class OAuth2CustomValidator(OAuth2Validator):
    def validate_user(self, username, password, client, request, *args, **kwargs):
        """
        Check username and password correspond to a valid and active User
        """
        u = authenticate(username=username, password=password)
        if u is not None and u.has_access_to_application(client):
            request.user = u
            return True
        return False
