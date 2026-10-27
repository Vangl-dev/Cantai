# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.2.0] - 2026-10-27

### Added
- Novo visual inspirado no hinário impresso: capa verde, números dourados,
  melodia em versalete, letra em Literata; modo escuro automático
- Novo logo (hinário aberto com nota) e ícones do app; os antigos estão em
  `arquivo/logo-antigo`
- Painel "Culto": nome e data, momento litúrgico de cada hino, arrastar para
  reordenar, Compartilhar (WhatsApp no celular), cultos salvos no mesmo painel
- No celular, barra fixa com o culto atual; no computador, painel ao lado
- Tamanho da letra ajustável na página do hino (A− / A+)
- Atalhos de tema na tela inicial

### Changed
- Resultados em lista, com botão "+" para incluir no culto direto da busca
- "Salvar este culto" atualiza o culto salvo de mesmo nome e data

## [1.1.0] - 2026-10-27

### Added
- Harpa Cristã (640 hinos, temas do índice de assuntos onde disponível)
- Novo Cântico (405 hinos, temas pelas seções do índice por assunto)
- Equivalências automáticas entre os 5 hinários, pelo texto da letra
  (`web/data/equivalencias.json`), mais o índice oficial CTP × SH
- Métrica e melodia herdadas do hino equivalente quando o hinário não as
  traz (SH, Harpa, Novo Cântico), indicando a origem ("via CTP-13")
- "Mesma métrica" e "mesma melodia" comparam entre hinários
  (8.7.8.7.D = 8.7.8.7.8.7.8.7; C.M. = 8.6.8.6)
- Busca por número com hinário ("sh 30", "ctp 314b") e resultados por relevância
- Botão "Escolher" na tela do hino
- Build reproduzível (`cantai build`) a partir de `data/base`
- Testes automatizados (`pytest`) contra regressão dos dados publicados

### Fixed
- Métricas do CTP: o importador só lia cabeçalhos "##" e aplicava a métrica
  anterior a dezenas de hinos (69 com "8.8.8.6 - 6.6.8.6")
- Métricas e melodias do HCC: cerca de 60% estavam erradas; agora vêm do
  índice de métricas do HCC lido por colunas
- 172 letras do CTP cortadas na quebra de página do PDF, com rodapé
  ("Hinário 1 - 136.pmd") dentro da letra
- CTP 30, 36 e 314: as variantes A e B tinham o mesmo número e a segunda
  ficava inacessível
- Clicar num equivalente não abria o hino (número comparado como texto)
- "Voltar" voltava para o hinário errado e empilhava a navegação em dobro
- SH: números de página, notas de rodapé e marcas " i" dentro das letras
- Temas do SH não eram mapeados para os temas canônicos
- Link "GitHub" do Sobre apontava para um repositório que não é do projeto

### Changed
- Dados no formato unificado (`id`, `hymnal`, `topics_canonical`,
  `metric_key`, `melody_keys`, `via`) em todos os hinários
- Scripts antigos que sobrescreviam dados arquivados em `arquivo/scripts-antigos`

## [0.4.0] - 2026-07-13

### Added
- Salmos e Hinos (SH) importado com 621 hinos
- Temas oficiais do SH via correspondências CTP × SH
- Registro Canônico de Temas (RCT) - 25 temas
- Mapa de Equivalências (111 equivalências)
- Ferramenta de Auditoria de Equivalências
- Suíte de Validação do Sistema
- Painel "Sobre o Cantai"
- Botão "Sobre" com informações do projeto
- Destaque "⭐ Também no CTP" para equivalentes
- Seção "Também disponível em" na tela do hino
- Persistência da seleção de hinários (localStorage)
- Validação de uso em culto real

### Changed
- Interface atualizada para suportar 3 hinários (CTP, HCC, SH)
- Temas canônicos substituem lista original (25 temas)
- Motor de Sugestões V2 com suporte multi-hinários
- Cabeçalho reorganizado (logo ao lado do título)

### Fixed
- Bug de navegação SH → CTP (botão "Ver letra")
- Bug de persistência dos hinários (localStorage)
- Bug de temas SH retornando todos os hinos
- Código paliativo removido da interface

## [0.4.1] - 2026-07-14

### Fixed
- SH hymns now show "⭐ Também no CTP" equivalent badge (index reverso adicionado)
- SH hymn detail view now shows CTP equivalents in "Também disponível em" section

## [0.3.0] - 2026-07-10

### Added
- HCC importer with relationship architecture
- HCC JSON with 609 hymns imported
- Content equivalences (20 confirmed HCC × CTP)
- Melody relationships (69 musical equivalences)
- Canonical themes mapping
- Metrics importer (323 hymns with metrics)
- Melodies display in hymn detail
- Navigation by themes, metrics, and melodies
- Continuous navigation with history
- Agenda de Culto (Sprint 25)
- Saved Lists (Sprint 26)
- Canonical topics YAML mapping
- Architecture Decision Records (ADR-0001, ADR-0002, ADR-0003)

### Changed
- Interface redesigned with dark theme (Cantai original style)
- Suggestion engine (3 hymns max)
- Cards with hymnal badge, number, title, first line
- Buttons: "Ver letra" and "Escolher"
- Results only appear after search or theme selection

### Fixed
- Hymns with duplicate numbers identified (30, 36, 314)
- Metrics and melodies imported from official sources

## [0.2.0] - 2026-07-10

### Added
- Metrics importer for CTP (323 hymns)
- Melodies importer for CTP (323 hymns)
- Metrics validation report
- Suggestion engine (V1)
- Navigation by relationships (themes, metrics, melodies)
- Continuous navigation with history stack

### Changed
- Interface updated with metrics and melodies display
- Hymn detail shows topics, metric, melody when available

## [0.1.0] - 2026-07-09

### Added
- Project structure with Python 3.12+
- Domain model `Hymn` with dataclass
- Parser interface `HymnParser` (ABC)
- CTP parser implementation
- JSON exporter
- Web preview with search functionality
- Theme importer from markdown index
- Theme dropdown menu

### Changed
- Parser now extracts 504 hymns (including variants)
- 82 themes imported from official index
- 501 hymns classified with themes

### Fixed
- Parser handles various PDF formats (leading spaces, double hyphens, variants)
- Parser handles special characters (accents, punctuation)
- Parser handles LaTeX-style notation in index

## [0.0.1] - 2026-07-09

### Added
- Initial project structure
- pyproject.toml with dependencies
- Configuration files
- README documentation
