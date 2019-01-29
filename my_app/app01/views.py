from django.shortcuts import render, HttpResponse

from rest_framework.views import APIView
from app01.models import Picture, Admin
from app01.serializers import AdminSerializer
from libs.swagger.swagger_param import swagger_doc


class UserViews(APIView):

    def get(self, request):
        admins = Admin.objects.filter(deleted=False).distinct()

        serializer = AdminSerializer(admins, many=True)

        return render(request, 'home.html')
