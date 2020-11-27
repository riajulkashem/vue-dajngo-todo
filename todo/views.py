from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from todo.models import Task
from todo.serializer import TaskSerializer


class TaskViewSet(ModelViewSet):
    queryset = Task.objects.all()
    authentication_classes = (BasicAuthentication,)
    permission_classes = (IsAuthenticated, )
    serializer_class = TaskSerializer

    def get_queryset(self):
        if self.request.query_params:
            status = self.request.GET.get('status')
            return self.queryset.filter(status=status)
        return super().get_queryset()
