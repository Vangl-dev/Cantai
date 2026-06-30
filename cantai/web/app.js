let database = { version: null, hymns: [] };

async function loadDatabase() {
  try {
    const response = await fetch("../data/output/cantai.json");
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

function suggestHymns() {
  const resultados = document.getElementById("resultados");
  resultados.innerHTML = "<p style='text-align:center;color:var(--text-secondary)'>Nenhuma sugestão ainda.</p>";
}

function chooseHymn(hymn) {
  console.log("Escolhido:", hymn);
}

function newSuggestions() {
  suggestHymns();
}

document.addEventListener("DOMContentLoaded", loadDatabase);
