#!/bin/bash

# Script de Validação de Projeto
# Uso: ./validar-projeto.sh [caminho-do-projeto]

set -e

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Diretório do projeto
PROJECT_DIR="${1:-.}"

echo -e "${GREEN}Validando projeto: $PROJECT_DIR${NC}"
echo ""

# Verificar arquivos obrigatórios
echo -e "${YELLOW}Verificando arquivos obrigatórios...${NC}"

REQUIRED_FILES=(
    "README.md"
    "PROJECT_STATE.md"
    "ROADMAP.md"
    "CHANGELOG.md"
    "KNOWN_ISSUES.md"
    "AI_INSTRUCTIONS.md"
    "ARCHITECTURE.md"
    "SECURITY.md"
    "TESTING.md"
    "DECISIONS.md"
)

MISSING_FILES=()

for file in "${REQUIRED_FILES[@]}"; do
    if [ ! -f "$PROJECT_DIR/$file" ]; then
        MISSING_FILES+=("$file")
        echo -e "${RED}✗ $file${NC}"
    else
        echo -e "${GREEN}✓ $file${NC}"
    fi
done

echo ""

# Verificar diretórios obrigatórios
echo -e "${YELLOW}Verificando diretórios obrigatórios...${NC}"

REQUIRED_DIRS=(
    "src"
    "tests"
    "docs"
)

MISSING_DIRS=()

for dir in "${REQUIRED_DIRS[@]}"; do
    if [ ! -d "$PROJECT_DIR/$dir" ]; then
        MISSING_DIRS+=("$dir")
        echo -e "${RED}✗ $dir/${NC}"
    else
        echo -e "${GREEN}✓ $dir/${NC}"
    fi
done

echo ""

# Verificar .gitignore
echo -e "${YELLOW}Verificando .gitignore...${NC}"

if [ ! -f "$PROJECT_DIR/.gitignore" ]; then
    echo -e "${RED}✗ .gitignore não encontrado${NC}"
else
    if grep -q "\.env" "$PROJECT_DIR/.gitignore"; then
        echo -e "${GREEN}✓ .env está no .gitignore${NC}"
    else
        echo -e "${RED}✗ .env NÃO está no .gitignore${NC}"
    fi
fi

echo ""

# Resumo
echo -e "${YELLOW}Resumo:${NC}"

if [ ${#MISSING_FILES[@]} -eq 0 ] && [ ${#MISSING_DIRS[@]} -eq 0 ]; then
    echo -e "${GREEN}✓ Projeto válido!${NC}"
else
    echo -e "${RED}✗ Projeto com problemas:${NC}"
    
    if [ ${#MISSING_FILES[@]} -gt 0 ]; then
        echo -e "${RED}  Arquivos faltando: ${MISSING_FILES[*]}${NC}"
    fi
    
    if [ ${#MISSING_DIRS[@]} -gt 0 ]; then
        echo -e "${RED}  Diretórios faltando: ${MISSING_DIRS[*]}${NC}"
    fi
fi
