#!/bin/bash

# Script de Geração de CHANGELOG
# Uso: ./gerar-changelog.sh [versão]

set -e

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Versão
VERSION="${1:-$(date +%Y-%m-%d)}"

echo -e "${GREEN}Gerando CHANGELOG para versão: $VERSION${NC}"

# Verificar se está em um repositório Git
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo -e "${RED}Erro: Não está em um repositório Git${NC}"
    exit 1
fi

# Obter commits desde última tag
LAST_TAG=$(git describe --tags --abbrev=0 2>/dev/null || echo "")

if [ -z "$LAST_TAG" ]; then
    echo -e "${YELLOW}Nenhuma tag encontrada, usando todos os commits${NC}"
    COMMITS=$(git log --pretty=format:"- %s (%h)" --no-merges)
else
    echo -e "${YELLOW}Última tag: $LAST_TAG${NC}"
    COMMITS=$(git log "$LAST_TAG"..HEAD --pretty=format:"- %s (%h)" --no-merges)
fi

# Classificar commits
FEAT_COMMITS=$(echo "$COMMITS" | grep -i "^- feat" || true)
FIX_COMMITS=$(echo "$COMMITS" | grep -i "^- fix" || true)
DOCS_COMMITS=$(echo "$COMMITS" | grep -i "^- docs" || true)
OTHER_COMMITS=$(echo "$COMMITS" | grep -iv "^- feat\|^- fix\|^- docs" || true)

# Gerar CHANGELOG
echo ""
echo -e "${GREEN}## [$VERSION] - $(date +%Y-%m-%d)${NC}"
echo ""

if [ ! -z "$FEAT_COMMITS" ]; then
    echo -e "${GREEN}### Added${NC}"
    echo "$FEAT_COMMITS"
    echo ""
fi

if [ ! -z "$FIX_COMMITS" ]; then
    echo -e "${GREEN}### Fixed${NC}"
    echo "$FIX_COMMITS"
    echo ""
fi

if [ ! -z "$DOCS_COMMITS" ]; then
    echo -e "${GREEN}### Documentation${NC}"
    echo "$DOCS_COMMITS"
    echo ""
fi

if [ ! -z "$OTHER_COMMITS" ]; then
    echo -e "${GREEN}### Other${NC}"
    echo "$OTHER_COMMITS"
    echo ""
fi

echo -e "${GREEN}CHANGELOG gerado com sucesso!${NC}"
