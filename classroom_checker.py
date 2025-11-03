#!/usr/bin/env python3
"""
Google Classroom - Verificador de Atividades Pendentes

Este script conecta-se à API do Google Classroom e lista todas as atividades
que ainda não foram entregues pelo usuário.
"""

import os.path
import pickle
from datetime import datetime
from typing import List, Dict, Any

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Escopos necessários para acessar o Google Classroom
SCOPES = [
    'https://www.googleapis.com/auth/classroom.courses.readonly',
    'https://www.googleapis.com/auth/classroom.coursework.me.readonly',
    'https://www.googleapis.com/auth/classroom.student-submissions.me.readonly'
]

# Arquivos de credenciais
CREDENTIALS_FILE = 'credentials.json'
TOKEN_FILE = 'token.pickle'


def authenticate() -> Credentials:
    """
    Autentica o usuário com a API do Google Classroom.

    Returns:
        Credentials: Credenciais autenticadas do usuário
    """
    creds = None

    # O arquivo token.pickle armazena os tokens de acesso e refresh do usuário
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, 'rb') as token:
            creds = pickle.load(token)

    # Se não há credenciais válidas, faça login
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("Atualizando token de acesso...")
            try:
                creds.refresh(Request())
            except Exception as e:
                print(f"⚠️  Erro ao atualizar token: {e}")
                print("Deletando token antigo e solicitando nova autenticação...\n")
                if os.path.exists(TOKEN_FILE):
                    os.remove(TOKEN_FILE)
                creds = None

        if not creds or not creds.valid:
            if not os.path.exists(CREDENTIALS_FILE):
                raise FileNotFoundError(
                    f"Arquivo '{CREDENTIALS_FILE}' não encontrado. "
                    "Por favor, baixe suas credenciais OAuth2 do Google Cloud Console."
                )
            print("Iniciando processo de autenticação...")
            print("Uma janela do navegador será aberta para você autorizar o acesso.\n")
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_FILE, SCOPES
            )
            creds = flow.run_local_server(port=0)

        # Salva as credenciais para a próxima execução
        with open(TOKEN_FILE, 'wb') as token:
            pickle.dump(creds, token)
        print("✅ Autenticação concluída!\n")

    return creds


def get_active_courses(service) -> List[Dict[str, Any]]:
    """
    Obtém a lista de cursos ativos do usuário.

    Args:
        service: Serviço da API do Google Classroom

    Returns:
        Lista de cursos ativos
    """
    try:
        results = service.courses().list(
            courseStates=['ACTIVE'],
            pageSize=100
        ).execute()

        courses = results.get('courses', [])
        return courses
    except HttpError as error:
        print(f"Erro ao buscar cursos: {error}")
        return []


def get_pending_coursework(service, course_id: str, user_id: str = 'me') -> List[Dict[str, Any]]:
    """
    Obtém atividades pendentes de um curso específico.

    Args:
        service: Serviço da API do Google Classroom
        course_id: ID do curso
        user_id: ID do usuário (padrão: 'me' para o usuário atual)

    Returns:
        Lista de atividades pendentes
    """
    pending_work = []

    try:
        # Busca todas as atividades do curso
        coursework_results = service.courses().courseWork().list(
            courseId=course_id,
            pageSize=100
        ).execute()

        courseworks = coursework_results.get('courseWork', [])

        for coursework in courseworks:
            coursework_id = coursework['id']

            # Verifica o status da submissão do aluno
            submission = service.courses().courseWork().studentSubmissions().list(
                courseId=course_id,
                courseWorkId=coursework_id,
                userId=user_id
            ).execute()

            submissions = submission.get('studentSubmissions', [])

            for sub in submissions:
                # Verifica se a atividade não foi entregue
                state = sub.get('state', '')
                if state in ['NEW', 'CREATED', 'RECLAIMED_BY_STUDENT']:
                    # Prepara informações sobre a atividade
                    work_info = {
                        'title': coursework.get('title', 'Sem título'),
                        'description': coursework.get('description', ''),
                        'due_date': coursework.get('dueDate'),
                        'due_time': coursework.get('dueTime'),
                        'state': state,
                        'link': coursework.get('alternateLink', ''),
                        'max_points': coursework.get('maxPoints', 0)
                    }
                    pending_work.append(work_info)

        return pending_work

    except HttpError as error:
        print(f"Erro ao buscar atividades do curso {course_id}: {error}")
        return []


def format_due_date(due_date: Dict, due_time: Dict = None) -> str:
    """
    Formata a data de entrega de uma atividade.

    Args:
        due_date: Dicionário com a data (year, month, day)
        due_time: Dicionário com o horário (hours, minutes)

    Returns:
        String formatada com a data/hora de entrega
    """
    if not due_date:
        return "Sem prazo definido"

    try:
        year = due_date.get('year')
        month = due_date.get('month')
        day = due_date.get('day')

        date_obj = datetime(year, month, day)
        date_str = date_obj.strftime('%d/%m/%Y')

        if due_time:
            hours = due_time.get('hours', 23)
            minutes = due_time.get('minutes', 59)
            time_str = f"{hours:02d}:{minutes:02d}"
            return f"{date_str} às {time_str}"

        return date_str
    except (ValueError, TypeError):
        return "Data inválida"


def is_overdue(due_date: Dict, due_time: Dict = None) -> bool:
    """
    Verifica se uma atividade está atrasada.

    Args:
        due_date: Dicionário com a data (year, month, day)
        due_time: Dicionário com o horário (hours, minutes)

    Returns:
        True se está atrasada, False caso contrário
    """
    if not due_date:
        return False

    try:
        year = due_date.get('year')
        month = due_date.get('month')
        day = due_date.get('day')
        hours = due_time.get('hours', 23) if due_time else 23
        minutes = due_time.get('minutes', 59) if due_time else 59

        due_datetime = datetime(year, month, day, hours, minutes)
        return datetime.now() > due_datetime
    except (ValueError, TypeError):
        return False


def display_pending_work(courses_work: Dict[str, List[Dict]]):
    """
    Exibe as atividades pendentes de forma organizada.

    Args:
        courses_work: Dicionário com cursos e suas atividades pendentes
    """
    total_pending = sum(len(work) for work in courses_work.values())

    print("=" * 80)
    print(f"ATIVIDADES PENDENTES NO GOOGLE CLASSROOM")
    print("=" * 80)
    print(f"\nTotal: {total_pending} atividade(s) pendente(s)\n")

    if total_pending == 0:
        print("🎉 Parabéns! Você não tem atividades pendentes!\n")
        return

    for course_name, pending_work in courses_work.items():
        if not pending_work:
            continue

        print(f"\n{'─' * 80}")
        print(f"📚 CURSO: {course_name}")
        print(f"{'─' * 80}")
        print(f"   {len(pending_work)} atividade(s) pendente(s)\n")

        for idx, work in enumerate(pending_work, 1):
            overdue = is_overdue(work['due_date'], work['due_time'])
            status_icon = "🔴" if overdue else "🟡"
            status_text = "ATRASADA" if overdue else "PENDENTE"

            print(f"{status_icon} {idx}. {work['title']}")
            print(f"   Status: {status_text}")
            print(f"   Prazo: {format_due_date(work['due_date'], work['due_time'])}")

            if work['max_points']:
                print(f"   Pontos: {work['max_points']}")

            if work['description']:
                desc = work['description'][:100]
                if len(work['description']) > 100:
                    desc += "..."
                print(f"   Descrição: {desc}")

            print(f"   Link: {work['link']}")
            print()

    print("=" * 80)


def main():
    """
    Função principal do script.
    """
    print("\n🎓 Google Classroom - Verificador de Atividades Pendentes\n")

    try:
        # Autentica o usuário
        creds = authenticate()

        # Constrói o serviço da API
        service = build('classroom', 'v1', credentials=creds)

        print("Buscando seus cursos...")
        courses = get_active_courses(service)

        if not courses:
            print("Nenhum curso ativo encontrado.")
            return

        print(f"Encontrados {len(courses)} curso(s) ativo(s).\n")
        print("Verificando atividades pendentes...\n")

        # Dicionário para armazenar atividades pendentes por curso
        courses_work = {}

        for course in courses:
            course_name = course.get('name', 'Sem nome')
            course_id = course['id']

            print(f"  • Verificando: {course_name}")

            pending_work = get_pending_coursework(service, course_id)

            if pending_work:
                courses_work[course_name] = pending_work

        print()

        # Exibe as atividades pendentes
        display_pending_work(courses_work)

    except FileNotFoundError as e:
        print(f"\n❌ Erro: {e}\n")
    except Exception as e:
        error_msg = str(e).lower()

        # Verifica se é erro relacionado a escopos
        if 'scope' in error_msg or 'permission' in error_msg or 'access' in error_msg:
            print(f"\n❌ ERRO DE PERMISSÕES/ESCOPOS: {e}\n")
            print("=" * 80)
            print("🔧 SOLUÇÃO:")
            print("=" * 80)
            print()
            print("1. Delete o arquivo 'token.pickle' (se existir)")
            print("2. Verifique se adicionou TODOS os 3 escopos no Google Cloud Console:")
            print("   • classroom.courses.readonly")
            print("   • classroom.coursework.me.readonly")
            print("   • classroom.student-submissions.me.readonly")
            print()
            print("3. Verifique se adicionou seu email como 'Test User'")
            print("4. Execute o script novamente")
            print()
            print("📖 Para instruções detalhadas, veja: TROUBLESHOOTING.md")
            print("=" * 80)
            print()
        else:
            print(f"\n❌ Erro inesperado: {e}\n")
            print("💡 Se o erro persistir, consulte o arquivo TROUBLESHOOTING.md\n")


if __name__ == '__main__':
    main()
