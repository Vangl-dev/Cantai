# Git

## Convenções de Commit

### Formato
```
tipo(escopo): descrição curta

[corpo opcional]

[footer opcional]
```

### Tipos de Commit
- `feat`: Nova funcionalidade
- `fix`: Correção de bug
- `docs`: Documentação
- `style`: Formatação (não afeta lógica)
- `refactor`: Refatoração (não afeta funcionalidade)
- `test`: Adição/correção de testes
- `chore`: Tarefas de manutenção
- `perf`: Melhoria de performance

### Exemplos
```bash
feat(auth): adicionar login com Google
fix(api): corrigir erro 500 ao listar usuários
docs(readme): atualizar instruções de instalação
refactor(database): otimizar queries
test(user): adicionar testes de validação
chore(deps): atualizar dependências
```

### Regras
- Descrição no imperativo ("adicionar", não "adicionado")
- Máximo 50 caracteres na primeira linha
- Corpo opcional com mais detalhes
- Referenciar issues quando aplicável

---

## Convenções de Branch

### Formato
```
tipo/numero-descricao
```

### Exemplos
```bash
feat/123-adicionar-login
fix/456-corrigir-erro-api
docs/789-atualizar-readme
```

### Branches Principais
- `main` ou `master`: Produção estável
- `develop`: Desenvolvimento integrado
- `feature/*`: Novas funcionalidades
- `fix/*`: Correções de bugs
- `release/*`: Preparação de release

### Fluxo de Trabalho
1. Criar branch a partir de `develop`
2. Desenvolver e commitar
3. Abrir Pull Request
4. Code review
5. Merge em `develop`
6. Delete branch após merge

---

## Pull Requests

### Título
```
tipo(escopo): descrição curta
```

### Corpo
```markdown
## Descrição
[O que mudou e por quê]

## Tipo de Mudança
- [ ] Nova funcionalidade
- [ ] Correção de bug
- [ ] Refatoração
- [ ] Documentação
- [ ] Outro

## Como Testar
1. [Passo 1]
2. [Passo 2]
3. [Passo 3]

## Issues Relacionadas
- Closes #123
- Fixes #456
```

### Checklist de PR
- [ ] Código segue padrões do projeto
- [ ] Testes foram adicionados/atualizados
- [ ] Documentação foi atualizada
- [ ] Não há secrets expostos
- [ ] Commit messages seguem convenção

---

## Tags e Versionamento

### Semver
```
MAJOR.MINOR.PATCH
```

- **MAJOR**: Mudanças incompatíveis
- **MINOR**: Novas funcionalidades (compatível)
- **PATCH**: Correções de bugs (compatível)

### Exemplos
```bash
git tag -a v1.0.0 -m "Release 1.0.0"
git tag -a v1.1.0 -m "Adicionar feature X"
git tag -a v1.1.1 -m "Corrigir bug Y"
```

---

## Regras Importantes

### NUNCA fazer
- ❌ Commitar direto em `main`
- ❌ Push sem testar
- ❌ Force push em branches compartilhadas
- ❌ Commitar `.env` ou credenciais
- ❌ Usar `--no-verify` para pular hooks

### SEMPRE fazer
- ✅ Criar branch para cada feature/fix
- ✅ Testar antes de commitar
- ✅ Usar mensagens semânticas
- ✅ Revisar antes de merge
- ✅ Atualizar CHANGELOG

---

## Git Hooks

### Pré-commit
```bash
#!/bin/sh
npm run lint
npm test
```

### Commit-msg
```bash
#!/bin/sh
# Validar formato de commit
```

### Configuração
```bash
# Instalar hooks
npm install husky --save-dev
npx husky install
```

---

## Referências

- [Versionamento](Versionamento.md)
- [Checklists de Git](../checklists/)
- [AI_CONSTITUTION.md](../AI_CONSTITUTION.md)
