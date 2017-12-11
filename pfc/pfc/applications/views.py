from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

# Create your views here.
from pfc.applications.models import ApplicationConfig


class ApplicationConfigurationView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        queryset = ApplicationConfig.objects.filter(application=request.auth.application)
        return Response(
            data={
                item.key: item.value
                for item in queryset
            },
            status=status.HTTP_200_OK
        )

