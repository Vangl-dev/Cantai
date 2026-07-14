# Prompt 040: Refatoração

## Objetivo
Melhorar código existente sem alterar comportamento externo.

## Checklist

### 1. Planejamento
- [ ] Identificar código para refatorar
- [ ] Garantir testes existentes
- [ ] Definir escopo da refatoração
- [ ] Estimar tempo

### 2. Execução
- [ ] Refatorar incrementalmente
- [ ] Rodar testes após cada mudança
- [ ] Manter comportamento externo
- [ ] Documentar mudanças

### 3. Validação
- [ ] Todos os testes passando
- [ ] Lint sem erros
- [ ] Performance mantida ou melhorada
- [ ] Código mais legível

### 4. Documentação
- [ ] Atualizar documentação
- [ ] Registrar decisões
- [ ] Atualizar CHANGELOG (se aplicável)

## Quando Refatorar

### Sinais
- Código duplicado
- Funções muito longas
- Nomes confusos
- Dependências circulares
- Testes difíceis de escrever

### Oportunidades
- Após correção de bug
- Antes de adicionar feature
- Durante code review
- Em sprint de manutenção

## Template de Refatoração

```markdown
# Refatoração: [Título]

## Status
[Planejada | Em Progresso | Concluída]

## Escopo
- [Componente 1]
- [Componente 2]

## Objetivo
[O que melhorar]

## Mudanças

### Antes
```código antigo
```

### Depois
```código novo
```

## Justificativa
[Por que essa mudança]

## Testes
- [ ] Testes existentes passando
- [ ] Novos testes adicionados

## Resultado
[Melhoria alcançada]
```

## Regras de Refatoração

### 1. Incremental
```bash
# Não refatorar tudo de uma vez
# Pequenas mudanças
# Testar cada passo
```

### 2. Seguro
```bash
# Garantir testes antes
# Rodar testes depois
# Não mudar comportamento
```

### 3. Documentado
```bash
# Registrar o que mudou
# Documentar por quê
# Atualizar documentação
```

## Perguntas para o Desenvolvedor

1. O que precisa ser refatorado?
2. Por que refatorar agora?
3. Há testes para esse código?
4. Qual o risco da mudança?
5. Qual o benefício esperado?

## Saída Esperada

Após completar este prompt:
- Código refatorado
- Testes passando
- Documentação atualizada
- Melhoria mensurável

## Referências

- [Boas Práticas](../docs/Boas_Praticas.md)
- [Qualidade](../docs/Qualidade.md)
- [Testes](../templates/projeto/TESTING.md)
