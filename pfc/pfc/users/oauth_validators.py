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

    def validate_bearer_token(self, token, scopes, request):
        if super(OAuth2CustomValidator, self).validate_bearer_token(token, scopes, request):
            access_token = request.access_token
            if access_token.user:
                for rule in access_token.user.rules.all():
                    if not rule.apply_rule(request):
                        return False
            return True
        return False
