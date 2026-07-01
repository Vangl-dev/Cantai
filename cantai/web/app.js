let database = { version: null, hymns: [] };

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

    if (
      numStr.includes(q) ||
      titleNorm.includes(q) ||
      firstLineNorm.includes(q) ||
      lyricsNorm.includes(q)
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
    const h = results[i];
    const card = document.createElement("div");
    card.className = "hino-card";
    card.innerHTML = `
      <div class="hino-cabecalho">
        <span class="hino-hinario">${h.hymnal}</span>
        <span class="hino-numero">${h.number}</span>
      </div>
      <div class="hino-titulo">${h.title}</div>
      <div class="hino-primeira-linha">${h.first_line}</div>
      <button class="btn-escolher" onclick="chooseHymn(${h.number})">✓ Escolher</button>
    `;
    container.appendChild(card);
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
  const map = {
    hctp: "CTP",
    harpa: "HARPA",
    cantor: "CC",
    sh: "SH",
    nc: "NC",
  };
  const selected = [];
  for (const [id, name] of Object.entries(map)) {
    if (document.getElementById(id).checked) {
      selected.push(name);
    }
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

  const byHymnal = {};
  for (const h of database.hymns) {
    if (!selected.includes(h.hymnal)) continue;
    if (h.hymnal === "CTP" && h.category !== momento) continue;
    if (!byHymnal[h.hymnal]) byHymnal[h.hymnal] = [];
    byHymnal[h.hymnal].push(h);
  }

  const picks = [];
  const shuffled = {};
  for (const h of selected) {
    shuffled[h] = [...(byHymnal[h] || [])].sort(() => Math.random() - 0.5);
  }

  for (const h of selected) {
    if (shuffled[h].length > 0 && picks.length < 3) {
      picks.push(shuffled[h].shift());
    }
  }

  if (picks.length < 3) {
    for (const h of selected) {
      while (shuffled[h].length > 0 && picks.length < 3) {
        picks.push(shuffled[h].shift());
      }
    }
  }

  if (picks.length === 0) {
    resultados.innerHTML =
      "<p style='text-align:center;color:var(--text-secondary)'>Nenhum hino encontrado para esta categoria.</p>";
    return;
  }

  resultados.innerHTML = "";

  picks.forEach((hymn) => {
    const card = document.createElement("div");
    card.className = "hino-card";
    card.innerHTML = `
      <div class="hino-cabecalho">
        <span class="hino-hinario">${hymn.hymnal}</span>
        <span class="hino-numero">${hymn.number}</span>
      </div>
      <div class="hino-titulo">${hymn.title}</div>
      <div class="hino-primeira-linha">${hymn.first_line}</div>
      <button class="btn-escolher" onclick="chooseHymn(${hymn.number})">✓ Escolher</button>
    `;
    resultados.appendChild(card);
  });

  const btnNovas = document.createElement("button");
  btnNovas.className = "btn-novas";
  btnNovas.textContent = "🔄 Outras sugestões";
  btnNovas.onclick = newSuggestions;
  resultados.appendChild(btnNovas);
}

function chooseHymn(number) {
  const chosen = JSON.parse(localStorage.getItem("chosenHymns") || "[]");
  if (!chosen.includes(number)) {
    chosen.push(number);
    localStorage.setItem("chosenHymns", JSON.stringify(chosen));
  }
}

function newSuggestions() {
  suggestHymns();
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
