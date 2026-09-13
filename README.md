# MegaSurpresinhas 2.0

Aplicação web para geração de jogos da **Mega-Sena** e da **Lotofácil**, desenvolvida com Python e Flask. O projeto possui arquitetura modular, interface com recursos de PWA, histórico no navegador e execução em contêiner Docker.

> Os jogos são aleatórios. A ponderação por resultados anteriores não prevê sorteios nem aumenta a probabilidade matemática de premiação de uma combinação.

## Objetivo do projeto

Além de gerar jogos, o MegaSurpresinhas 2.0 é um projeto prático de aprendizado e evolução em desenvolvimento de software, aplicando:

- Python, Flask e desenvolvimento web;
- arquitetura modular, separação de responsabilidades e princípios de Clean Architecture;
- integração com API externa e tratamento de indisponibilidade;
- versionamento com Git e GitHub;
- qualidade de código, análise estática de segurança e práticas de CI/CD;
- conteinerização com Docker e publicação de imagens no Docker Hub.

## Funcionalidades

- Geração de dezenas ordenadas e sem repetição dentro de cada jogo.
- Seleção aleatória ponderada pela frequência das dezenas em concursos recentes.
- Consulta de resultados pela API externa, com cache JSON e geração uniforme como contingência.
- Histórico independente por modalidade, armazenado no `localStorage` do navegador.
- Armazenamento das últimas 30 gerações por modalidade e opção de limpar o histórico.
- Alternância entre temas claro e escuro.
- Recursos de PWA com service worker e página de indisponibilidade.
- Endpoint de verificação de atividade da aplicação.

### Limites implementados

Os valores abaixo são os limites definidos **nesta aplicação**.

| Modalidade | Faixa das dezenas | Dezenas por jogo | Jogos por geração | Concursos recentes consultados |
| --- | --- | --- | --- | --- |
| Mega-Sena | 1 a 60 | 6 a 12 | 1 a 12 | 10 |
| Lotofácil | 1 a 25 | 15 a 20 | 1 | 3 |

## Tecnologias

| Tecnologia | Uso |
| --- | --- |
| Python 3.11 ou superior | Linguagem da aplicação |
| Flask | Rotas HTTP e renderização de templates |
| Requests | Consulta à API de loterias |
| platformdirs | Localização do diretório de cache |
| HTML, CSS e JavaScript | Interface, tema e histórico local |
| Gunicorn | Servidor WSGI para execução em produção |
| Docker | Empacotamento e execução em contêiner |
| GitHub Actions e Ruff | Automação e análise de qualidade |
| CodeQL | Análise estática de segurança, conforme configuração do GitHub |

As dependências estão declaradas em [pyproject.toml](pyproject.toml) e [requirements.txt](requirements.txt).

## Executar localmente

Requisitos: **Python 3.11 ou superior** e **Git**.

### 1. Clonar o repositório

```bash
git clone https://github.com/DavidMaciel86/megasurpresinhas2.0.git
cd megasurpresinhas2.0
```

### 2. Criar e ativar o ambiente virtual

**Windows — PowerShell:**

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**Linux/macOS:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instalar as dependências e o pacote

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install -e .
```

A instalação editável (`-e .`) permite importar o pacote localizado em `src/` e refletir alterações no código durante o desenvolvimento.

### 4. Iniciar a aplicação

```bash
python run.py
```

Acesse [http://127.0.0.1:5000](http://127.0.0.1:5000).

O comando utiliza o servidor de desenvolvimento do Flask.

## Configuração

As configurações são lidas das variáveis de ambiente em [config.py](src/megasurpresinhas2_0/config.py).

O arquivo [.env.example](.env.example) serve como referência. **Copiar esse arquivo para `.env` não carrega as variáveis automaticamente ao executar `python run.py`.** Defina-as no terminal ou na plataforma de execução. Com Docker, é possível fornecê-las explicitamente por `--env-file`.

| Variável | Padrão | Finalidade |
| --- | --- | --- |
| `FLASK_ENV` | `production` | O valor `development` ativa o debug; use apenas localmente |
| `APP_HOST` | `127.0.0.1` | Endereço do servidor iniciado por `run.py` |
| `APP_PORT` | `5000` | Porta do servidor iniciado por `run.py` |
| `APP_LOG_LEVEL` | `INFO` | Nível de registro da aplicação |
| `LOTTERY_API_BASE_URL` | `https://api.guidi.dev.br/loteria` | Endereço-base do provedor de resultados |
| `API_CONNECT_TIMEOUT` | `3.05` | Tempo limite de conexão, em segundos |
| `API_READ_TIMEOUT` | `10` | Tempo limite de leitura, em segundos |
| `CACHE_DIR` | Diretório de cache do usuário, via platformdirs | Caminho do cache técnico em JSON |
| `PORT` | `8000` no Docker | Porta utilizada pelo Gunicorn no comando do contêiner |


## Arquitetura

O pacote principal está em [src/megasurpresinhas2_0](src/megasurpresinhas2_0).

| Caminho | Responsabilidade |
| --- | --- |
| `domain/` | Regras das modalidades, validação e geração de jogos |
| `application/` | Caso de uso de geração, DTO e contratos de integração |
| `infrastructure/` | Cliente HTTP da API e repositório de cache JSON |
| `web/` | Rotas Flask, templates, CSS, JavaScript e recursos da PWA |
| `app.py` | Fábrica `create_app()`, composição das dependências e cabeçalhos HTTP |
| `config.py` | Configurações obtidas do ambiente |
| `run.py` na raiz | Entrada para execução local |
| `wsgi.py` na raiz | Entrada WSGI utilizada pelo Gunicorn |
| `.github/workflows/` | Automações de CI, entrega e alertas |

O domínio permanece independente de Flask, HTTP e persistência. A camada de aplicação coordena a obtenção dos dados e a geração; a infraestrutura implementa o acesso à API e ao cache.

### Origem dos dados e geração

1. A aplicação tenta consultar os concursos recentes da modalidade na API externa.
2. Quando a consulta funciona, utiliza os dados e tenta atualizar o cache técnico.
3. Se a API estiver indisponível, tenta recuperar os dados do cache.
4. Sem dados da API e sem cache utilizável, gera jogos com distribuição uniforme.

Quando há histórico disponível, cada dezena recebe peso igual à sua frequência nos resultados consultados **mais 1**. A seleção ocorre sem reposição dentro de cada jogo. Essa regra influencia os palpites gerados, mas não representa previsão do próximo sorteio.

### Histórico, cache e uso offline

- **Histórico de jogos:** fica no navegador, por modalidade, e não é gravado no servidor. Não há sincronização entre dispositivos.
- **Cache técnico:** guarda dados de resultados consultados para contingência da API externa.
- **PWA:** mantém recursos da interface em cache. Gerar novos jogos exige conexão com o servidor.

O modo `fallback` trata a ausência de dados da API/cache; ele não significa geração de jogos sem conexão entre navegador e o servidor de deploy da aplicação.

## Rotas principais

| Método | Rota | Finalidade |
| --- | --- | --- |
| GET | `/` | Página da Mega-Sena |
| GET | `/lotofacil` | Página da Lotofácil |
| POST | `/gerar/megasena` | Geração de jogos da Mega-Sena |
| POST | `/gerar/lotofacil` | Geração de jogo da Lotofácil |
| GET | `/health/live` | Retorna `{"status":"ok"}` |
| GET | `/offline` | Página de indisponibilidade |
| GET | `/sw.js` | Service worker |

As rotas de geração recebem os campos de formulário `games` e `picks` e retornam HTML. O endpoint de saúde verifica a atividade da aplicação; ele não consulta a API externa.

## Qualidade e verificação

### Ruff

Instale a ferramenta e execute a análise:

```bash
python -m pip install ruff
ruff check .
```

Para aplicar as correções automáticas suportadas, revise as alterações e execute novamente:

```bash
ruff check . --fix
ruff check .
```

### Verificação manual

O repositório ainda não possui uma suíte de testes automatizados versionada. Para validar o comportamento:

- Abra as páginas da Mega-Sena e da Lotofácil.
- Gere jogos nos limites permitidos e confira quantidade, faixa e ausência de dezenas repetidas em cada jogo.
- Envie entradas inválidas e confira as mensagens de validação.
- Confira o histórico separado por modalidade e a opção de limpeza.
- Alterne entre os temas claro e escuro.
- Consulte `/health/live` e confira o JSON retornado.
- Simule indisponibilidade da API para conferir o uso de cache e, sem cache, o modo uniforme.
- Confira `/offline` e o comportamento da interface sem conexão.

## CI/CD e alertas

### Integração contínua

O workflow [ci.yml](.github/workflows/ci.yml) executa o Ruff em Pull Requests direcionadas à branch `main`, usando Python 3.11.

A análise de segurança com **CodeQL** é descrita no projeto como configurada pelo *Default Setup* do GitHub, fora dos arquivos de workflow versionados.

### Entrega de imagem Docker

O workflow [cd.yml](.github/workflows/cd.yml) é acionado por pushes na `main` e possui dois jobs:

| Job | Etapas |
| --- | --- |
| `deliver` | Faz checkout, constrói a imagem, salva o arquivo `megasurpresinhas2.0.tar` e publica o artefato `megasurpresinhas-docker-image` |
| `deploy` | Baixa o artefato, carrega a imagem, autentica no Docker Hub e publica `<DOCKERHUB_USERNAME>/megasurpresinhas2.0:latest` |

O pipeline já implementa a publicação da imagem no Docker Hub. **Ainda não há, nesse workflow, uma etapa de implantação da aplicação em um servidor ou plataforma de hospedagem.**

### Alertas no Discord

O workflow [discord-alert.yml](.github/workflows/discord-alert.yml) acompanha a conclusão dos workflows `Continuous Integration` e `CodeQL`, com etapas de notificação de sucesso ou falha no Discord.

### Secrets utilizados pelos workflows

Configure os valores como secrets do repositório no GitHub:

| Secret | Uso |
| --- | --- |
| `DOCKERHUB_USERNAME` | Usuário do Docker Hub para autenticação e tag da imagem |
| `DOCKERHUB_TOKEN` | Token utilizado para publicar a imagem |
| `DISCORD_WEBHOOK` | URL do webhook para os alertas no Discord |

Esses secrets pertencem às automações do GitHub Actions e não são necessários para executar a aplicação localmente. Não inclua seus valores no código ou no README.

## Evoluções futuras

- Adicionar testes automatizados de domínio, aplicação e interface HTTP.
- Adicionar checagem de tipos e auditoria de dependências.
- Evoluir da publicação da imagem para implantação em um ambiente de hospedagem.
- Explorar uma interface conversacional com IA, reutilizando as funcionalidades existentes como ferramentas.

A proposta da interface conversacional é permitir a geração de palpites e a consulta de resultados em linguagem natural, preservando a separação entre domínio, aplicação, infraestrutura e interface. Essa funcionalidade ainda não está implementada.

## Autor

Desenvolvido por [David Maciel](https://github.com/DavidMaciel86).
