# Cantai2

Aplicação web para busca e consulta do Hinário Cantai Todos os Povos (CTP).

## Visão Geral

O projeto Cantai2 é uma aplicação web simples e testável para importar, armazenar e buscar hinos do hinário CTP (Cantai Todos os Povos). A aplicação permite busca por número, título, primeira linha, letra completa e tema.

## Funcionalidades

- Importação de PDF do hinário CTP
- Extração e armazenamento de todos os hinos
- Busca textual por número, título, primeira linha, letra e tema
- Interface web simples e responsiva

## Pré-requisitos

- Python 3.12+
- pip ou uv

## Instalação

```bash
# Clonar repositório
git clone https://github.com/[org]/cantai2.git

# Entrar no diretório
cd cantai2

# Criar ambiente virtual
python -m venv .venv
source .venv/bin/activate

# Instalar dependências
pip install -e ".[dev]"
```

## Uso

```bash
# Executar CLI
cantai --help

# Rodar testes
pytest

# Verificar código
ruff check src/ tests/
mypy src/
```

## Estrutura

```
cantai2/
├── src/
│   └── cantai/           # Código fonte principal
├── tests/                # Testes
├── docs/                 # Documentação
├── data/
│   ├── input/            # Arquivos de entrada (PDFs)
│   └── output/           # Arquivos de saída
├── config.toml           # Configurações
├── pyproject.toml        # Configurações do projeto
└── README.md
```

## Documentação

- [CHANGELOG.md](CHANGELOG.md) - Histórico de versões

## Licença

[MIT License](LICENSE)
