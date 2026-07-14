# Prompt 030: Debug

## Objetivo
Identificar e corrigir bugs de forma sistemática e documentada.

## Checklist

### 1. Identificação
- [ ] Documentar bug em `KNOWN_ISSUES.md`
- [ ] Criar issue no GitHub (se aplicável)
- [ ] Classificar severidade
- [ ] Identificar passos para reproduzir

### 2. Investigação
- [ ] Reproduzir o bug
- [ ] Analisar logs
- [ ] Verificar variáveis de ambiente
- [ ] Identificar causa raiz

### 3. Correção
- [ ] Implementar correção
- [ ] Testar a correção
- [ ] Verificar regressões
- [ ] Documentar a correção

### 4. Prevenção
- [ ] Adicionar teste para o bug
- [ ] Atualizar checklist se necessário
- [ ] Registrar lição aprendida

## Template de Bug Report

```markdown
# Bug: [Título]

## Status
[Aberto | Em Progresso | Resolvido]

## Severidade
[Alta | Média | Baixa]

## Data Identificação
YYYY-MM-DD

## Descrição
[Descrição do bug]

## Passos para Reproduzir
1. [Passo 1]
2. [Passo 2]
3. [Passo 3]

## Comportamento Esperado
[O que deveria acontecer]

## Comportamento Atual
[O que está acontecendo]

## Ambiente
- SO: [SO]
- Navegador: [se aplicável]
- Versão: [versão]

## Possível Causa
[Causa identificada]

## Solução
[Como foi corrigido]

## Lição Aprendida
[O que aprender]
```

## Processo de Debug

### 1. Reproduzir
```bash
# Garantir que consegue reproduzir
# Anotar passos exatos
```

### 2. Isolar
```bash
# Reduzir o problema ao mínimo
# Identificar componente afetado
```

### 3. Analisar
```bash
# Verificar logs
# Usar debugger
# Inspecionar estado
```

### 4. Corrigir
```bash
# Implementar correção
# Testar
# Verificar não quebrou nada
```

### 5. Documentar
```bash
# Atualizar KNOWN_ISSUES.md
# Criar teste
# Registrar lição
```

## Perguntas para o Desenvolvedor

1. Qual é o bug?
2. Como reproduzir?
3. Qual o impacto?
4. Já tentou corrigir?
5. Precisa de ajuda?

## Saída Esperada

Após completar este prompt:
- Bug documentado
- Causa raiz identificada
- Correção implementada
- Teste adicionado
- Lição registrada

## Referências

- [Lições Aprendidas](../docs/Licoes_Aprendidas.md)
- [Qualidade](../docs/Qualidade.md)
- [Checklists](../checklists/)
