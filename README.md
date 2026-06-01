# EduTrack AI

Sistema academico em Streamlit integrado ao Xano, com painel, professores, disciplinas, tarefas, notas, perfil, assistente de IA e automacoes inteligentes.

## Rodar o projeto

`
```

Se preferir instalar dependencias novamente:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

## Modulos de IA e automacao

- `AI Assistant`: analisa notas por disciplina, identifica risco de media abaixo de 6, recomenda estudos e cria cronograma semanal.
- `Automações`: mostra progresso de tarefas, boletim semanal, sugestoes automaticas, estrutura pronta para Google Calendar e cronograma automatico.

## Integracoes preparadas

- Xano para autenticação e CRUD.
- Google Calendar por payload pronto para envio a uma API externa.
- Gmail, WhatsApp e Telegram podem usar a mesma camada de automacoes.
