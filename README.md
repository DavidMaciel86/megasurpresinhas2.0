# MegaSurpresinhas 2.0

Aplicação web modular para geração de jogos da Mega-Sena e Lotofácil. Esta versão foi reconstruída para separar domínio, casos de uso, infraestrutura e interface, permanecendo simples o suficiente para estudo.

> Os jogos são aleatórios. Resultados anteriores não alteram a probabilidade matemática de premiação.

## Objetivo do projeto

O MegaSurpresinhas 2.0 também é utilizado como projeto prático de aprendizado e evolução em desenvolvimento de software.

Além das funcionalidades voltadas à geração de jogos, o projeto busca aplicar e aprimorar conceitos como:

- desenvolvimento com Python e Flask;
- arquitetura modular e separação de responsabilidades;
- princípios de Clean Architecture;
- organização e manutenção de código;
- versionamento com Git e GitHub;
- práticas de DevOps e evolução contínua do software.

## Requisitos

- Python 3.11 ou superior

## Preparação no Windows

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
pip install -e .
```

## Executar

```powershell
python run.py
```

Acesse `http://127.0.0.1:5000`.

## Configuração

Copie `.env.example` para `.env` se desejar registrar valores locais. As variáveis não são carregadas automaticamente; defina-as no terminal ou configure-as pela plataforma de execução.

- `FLASK_ENV`: use `development` apenas localmente.
- `APP_HOST` e `APP_PORT`: endereço local.
- `APP_LOG_LEVEL`: nível de log.
- `LOTTERY_API_BASE_URL`: endpoint-base do provedor.
- `API_CONNECT_TIMEOUT` e `API_READ_TIMEOUT`: timeouts HTTP.
- `CACHE_DIR`: diretório opcional para cache técnico.

## Arquitetura

- `domain`: regras e geração, sem dependências de Flask, HTTP ou arquivos.
- `application`: caso de uso e contratos.
- `infrastructure`: cliente da API e cache JSON.
- `web`: rotas, templates, CSS, JavaScript e PWA.

O histórico pertence ao navegador e não é gravado no servidor. O cache JSON guarda apenas resultados recentes da API.

## Modo de funcionamento

1. Consulta resultados recentes na API.
2. Se a API falhar, utiliza o cache técnico.
3. Sem API e sem cache, gera com distribuição uniforme.

A PWA mantém a interface básica disponível no cache. Gerar novos jogos exige conexão com o servidor; o termo fallback se refere à indisponibilidade da API externa, não à ausência de conexão entre navegador e servidor.

## Verificação manual

- abrir Mega-Sena e Lotofácil;
- gerar entradas nos limites permitidos;
- enviar entradas inválidas;
- confirmar o histórico por modalidade;
- alternar tema;
- abrir `/health/live`;
- simular indisponibilidade da API e conferir cache/fallback;
- conferir a página `/offline`.

## Evoluções futuras

Como evolução do projeto, está prevista a possibilidade de incorporar uma interface conversacional com um agente de inteligência artificial.

A proposta é permitir que o agente utilize as funcionalidades existentes da aplicação como ferramentas, mantendo as regras de negócio independentes da camada de IA. Entre as possibilidades estão:

- gerar palpites por meio de interação em linguagem natural;
- consultar resultados recentes das loterias;
- utilizar as funcionalidades do domínio como ferramentas do agente;
- oferecer uma experiência conversacional integrada à interface web.

Essa evolução deverá preservar a arquitetura modular do projeto, mantendo as responsabilidades de domínio, aplicação, infraestrutura e interface desacopladas.

## Próximos passos de DevOps

Este repositório não inclui CI/CD nem testes automatizados de propósito. Sugestões para prática futura:

1. adicionar suíte de testes;
2. configurar lint e checagem de tipos;
3. criar pipeline no GitHub Actions;
4. auditar dependências e segredos;
5. criar imagem Docker;
6. configurar staging e produção no Render;
7. adicionar smoke test e rollback.
