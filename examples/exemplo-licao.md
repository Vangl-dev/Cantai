# Exemplo de Lição Aprendida

---

# Lição: Sempre Testar Antes de Deploy

## Data
2026-07-06

## Contexto

Estávamos fazendo deploy de uma feature nova em produção. A feature parecia simples e decidimos pular os testes por "pressa".

## O que Aconteceu

Após o deploy, a feature quebrou em produção. Usuários não conseguiam fazer login. O time precisou trabalhar horas para identificar e corrigir o problema.

## Causa Raiz

A feature tinha um bug que só aparecia em produção devido a uma diferença de configuração entre ambientes. Os testes locais passavam porque usavam configuração diferente.

## Lição

**NUNCA pular testes, mesmo que a mudança pareça pequena.**

Testes existem justamente para pegar problemas que não imaginamos.

## Ação Preventiva

1. **Checklist obrigatório** antes de deploy
2. **CI/CD com testes automáticos** que bloqueiam merge se falharem
3. **Time ciente** da importância dos testes
4. **Testes em ambiente de staging** idêntico ao produção

## Implementação

```yaml
# GitHub Actions - testes obrigatórios
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - run: npm test
      - run: npm run lint
```

## Resultado

Desde que implementamos testes obrigatórios, não tivemos mais incidents causados por bugs em produção.

## Tags

`deploy`, `testes`, `qualidade`, `processo`

## Referências

- [Checklists de Deploy](../checklists/deploy.md)
- [Qualidade](../docs/Qualidade.md)

---

**Última atualização:** 2026-07-06
