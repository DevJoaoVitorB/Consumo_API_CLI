from django.contrib.auth import authenticate, login, logout
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import *
from .serializers import *

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    @action(detail=False, methods=["POST"])
    def register(self, request):
        username = request.data.get("username")
        email = request.data.get("email")
        password = request.data.get("password")

        if not all([username, email, password]):
            return Response({"error": "Preencha todos os campos!"}, status=status.HTTP_400_BAD_REQUEST)
        if self.queryset.filter(username=username).exists():
            return Response({"error": "Usuário já existente!"}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        return Response({"message": f"Usuário {user.username} registrado com sucesso!"}, status=status.HTTP_201_CREATED)
    
    
    @action(detail=False, methods=["POST"])
    def login(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(
            username=username, 
            password=password
        )

        if user:
            login(request, user)
            return Response({"message": "Login efetuado com sucesso!"}, status=status.HTTP_200_OK)

        return Response({"error": "Credenciais Inválidas!"}, status=status.HTTP_401_UNAUTHORIZED)

    @action(detail=False, methods=["POST"])
    def logout(self, request):
        logout(request)
        return Response({"message": "Logout efetuado com sucesso!"}, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=["GET"], permission_classes=[permissions.IsAuthenticated])
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = permissions.IsAuthenticated

    def get_queryset(self):
        user = self.request.user
        return self.queryset.filter(owner=user)

    def create(self, request, *args, **kwargs):
        user = request.user
        name = request.data.get("name")
        description = request.data.get("description")

        if not name:
            return Response({"error": "O projeto necessita de um nome!"}, status=status.HTTP_400_BAD_REQUEST)
        
        project = Project.objects.create(
            name=name,
            description=description or None,
            owner=user
        )

        return Response({"message": f"Projeto {project.name} criado com sucesso!"}, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=["GET"])
    def my_projects(self, request):
        projects = self.get_queryset()
        serializer = self.get_serializer(projects, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["GET"])
    def tasks(self, request, pk=None):
        project = self.get_object()
        tasks = project.tasks.all()
        serializer = self.get_serializer(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = permissions.IsAuthenticated

    def get_queryset(self):
        user = self.request.user
        return self.queryset.filter(project__owner=user)

    def create(self, request, *args, **kwargs):
        user = request.user
        title = request.data.get("title")
        description = request.data.get("description")
        project_id = request.data.get("project_id")

        if not all([title, project_id]):
            return Response({"error": "É necessário o título da tarefa e o id do projeto!"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            project = Project.objects.get(id=project_id, owner=user)
        except Project.DoesNotExist:
            return Response({"error": "Projeto inválido ou pertecente a outro usuário!"}, status=status.HTTP_403_FORBIDDEN)
        
        task = Task.objects.create(
            title=title,
            description=description or None,
            project=project
        )

        return Response({"message": f"Tarefa {task.title} criada com sucesso!"}, status=status.HTTP_201_CREATED)
