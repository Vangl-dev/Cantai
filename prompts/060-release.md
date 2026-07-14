# Prompt 060: Release

## Objetivo
Preparar e executar uma release do projeto.

## Checklist

### 1. Pré-Release
- [ ] Todos os testes passando
- [ ] Lint sem erros
- [ ] Documentação atualizada
- [ ] CHANGELOG atualizado
- [ ] Versão definida

### 2. Validação
- [ ] Testes E2E passando
- [ ] Performance verificada
- [ ] Segurança verificada
- [ ] Compatibilidade verificada

### 3. Execução
- [ ] Tag criada
- [ ] Release publicada
- [ ] Notificação enviada
- [ ] Documentação publicada

### 4. Pós-Release
- [ ] Monitoramento ativo
- [ ] Issues verificadas
- [ ] Feedback coletado
- [ ] Próxima versão planejada

## Template de Release

```markdown
# Release [Versão]

## Data
YYYY-MM-DD

## Versão
[MAJOR.MINOR.PATCH]

## Mudanças

### Added
- [Feature 1]
- [Feature 2]

### Changed
- [Mudança 1]
- [Mudança 2]

### Fixed
- [Bug 1]
- [Bug 2]

### Deprecated
- [Feature deprecada]

### Removed
- [Feature removida]

### Security
- [Correção de segurança]

## Instalação
```bash
# Comando de instalação
```

## Upgrade
```bash
# Comando de upgrade
```

## Known Issues
- [Issue 1]

## Agradecimentos
- [Contribuidores]
```

## Processo de Release

### 1. Preparação
```bash
# Atualizar versão
npm version [major|minor|patch]

# Atualizar CHANGELOG
# Documentar mudanças

# Rodar testes finais
npm test
```

### 2. Publicação
```bash
# Criar tag
git tag -a v[versão] -m "Release [versão]"

# Push
git push origin v[versão]
git push origin --tags

# Publicar (se aplicável)
npm publish
```

### 3. Comunicação
```bash
# Notificar time
# Atualizar documentação
# Publicar release notes
```

## Versionamento

### Semver
- **MAJOR:** Breaking changes
- **MINOR:** Novas features (compatível)
- **PATCH:** Bug fixes (compatível)

### Exemplos
```bash
# Nova feature
npm version minor

# Bug fix
npm version patch

# Breaking change
npm version major
```

## Perguntas para o Desenvolvedor

1. Qual a versão a ser publicada?
2. Há breaking changes?
3. Todos os testes passando?
4. Documentação atualizada?
5. Quem deve ser notificado?

## Saída Esperada

Após completar este prompt:
- Release publicada
- Tag criada
- Documentação atualizada
- Time notificado

## Referências

- [Versionamento](../docs/Versionamento.md)
- [Deploy](../docs/Deploy.md)
- [Checklists](../checklists/)
