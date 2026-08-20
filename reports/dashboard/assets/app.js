const data = window.DASHBOARD_DATA;

const splitSelect = document.querySelector("#splitSelect");
const labelSelect = document.querySelector("#labelSelect");
const totalImages = document.querySelector("#totalImages");
const totalSize = document.querySelector("#totalSize");
const totalLabels = document.querySelector("#totalLabels");
const barChart = document.querySelector("#barChart");
const summaryBody = document.querySelector("#summaryBody");
const gallery = document.querySelector("#gallery");
const chartCaption = document.querySelector("#chartCaption");
const galleryCaption = document.querySelector("#galleryCaption");
const trainNotebookChart = document.querySelector("#trainNotebookChart");
const testNotebookChart = document.querySelector("#testNotebookChart");
const notebookComparison = document.querySelector("#notebookComparison");
const notebookMosaic = document.querySelector("#notebookMosaic");
const articleTitle = document.querySelector("#articleTitle");
const articleSummary = document.querySelector("#articleSummary");
const articleLink = document.querySelector("#articleLink");
const articlePdf = document.querySelector("#articlePdf");
const articleAuthors = document.querySelector("#articleAuthors");
const articleJournal = document.querySelector("#articleJournal");
const articlePublished = document.querySelector("#articlePublished");
const articleKeywords = document.querySelector("#articleKeywords");

const splitNames = {
  all: "Todos",
  train: "Treino",
  test: "Teste",
};

function option(value, label) {
  const item = document.createElement("option");
  item.value = value;
  item.textContent = label;
  return item;
}

function setupControls() {
  splitSelect.append(option("all", "Todos"));
  data.splits.forEach((split) => splitSelect.append(option(split, splitNames[split] || split)));

  labelSelect.append(option("all", "Todas"));
  data.labels.forEach((label) => labelSelect.append(option(label, label)));
}

function countsForSelectedSplit(split) {
  const counts = Object.fromEntries(data.labels.map((label) => [label, 0]));
  const splits = split === "all" ? data.splits : [split];
  splits.forEach((currentSplit) => {
    data.labels.forEach((label) => {
      counts[label] += data.counts[currentSplit][label] || 0;
    });
  });
  return counts;
}

function renderBars() {
  const split = splitSelect.value;
  const selectedLabel = labelSelect.value;
  const counts = countsForSelectedSplit(split);
  const rows = data.labels
    .filter((label) => selectedLabel === "all" || label === selectedLabel)
    .map((label) => ({ label, value: counts[label] }));
  const max = Math.max(...rows.map((row) => row.value), 1);

  chartCaption.textContent = `${splitNames[split] || split} - ${selectedLabel === "all" ? "todas as classes" : selectedLabel}`;
  barChart.replaceChildren(
    ...rows.map((row) => {
      const wrapper = document.createElement("div");
      wrapper.className = "bar-row";
      wrapper.innerHTML = `
        <span class="bar-label">${row.label}</span>
        <span class="bar-track"><span class="bar-fill" style="width: ${(row.value / max) * 100}%"></span></span>
        <span class="bar-value">${row.value}</span>
      `;
      return wrapper;
    }),
  );
}

function renderSummary() {
  const split = splitSelect.value;
  const selectedLabel = labelSelect.value;
  const rows = data.summary.filter((row) => {
    const splitMatch = split === "all" || row.split === split;
    const labelMatch = selectedLabel === "all" || row.label === selectedLabel;
    return splitMatch && labelMatch;
  });

  summaryBody.replaceChildren(
    ...rows.map((row) => {
      const tr = document.createElement("tr");
      tr.innerHTML = `
        <td>${splitNames[row.split] || row.split}</td>
        <td>${row.label}</td>
        <td>${row.image_count.toLocaleString("pt-BR")}</td>
        <td>${row.total_size_mb.toLocaleString("pt-BR")}</td>
      `;
      return tr;
    }),
  );
}

function renderGallery() {
  const split = splitSelect.value === "all" ? "train" : splitSelect.value;
  const label = labelSelect.value === "all" ? data.labels[0] : labelSelect.value;
  const key = `${split}:${label}`;
  const samples = data.samples[key] || [];

  galleryCaption.textContent = `${splitNames[split] || split} - ${label}`;
  gallery.replaceChildren(
    ...samples.map((sample) => {
      const card = document.createElement("article");
      card.className = "sample-card";
      card.innerHTML = `
        <img src="${sample.path}" alt="Amostra ${sample.label}">
        <div>
          <strong>${sample.label}</strong>
          <span>${sample.file_name} - ${sample.width || "?"}x${sample.height || "?"}</span>
        </div>
      `;
      return card;
    }),
  );
}

function renderNotebookCountplot(target, split) {
  const rows = data.labels.map((label) => ({
    label,
    value: data.counts[split][label] || 0,
  }));
  const max = Math.max(...rows.map((row) => row.value), 1);
  target.replaceChildren(
    ...rows.map((row) => {
      const wrapper = document.createElement("div");
      wrapper.className = "vertical-bar";
      wrapper.innerHTML = `
        <span class="vertical-bar-fill" style="height: ${(row.value / max) * 160}px"></span>
        <strong>${row.value}</strong>
        <span title="${row.label}">${row.label}</span>
      `;
      return wrapper;
    }),
  );
}

function renderNotebookComparison() {
  const comparison = data.notebook_views.comparison;
  const cards = ["train", "test"].map((split) => {
    const sample = comparison[split];
    const card = document.createElement("article");
    card.className = "comparison-card";
    card.innerHTML = `
      <img src="${sample.path}" alt="Amostra ${splitNames[split]} ${sample.label}">
      <div>
        <strong>${splitNames[split]} - ${sample.label}</strong>
        <span>${sample.file_name} - ${sample.width || "?"}x${sample.height || "?"}</span>
      </div>
    `;
    return card;
  });
  notebookComparison.replaceChildren(...cards);
}

function renderNotebookMosaic() {
  notebookMosaic.replaceChildren(
    ...data.notebook_views.sample_grid.map((sample) => {
      const cell = document.createElement("article");
      cell.className = "mosaic-cell";
      cell.innerHTML = `
        <img src="${sample.path}" alt="Amostra ${sample.label}">
        <span>${sample.label}</span>
      `;
      return cell;
    }),
  );
}

function renderArticle() {
  const article = data.article;
  articleTitle.textContent = article.title;
  articleSummary.textContent = article.summary;
  articleLink.href = article.url;
  articlePdf.href = article.pdf_url;
  articleAuthors.textContent = article.authors.join("; ");
  articleJournal.textContent = `${article.journal} - ${article.issue}`;
  articlePublished.textContent = article.published;
  articleKeywords.textContent = article.keywords.join("; ");
}

function render() {
  renderBars();
  renderSummary();
  renderGallery();
}

totalImages.textContent = data.total_images.toLocaleString("pt-BR");
totalSize.textContent = data.total_size_mb.toLocaleString("pt-BR");
totalLabels.textContent = data.labels.length;

setupControls();
splitSelect.addEventListener("change", render);
labelSelect.addEventListener("change", render);
renderNotebookCountplot(trainNotebookChart, "train");
renderNotebookCountplot(testNotebookChart, "test");
renderNotebookComparison();
renderNotebookMosaic();
renderArticle();
render();
