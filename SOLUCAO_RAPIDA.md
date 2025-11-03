# 🚨 SOLUÇÃO RÁPIDA - Escopo Faltando

## O Problema

Você recebeu este erro:
```
Scope has changed from "... classroom.coursework.me.readonly" to "..."
```

**Está faltando 1 escopo!** Especificamente: `classroom.coursework.me.readonly`

---

## ✅ SOLUÇÃO EM 5 PASSOS

### PASSO 1: Acesse o Google Cloud Console

1. Abra: https://console.cloud.google.com/
2. **Selecione seu projeto** (o que você criou para o Classroom)

### PASSO 2: Vá para OAuth Consent Screen

1. No menu lateral esquerdo (☰), clique em:
   ```
   APIs & Services → OAuth consent screen
   ```

2. Você verá uma página com informações do seu app

### PASSO 3: Editar o App

1. Role a página e encontre o botão **"EDIT APP"** (pode estar escrito em português: "EDITAR APLICATIVO")
2. Clique nele

### PASSO 4: Adicionar o Escopo Faltante

1. Clique em **"SAVE AND CONTINUE"** até chegar na página **"Scopes"** (Escopos)

2. Na página de Scopes, clique no botão **"ADD OR REMOVE SCOPES"**

3. **IMPORTANTE**: Uma janela lateral vai abrir. Procure pelos seguintes escopos:

   Na caixa de busca, digite: `classroom`

4. **MARQUE EXATAMENTE ESTES 3 ESCOPOS** (confirme que todos estão marcados ✓):

   ```
   ✓ .../auth/classroom.courses.readonly
   ✓ .../auth/classroom.coursework.me.readonly          ← ESTE ESTÁ FALTANDO!
   ✓ .../auth/classroom.student-submissions.me.readonly
   ```

   **Descrições que você vai ver:**
   - "View your Google Classroom classes"
   - "View course work and grades for courses you teach or administer"
   - "View your course work and grades in Google Classroom"

5. Clique em **"UPDATE"** (Atualizar)

6. Clique em **"SAVE AND CONTINUE"** até finalizar

### PASSO 5: Deletar Token e Executar Novamente

1. **Delete o arquivo `token.pickle`** na pasta do projeto (se existir)

2. Execute o script novamente:
   ```bash
   python classroom_checker.py
   ```

3. Autorize novamente no navegador quando solicitado

---

## 🔍 COMO SABER SE DEU CERTO

Quando você clicar em "ADD OR REMOVE SCOPES", você deve ver **EXATAMENTE 3 escopos marcados**.

Se você ver algo como:
```
Selected scopes: 3
```

Está correto! ✅

Se aparecer:
```
Selected scopes: 2
```

Está faltando 1 escopo! ❌ (volte e adicione)

---

## 📸 Onde Encontrar Cada Coisa

```
Google Cloud Console (console.cloud.google.com)
│
├─ [Selecionar Projeto] ← No topo da página
│
└─ ☰ Menu Lateral
   └─ APIs & Services
      └─ OAuth consent screen
         └─ [Botão: EDIT APP]
            └─ Click "SAVE AND CONTINUE" até "Scopes"
               └─ [Botão: ADD OR REMOVE SCOPES]
                  └─ Marque os 3 escopos
                     └─ [Botão: UPDATE]
                        └─ [Botão: SAVE AND CONTINUE]
```

---

## ⚠️ ATENÇÃO

- Você DEVE adicionar os 3 escopos
- Você DEVE adicionar seu email como "Test User" (na próxima tela após Scopes)
- Você DEVE deletar o arquivo `token.pickle` antes de executar novamente

---

## 🆘 Ainda com Problemas?

Se após seguir todos os passos ainda der erro:

1. Verifique se a **Google Classroom API** está ativada:
   - Menu: **APIs & Services → Library**
   - Procure: **"Google Classroom API"**
   - Deve estar: **MANAGE** (verde) ou clique em **ENABLE**

2. Verifique se você está na lista de Test Users:
   - **OAuth consent screen** → seção **"Test users"**
   - Seu email deve estar listado lá

3. Tente criar novas credenciais:
   - Delete as antigas em **APIs & Services → Credentials**
   - Crie novas e baixe o novo `credentials.json`

---

Depois de adicionar o escopo, delete o `token.pickle` e tente novamente! 🚀
