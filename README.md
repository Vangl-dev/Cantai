# Cantai

Selecionador de hinos para o culto: letra, métrica, melodia original, temas e
o mesmo hino em outros hinários. Ajuda a pianista a escolher as músicas.

![Página do hino no computador, com o culto ao lado](docs/img/tela-computador.png)

## O que o app faz

- **Busca** por título, primeira linha, número ("sh 30", "ctp 314b") ou tema,
  nos hinários de uma vez ou só nos marcados.
- **Página do hino**: letra (tamanho ajustável com A / A), métrica, melodia
  original e temas. Tocar na métrica ou na melodia lista os hinos que podem
  ser cantados com a mesma música, em qualquer hinário.
- **Em outros hinários**: o mesmo hino no CTP, HCC, SH, Harpa e Novo Cântico.
- **Culto**: o "+" ao lado de cada hino monta a ordem do culto. Dá para dar
  nome e data, marcar o momento (Abertura, Ofertório, Ceia…), arrastar para
  reordenar, compartilhar pelo WhatsApp e guardar cultos para reabrir depois.
  No celular, o culto fica numa barra embaixo da tela; no computador, ao lado.
- Modo escuro automático e instalação na tela inicial do celular.

<img src="docs/img/tela-celular-culto.png" alt="Painel do culto no celular" width="300">

## Hinários

| Código | Hinário | Hinos | Métrica/melodia |
|--------|---------|-------|-----------------|
| CTP | Cantai Todos os Povos | 504 | índice de métricas |
| HCC | Hinário para o Culto Cristão | 609 | índice de métricas |
| SH  | Salmos e Hinos | 621 | herdada do equivalente |
| HC  | Harpa Cristã | 640 | herdada do equivalente |
| NC  | Novo Cântico | 405 | herdada do equivalente |
| CE  | Celebration Hymnal (inglês) | 693 | índice do livro, mais o tom |

Quando um hinário não traz métrica nem melodia, o hino herda as do mesmo
hino em outro hinário (CTP primeiro, depois HCC), e a tela mostra de onde veio.

O Celebration Hymnal entra **sem letra**: só existe em PDF de partitura, então
título, primeira linha, tom, melodia, métrica e temas vêm dos índices do fim do
livro (OCR). Ele se liga aos outros hinários pela **melodia**: a página de um
hino em português mostra o número e o tom no Celebration, e vice-versa. Mesma
melodia não quer dizer necessariamente a mesma letra.

## Como funciona

```
data/input/   PDFs e índices originais (fora do git)
     │  cantai importar-harpa | importar-nc | importar-metricas
     │         importar-continuacoes-ctp | importar-celebration
     ▼
data/base/    dados de base, versionados (não editar à mão)
     │  cantai build
     ▼
web/data/     o que o site publica (Netlify publica a pasta web/)
```

`cantai build` pode rodar quantas vezes quiser: não altera `data/base` e dá
sempre o mesmo resultado. As equivalências entre hinários são calculadas pelo
texto da letra (mesma sequência de palavras), mais o índice oficial CTP × SH.

## Uso

```bash
pip install -e ".[dev]"

PYTHONPATH=src python3 -m cantai.cli build      # gera web/data
PYTHONPATH=src python3 -m cantai.cli preview    # http://localhost:8000 (--port 8080 para outra porta)
python3 -m pytest                                # testes
```

## Antes de publicar

Rode `pytest`. Os testes conferem contagens, métricas conhecidas,
equivalências e se `web/data` está igual ao resultado do build. Se algum
falhar, algo que estava certo foi desfeito.

## Limitações conhecidas

- Traduções diferentes do mesmo hino original (ex.: "Castelo Forte" na Harpa
  e no CTP) não são ligadas, pois o texto é outro.
- O índice de temas da Harpa disponível está incompleto (403 de 640 hinos).
- O hino 378 do Novo Cântico não existe no PDF de origem.
- O HCC não tem tema de Natal no índice usado.
- Celebration: 26 primeiras linhas do índice ficaram sem número no OCR e não
  entraram (o hino entra pelo título); os nomes de melodia vêm do OCR e podem
  ter algum erro não detectado.

## Licença

[MIT License](LICENSE)
