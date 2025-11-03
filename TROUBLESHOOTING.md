# ⚠️ SOLUÇÃO: Erro de Escopos OAuth2

## Problema Encontrado

Você recebeu este erro:
```
Scope has changed from "..." to "..."
```

Isso significa que **nem todos os escopos necessários** foram adicionados corretamente no Google Cloud Console.

## 🔧 SOLUÇÃO PASSO A PASSO

### Etapa 1: Deletar o token antigo

Na pasta do projeto, **delete** o arquivo `token.pickle` se ele existir.

### Etapa 2: Reconfigurar os Escopos no Google Cloud Console

1. Acesse: https://console.cloud.google.com/

2. Selecione seu projeto (o que você criou para o Classroom Checker)

3. No menu lateral esquerdo, vá em:
   ```
   APIs & Services → OAuth consent screen
   ```

4. Role a página até a seção **"Scopes"**

5. Clique no botão **"EDIT APP"** (ou "EDITAR APLICATIVO")

6. Clique em **"SAVE AND CONTINUE"** até chegar na página de **"Scopes"**

7. Na seção de Scopes, clique em **"ADD OR REMOVE SCOPES"**

8. **IMPORTANTE**: Na caixa de busca, procure e marque **EXATAMENTE** estes 3 escopos:

   ✅ `https://www.googleapis.com/auth/classroom.courses.readonly`
   - Descrição: "View your Google Classroom classes"

   ✅ `https://www.googleapis.com/auth/classroom.coursework.me.readonly`
   - Descrição: "View course work and grades for courses you teach or administer"

   ✅ `https://www.googleapis.com/auth/classroom.student-submissions.me.readonly`
   - Descrição: "View your course work and grades in Google Classroom"

9. Clique em **"UPDATE"** (atualizar)

10. Clique em **"SAVE AND CONTINUE"** até finalizar

### Etapa 3: Adicionar-se como Usuário de Teste

Ainda no Google Cloud Console:

1. Na mesma página **"OAuth consent screen"**

2. Role até a seção **"Test users"**

3. Clique em **"ADD USERS"**

4. Digite **o email que você usa no Google Classroom** (sua conta de estudante)

5. Clique em **"SAVE"**

### Etapa 4: Verificar se a API está ativada

1. No menu lateral, vá em:
   ```
   APIs & Services → Library
   ```

2. Procure por **"Google Classroom API"**

3. Certifique-se de que está com o botão **"MANAGE"** (verde)
   - Se estiver "ENABLE", clique para ativar

### Etapa 5: Executar novamente o script

Agora execute:

```bash
python classroom_checker.py
```

O navegador abrirá novamente. **Authorize o acesso** e o script deve funcionar!

## 🚨 Se o erro persistir

### Opção 1: Criar novas credenciais

1. Vá em **APIs & Services → Credentials**
2. Delete a credencial antiga (OAuth 2.0 Client ID)
3. Crie uma nova:
   - Clique em **"CREATE CREDENTIALS"** → **"OAuth client ID"**
   - Tipo: **"Desktop app"**
   - Nome: "Classroom Checker"
   - Clique em **"CREATE"**
4. Baixe o novo JSON
5. Substitua o arquivo `credentials.json` na pasta do projeto

### Opção 2: Usar versão simplificada

Se ainda assim não funcionar, eu posso criar uma versão do script que usa menos escopos. Avise-me se precisar!

## 📸 Onde encontrar cada coisa

### Menu "APIs & Services"
```
Google Cloud Console
├── Navigation Menu (☰)
    └── APIs & Services
        ├── OAuth consent screen  ← Configure aqui
        ├── Credentials          ← Credenciais OAuth
        └── Library              ← Ative a API aqui
```

### Escopos para adicionar
Na tela "OAuth consent screen" → "Scopes" → "ADD OR REMOVE SCOPES", procure por:
- `classroom.courses.readonly`
- `classroom.coursework.me.readonly`
- `classroom.student-submissions.me.readonly`

## ✅ Checklist Final

Antes de executar novamente, verifique:

- [ ] Os 3 escopos foram adicionados corretamente
- [ ] Você está na lista de Test Users
- [ ] A Google Classroom API está ativada (ENABLED)
- [ ] O arquivo `token.pickle` foi deletado (se existia)
- [ ] O arquivo `credentials.json` está na pasta do projeto

Se tudo estiver certo, execute o script e deve funcionar! 🎉
