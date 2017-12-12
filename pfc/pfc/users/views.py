import urllib

from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.views.generic import DetailView, ListView, RedirectView, UpdateView

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import View
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from .models import User


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    # These next two lines tell the view to index lookups by username
    slug_field = 'username'
    slug_url_kwarg = 'username'


class UserRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self):
        return reverse('users:detail',
                       kwargs={'username': self.request.user.username})


class UserUpdateView(LoginRequiredMixin, UpdateView):

    fields = ['name', ]

    # we already imported User in the view code above, remember?
    model = User

    # send the user back to their own page after a successful update
    def get_success_url(self):
        return reverse('users:detail',
                       kwargs={'username': self.request.user.username})

    def get_object(self):
        # Only get the User record for the user making the request
        return User.objects.get(username=self.request.user.username)


class UserListView(LoginRequiredMixin, ListView):
    model = User
    # These next two lines tell the view to index lookups by username
    slug_field = 'username'
    slug_url_kwarg = 'username'


class UserListRestView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        return Response(
            status=status.HTTP_200_OK,
            data=[
                {
                    "id": item.id,
                    "name": item.name,
                    "email": item.email,
                }
                for item in request.user.company.users.all()
            ]
        )


class UserPermissionsView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        application = request.auth.application
        user = request.user
        return Response(
            status=status.HTTP_200_OK,
            data=[
                item.codename
                for item in request.user.permissions.filter(
                    application=application
                )
            ]
        )


class UserMe(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        return Response(
            status=status.HTTP_200_OK,
            data={
                'id': request.user.id,
                'email': request.user.email
            }
        )


class LoginView(View):
    def get(self, request, *args, **kawrgs):
        next = request.GET.get('next', '')
        next_encoded = urllib.urlencode({'next': next})
        return redirect('/admin/login/?{}'.format(next_encoded))
