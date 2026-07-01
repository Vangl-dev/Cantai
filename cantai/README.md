# Cantai Builder

Builder para importação, organização e exportação de hinários cristãos.

Site estático para planejamento de hinos em cultos.

## Hinários suportados

| Hinário | Sigla | Formato | Qtd approximate |
|---------|-------|---------|-----------------|
| Cantai Todos os Povos | CTP | PPT/PPTX | ~500 |
| Harpa Cristã | HARPA | PDF | ~640 |
| Cantor Cristão | CC | PDF | ~580 |
| Salmos e Hinos | SH | PDF | ~100 |
| Novo Cântico | NC | PDF | ~400 |

## Instalação

```bash
pip install -e .
```

## Uso

### Build completo

```bash
python -m cantai build --ctp-dir "/caminho/para/CTP"
```

### Importação individual

```bash
python -m cantai importar /caminho/para/CTP
python -m cantai importar-harpa /caminho/para/HARPA.pdf
python -m cantai importar-cc /caminho/para/CC.pdf
python -m cantai importar-sh /caminho/para/SH.pdf
python -m cantai importar-nc /caminho/para/NC.pdf
```

### Exportação

```bash
python -m cantai exportar
```

## Arquitetura

```
cantai/
├── src/cantai/           # Código fonte
│   ├── importers/        # Importadores por hinário
│   ├── exporters/        # Exportadores (JSON)
│   ├── database.py       # Persistência SQLite
│   ├── models.py         # Modelos de dados
│   ├── schemas.py        # Schemas
│   └── cli.py            # Interface de linha de comando
├── data/
│   ├── input/            # PDFs dos hinários
│   ├── output/           # cantai.json exportado
│   └── database/         # SQLite (gitignored)
├── web/                  # Site estático
│   ├── index.html
│   ├── app.js
│   ├── style.css
│   └── cantai.json       # Dados para o site
└── pyproject.toml
```

## Site estático

O diretório `web/` contém um site estático HTML/CSS/JavaScript que pode ser publicado diretamente no Netlify ou GitHub Pages.

## Licença

MIT
