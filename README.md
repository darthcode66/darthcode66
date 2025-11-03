# Google Classroom - Verificador de Atividades Pendentes

Este projeto permite verificar todas as suas atividades pendentes no Google Classroom através de um script Python que usa a API oficial do Google.

## 📋 Funcionalidades

- 🔍 Lista todos os cursos ativos
- 📚 Verifica atividades não entregues em cada curso
- ⏰ Mostra prazos de entrega
- 🔴 Identifica atividades atrasadas
- 📊 Exibe pontuação máxima de cada atividade
- 🔗 Fornece links diretos para as atividades

## ⚠️ Problemas ou Erros?

**Se você receber erros de escopos/permissões**, consulte o arquivo **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** com instruções detalhadas de solução de problemas.

## 🚀 Instalação

### 1. Pré-requisitos

- Python 3.7 ou superior
- Uma conta Google com acesso ao Google Classroom

### 2. Clone o repositório e instale as dependências

```bash
# Clone o repositório
git clone <url-do-repositorio>
cd darthcode66

# Crie um ambiente virtual (recomendado)
python3 -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate

# Instale as dependências
pip install -r requirements.txt
```

## 🔑 Configuração do Google Cloud Console

Para usar este script, você precisa criar credenciais OAuth2 no Google Cloud Console. Siga os passos abaixo:

### Passo 1: Criar um Projeto no Google Cloud

1. Acesse o [Google Cloud Console](https://console.cloud.google.com/)
2. Clique em **"Select a project"** no topo da página
3. Clique em **"NEW PROJECT"**
4. Digite um nome para o projeto (ex: "Classroom Checker")
5. Clique em **"CREATE"**

### Passo 2: Ativar a API do Google Classroom

1. No menu lateral, vá em **"APIs & Services"** > **"Library"**
2. Pesquise por **"Google Classroom API"**
3. Clique na API e depois em **"ENABLE"**

### Passo 3: Configurar a Tela de Consentimento OAuth

1. No menu lateral, vá em **"APIs & Services"** > **"OAuth consent screen"**
2. Selecione **"External"** como User Type
3. Clique em **"CREATE"**
4. Preencha os campos obrigatórios:
   - **App name**: Nome da sua aplicação (ex: "Classroom Checker")
   - **User support email**: Seu e-mail
   - **Developer contact information**: Seu e-mail
5. Clique em **"SAVE AND CONTINUE"**
6. Na seção **"Scopes"**, clique em **"ADD OR REMOVE SCOPES"**
7. Procure e adicione os seguintes escopos:
   - `https://www.googleapis.com/auth/classroom.courses.readonly`
   - `https://www.googleapis.com/auth/classroom.coursework.me.readonly`
   - `https://www.googleapis.com/auth/classroom.student-submissions.me.readonly`
8. Clique em **"UPDATE"** e depois **"SAVE AND CONTINUE"**
9. Na seção **"Test users"**, clique em **"ADD USERS"**
10. Adicione seu e-mail do Google (o que você usa no Classroom)
11. Clique em **"SAVE AND CONTINUE"**

### Passo 4: Criar Credenciais OAuth2

1. No menu lateral, vá em **"APIs & Services"** > **"Credentials"**
2. Clique em **"CREATE CREDENTIALS"** > **"OAuth client ID"**
3. Selecione **"Desktop app"** como Application type
4. Digite um nome (ex: "Classroom Desktop Client")
5. Clique em **"CREATE"**
6. Na janela que aparecer, clique em **"DOWNLOAD JSON"**
7. **IMPORTANTE**: Renomeie o arquivo baixado para `credentials.json`
8. Mova o arquivo `credentials.json` para a pasta raiz deste projeto

### Estrutura do arquivo credentials.json

O arquivo deve estar no mesmo diretório que o `classroom_checker.py`:

```
darthcode66/
├── classroom_checker.py
├── credentials.json       ← Arquivo baixado do Google Cloud
├── requirements.txt
└── README.md
```

## 🎯 Como Usar

### Primeira Execução

Na primeira vez que você executar o script, ele abrirá uma janela do navegador para você autorizar o acesso:

```bash
python classroom_checker.py
```

1. Uma janela do navegador será aberta
2. Faça login com sua conta do Google (a mesma que você usa no Classroom)
3. Clique em **"Permitir"** para autorizar o acesso
4. Você pode fechar a janela do navegador após a autorização
5. O script criará um arquivo `token.pickle` que armazenará suas credenciais

### Execuções Seguintes

Nas próximas execuções, o script usará o token salvo e não pedirá autorização novamente:

```bash
python classroom_checker.py
```

### Saída Esperada

O script exibirá algo assim:

```
🎓 Google Classroom - Verificador de Atividades Pendentes

Buscando seus cursos...
Encontrados 3 curso(s) ativo(s).

Verificando atividades pendentes...
  • Verificando: Matemática
  • Verificando: Português
  • Verificando: História

================================================================================
ATIVIDADES PENDENTES NO GOOGLE CLASSROOM
================================================================================

Total: 5 atividade(s) pendente(s)

────────────────────────────────────────────────────────────────────────────────
📚 CURSO: Matemática
────────────────────────────────────────────────────────────────────────────────
   2 atividade(s) pendente(s)

🔴 1. Lista de Exercícios - Álgebra
   Status: ATRASADA
   Prazo: 25/10/2025 às 23:59
   Pontos: 10.0
   Link: https://classroom.google.com/c/...

🟡 2. Trabalho sobre Geometria
   Status: PENDENTE
   Prazo: 05/11/2025
   Pontos: 15.0
   Link: https://classroom.google.com/c/...

================================================================================
```

## 🔒 Segurança

- **NUNCA** compartilhe seus arquivos `credentials.json` ou `token.pickle`
- Estes arquivos estão no `.gitignore` para evitar commits acidentais
- Se você acidentalmente compartilhar suas credenciais, revogue-as imediatamente no [Google Cloud Console](https://console.cloud.google.com/)

## 🐛 Solução de Problemas

### Erro de Escopos/Permissões

Se você receber um erro como:
```
Scope has changed from "..." to "..."
```

**SOLUÇÃO RÁPIDA:**
1. Delete o arquivo `token.pickle`
2. Veja o arquivo **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** para instruções detalhadas

### Erro: "credentials.json não encontrado"

Certifique-se de que você:
1. Baixou o arquivo de credenciais do Google Cloud Console
2. Renomeou para `credentials.json`
3. Colocou na mesma pasta do script

### Outros Problemas

Para todos os outros problemas, consulte o guia completo: **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)**

## 📝 Notas

- Este script é **somente leitura** - ele não modifica nada no Google Classroom
- As credenciais são armazenadas localmente e nunca são enviadas para servidores terceiros
- O script funciona com qualquer conta Google que tenha acesso ao Classroom

## 🤝 Contribuindo

Sinta-se à vontade para abrir issues ou pull requests com melhorias!

## 📄 Licença

Este projeto é de código aberto e está disponível para uso educacional.
