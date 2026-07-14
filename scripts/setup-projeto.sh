#!/bin/bash

# Script de Setup de Projeto
# Uso: ./setup-projeto.sh nome-do-projeto

set -e

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Verificar argumento
if [ -z "$1" ]; then
    echo -e "${RED}Erro: Nome do projeto não fornecido${NC}"
    echo "Uso: ./setup-projeto.sh nome-do-projeto"
    exit 1
fi

PROJECT_NAME=$1
TEMPLATE_DIR="$(dirname "$0")/../templates/projeto"

echo -e "${GREEN}Criando projeto: $PROJECT_NAME${NC}"

# Criar diretório do projeto
if [ -d "$PROJECT_NAME" ]; then
    echo -e "${RED}Erro: Diretório já existe${NC}"
    exit 1
fi

mkdir -p "$PROJECT_NAME"

# Copiar templates
echo -e "${YELLOW}Copiando templates...${NC}"
cp -r "$TEMPLATE_DIR"/* "$PROJECT_NAME/"

# Criar diretórios adicionais
echo -e "${YELLOW}Criando estrutura de pastas...${NC}"
mkdir -p "$PROJECT_NAME/src"
mkdir -p "$PROJECT_NAME/tests"
mkdir -p "$PROJECT_NAME/docs"
mkdir -p "$PROJECT_NAME/.github/ISSUE_TEMPLATE"

# Criar .gitignore básico
echo -e "${YELLOW}Criando .gitignore...${NC}"
cat > "$PROJECT_NAME/.gitignore" << 'EOF'
# OS
.DS_Store
Thumbs.db

# IDEs
.vscode/
.idea/
*.swp
*.swo

# Node
node_modules/
package-lock.json
yarn.lock

# Python
__pycache__/
*.py[cod]
*.egg-info/
.venv/
venv/

# Env
.env
.env.local
.env.*.local

# Logs
*.log
logs/

# Build
dist/
build/
*.tmp
*.temp

# Backup
*.bak
*.backup

# Secrets
credentials.json
secrets.json
*.key
*.pem
EOF

# Criar .env.example
echo -e "${YELLOW}Criando .env.example...${NC}"
cat > "$PROJECT_NAME/.env.example" << 'EOF'
# Banco de Dados
DATABASE_URL=postgresql://user:pass@localhost:5432/db

# API Keys
API_KEY=your-api-key-here
SECRET_KEY=your-secret-key-here

# Autenticação
JWT_SECRET=your-jwt-secret-here
JWT_EXPIRATION=24h
EOF

# Inicializar Git
echo -e "${YELLOW}Inicializando repositório Git...${NC}"
cd "$PROJECT_NAME"
git init
git add .
git commit -m "feat: initial project setup"

echo -e "${GREEN}Projeto criado com sucesso!${NC}"
echo ""
echo -e "${GREEN}Próximos passos:${NC}"
echo "1. cd $PROJECT_NAME"
echo "2. Configure suas variáveis de ambiente em .env"
echo "3. Comece a desenvolver!"
echo ""
echo -e "${YELLOW}Documentação:${NC}"
echo "- README.md: Visão geral do projeto"
echo "- PROJECT_STATE.md: Estado atual do projeto"
echo "- DECISIONS.md: Decisões arquiteturais"
echo "- ROADMAP.md: Roadmap do projeto"
