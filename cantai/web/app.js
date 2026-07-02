let database = { version: null, hymns: [] };
let cultoHymns = JSON.parse(localStorage.getItem("cultoHymns") || "[]");
let historico = JSON.parse(localStorage.getItem("cantaiHistorico") || "[]");
let currentModalHymn = null;
let selectedTopics = [];
let allTopicsSorted = [];
const SHOW_INITIAL_TOPICS = 12;

const CANONICAL_TOPICS = [
  "Adoração","Santidade","Trindade","Ceia do Senhor","Natal","Páscoa",
  "Pentecostes","Espírito Santo","Missões","Evangelização","Consagração",
  "Confiança","Esperança","Despedida","Chamado","Oração","Família",
  "Casamento","Batismo","Juventude","Crianças","Funeral","Ressurreição",
  "Segunda Vinda","Vida Cristã","Gratidão","Ano Novo","Palavra de Deus",
  "Serviço","Soberania de Deus","Redenção","Graça","Salvação"
];

const SYNONYMS = {
  "Adoração":["Adoração","Louvor","Louvores","Adoração e Louvor","Convite à Adoração","Convite à Adoração e Louvor","Louvores ao Deus Trino","Exaltação","Glória","Magnificar","Introito","Deus, o Filho - Louvores","Culto - Abertura"],
  "Santidade":["Santidade","Afirmação de Fé","Credo (Após o)","Profissão de Fé","Reforma Protestante"],
  "Trindade":["Trindade","Deus, o Pai","Cristo, Rei do Universo"],
  "Ceia do Senhor":["Ceia do Senhor","Santa Ceia","Santa Ceia (Após a Celebração da)","Santa Ceia (Durante a)","Comunhão","Ceia","Igreja - Ceia do Senhor","Partir do Pão (Após o)","Oração Eucarística","Oração Eucarística (Após a)","Oração Eucarística (Na)","Pai Nosso","Igreja","União Fraternal"],
  "Natal":["Natal","Nascimento","Ciclo do Natal","Epifania","Deus, o Filho - Natal","Seu nascimento (Natal)","CRISTO - NATAL DE","IV. JESUS CRISTO - B. Nascimento"],
  "Páscoa":["Páscoa","Tempo Pascal","Semana da Paixão","Domingo de Ramos","Transfiguração do Senhor","Ascensão do Senhor"],
  "Pentecostes":["Pentecostes"],
  "Espírito Santo":["Espírito Santo","Deus, o Espírito Santo","ESPÍRITO SANTO","V. ESPÍRITO SANTO"],
  "Missões":["Missões","Missão","Envio","Envio (Após o)","FATIPI","IPIB","UMPI"],
  "Evangelização":["Evangelização","Evangelho","Culto - Evangelho","Culto - Apelo","Culto - Decisão","Testemunho"],
  "Consagração":["Consagração","Igreja - Consagração","Ofertório","Ofertório (Antes do)","Primícias","Obediência","VIDA CRISTA - CONSAGRAÇÃO","VIII. VIDA CRISTÃ - C. Consagração Pessoal"],
  "Confiança":["Confiança","Firmeza","Proteção e Ajuda","Guia","VIII. VIDA CRISTÃ - J. Confiança"],
  "Esperança":["Esperança","Advento"],
  "Despedida":["Despedida","Consolo","Encerramento","Final do Culto","Paz e Descanso","SAUDAÇÕES - DESPEDIDAS","VI. CULTO PÚBLICO - F. Encerramento do Culto","XIII. ASSUNTOS ESPECIAIS - L. Despedida","Culto - Encerramento"],
  "Chamado":["Chamado","Admoestação"],
  "Oração":["Oração","Súplica","Clamor","Reunião de Oração","Oração por Iluminação","Oração de Confissão (Antes ou após a)","Oração de Confissão (Após a)","Orações (Após as)","Orações de Intercessão (Após as)","Oração de Gratidão (Após a)","Intercessão","IX. ORAÇÃO E SÚPLICA"],
  "Família":["Família","Lar","Aniversário","Dia Internacional da Mulher","Dia das Mães","Dia dos Pais"],
  "Casamento":["Casamento","Matrimônio","X. IGREJA - G. Casamento"],
  "Batismo":["Batismo","Batismo Infantil","Batismo do Senhor","Batismo nas águas","Igreja - Batismo","BATISMO","X. IGREJA - B. Batismo e Recepção de Membros"],
  "Juventude":["Juventude"],
  "Crianças":["Crianças","CRIANÇAS","XII. CRIANÇAS"],
  "Funeral":["Funeral"],
  "Ressurreição":["Ressurreição","Ascensão","Deus, o Filho - Sua Ressurreição","Sua ressurreição","CRISTO - RESSURREIÇÃO DE","IV. JESUS CRISTO - F. Ressurreição e Ascenção"],
  "Segunda Vinda":["Segunda Vinda","Volta de Cristo","Volta do Senhor","Sua segunda vinda","CRISTO - A VOLTA DE","IV. JESUS CRISTO - G. Segunda Vinda"],
  "Vida Cristã":["Vida Cristã","Declaração de Perdão","Declaração de Perdão (Após a)","Confissão","Contrição","Quaresma","Quaresma (Início da)","VIII. VIDA CRISTÃ"],
  "Gratidão":["Gratidão","Ação de Graças","GRATIDÃO","VIII. VIDA CRISTÃ - H. Gratidão e Ação de graças"],
  "Ano Novo":["Ano Novo","Passagem do Ano","Passagem do ano","ANO NOVO","XIII. ASSUNTOS ESPECIAIS - A. Ano Novo"],
  "Palavra de Deus":["Palavra de Deus","Bíblia","Leitura Bíblica","A Palavra do Senhor","BÍBLIA","XIII. ASSUNTOS ESPECIAIS - E. Bíblia","VI. CULTO PÚBLICO - D. Para Leitura Bíblica","Culto - Palavra do Senhor"],
  "Serviço":["Serviço","Diacônia"],
  "Soberania de Deus":["Soberania de Deus"],
  "Redenção":["Redenção","Paixão de Cristo","Cruz"],
  "Graça":["Graça","Emergência"],
  "Salvação":["Salvação","Leitura da Palavra (Após a)","Leitura do Evangelho (Antes ou após a)","Leitura do Evangelho (Após a)","Proclamação da Palavra (Após a)"]
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
  buildTopicCounts();
  renderTopicTags();
  renderCulto();
}

function normalize(str) {
  return str
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .toLowerCase();
}

function buildTopicCounts() {
  const counts = {};
  for (const t of CANONICAL_TOPICS) counts[t] = 0;
  for (const h of database.hymns) {
    for (const t of (h.topics || [])) {
      const canonical = _synonymToCanonical[normalize(t)] || t;
      if (counts[canonical] !== undefined) counts[canonical]++;
    }
  }
  allTopicsSorted = CANONICAL_TOPICS.slice().sort((a, b) => counts[b] - counts[a]);
}

function renderTopicTags() {
  const container = document.getElementById("temas-tags");
  const btnMais = document.getElementById("btn-mais-temas");
  container.innerHTML = "";
  const showAll = selectedTopics._showAll || false;
  const limit = showAll ? allTopicsSorted.length : SHOW_INITIAL_TOPICS;
  const visible = allTopicsSorted.slice(0, limit);

  for (const topic of visible) {
    const chip = document.createElement("button");
    chip.className = "tema-chip" + (selectedTopics.includes(topic) ? " tema-chip-active" : "");
    chip.textContent = topic;
    chip.onclick = () => toggleTopic(topic);
    container.appendChild(chip);
  }

  if (allTopicsSorted.length > SHOW_INITIAL_TOPICS) {
    btnMais.style.display = "";
    btnMais.textContent = showAll ? "Mostrar menos" : "Mostrar mais";
  } else {
    btnMais.style.display = "none";
  }
}

function toggleTopic(topic) {
  const idx = selectedTopics.indexOf(topic);
  if (idx >= 0) {
    selectedTopics.splice(idx, 1);
  } else {
    selectedTopics.push(topic);
  }
  renderTopicTags();
}

function toggleMoreTopics() {
  selectedTopics._showAll = !selectedTopics._showAll;
  renderTopicTags();
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
    const topicsArr = (h.topics || []).map(t => normalize(t));

    let score = 0;
    const matched = numStr.includes(q) ||
      titleNorm.includes(q) ||
      firstLineNorm.includes(q) ||
      lyricsNorm.includes(q) ||
      topicsArr.some(t => t.includes(q));
    if (!matched) continue;

    if (topicsArr.some(t => t.includes(q))) score += 100;
    if (titleNorm.includes(q)) score += 50;
    if (firstLineNorm.includes(q)) score += 30;
    if (topicsArr.some(t => t.includes(q))) score += 10;
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
  const momento = document.getElementById("momento").value;
  const resultados = document.getElementById("resultados");
  const selectedHymnals = getSelectedHymnals();
  const activeTopics = selectedTopics.filter(t => typeof t === "string");

  if (selectedHymnals.length === 0) {
    resultados.innerHTML =
      "<p style='text-align:center;color:var(--text-secondary)'>Selecione pelo menos um hinário.</p>";
    return;
  }

  const momentoNormalized = normalize(momento);

  function hymnMatchesTopics(h) {
    if (!h.topics || h.topics.length === 0) return false;
    const hTopics = h.topics.map(t => _synonymToCanonical[normalize(t)] || t);
    for (const sel of activeTopics) {
      if (hTopics.includes(sel)) return true;
    }
    return false;
  }

  function hymnMatchesMomento(h) {
    if (h.category && normalize(h.category) === momentoNormalized) return true;
    if (h.topics && h.topics.some(t => normalize(t) === momentoNormalized)) return true;
    return false;
  }

  let candidates;
  if (activeTopics.length > 0) {
    candidates = database.hymns.filter(h =>
      selectedHymnals.includes(h.hymnal) && hymnMatchesTopics(h)
    );
  } else {
    candidates = database.hymns.filter(h =>
      selectedHymnals.includes(h.hymnal) && hymnMatchesMomento(h)
    );
  }

  if (candidates.length === 0 && activeTopics.length > 0) {
    candidates = database.hymns.filter(h =>
      selectedHymnals.includes(h.hymnal) && hymnMatchesMomento(h)
    );
  }

  const shuffled = [...candidates].sort(() => Math.random() - 0.5);
  const picks = shuffled.slice(0, 4);

  if (picks.length === 0) {
    resultados.innerHTML =
      "<p style='text-align:center;color:var(--text-secondary)'>Nenhum hino encontrado para esta seleção.</p>";
    return;
  }

  resultados.innerHTML = "";
  picks.forEach((hymn) => resultados.appendChild(makeCard(hymn)));

  const btnNovas = document.createElement("button");
  btnNovas.className = "btn-novas";
  btnNovas.textContent = "🔄 Outras sugestões";
  btnNovas.onclick = () => suggestHymns();
  resultados.appendChild(btnNovas);
}

function makeCard(hymn) {
  const card = document.createElement("div");
  card.className = "hino-card";

  let topicsHtml = "";
  if (hymn.topics && hymn.topics.length > 0) {
    const tags = hymn.topics.slice(0, 4).map(t =>
      `<span class="hino-topic-tag">${t}</span>`
    ).join("");
    topicsHtml = `<div class="hino-topics">${tags}</div>`;
  }

  card.innerHTML = `
    <div class="hino-cabecalho">
      <span class="hino-hinario">${hymn.hymnal}</span>
      <span class="hino-numero">${hymn.number}</span>
    </div>
    <div class="hino-titulo">${hymn.title}</div>
    <div class="hino-primeira-linha">${hymn.first_line}</div>
    ${topicsHtml}
    <div style="display:flex;gap:0.5rem">
      <button class="btn-ver-letra" onclick='openLetra(${JSON.stringify(hymn).replace(/'/g, "&#39;")})'>📖 Ver letra</button>
      <button class="btn-escolher" onclick="addToCulto('${hymn.hymnal}','${hymn.number}','${hymn.title.replace(/'/g, "\\'")}')">✓ Escolher</button>
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
  document.getElementById("modal-letra-texto").textContent = hymn.lyrics || "Letra não disponível.";
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
      <button class="culto-item-remover" onclick="removeFromCulto(${i})">✕</button>
    `;
    container.appendChild(item);
  });
}

function copyProgramacao() {
  if (cultoHymns.length === 0) return;
  const lines = ["Culto", ""];
  for (const h of cultoHymns) {
    lines.push(`${h.hymnal} ${h.number} – ${h.title}`);
  }
  const text = lines.join("\n");
  navigator.clipboard.writeText(text).then(() => {
    const btn = document.getElementById("btn-copiar");
    const original = btn.textContent;
    btn.textContent = "✓ Copiado!";
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
        alert("Arquivo inválido.");
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
  if (diffDays < 30) return "Este mês";
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
        <button class="historico-btn" onclick="copiarHistorico(${i})" title="Copiar">📋</button>
        <button class="historico-btn historico-btn-perigo" onclick="removerHistorico(${i})" title="Remover">✕</button>
      </div>
    `;
    container.appendChild(item);
  }

  document.getElementById("modal-historico").classList.add("active");
}

function copiarHistorico(index) {
  const entry = historico[index];
  const lines = entry.hymns.map(h => `${h.hymnal} ${h.number} – ${h.title}`);
  navigator.clipboard.writeText(lines.join("\n")).then(() => {
    alert("Copiado!");
  });
}

function removerHistorico(index) {
  if (!confirm("Remover este culto do histórico?")) return;
  historico.splice(index, 1);
  localStorage.setItem("cantaiHistorico", JSON.stringify(historico));
  openHistorico();
}

function limparHistoricoCompleto() {
  if (historico.length === 0) return;
  if (!confirm("Limpar todo o histórico de cultos?")) return;
  historico = [];
  localStorage.setItem("cantaiHistorico", JSON.stringify(historico));
  openHistorico();
}

document.addEventListener("DOMContentLoaded", () => {
  loadDatabase();
  document.getElementById("busca").addEventListener("input", handleSearch);
});
