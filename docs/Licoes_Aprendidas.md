# Lições Aprendidas

## Visão Geral

Lições aprendidas são insights valiosos que vêm da experiência. Documentá-las ajuda a evitar repetir erros e compartilhar conhecimento.

## Princípios

### 1. Toda Lição é Válida
- Não importa a origem
- Não importa a gravidade
- Se aprendeu, vale documentar

### 2. Lição é Ação
- Não apenas o que aconteceu
- Mas o que fazer diferente
- E como prevenir no futuro

### 3. Lição é Compartilhamento
- Documentar para outros
- Revisitar periodicamente
- Atualizar conforme necessário

---

## Formato de Registro

```markdown
# Lição: [Título]

## Data
YYYY-MM-DD

## Contexto
[O que estava fazendo]

## O que Aconteceu
[Descrição do evento]

## Causa Raiz
[Por que aconteceu]

## Lição
[O que aprender]

## Ação Preventiva
[O que fazer para evitar]

## Tags
[tag1, tag2, tag3]
```

---

## Exemplos

### Lição 1: Sempre Testar Antes de Deploy

```markdown
# Lição: Sempre Testar Antes de Deploy

## Data
2026-07-06

## Contexto
Deploy de feature nova em produção

## O que Aconteceu
Deploy feito sem testar. Feature quebrou em produção.

## Causa Raiz
Pular etapa de teste por "pressa"

## Lição
NUNCA pular testes. Mesmo que seja "mudança pequena".

## Ação Preventiva
- Checklist obrigatório antes de deploy
- CI/CD com testes automáticos
- Time ciente da importância

## Tags
deploy, testes, qualidade
```

### Lição 2: Documentar Decisões

```markdown
# Lição: Documentar Decisões

## Data
2026-07-07

## Contexto
Mudança de arquitetura sem documentar

## O que Aconteceu
Time não sabia por que a mudança foi feita. Revertendo sem entender.

## Causa Raiz
Falta de documentação em DECISIONS.md

## Lição
Toda decisão técnica DEVE ser documentada.

## Ação Preventiva
- Checklist com item "documentar decisão"
- Revisão de DECISIONS.md em cada sprint
- IA obrigada a documentar decisões

## Tags
documentacao, decisoes, comunicacao
```

---

## Categorias de Lições

### Técnico
- Arquitetura
- Padrões de código
- Ferramentas
- Performance

### Processo
- Comunicação
- Planejamento
- Execução
- Controle de qualidade

### Pessoal
- Aprendizado
- Colaboração
- Liderança
- Motivação

---

## Como Coletar Lições

### Fontes
- Retrospectivas de sprint
- Incidentes e post-mortems
- Code reviews
- Feedback de usuários
- Própria experiência

### Processo
1. Identificar o evento
2. Analisar causa raiz
3. Extrair lição
4. Documentar
5. Compartilhar

---

## Banco de Lições

### Índice por Tags
- **deploy:** lições sobre deploy
- **seguranca:** lições sobre segurança
- **performance:** lições sobre performance
- **comunicacao:** lições sobre comunicação
- **qualidade:** lições sobre qualidade

### Busca
Use tags para encontrar lições relacionadas ao tema que precisa.

---

## Revisão de Lições

### Quando Revisar
- Início de sprint
- Após incidente
- Antes de decisão importante
- Periodicamente (mensal)

### O que Verificar
- Lições ainda relevantes?
- Ações preventivas implementadas?
- Novas lições para adicionar?

---

## Referências

- [Qualidade](Qualidade.md)
- [Fluxo de Desenvolvimento](Fluxo.md)
- [Checklists](Checklists.md)
- [PROJECT_MEMORY](PROJECT_MEMORY.md)
- [CASE_STUDIES](CASE_STUDIES.md)
