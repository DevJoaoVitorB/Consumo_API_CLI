import requests
import os, time

SESSION = requests.Session()
API_URL = "http://127.0.0.1:8000/api"

class Commands:
    @staticmethod
    def register(username, email, password):
        data = {
            "username": username,
            "email": email,
            "password": password
        }
        response = SESSION.post(f"{API_URL}/users/register/", json=data)
        return response

    @staticmethod
    def login(username, password):
        data = {
            "username": username,
            "password": password
        }
        response = SESSION.post(f"{API_URL}/users/login/", json=data)
        return response
    
    @staticmethod
    def logout():
        response = SESSION.post(f"{API_URL}/users/logout/", json={})
        return response
    
    @staticmethod
    def is_authenticated():
        response = SESSION.get(f"{API_URL}/users/me/")
        return response
    
    @staticmethod
    def view_projects():
        response = SESSION.get(f"{API_URL}/projects/")
        return response

    @staticmethod
    def create_project(name, description):
        data = {
            "name": name,
            "description": description
        }
        headers = {"X-CSRFToken": SESSION.cookies.get("csrftoken")}
        response = SESSION.post(f"{API_URL}/projects/", json=data, headers=headers)
        return response
    
    @staticmethod
    def add_task(project_id, title, description):
        data = {
            "title": title,
            "description": description,
            "project_id": project_id
        }
        headers = {"X-CSRFToken": SESSION.cookies.get("csrftoken")}
        response = SESSION.post(f"{API_URL}/tasks/", json=data, headers=headers)
        return response
    
    @staticmethod
    def list_tasks():
        response = SESSION.get(f"{API_URL}/tasks/")
        return response
    
    @staticmethod
    def clear():
        os.system('cls' if os.name == 'nt' else 'clear')

class CLI:
    @staticmethod
    def menu_principal():
        while True:
            Commands.clear()
            print("===== Gerenciador de Projetos =====")

            if Commands.is_authenticated().status_code == 200:
                print("1. Ver Meus Projetos")
                print("2. Criar Novo Projeto")
                print("3. Adicionar Tarefa (Projeto)")
                print("4. Lista Tarefas")
                print("5. Listar Tarefas (Projeto)")
                print("6. Logout")
                print("0. Sair")
            else:
                print("1. Login")
                print("2. Registrar")
                print("0. Sair")
            try:
                choice = int(input("Escolha uma opção: "))
            except ValueError:
                print("Por favor, insira um número válido.")
                time.sleep(2)
                continue

            if Commands.is_authenticated().status_code == 200:
                match choice:
                    case 1:
                        CLI.view_projects()
                    case 2:
                        CLI.create_project()
                    case 3:
                        CLI.add_task()
                    case 4:
                        CLI.list_tasks()
                    case 5:
                        CLI.list_tasks_project()
                    case 6:
                        Commands.logout()
                    case 0:
                        break
                    case _:
                        print("Opção inválida. Tente novamente.")
                        time.sleep(2)
            else:
                match choice:
                    case 1:
                        CLI.login()
                    case 2:
                        CLI.register()
                    case 0:
                        break
                    case _:
                        print("Opção inválida. Tente novamente.")
                        time.sleep(2)
    
    @staticmethod
    def login():
        Commands.clear()
        print("===== Login =====")
        username = input("Username: ")
        password = input("Password: ")
        response = Commands.login(username, password)
        if response.status_code == 200:
            print(response.json().get("message", "Login realizado com sucesso!"))
        else:
            print("Login Falhou:", response.json().get("error", "Erro ao realizar login!"))
        time.sleep(2)
    
    @staticmethod
    def register():
        Commands.clear()
        print("===== Registrar =====")
        username = input("Username: ")
        email = input("Email: ")
        password = input("Password: ")
        response = Commands.register(username, email, password)
        if response.status_code == 201:
            print(response.json().get("message", "Registro realizado com sucesso!"))
        else:
            print("Registro Falhou:", response.json().get("error", "Erro ao realizar registro!"))
        time.sleep(2)
    
    @staticmethod
    def view_projects():
        Commands.clear()
        print("===== Meus Projetos =====")
        response = Commands.view_projects()
        if response.status_code == 200:
            projects = response.json()
            for project in projects:
                print(f"ID: {project['id']} - Nome: {project['name']} - Descrição: {project['description'] if project['description'] else 'Sem Descrição'}")
        else:
            print(response.json().get("error", "Erro ao buscar projetos!"))
        input("Pressione Enter para continuar...")
    
    @staticmethod
    def create_project():
        Commands.clear()
        print("===== Criar Novo Projeto =====")
        name = input("Nome do Projeto: ")
        description = input("Descrição do Projeto (opcional): ")
        response = Commands.create_project(name, description)
        if response.status_code == 201:
            print(response.json().get("message", "Projeto criado com sucesso!"))
        else:
            print("Falha ao criar projeto:", response.json().get("error", "Erro ao criar projeto!"))
        time.sleep(2)
    
    @staticmethod
    def add_task():
        Commands.clear()
        print("===== Adicionar Tarefa =====")
        project_id = input("ID do Projeto: ")
        title = input("Título da Tarefa: ")
        description = input("Descrição da Tarefa (opcional): ")
        response = Commands.add_task(project_id, title, description)
        if response.status_code == 201:
            print(response.json().get("message", "Tarefa adicionada com sucesso!"))
        else:
            print("Falha ao adicionar tarefa:", response.json().get("error", "Erro ao adicionar tarefa!"))
        time.sleep(2)
    
    @staticmethod
    def list_tasks():
        Commands.clear()
        print("===== Lista de Tarefas =====")
        response = Commands.list_tasks()
        if response.status_code == 200:
            tasks = response.json()
            for task in tasks:
                print(f"ID: {task['id']} - Título: {task['title']} - Descrição: {task['description'] if task['description'] else 'Sem Descrição'} - Projeto ID: {task['project']}")
        else:
            print(response.json().get("error", "Erro ao buscar tarefas!"))
        input("Pressione Enter para continuar...")
    
    @staticmethod
    def list_tasks_project():
        Commands.clear()
        print("===== Lista de Tarefas por Projeto =====")
        response = Commands.view_projects()
        if response.status_code == 200:
            projects = response.json()
            for project in projects:
                print(f"ID: {project['id']} - Nome: {project['name']}")
        else:
            print(response.json().get("error", "Erro ao buscar projetos!"))
            input("Pressione Enter para continuar...")
            return
        
        project_id = input("ID do Projeto: ")
        response = SESSION.get(f"{API_URL}/projects/{project_id}/tasks/")
        if response.status_code == 200:
            tasks = response.json()
            for task in tasks:
                print(f"ID: {task['id']} - Título: {task['title']} - Descrição: {task['description'] if task['description'] else 'Sem Descrição'}")
        else:
            print(response.json().get("error", "Erro ao buscar tarefas do projeto!"))
        input("Pressione Enter para continuar...")

CLI.menu_principal()
