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
- conteinerização com Docker e publicação de imagens no Docker Hub;
- implantação em nuvem com Render, mantendo o serviço acessível por HTTPS.

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
| ---------- | ----------------- | ---------------- | ----------------- | ------------------------------ |
| Mega-Sena  | 1 a 60            | 6 a 12           | 1 a 12            | 10                             |
| Lotofácil  | 1 a 25            | 15 a 20          | 1                 | 3                              |

## Tecnologias

| Tecnologia              | Uso                                                            |
| ----------------------- | -------------------------------------------------------------- |
| Python 3.11 ou superior | Linguagem da aplicação                                         |
| Flask                   | Rotas HTTP e renderização de templates                         |
| Requests                | Consulta à API de loterias                                     |
| platformdirs            | Localização do diretório de cache                              |
| HTML, CSS e JavaScript  | Interface, tema e histórico local                              |
| Gunicorn                | Servidor WSGI para execução em produção                        |
| Docker                  | Empacotamento e execução em contêiner                          |
| Render                  | Hospedagem do serviço web em nuvem                             |
| Pytest                  | Testes automatizados de domínio e interface HTTP               |
| GitHub Actions e Ruff   | Automação, CI e análise de qualidade                           |
| CodeQL                  | Análise estática de segurança, conforme configuração do GitHub |

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

## Deploy em produção

A aplicação está publicada no **Render** como Web Service e utiliza o `Dockerfile` da raiz do repositório para construir e iniciar o contêiner.

- **URL:** https://megasurpresinhas.onrender.com
- **Branch de produção:** `main`
- **Runtime:** Docker
- **Servidor:** Gunicorn
- **Health check:** `GET /health/live`

O contêiner inicia o Gunicorn escutando em `0.0.0.0` e utiliza a variável `PORT` fornecida pelo ambiente de execução. No plano gratuito, o serviço pode entrar em inatividade após um período sem acessos e levar alguns segundos para responder na primeira requisição após o *spin down*.

## Configuração

As configurações são lidas das variáveis de ambiente em [config.py](src/megasurpresinhas2_0/config.py).

O arquivo [.env.example](.env.example) serve como referência. **Copiar esse arquivo para `.env` não carrega as variáveis automaticamente ao executar `python run.py`.** Defina-as no terminal ou na plataforma de execução. Com Docker, é possível fornecê-las explicitamente por `--env-file`.

| Variável               | Padrão                                          | Finalidade                                                 |
| ---------------------- | ----------------------------------------------- | ---------------------------------------------------------- |
| `FLASK_ENV`            | `production`                                    | O valor `development` ativa o debug; use apenas localmente |
| `APP_HOST`             | `127.0.0.1`                                     | Endereço do servidor iniciado por `run.py`                 |
| `APP_PORT`             | `5000`                                          | Porta do servidor iniciado por `run.py`                    |
| `APP_LOG_LEVEL`        | `INFO`                                          | Nível de registro da aplicação                             |
| `LOTTERY_API_BASE_URL` | `https://api.guidi.dev.br/loteria`              | Endereço-base do provedor de resultados                    |
| `API_CONNECT_TIMEOUT`  | `3.05`                                          | Tempo limite de conexão, em segundos                       |
| `API_READ_TIMEOUT`     | `10`                                            | Tempo limite de leitura, em segundos                       |
| `CACHE_DIR`            | Diretório de cache do usuário, via platformdirs | Caminho do cache técnico em JSON                           |
| `PORT`                 | `8000` no Docker                                | Porta utilizada pelo Gunicorn no comando do contêiner      |

## Arquitetura

O pacote principal está em [src/megasurpresinhas2_0](src/megasurpresinhas2_0).

| Caminho              | Responsabilidade                                                      |
| -------------------- | --------------------------------------------------------------------- |
| `domain/`            | Regras das modalidades, validação e geração de jogos                  |
| `application/`       | Caso de uso de geração, DTO e contratos de integração                 |
| `infrastructure/`    | Cliente HTTP da API e repositório de cache JSON                       |
| `web/`               | Rotas Flask, templates, CSS, JavaScript e recursos da PWA             |
| `app.py`             | Fábrica `create_app()`, composição das dependências e cabeçalhos HTTP |
| `config.py`          | Configurações obtidas do ambiente                                     |
| `run.py` na raiz     | Entrada para execução local                                           |
| `wsgi.py` na raiz    | Entrada WSGI utilizada pelo Gunicorn                                  |
| `.github/workflows/` | Automações de CI, entrega e alertas                                   |

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

| Método | Rota               | Finalidade                    |
| ------ | ------------------ | ----------------------------- |
| GET    | `/`                | Página da Mega-Sena           |
| GET    | `/lotofacil`       | Página da Lotofácil           |
| POST   | `/gerar/megasena`  | Geração de jogos da Mega-Sena |
| POST   | `/gerar/lotofacil` | Geração de jogo da Lotofácil  |
| GET    | `/health/live`     | Retorna `{"status":"ok"}`     |
| GET    | `/offline`         | Página de indisponibilidade   |
| GET    | `/sw.js`           | Service worker                |

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

### Pytest

O projeto possui uma suíte de testes automatizados versionada em `tests/`, incluindo testes das regras de domínio e das rotas web. Para executar:

```bash
python -m pip install -r requirements-dev.txt
python -m pytest -v
```

### Verificação manual

Além dos testes automatizados, algumas validações continuam úteis para conferir a experiência completa no navegador:

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

O workflow [ci.yml](.github/workflows/ci.yml) é executado em Pull Requests direcionadas à branch `main`, usando Python 3.11. O job de CI instala as dependências de desenvolvimento, executa o **Ruff** e roda a suíte de testes com **Pytest** antes da integração.

A análise de segurança com **CodeQL** é descrita no projeto como configurada pelo *Default Setup* do GitHub, fora dos arquivos de workflow versionados.

### Entrega de imagem Docker

O workflow [cd.yml](.github/workflows/cd.yml) é acionado por pushes na `main` e possui dois jobs:

| Job       | Etapas                                                                                                                          |
| --------- | ------------------------------------------------------------------------------------------------------------------------------- |
| `deliver` | Faz checkout, constrói a imagem, salva o arquivo `megasurpresinhas2.0.tar` e publica o artefato `megasurpresinhas-docker-image` |
| `deploy`  | Baixa o artefato, carrega a imagem, autentica no Docker Hub e publica `<DOCKERHUB_USERNAME>/megasurpresinhas2.0:latest`         |

O pipeline já implementa a publicação da imagem no Docker Hub. A aplicação também está implantada no Render, porém essa implantação é atualmente configurada diretamente no serviço da plataforma e **não faz parte do workflow `cd.yml`**.

### Implantação no Render

O Web Service de produção está conectado ao repositório `megasurpresinhas2.0`, branch `main`, e utiliza o `Dockerfile` versionado no projeto. Isso separa duas responsabilidades:

- **GitHub Actions:** validação, construção e publicação da imagem Docker;
- **Render:** hospedagem e execução da aplicação web em produção.

Uma evolução futura possível é tornar essa etapa de implantação mais declarativa e automatizada, por exemplo com configuração versionada da infraestrutura e gatilhos de deploy controlados pelo pipeline.

### Alertas no Discord

O workflow [discord-alert.yml](.github/workflows/discord-alert.yml) acompanha a conclusão dos workflows `Continuous Integration` e `CodeQL`, com etapas de notificação de sucesso ou falha no Discord.

### Secrets utilizados pelos workflows

Configure os valores como secrets do repositório no GitHub:

| Secret               | Uso                                                     |
| -------------------- | ------------------------------------------------------- |
| `DOCKERHUB_USERNAME` | Usuário do Docker Hub para autenticação e tag da imagem |
| `DOCKERHUB_TOKEN`    | Token utilizado para publicar a imagem                  |
| `DISCORD_WEBHOOK`    | URL do webhook para os alertas no Discord               |

Esses secrets pertencem às automações do GitHub Actions e não são necessários para executar a aplicação localmente. Não inclua seus valores no código ou no README.

## Roadmap de evolução

O MegaSurpresinhas 2.0 já possui uma base funcional com arquitetura modular, PWA, Docker, CI/CD, publicação de imagem e deploy em nuvem. As próximas evoluções podem priorizar confiabilidade, observabilidade e automação antes da inclusão de funcionalidades mais avançadas.

### 1. Confiabilidade e testes

- Ampliar a cobertura dos testes automatizados já existentes, especialmente na camada de aplicação e nos cenários de integração.
- Adicionar testes de integração para o cliente da API de loterias, cache e mecanismo de `fallback`.
- Expandir a cobertura de regras de validação, limites de apostas e cenários de indisponibilidade externa.
- Adicionar checagem de tipos e auditoria periódica de dependências.

### 2. Integração com dados externos

- Investigar e tornar mais robusta a comunicação com a API externa no ambiente de produção.
- Melhorar logs de falhas, timeouts e uso do cache para facilitar diagnóstico.
- Avaliar uma estratégia de cache mais adequada ao ambiente de nuvem, considerando que instâncias podem ser reiniciadas e o armazenamento local pode não ser permanente.
- Permitir a troca de provedor da API com baixo acoplamento, preservando os contratos existentes da camada de aplicação.

### 3. Observabilidade e operação

- Evoluir os logs para um formato estruturado e padronizado.
- Adicionar métricas básicas de disponibilidade, tempo de resposta e falhas na API externa.
- Configurar verificações de saúde e alertas orientados ao ambiente de produção.
- Documentar procedimentos simples de diagnóstico e recuperação.

### 4. CI/CD e infraestrutura

- Evoluir o CI existente com cobertura de testes e critérios mínimos de qualidade.
- Adicionar auditoria de dependências e verificações de segurança ao pipeline.
- Tornar o deploy mais automatizado e reproduzível, reduzindo configurações manuais.
- Avaliar infraestrutura como código para versionar a configuração do serviço de produção.
- Manter separadas as etapas de validação, construção da imagem, publicação e implantação.

### 5. Evolução da experiência do usuário

- Melhorar acessibilidade, feedback de erros e estados de carregamento.
- Ampliar os recursos da PWA e revisar a experiência em dispositivos móveis.
- Adicionar uma área de consulta dos resultados recentes das modalidades.
- Evoluir o histórico local com filtros ou visualizações adicionais, preservando a simplicidade da aplicação.

### 6. Interface conversacional e IA

Em uma etapa posterior, o projeto pode explorar uma interface conversacional capaz de gerar palpites e consultar resultados em linguagem natural. A recomendação é reutilizar os casos de uso já existentes como ferramentas da interface, sem mover regras de negócio para o componente de IA.

Essa evolução deve preservar a arquitetura atual: o domínio continua responsável pelas regras, a camada de aplicação coordena os casos de uso, a infraestrutura integra serviços externos e novas interfaces apenas consomem essas capacidades.

## Autor

Desenvolvido por [David Maciel](https://github.com/DavidMaciel86).
