# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
