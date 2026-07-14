# AI_CONSTITUTION.md

## Constituição Permanente dos Projetos

**Data de Criação:** 2026-07-06
**Versão:** 2.1.0
**Status:** Ativo
**Última Atualização:** 2026-07-09

---

## Preâmbulo

Esta Constituição define as regras inegociáveis que toda Inteligência Artificial deve seguir ao trabalhar em qualquer projeto deste framework. Ela existe para garantir qualidade, segurança e consistência.

---

## Artigo I - Princípios Fundamentais

### 1.1 Segurança em Primeiro Lugar
- NUNCA armazenar chaves, senhas ou tokens em código
- NUNCA committar arquivos `.env` ou credenciais
- SEMPRE usar variáveis de ambiente para segredos
- Validar todas as entradas de usuário

### 1.2 Qualidade Não Negociável
- Todo código deve passar em testes antes de ser commitado
- Todo código deve passar em lint antes de ser commitado
- Documentar decisões arquiteturais significativas
- Manter cobertura de testes acima de 80%

### 1.3 Transparência Radical
- Registrar toda decisão técnica importante
- Documentar lições aprendidas
- Manter CHANGELOG atualizado
- Comunicar bloqueios imediatamente

---

## Artigo II - Regras de Trabalho

### 2.1 Ao Iniciar um Projeto
1. Criar estrutura base usando `templates/projeto/`
2. Preencher `PROJECT_STATE.md` com contexto atual
3. Criar `ROADMAP.md` com fases iniciais
4. Configurar `AI_INSTRUCTIONS.md` específico do projeto
5. Registrar primeira decisão em `DECISIONS.md`

### 2.2 Ao Iniciar uma Sprint
1. Revisar `PROJECT_STATE.md`
2. Atualizar `ROADMAP.md` se necessário
3. Criar tarefas com estimativas
4. Preencher checklist de sprint
5. Registrar lições no final

### 2.3 Ao Commitar Código
1. Rodar testes: `npm test` / `pytest` / equivalente
2. Rodar lint: `npm run lint` / `ruff` / equivalente
3. Verificar que não há segredos expostos
4. Usar mensagens de commit semanticas
5. Atualizar CHANGELOG se for feature/fix relevante

### 2.4 Ao Fazer Deploy
1. Preencher checklist de deploy
2. Verificar variáveis de ambiente
3. Confirmar backup do banco (se aplicável)
4. Documentar o que mudou
5. Verificar health checks pós-deploy

### 2.5 Ao Encontrar um Bug
1. Documentar em `KNOWN_ISSUES.md`
2. Criar issue no GitHub (se aplicável)
3. Classificar severidade
4. Registrar lição aprendida se aplicável

---

## Artigo III - Regras de IA

### 3.1 O que a IA DEVE fazer
- Seguir esta Constituição em todos os momentos
- Perguntar quando houver dúvida
- Documentar decisões significativas
- Respeitar a estrutura de pastas definida
- Usar os prompts na ordem correta (000 → 090)
- Preencher checklists obrigatórios

### 3.2 O que a IA NÃO DEVE fazer
- Ignorar esta Constituição
- Pular etapas do fluxo
- Commitar sem testar
- Expor credenciais ou segredos
- Modificar `AI_CONSTITUTION.md` sem autorização explícita
- Tomar decisões arquiteturais sem registro

### 3.3 Comunicação com o Desenvolvedor
- Sempre informar o que está fazendo
- Alertar sobre riscos potenciais
- Sugerir alternativas quando apropriado
- Pedir confirmação antes de ações destrutivas

---

## Artigo IV - Padrões Obrigatórios

### 4.1 Estrutura de Pastas
Todo projeto DEVE seguir:
```
projeto/
├── README.md
├── PROJECT_STATE.md
├── ROADMAP.md
├── CHANGELOG.md
├── KNOWN_ISSUES.md
├── AI_INSTRUCTIONS.md
├── ARCHITECTURE.md
├── DATA_SOURCES.md
├── RECOVERY.md
├── SECURITY.md
├── TESTING.md
├── DECISIONS.md
├── docs/
├── src/
├── tests/
└── .github/
```

### 4.2 Formato de Commits
```
tipo(escopo): descrição curta

[corpo opcional]

[footer opcional - issues relacionadas]
```

Tipos: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`, `perf`

### 4.3 Formato de Branches
```
tipo/numero-descricao
feat/123-adicionar-login
fix/456-corrigir-erro-api
```

---

## Artigo V - Segurança

### 5.1 Dados Sensíveis
- NUNCA em código fonte
- NUNCA em commits
- NUNCA em logs
- SEMPRE em variáveis de ambiente
- SEMPRE em `.env` (nunca committado)

### 5.2 Autenticação
- Usar provedores confiáveis (OAuth, JWT)
- Nunca implementar criptografia caseira
- Rotacionar chaves periodicamente
- Usar HTTPS sempre

### 5.3 Validação
- Validar TODAS as entradas de usuário
- Sanitizar dados antes de usar
- Usar prepared statements em SQL
- Implementar rate limiting

---

## Artigo VI - Documentação

### 6.1 O que deve ser documentado
- Decisões arquiteturais (em DECISIONS.md)
- Lições aprendidas (em Licoes_Aprendidas.md)
- Mudanças significativas (em CHANGELOG.md)
- Problemas conhecidos (em KNOWN_ISSUES.md)
- Estado atual (em PROJECT_STATE.md)

### 6.2 Quando documentar
- Ao tomar uma decisão técnica
- Ao aprender algo novo
- Ao encontrar um problema
- Ao completar uma sprint
- Ao fazer um deploy

---

## Artigo VII - Emergências

### 7.1 Se o sistema quebrar
1. Verificar logs
2. Identificar a causa raiz
3. Documentar o incidente
4. Implementar correção
5. Testar a correção
6. Atualizar RECOVERY.md

### 7.2 Se dados forem perdidos
1. Verificar backups
2. Restaurar do backup mais recente
3. Documentar o que aconteceu
4. Implementar prevenção

---

## Artigo VIII - Ações Proibidas

### 8.1 Banco de Dados
- NUNCA apagar banco de dados
- NUNCA recriar banco existente
- NUNCA alterar schema sem migração
- NUNCA remover campos existentes
- NUNCA executar DELETE sem WHERE
- NUNCA truncar tabelas
- NUNCA dropar tabelas

### 8.2 Arquivos
- NUNCA apagar diretórios
- NUNCA executar rm em arquivos importantes
- NUNCA substituir arquivos oficiais
- NUNCA utilizar diretórios temporários como fonte definitiva
- NUNCA remover documentação
- NUNCA remover testes
- NUNCA apagar histórico

### 8.3 JSON/Configurações
- NUNCA substituir JSON de produção
- NUNCA alterar configurações sem validação
- NUNCA sobrescrever .env

### 8.4 Funcionalidades
- NUNCA remover funcionalidades existentes
- NUNCA quebrar retrocompatibilidade
- NUNCA alterar interfaces públicas sem versão

### 8.5 Git/Deploy
- NUNCA alterar Git sem autorização
- NUNCA executar deploy automático
- NUNCA alterar arquivos em produção sem validação
- NUNCA force push sem autorização
- NUNCA alterar histórico de commits

### 8.6 Protocolo Obrigatório
ANTES de qualquer alteração estrutural:
1. BACKUP
2. PLANO
3. APROVAÇÃO
4. EXECUÇÃO
5. VALIDAÇÃO

---

## Artigo IX - Testes Obrigatórios

### 9.1 Princípio Fundamental
Test Driven Development (TDD) sempre que possível.
Nenhuma Sprint poderá ser considerada concluída sem testes.

### 9.2 Tipos de Teste
- **Unitários:** Obrigatório, cobertura > 80%
- **Integração:** Obrigatório, cobertura > 60%
- **Regressão:** Obrigatório após cada correção de bug
- **Interface:** Obrigatório quando aplicável
- **Manuais:** Obrigatório após cada feature
- **Performance:** Quando aplicável
- **Importação/Exportação:** Quando aplicável
- **Banco:** Obrigatório para qualquer alteração de banco
- **Compatibilidade:** Quando aplicável

### 9.3 Regras
- Toda funcionalidade nova DEVE possuir testes próprios
- Toda correção de bug DEVE incluir teste que impeça retorno
- Nenhuma Sprint é concluída sem testes
- Nenhum deploy ocorre sem todos os testes aprovados

---

## Artigo X - Checkpoints

### 10.1 Ao término de cada etapa executar:
- ✓ Build
- ✓ Auditoria
- ✓ Testes
- ✓ Preview
- ✓ Backup
- ✓ Atualização da documentação
- ✓ Atualização do changelog
- ✓ Atualização do roadmap
- ✓ Atualização do PROJECT_MEMORY

---

## Artigo XI - Validação Antes do Deploy

### 11.1 Nenhum deploy sem:
- ✔ Build concluído
- ✔ Todos os testes aprovados
- ✔ Auditorias aprovadas
- ✔ Preview aprovado pelo usuário
- ✔ Backup realizado
- ✔ Changelog atualizado
- ✔ Roadmap atualizado
- ✔ PROJECT_MEMORY atualizado
- ✔ Documentação sincronizada
- ✔ Versionamento Git correto

---

## Artigo XII - Padrão de Sprint

### 12.1 Sequência Obrigatória
1. Planejamento
2. Implementação
3. Testes unitários
4. Testes de integração
5. Auditoria
6. Preview local
7. Correções
8. Nova bateria de testes
9. Atualização da documentação
10. Atualização da memória do projeto
11. Backup
12. Aprovação do usuário
13. Commit
14. Deploy

**É proibido pular etapas.**

---

## Artigo XIII - Regra Geral

### 13.1 Princípios Absolutos
- Sempre preservar o trabalho existente
- Sempre evoluir o projeto
- Nunca reconstruir algo que possa ser migrado
- Nunca perder informações já produzidas
- Documentação, testes e memória do projeto possuem a mesma importância que o código-fonte

---

## Artigo XIV - Modificações

### 14.1 Processo de alteração
1. Propor mudança por escrito
2. Justificar a necessidade
3. Revisar impactos
4. Aprovar com desenvolvedor
5. Implementar mudança
6. Atualizar versão desta Constituição

### 14.2 Versionamento
- Mudanças menores: incrementar patch (1.0.x)
- Novos artigos: incrementar minor (1.x.0)
- Reestruturação completa: incrementar major (x.0.0)

---

## Artigo XV - Condições de Parada (Stopping Conditions)

### 15.1 Objetivo
Prevenir que agentes de IA entrem em loops infinitos de validação, documentação ou reescrita. Estas regras são permanentes e inegociáveis.

### 15.2 Regras

#### Regra 1 - Sprint Única
Cada Sprint possui apenas um objetivo. Quando esse objetivo for entregue, a Sprint termina. **É proibido iniciar automaticamente a Sprint seguinte.**

#### Regra 2 - Checklist Única Execução
Checklist é executada apenas **UMA vez**. Caso exista alguma pendência: registrar a pendência, encerrar a Sprint, aguardar decisão do usuário. **É proibido executar novamente a mesma checklist.**

#### Regra 3 - Parada Após Relatório
Após apresentar o relatório final, a IA deve **parar imediatamente**. Não revisar novamente. Não validar novamente. Não melhorar novamente.

#### Regra 4 - Documentação Aprovada é Estável
Documentação aprovada é considerada estável. Ela somente poderá ser alterada quando uma Sprint modificar informações daquele documento. **É proibido reescrever documentação apenas por melhoria de texto.**

#### Regra 5 - Artefatos Protegidos
Artefatos aprovados pelo usuário tornam-se protegidos. **É proibido:** apagar, substituir, mover ou renomear qualquer artefato aprovado sem autorização explícita do usuário.

#### Regra 6 - Sem Repetição de Tarefas
Nenhuma Sprint poderá executar novamente tarefas já concluídas. Exemplos: copiar documentação, recriar estrutura, executar checklist, validar arquitetura — caso essas tarefas já tenham sido aprovadas.

#### Regra 7 - Alterações em Sprints Anteriores
Caso a IA identifique necessidade de alterar uma Sprint anterior, ela deverá **interromper a execução e perguntar ao usuário**. Nunca poderá tomar essa decisão automaticamente.

#### Regra 8 - Limite de Tempo
Tempo máximo de execução contínua: **30 minutos**. Ao atingir esse limite: encerrar, apresentar o estado atual, aguardar nova Sprint. **Nunca permanecer em execução indefinidamente.**

#### Regra 9 - Condição Explícita de Conclusão
Toda Sprint deve possuir uma condição explícita de conclusão. Exemplo: "Após criar o arquivo X, parar." ou "Após apresentar o relatório, parar."

### 15.3 Princípio Central
Estas regras existem para impedir que a IA execute trabalho desnecessário, desperdice tempo ou modifique o que já foi aprovado. O usuário é sempre quem decide quando algo está pronto.

---

## Termo de Aceite

Ao trabalhar em qualquer projeto deste framework, a IA confirma que leu, compreende e seguirá esta Constituição em sua totalidade.

**Última atualização:** 2026-07-09
