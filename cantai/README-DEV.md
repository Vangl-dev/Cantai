# Cantai — Fluxo de Desenvolvimento

## Comandos

### Preview Local

```bash
cantai preview
```

ou

```bash
python -m cantai preview
```

Executa automaticamente:

1. Atualiza SQLite (importa todos os hinários)
2. Gera `cantai.json`
3. Sincroniza `web/cantai.json`
4. Inicia servidor HTTP em `http://localhost:8000`
5. Abre o navegador automaticamente

### Build Completo

```bash
python -m cantai build
```

Executa o pipeline completo com relatório detalhado.

---

## Fluxo Oficial

```
MiMo implementa
       ↓
cantai preview (teste local)
       ↓
Vanessa aprova
       ↓
git add + commit + push
       ↓
Deploy Netlify (automático)
```

---

## Regras

1. **Nunca fazer push sem aprovação**
2. **Sempre testar com `cantai preview` antes de commitar**
3. **Se algo quebrar, o preview local mostra o erro**

---

## Estrutura do Projeto

```
cantai/
├── src/cantai/          # Código Python
│   ├── cli.py           # Comandos (build, preview, importar_*)
│   ├── database.py      # SQLite
│   ├── importers/       # Importadores por hinário
│   ├── exporters/       # Exportação JSON
│   └── topics/          # Sistema de temas
├── web/                 # Frontend estático
│   ├── index.html       # Interface principal
│   ├── app.js           # Lógica JavaScript
│   ├── style.css        # Estilos
│   └── cantai.json      # Banco de dados para o frontend
├── data/
│   ├── input/           # PDFs e fontes
│   ├── output/          # JSON exportado
│   └── database/        # SQLite
└── canonical_topics.yaml
```
