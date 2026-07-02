let database = { version: null, hymns: [] };
let cultoHymns = JSON.parse(localStorage.getItem("cultoHymns") || "[]");
let currentModalHymn = null;

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
  renderCulto();
}

function normalize(str) {
  return str
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .toLowerCase();
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
    const topicsNorm = (h.topics || []).map(t => normalize(t)).join(" ");
    if (
      numStr.includes(q) ||
      titleNorm.includes(q) ||
      firstLineNorm.includes(q) ||
      lyricsNorm.includes(q) ||
      topicsNorm.includes(q)
    ) {
      results.push(h);
    }
  }
  return results;
}

function renderSearchResults(results) {
  const container = document.getElementById("resultados");
  if (results.length === 0) {
    container.innerHTML =
      "<p style='text-align:center;color:var(--text-secondary)'>Nenhum hino encontrado.</p>";
    return;
  }
  container.innerHTML = "";
  const limit = Math.min(results.length, 50);
  for (let i = 0; i < limit; i++) {
    container.appendChild(makeCard(results[i]));
  }
  if (results.length > limit) {
    const more = document.createElement("p");
    more.style.textAlign = "center";
    more.style.color = "var(--text-secondary)";
    more.textContent = `... e mais ${results.length - limit} hinos`;
    container.appendChild(more);
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
  const selected = getSelectedHymnals();

  if (selected.length === 0) {
    resultados.innerHTML =
      "<p style='text-align:center;color:var(--text-secondary)'>Selecione pelo menos um hinário.</p>";
    return;
  }

  const momentoNormalized = normalize(momento);
  const ctpHymns = database.hymns.filter((h) => {
    if (h.hymnal !== "CTP") return false;
    if (h.category && normalize(h.category) === momentoNormalized) return true;
    if (h.topics && h.topics.some(t => normalize(t) === momentoNormalized)) return true;
    return false;
  });

  const otherHymnals = selected.filter((h) => h !== "CTP");
  const otherHymns = database.hymns.filter(
    (h) => otherHymnals.includes(h.hymnal) && h.topics && h.topics.some(t => normalize(t) === momentoNormalized)
  );

  const allMatching = [...ctpHymns, ...otherHymns];

  const picks = [];
  const shuffled = [...allMatching].sort(() => Math.random() - 0.5);
  for (let i = 0; i < 4 && shuffled.length > 0; i++) {
    picks.push(shuffled.shift());
  }

  if (picks.length === 0) {
    resultados.innerHTML =
      "<p style='text-align:center;color:var(--text-secondary)'>Nenhum hino encontrado para esta categoria.</p>";
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
  if (query.length === 0) {
    btnSugerir.style.display = "";
    return;
  }
  btnSugerir.style.display = "none";
  const results = searchHymns(query);
  renderSearchResults(results);
}

document.addEventListener("DOMContentLoaded", () => {
  loadDatabase();
  document.getElementById("busca").addEventListener("input", handleSearch);
});
