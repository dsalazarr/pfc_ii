from django.contrib.auth import authenticate
from oauth2_provider.oauth2_validators import OAuth2Validator


class OAuth2CustomValidator(OAuth2Validator):
    def validate_user(self, username, password, client, request, *args, **kwargs):
        """
        Check username and password correspond to a valid and active User
        """
        u = authenticate(username=username, password=password)
        if u is not None and u.has_access_to_application(client):
            print('has access')
            request.user = u
            return True
        return False

    def validate_code(self, client_id, code, client, request, *args, **kwargs):
        result = super(OAuth2CustomValidator, self).validate_code(
            client_id,
            code,
            client,
            request,
            *args,
            **kwargs
        )
        if result and not request.user.has_access_to_application(client):
            return False
        return result

    def validate_bearer_token(self, token, scopes, request):
        if super(OAuth2CustomValidator, self).validate_bearer_token(token, scopes, request):
            access_token = request.access_token
            if access_token.user:
                return access_token.user.apply_rules(request)
            return True
        return False
