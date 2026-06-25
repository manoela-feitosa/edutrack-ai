# EduTrack

![Python](https://img.shields.io/badge/Python-3.12+-3776AB?style=flat-square&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.58-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)
![Status](https://img.shields.io/badge/Status-Em%20desenvolvimento-F59E0B?style=flat-square)

O **EduTrack** é uma aplicação desenvolvida em Python e Streamlit para auxiliar estudantes na organização acadêmica. O sistema centraliza disciplinas, professores, tarefas e notas em uma interface moderna, integrada ao backend [Xano](https://www.xano.com/) via API REST.

## Funcionalidades

- Gerenciamento de disciplinas
- Cadastro de professores
- Controle de tarefas e prazos
- Registro de notas
- Acompanhamento do desempenho acadêmico
- Perfil do estudante
- Interface moderna e intuitiva

## Interface do sistema

Elementos visuais utilizados na aplicação:

<p align="center">
  <img src="assets/books-left.png" alt="Ilustração temática da tela de login do EduTrack" width="420">
</p>

<p align="center">
  <img src="assets/space-bg.png" alt="Fundo ambiente do painel principal do EduTrack" width="600">
</p>

## Tecnologias utilizadas

| Tecnologia | Uso no projeto |
|------------|----------------|
| Python | Linguagem principal |
| Streamlit | Interface web interativa |
| Xano | Backend e banco de dados |
| Pandas | Manipulação e exibição de dados |
| Plotly | Gráficos no dashboard |
| Requests | Comunicação com a API |
| Git/GitHub | Controle de versão e hospedagem |

## Status do projeto

O EduTrack encontra-se em **desenvolvimento ativo**. O projeto permanece em desenvolvimento contínuo e novas funcionalidades estão sendo implementadas gradualmente.

Entre as frentes de trabalho atuais estão:

- Aprimoramento da interface
- Correções de bugs
- Melhorias nas validações dos formulários
- Evolução do sistema de notas
- Otimização da integração com o Xano

## Aprendizados

Durante o desenvolvimento deste projeto, foram consolidados conhecimentos em:

- Python
- Streamlit
- Consumo de APIs
- Integração com Xano
- Manipulação de dados com Pandas
- Organização de projetos
- Git e GitHub

## Próximas melhorias

- [ ] Integração com Google Calendar
- [ ] Exportação de relatórios em PDF
- [ ] Melhorias na experiência do usuário
- [ ] Dashboard com mais métricas
- [ ] Novas funcionalidades de produtividade acadêmica

## Como executar o projeto

### Clonar o repositório

```bash
git clone https://github.com/manoela-feitosa/edutrack-ai.git
cd edutrack-ai
```

### Criar ambiente virtual

```bash
python -m venv .venv
```

**Windows:**

```powershell
.venv\Scripts\activate
```

**Linux/macOS:**

```bash
source .venv/bin/activate
```

### Instalar dependências

```bash
pip install -r requirements.txt
```

### Executar o projeto

```bash
streamlit run app.py
```

O arquivo principal da aplicação é `app.py`, na raiz do projeto.
