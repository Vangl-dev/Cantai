# Estrutura do PDF CTP - Relatório de Engenharia Reversa

## Visão Geral

O PDF do Hinário Cantai Todos os Povos possui 390 páginas e contém 501 hinos.

## Estrutura do Documento

### Páginas Iniciais (1-14)
- Página 1: Capa
- Página 2: Dados de publicação
- Página 3: Versículo (Salmo 96.1)
- Página 4: Créditos
- Página 5: Sumário
- Páginas 6-14: Introdução e texto explicativo

### Páginas de Hinos (15-342)
- Início: Página 15 (Hino nº 1)
- Fim: Página 342 (Hino nº 501)
- Total de páginas com hinos: 328

### Páginas Finais (343-390)
- Índices e apêndices

## Padrão dos Hinos

### Início de um Hino
```
[NÚMERO]- [TÍTULO EM MAIÚSCULAS]
[Autor/Compositor]
[Primeira linha da letra]
```

Exemplo real (Página 15):
```
1- ADORAI EM MAJESTADE
Jack W. Hayford  -  Trad. João Wilson Faustini
Adorai em majestade!
```

### Fim de um Hino
```
[Última linha da letra]
[Copyright - opcional]
Hinário [seção].pmd
[Data]
[Número da página]
```

## Identificação Automática

### Padrão de Início
- **Regex**: `^(\d+)[-–]\s+[A-ZÀ-Ú][A-ZÀ-Ú\s]+$`
- **Posição**: Início de linha
- **Características**:
  - Número inteiro
  - Seguido de hífen ou traço
  - Espaço
  - Título em MAIÚSCULAS

### Padrão de Fim
- **Sinalizador**: Próximo hino ou Copyright
- **Marcadores**:
  - `© Copyright` (opcional)
  - `Hinário [seção].pmd`
  - `6/10/2009, 14:51`
  - Número da página

## Exceções e Casos Especiais

### Hinos com Mais de Uma Página
- Sim, existem
- Exemplo: Hino nº 7 (páginas 19-21)
- Identificação: Não há marcador explícito de continuação

### Variantes (A, B)
- **Não existem no PDF**
- O índice markdown usa notação `$^{A}$` e `$^{B}$`
- No PDF, variantes são hinos separados com números diferentes

### Hinos com Múltiplos Versos
- Numerados internamente (1-, 2-, 3-, etc.)
- Não devem ser confundidos com números de hino

## Estratégia Recomendada

### Para Localizar Automaticamente um Hino

1. **Buscar padrão de início**: `^(\d+)[-–]\s+[A-ZÀ-Ú]`
2. **Extrair número e título** da linha encontrada
3. **Extrair autor** da linha seguinte
4. **Extrair letra** até encontrar:
   - Próximo padrão de início de hino
   - Ou copyright
   - Ou final da página com marcador `Hinário`

### Limitações
- Hinos multi-página requerem lógica de continuação
- Copyright pode estar presente ou não
- Alguns hinos têm notas de rodapé

## Resposta à Pergunta

**O parser conseguirá localizar automaticamente um hino?**

**SIM**

Estratégia:
1. Usar regex para identificar início de hino
2. Extrair dados da página atual
3. Continuar extraindo se houver mais conteúdo na página
4. Parar ao encontrar próximo hino ou copyright
5. Repetir para todas as páginas

## Arquivos Analisados

- `data/input/Hinário Cantai Todos os Povos.pdf` (390 páginas)
- `data/input/markdown_índice_ctp.md` (referência)
- `data/input/HinarioCTP_metricas.md` (referência)
