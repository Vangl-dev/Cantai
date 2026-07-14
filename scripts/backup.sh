#!/bin/bash

# Script de Backup
# Uso: ./backup.sh [diretório-de-destino]

set -e

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configurações
BACKUP_DIR="${1:-./backups}"
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_NAME="backup_$DATE.tar.gz"

echo -e "${GREEN}Iniciando backup...${NC}"

# Criar diretório de backup se não existir
mkdir -p "$BACKUP_DIR"

# Verificar se está em um repositório Git
if git rev-parse --git-dir > /dev/null 2>&1; then
    echo -e "${YELLOW}Repositório Git detectado${NC}"
    
    # Backup do código
    echo -e "${YELLOW}Fazendo backup do código...${NC}"
    git archive --format=tar.gz --output="$BACKUP_DIR/$BACKUP_NAME" HEAD
    
    echo -e "${GREEN}✓ Backup do código: $BACKUP_DIR/$BACKUP_NAME${NC}"
else
    echo -e "${RED}Aviso: Não está em um repositório Git${NC}"
    
    # Backup manual
    echo -e "${YELLOW}Fazendo backup manual...${NC}"
    tar -czf "$BACKUP_DIR/$BACKUP_NAME" \
        --exclude='node_modules' \
        --exclude='.git' \
        --exclude='backups' \
        .
    
    echo -e "${GREEN}✓ Backup manual: $BACKUP_DIR/$BACKUP_NAME${NC}"
fi

# Verificar tamanho do backup
BACKUP_SIZE=$(du -h "$BACKUP_DIR/$BACKUP_NAME" | cut -f1)
echo -e "${GREEN}Tamanho do backup: $BACKUP_SIZE${NC}"

# Limpar backups antigos (manter últimos 7)
echo -e "${YELLOW}Limpando backups antigos...${NC}"
cd "$BACKUP_DIR"
ls -t backup_*.tar.gz 2>/dev/null | tail -n +8 | xargs -r rm
cd -

echo -e "${GREEN}Backup concluído com sucesso!${NC}"
echo ""
echo -e "${GREEN}Arquivo: $BACKUP_DIR/$BACKUP_NAME${NC}"
echo -e "${GREEN}Tamanho: $BACKUP_SIZE${NC}"
