let database = { version: null, hymns: [] };
let cultoHymns = JSON.parse(localStorage.getItem("cultoHymns") || "[]");
let historico = JSON.parse(localStorage.getItem("cantaiHistorico") || "[]");
let currentModalHymn = null;

const CANONICAL_TOPICS = [
  "Acao de Gracas","Adoracao","Advento","Afirmacao de Fe","Aniversario",
  "Ano Novo","Ascensao do Senhor","Batismo","Batismo do Senhor","Batismo Infantil",
  "Bencao","Casamento","Ciclo do Natal","Comunhao","Confianca","Confissao",
  "Consagracao","Contricao","Convite a Adoracao","Credo","Criancas","Cristo Rei",
  "Declaracao de Perdao","Dia da Mulher","Dia do Senhor","Dia dos Pais","Diaconia",
  "Domingo de Ramos","Emerencia","Envio","Epifania","Espirito Santo","Evangelho",
  "Familia","FATIPI","Funeral","Igreja","Intercessao","Introito","IPIB",
  "Jubilacao","Juventude","Leitura da Palavra","Leitura do Evangelho","Louvor",
  "Missao","Missoes","Natal","Ofertorio","Oracao","Oracao de Confissao",
  "Oracao de Gratidao","Oracao Eucaristica","Oracao por Iluminacao","Oracoes",
  "Pai Nosso","Paixao de Cristo","Palavra de Deus","Pascoa","Partir do Pao",
  "Patria","Pentecostes","Primicias","Proclamacao da Palavra","Profissao de Fe",
  "Quaresma","Reforma","Ressurreicao","Santa Ceia","Santificacao",
  "Saudacao da Paz","Segunda Vinda","Semana da Paixao","Tempo Pascal",
  "Testemunho","Transfiguracao do Senhor","Trindade","UMPI"
];

const SYNONYMS = {
  "Acao de Gracas":["Acao de Gracas","Gratidao","GRATIDAO"],
  "Adoracao":["Adoracao","Louvor","Louvores","Adoracao e Louvor","Exaltacao","Gloria","Magnificar","Deus, o Filho - Louvores","Culto - Abertura"],
  "Advento":["Advento","Esperanca"],
  "Afirmacao de Fe":["Afirmacao de Fe","Credo (Apos o)","Profissao de Fe"],
  "Aniversario":["Aniversario"],
  "Ano Novo":["Ano Novo","Passagem do Ano","Passagem do ano","ANO NOVO"],
  "Ascensao do Senhor":["Ascensao do Senhor","Ascensao"],
  "Batismo":["Batismo","Batismo nas aguas","Igreja - Batismo","BATISMO"],
  "Batismo do Senhor":["Batismo do Senhor"],
  "Batismo Infantil":["Batismo Infantil"],
  "Bencao":["Bencao","Bencao Apostolica"],
  "Casamento":["Casamento","Matrimonio"],
  "Ciclo do Natal":["Ciclo do Natal"],
  "Comunhao":["Comunhao","Uniao Fraternal"],
  "Confianca":["Confianca","Firmeza","Protecao e Ajuda","Guia"],
  "Confissao":["Confissao"],
  "Consagracao":["Consagracao","Igreja - Consagracao","Obediencia","VIDA CRISTA - CONSAGRACAO"],
  "Contricao":["Contricao"],
  "Convite a Adoracao":["Convite a Adoracao","Convite a Adoracao e Louvor","Louvores ao Deus Trino","Introito"],
  "Credo":["Credo"],
  "Criancas":["Criancas","CRIANCAS"],
  "Cristo Rei":["Cristo Rei","Cristo, Rei do Universo"],
  "Declaracao de Perdao":["Declaracao de Perdao","Perdao"],
  "Dia da Mulher":["Dia da Mulher","Dia Internacional da Mulher","Dia das Maes"],
  "Dia do Senhor":["Dia do Senhor"],
  "Dia dos Pais":["Dia dos Pais"],
  "Diaconia":["Diaconia","Diakonia"],
  "Domingo de Ramos":["Domingo de Ramos","Entrada Triunfal"],
  "Emerencia":["Emerencia","Emergencia"],
  "Envio":["Envio","Envio (Apos o)","Comissionamento","FATIPI","IPIB","UMPI"],
  "Epifania":["Epifania","Manifestacao de Cristo"],
  "Espirito Santo":["Espirito Santo","Deus, o Espirito Santo","ESPIRITO SANTO"],
  "Evangelho":["Evangelho","Salvacao","Culto - Evangelho"],
  "Familia":["Familia","Lar"],
  "FATIPI":["FATIPI"],
  "Funeral":["Funeral","Consolacao"],
  "Igreja":["Igreja"],
  "Intercessao":["Intercessao"],
  "Introito":["Introito"],
  "IPIB":["IPIB"],
  "Jubilacao":["Jubilacao"],
  "Juventude":["Juventude","Mocidade"],
  "Leitura da Palavra":["Leitura da Palavra","Leitura da Palavra (Apos a)","Leitura Biblica","Para Leitura Biblica"],
  "Leitura do Evangelho":["Leitura do Evangelho","Leitura do Evangelho (Apos ou apos a)","Leitura do Evangelho (Apos a)"],
  "Louvor":["Louvor"],
  "Missao":["Missao","Evangelizacao"],
  "Missoes":["Missoes","Evangelizacao Mundial"],
  "Natal":["Natal","Nascimento","Nascimento de Cristo","Deus, o Filho - Natal","Seu nascimento (Natal)","CRISTO - NATAL DE"],
  "Ofertorio":["Ofertorio","Ofertorio (Antes do)"],
  "Oracao":["Oracao","Suplica","Clamor","Reuniao de Oracao"],
  "Oracao de Confissao":["Oracao de Confissao","Oracao de Confissao (Apos ou apos a)","Oracao de Confissao (Apos a)"],
  "Oracao de Gratidao":["Oracao de Gratidao","Oracao de Gratidao (Apos a)"],
  "Oracao Eucaristica":["Oracao Eucaristica","Oracao Eucaristica (Apos a)","Oracao Eucaristica (Na)"],
  "Oracao por Iluminacao":["Oracao por Iluminacao"],
  "Oracoes":["Oracoes","Oracoes (Apos as)","Oracoes de Intercessao (Apos as)"],
  "Pai Nosso":["Pai Nosso"],
  "Paixao de Cristo":["Paixao de Cristo","Cruz"],
  "Palavra de Deus":["Palavra de Deus","Biblia","Escrituras","A Palavra do Senhor","BIBLIA"],
  "Pascoa":["Pascoa","Tempo Pascal","Semana da Paixao","Transfiguracao do Senhor"],
  "Partir do Pao":["Partir do Pao","Partir do Pao (Apos o)"],
  "Patria":["Patria"],
  "Pentecostes":["Pentecostes"],
  "Primicias":["Primicias"],
  "Proclamacao da Palavra":["Proclamacao da Palavra","Proclamacao da Palavra (Apos a)"],
  "Profissao de Fe":["Profissao de Fe"],
  "Quaresma":["Quaresma","Quaresma (Inicio da)"],
  "Reforma":["Reforma","Reforma Protestante"],
  "Ressurreicao":["Ressurreicao","Ressurreicao e Ascensao","Deus, o Filho - Sua Ressurreicao","Sua ressurreicao","CRISTO - RESSURREICAO DE"],
  "Santa Ceia":["Santa Ceia","Ceia do Senhor","Santa Ceia (Apos a)","Santa Ceia (Apos a Celebracao da)","Santa Ceia (Durante a)","Ceia","Igreja - Ceia do Senhor"],
  "Santificacao":["Santificacao","Vida Santa","Santidade"],
  "Saudacao da Paz":["Saudacao da Paz"],
  "Segunda Vinda":["Segunda Vinda","Volta de Cristo","Volta do Senhor","Sua segunda vinda","CRISTO - A VOLTA DE"],
  "Semana da Paixao":["Semana da Paixao"],
  "Tempo Pascal":["Tempo Pascal"],
  "Testemunho":["Testemunho"],
  "Transfiguracao do Senhor":["Transfiguracao do Senhor"],
  "Trindade":["Trindade","Deus, o Pai"],
  "UMPI":["UMPI"]
};

let _synonymToCanonical = {};
for (const [canon, variants] of Object.entries(SYNONYMS)) {
  for (const v of variants) {
    _synonymToCanonical[normalize(v)] = canon;
  }
}

async function loadDatabase() {
  try {
    const response = await fetch("cantai.json");
    const data = await response.json();
    database = data;
    document.getElementById("db-version").textContent = data.version;
    document.getElementById("db-count").textContent = data.hymns.length;
  } catch (error) {
    console.error("Erro ao carregar banco de dados:", error);
    document.getElementById("db-version").textContent = "erro";
    document.getElementById("db-count").textContent = "0";
  }
  populateTemaDropdown();
  renderCulto();
}

function normalize(str) {
  return str
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .toLowerCase();
}

function populateTemaDropdown() {
  const select = document.getElementById("tema");
  const sorted = CANONICAL_TOPICS.slice().sort((a, b) => a.localeCompare(b, "pt-BR"));
  for (const topic of sorted) {
    const opt = document.createElement("option");
    opt.value = topic;
    opt.textContent = topic;
    select.appendChild(opt);
  }
}

function searchHymns(query) {
  if (!query || query.trim().length === 0) return [];
  const q = normalize(query.trim());
  if (q.length === 0) return [];
  const results = [];
  for (const h of database.hymns) {
    const numStr = String(h.number);
    const titleNorm = normalize(h.title || "");
    const firstLineNorm = normalize(h.first_line || "");
    const lyricsNorm = normalize(h.lyrics || "");

    let score = 0;
    const matched = numStr.includes(q) ||
      titleNorm.includes(q) ||
      firstLineNorm.includes(q) ||
      lyricsNorm.includes(q);
    if (!matched) continue;

    if (titleNorm.includes(q)) score += 50;
    if (firstLineNorm.includes(q)) score += 30;
    if (lyricsNorm.includes(q)) score += 5;
    if (numStr === q) score += 200;

    results.push({ hymn: h, score });
  }
  results.sort((a, b) => b.score - a.score);
  return results.map(r => r.hymn);
}

let searchShowAll = false;

function renderSearchResults(results) {
  const container = document.getElementById("resultados-busca");
  const info = document.getElementById("busca-info");
  container.style.display = "";

  if (results.length === 0) {
    container.innerHTML = "";
    info.style.display = "none";
    return;
  }

  info.style.display = "";
  const limit = searchShowAll ? results.length : Math.min(results.length, 5);
  const shown = results.slice(0, limit);

  info.innerHTML = `Encontrados: <strong>${results.length}</strong> hinos`;

  container.innerHTML = "";
  for (const h of shown) {
    container.appendChild(makeCard(h));
  }

  if (results.length > 5 && !searchShowAll) {
    const btn = document.createElement("button");
    btn.className = "btn-mostrar-mais";
    btn.textContent = `Mostrar todos (${results.length})`;
    btn.onclick = () => {
      searchShowAll = true;
      renderSearchResults(results);
    };
    container.appendChild(btn);
  } else if (searchShowAll && results.length > 5) {
    const btn = document.createElement("button");
    btn.className = "btn-mostrar-mais";
    btn.textContent = "Mostrar menos";
    btn.onclick = () => {
      searchShowAll = false;
      renderSearchResults(results);
    };
    container.appendChild(btn);
  }
}

function getSelectedHymnals() {
  const map = { hctp: "CTP", harpa: "HARPA", cantor: "CC", sh: "SH", nc: "NC" };
  const selected = [];
  for (const [id, name] of Object.entries(map)) {
    if (document.getElementById(id).checked) selected.push(name);
  }
  return selected;
}

function suggestHymns() {
  const tema = document.getElementById("tema").value;
  const resultados = document.getElementById("resultados");
  const selectedHymnals = getSelectedHymnals();

  if (selectedHymnals.length === 0) {
    resultados.innerHTML =
      "<p style='text-align:center;color:var(--text-secondary)'>Selecione pelo menos um hinario.</p>";
    return;
  }

  const temaNormalized = normalize(tema);
  const canonicalTema = _synonymToCanonical[temaNormalized] || tema;

  function hymnMatchesTema(h) {
    if (!h.topics || h.topics.length === 0) return false;
    for (const t of h.topics) {
      const tCanonical = _synonymToCanonical[normalize(t)] || t;
      if (tCanonical === canonicalTema) return true;
    }
    return false;
  }

  const candidates = database.hymns.filter(h =>
    selectedHymnals.includes(h.hymnal) && hymnMatchesTema(h)
  );

  const shuffled = [...candidates].sort(() => Math.random() - 0.5);

  const byHymnal = {};
  for (const h of shuffled) {
    if (!byHymnal[h.hymnal]) byHymnal[h.hymnal] = [];
    byHymnal[h.hymnal].push(h);
  }

  const picks = [];
  const limits = { CTP: 3, HARPA: 1, CC: 1, SH: 1, NC: 1 };
  for (const hymnal of ["CTP", "HARPA", "CC", "SH", "NC"]) {
    if (!selectedHymnals.includes(hymnal)) continue;
    const limit = limits[hymnal] || 1;
    const pool = byHymnal[hymnal] || [];
    for (let i = 0; i < Math.min(limit, pool.length); i++) {
      picks.push(pool[i]);
    }
  }

  if (picks.length === 0) {
    resultados.innerHTML =
      "<p style='text-align:center;color:var(--text-secondary)'>Nenhum hino encontrado para esta selecao.</p>";
    return;
  }

  resultados.innerHTML = "";
  picks.forEach((hymn) => resultados.appendChild(makeCard(hymn)));

  const btnNovas = document.createElement("button");
  btnNovas.className = "btn-novas";
  btnNovas.textContent = "Outras sugestoes";
  btnNovas.onclick = () => suggestHymns();
  resultados.appendChild(btnNovas);
}

function makeCard(hymn) {
  const card = document.createElement("div");
  card.className = "hino-card";

  card.innerHTML = `
    <div class="hino-cabecalho">
      <span class="hino-hinario">${hymn.hymnal}</span>
      <span class="hino-numero">${hymn.number}</span>
    </div>
    <div class="hino-titulo">${hymn.title}</div>
    <div class="hino-primeira-linha">${hymn.first_line}</div>
    <div style="display:flex;gap:0.5rem">
      <button class="btn-ver-letra" onclick='openLetra(${JSON.stringify(hymn).replace(/'/g, "&#39;")})'>Ver letra</button>
      <button class="btn-escolher" onclick="addToCulto('${hymn.hymnal}','${hymn.number}','${hymn.title.replace(/'/g, "\\'")}')">Escolher</button>
    </div>
  `;
  return card;
}

function openLetra(hymn) {
  currentModalHymn = hymn;
  document.getElementById("modal-hinario").textContent = hymn.hymnal;
  document.getElementById("modal-numero").textContent = hymn.number;
  document.getElementById("modal-titulo").textContent = hymn.title;
  document.getElementById("modal-primeira-linha").textContent = hymn.first_line;
  document.getElementById("modal-letra-texto").textContent = hymn.lyrics || "Letra nao disponivel.";
  document.getElementById("modal-letra").classList.add("active");
}

function chooseFromModal() {
  if (currentModalHymn) {
    addToCulto(currentModalHymn.hymnal, currentModalHymn.number, currentModalHymn.title);
    closeModalById("modal-letra");
  }
}

function closeModal(event, modalId) {
  if (event.target.id === modalId) {
    document.getElementById(modalId).classList.remove("active");
  }
}

function closeModalById(modalId) {
  document.getElementById(modalId).classList.remove("active");
}

function openSobre() {
  document.getElementById("sobre-count").textContent = database.hymns ? database.hymns.length : 0;
  document.getElementById("modal-sobre").classList.add("active");
}

function addToCulto(hymnal, number, title) {
  const exists = cultoHymns.some(
    (h) => h.hymnal === hymnal && h.number === number
  );
  if (!exists) {
    cultoHymns.push({ hymnal, number, title });
    localStorage.setItem("cultoHymns", JSON.stringify(cultoHymns));
    renderCulto();
  }
}

function removeFromCulto(index) {
  cultoHymns.splice(index, 1);
  localStorage.setItem("cultoHymns", JSON.stringify(cultoHymns));
  renderCulto();
}

function renderCulto() {
  const container = document.getElementById("culto-lista");
  const section = document.getElementById("secao-culto");
  if (cultoHymns.length === 0) {
    section.style.display = "none";
    return;
  }
  section.style.display = "";
  container.innerHTML = "";
  cultoHymns.forEach((h, i) => {
    const item = document.createElement("div");
    item.className = "culto-item";
    item.innerHTML = `
      <div class="culto-item-info">
        <span class="culto-item-hinario">${h.hymnal}</span>
        <span class="culto-item-numero">${h.number}</span>
        <span class="culto-item-titulo">${h.title}</span>
      </div>
      <button class="culto-item-remover" onclick="removeFromCulto(${i})">X</button>
    `;
    container.appendChild(item);
  });
}

function copyProgramacao() {
  if (cultoHymns.length === 0) return;
  const lines = ["Culto", ""];
  for (const h of cultoHymns) {
    lines.push(`${h.hymnal} ${h.number} - ${h.title}`);
  }
  const text = lines.join("\n");
  navigator.clipboard.writeText(text).then(() => {
    const btn = document.getElementById("btn-copiar");
    const original = btn.textContent;
    btn.textContent = "Copiado!";
    setTimeout(() => (btn.textContent = original), 2000);
  });

  const entry = {
    date: new Date().toISOString(),
    hymns: cultoHymns.map(h => ({ hymnal: h.hymnal, number: h.number, title: h.title }))
  };
  historico.unshift(entry);
  if (historico.length > 50) historico = historico.slice(0, 50);
  localStorage.setItem("cantaiHistorico", JSON.stringify(historico));
}

function exportHistorico() {
  if (cultoHymns.length === 0) return;
  const data = {
    exported_at: new Date().toISOString(),
    hymns: cultoHymns,
  };
  const blob = new Blob([JSON.stringify(data, null, 2)], {
    type: "application/json",
  });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = `cantai-culto-${new Date().toISOString().slice(0, 10)}.json`;
  a.click();
  URL.revokeObjectURL(url);
}

function importHistorico() {
  const input = document.createElement("input");
  input.type = "file";
  input.accept = ".json";
  input.onchange = (e) => {
    const file = e.target.files[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = (ev) => {
      try {
        const data = JSON.parse(ev.target.result);
        if (data.hymns && Array.isArray(data.hymns)) {
          cultoHymns = data.hymns;
          localStorage.setItem("cultoHymns", JSON.stringify(cultoHymns));
          renderCulto();
        }
      } catch {
        alert("Arquivo invalido.");
      }
    };
    reader.readAsText(file);
  };
  input.click();
}

function limparHistorico() {
  if (cultoHymns.length === 0) return;
  if (!confirm("Limpar todos os hinos deste culto?")) return;
  cultoHymns = [];
  localStorage.setItem("cultoHymns", JSON.stringify(cultoHymns));
  renderCulto();
}

function handleSearch() {
  const input = document.getElementById("busca");
  const query = input.value.trim();
  const btnSugerir = document.getElementById("btn-sugerir");
  const resultadosBusca = document.getElementById("resultados-busca");
  const info = document.getElementById("busca-info");

  searchShowAll = false;

  if (query.length === 0) {
    btnSugerir.style.display = "";
    resultadosBusca.style.display = "none";
    info.style.display = "none";
    return;
  }
  btnSugerir.style.display = "none";
  const results = searchHymns(query);
  renderSearchResults(results);
}

function formatDate(isoStr) {
  const d = new Date(isoStr);
  const now = new Date();
  const diffMs = now - d;
  const diffDays = Math.floor(diffMs / 86400000);

  if (diffDays === 0) return "Hoje";
  if (diffDays === 1) return "Ontem";
  if (diffDays < 7) return "Semana passada";
  if (diffDays < 30) return "Este mes";
  return d.toLocaleDateString("pt-BR", { day: "2-digit", month: "short", year: "numeric" });
}

function openHistorico() {
  const container = document.getElementById("historico-lista");
  container.innerHTML = "";

  if (historico.length === 0) {
    container.innerHTML = "<p style='text-align:center;color:var(--text-secondary)'>Nenhum culto registrado.</p>";
    document.getElementById("modal-historico").classList.add("active");
    return;
  }

  let lastGroup = "";
  for (let i = 0; i < historico.length; i++) {
    const entry = historico[i];
    const group = formatDate(entry.date);

    if (group !== lastGroup) {
      const sep = document.createElement("div");
      sep.className = "historico-sep";
      if (lastGroup !== "") {
        const line = document.createElement("div");
        line.className = "historico-linha";
        container.appendChild(line);
      }
      sep.textContent = group;
      container.appendChild(sep);
      lastGroup = group;
    }

    const item = document.createElement("div");
    item.className = "historico-item";
    item.innerHTML = `
      <div class="historico-item-hinos">
        ${entry.hymns.map(h => `<span class="historico-hino">${h.hymnal} ${h.number}</span>`).join(" ")}
      </div>
      <div class="historico-item-botoes">
        <button class="historico-btn" onclick="copiarHistorico(${i})" title="Copiar">Copiar</button>
        <button class="historico-btn historico-btn-perigo" onclick="removerHistorico(${i})" title="Remover">X</button>
      </div>
    `;
    container.appendChild(item);
  }

  document.getElementById("modal-historico").classList.add("active");
}

function copiarHistorico(index) {
  const entry = historico[index];
  const lines = entry.hymns.map(h => `${h.hymnal} ${h.number} - ${h.title}`);
  navigator.clipboard.writeText(lines.join("\n")).then(() => {
    alert("Copiado!");
  });
}

function removerHistorico(index) {
  if (!confirm("Remover este culto do historico?")) return;
  historico.splice(index, 1);
  localStorage.setItem("cantaiHistorico", JSON.stringify(historico));
  openHistorico();
}

function limparHistoricoCompleto() {
  if (historico.length === 0) return;
  if (!confirm("Limpar todo o historico de cultos?")) return;
  historico = [];
  localStorage.setItem("cantaiHistorico", JSON.stringify(historico));
  openHistorico();
}

document.addEventListener("DOMContentLoaded", () => {
  loadDatabase();
  document.getElementById("busca").addEventListener("input", handleSearch);
});
