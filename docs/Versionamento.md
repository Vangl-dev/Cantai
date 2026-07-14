# Versionamento

## Semantic Versioning (Semver)

### Formato
```
MAJOR.MINOR.PATCH
```

### Definições

#### MAJOR (X.0.0)
Mudanças que quebram compatibilidade:
- API incompatível
- Mudança de estrutura de banco
- Remoção de funcionalidades
- Mudança de comportamento esperado

#### MINOR (x.Y.0)
Novas funcionalidades compatíveis:
- Nova feature
- Nova endpoint
- Nova opção de configuração
- Melhoria de performance

#### PATCH (x.y.Z)
Correções compatíveis:
- Bug fix
- Correção de segurança
- Melhoria de documentação
- Ajuste de configuração

---

## Regras de Versionamento

### Antes de Incrementar
1. Revisar mudanças desde última versão
2. Classificar mudanças (MAJOR/MINOR/PATCH)
3. Atualizar CHANGELOG
4. Criar tag

### Exemplos

#### v1.0.0 → v1.1.0 (MINOR)
```markdown
## [1.1.0] - 2026-07-06

### Added
- Login com Google
- Dashboard de métricas

### Changed
- Otimização de queries

### Fixed
- Correção de timezone
```

#### v1.1.0 → v1.1.1 (PATCH)
```markdown
## [1.1.1] - 2026-07-07

### Fixed
- Correção de bug no login
- Ajuste de formatação de data
```

#### v1.1.1 → v2.0.0 (MAJOR)
```markdown
## [2.0.0] - 2026-08-01

### BREAKING CHANGE
- API v1 removida
- Estrutura de banco alterada

### Added
- API v2 com novos endpoints

### Migration
- Veja guia de migração em docs/migration.md
```

---

## CHANGELOG

### Formato Recomendado
```markdown
# Changelog

Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
e este projeto adere ao [Semantic Versioning](https://semver.org/lang/pt-BR/).

## [Versão] - YYYY-MM-DD

### Added (Adicionado)
- Para novas funcionalidades

### Changed (Alterado)
- Para mudanças em funcionalidades existentes

### Deprecated (Depreciado)
- Para funcionalidades que serão removidas

### Removed (Removido)
- Para funcionalidades removidas

### Fixed (Corrigido)
- Para correções de bugs

### Security (Segurança)
- Para vulnerabilidades de segurança
```

---

## Tags Git

### Criar Tag Anotada
```bash
git tag -a v1.0.0 -m "Release 1.0.0"
```

### Criar Tag com Descrição
```bash
git tag -a v1.0.0 -m "## Features
- Login com Google
- Dashboard

## Bug Fixes
- Correção de timezone"
```

### Listar Tags
```bash
git tag -l
git tag -l "v1.*"
```

### Push Tags
```bash
git push origin v1.0.0
git push origin --tags
```

---

## Versionamento em Projetos

### Quem Decide
- Desenvolvedor principal
- Time de desenvolvimento
- Produto (para features)

### Quando Decidir
- Antes de cada release
- Após milestone completo
- Quando há breaking changes

### Documentação
- Registrar em DECISIONS.md
- Atualizar CHANGELOG
- Comunicar ao time

---

## Ferramentas

### Geradores de CHANGELOG
- [conventional-changelog](https://github.com/conventional-changelog/conventional-changelog)
- [standard-version](https://github.com/conventional-changelog/standard-version)
- [release-please](https://github.com/googleapis/release-please)

### Validação de Commits
- [commitlint](https://commitlint.js.org/)
- [husky](https://typicode.github.io/husky/)

---

## Referências

- [Git](Git.md)
- [Fluxo de Desenvolvimento](Fluxo.md)
- [Checklists de Release](../checklists/)
