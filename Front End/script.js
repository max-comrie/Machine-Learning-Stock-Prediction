const form = document.getElementById("stockForm");
const resultDiv = document.getElementById("result");
const viewDetailsBtn = document.getElementById("viewDetailsBtn");

const modal = document.getElementById("stockModal");
const modalContent = document.getElementById("modalContent");
const closeModal = document.getElementById("closeModal");

let lastPrediction = "";

// Helper to find the next trading day (skips Saturday & Sunday)
function getNextTradingDay(date) {
  const d = new Date(date);
  d.setDate(d.getDate() + 1);
  const day = d.getDay();
  if (day === 6) {
    d.setDate(d.getDate() + 2);
  } else if (day === 0) {
    d.setDate(d.getDate() + 1);
  }
  return d;
}

// Format helper
function formatDate(date) {
  return date.toLocaleDateString("en-US", {
    year: "numeric",
    month: "long",
    day: "numeric",
  });
}

// Renders chart-like history lists
function renderChart(dataArray, title, asArrows = false) {
  if (!dataArray || dataArray.length === 0) return "";
  return `
    <h3>${title}</h3>
    <div style="max-height:200px;overflow-y:auto;border:1px solid #ccc;padding:10px;border-radius:6px;background:#f9f9f9;">
      ${dataArray
        .map((val, idx) => {
          const display = asArrows ? (val === 1 ? "📈 Up" : "📉 Down") : val;
          return `Day ${idx + 1}: ${display}`;
        })
        .join("<br>")}
    </div>
  `;
}

form.addEventListener("submit", function (event) {
  event.preventDefault();

  const symbol = document.getElementById("stockSymbol").value.toUpperCase();
  resultDiv.innerHTML = `Searching for: ${symbol}...`;
  viewDetailsBtn.style.display = "none";

  fetch(`http://localhost:5000/predict?ticker=${symbol}`)
    .then((res) => res.json())
    .then((data) => {
      if (data.error) {
        resultDiv.innerHTML = `Error: ${data.error}`;
        return;
      }

      // Calculate display confidence
      const conf = data.confidence;
      const displayConf = conf >= 0.5 ? conf.toFixed(2) : (1 - conf).toFixed(2);
      const confPercent = (displayConf * 100).toFixed(0) + "%";

      const nextTradeDay = getNextTradingDay(new Date());
      const nextTradeStr = formatDate(nextTradeDay);

      let directionText;
      if (data.predicted_price === 1) {
        directionText = `${data.ticker} is predicted to go up on the next trading day (${nextTradeStr})`;
      } else {
        directionText = `${data.ticker} is predicted to go down on the next trading day (${nextTradeStr})`;
      }

      resultDiv.innerHTML = `${directionText}<br />`;
      viewDetailsBtn.style.display = "inline-block";
      resultDiv.appendChild(viewDetailsBtn);

      lastPrediction = `
        <strong>Symbol:</strong> ${data.ticker}<br />
        <strong>Prediction:</strong> ${directionText}<br />
        <strong>Confidence:</strong> ${confPercent}<br />
        <strong>Timestamp:</strong> ${data.timestamp}<br /><br />
        ${renderChart((data.history || []).slice(-50), "Last 50 Days", true)}
      `;
    })
    .catch((err) => {
      console.error(err);
      resultDiv.innerText = "Something went wrong";
      viewDetailsBtn.style.display = "none";
    });
});

// Modal control
viewDetailsBtn.onclick = () => {
  modalContent.innerHTML = lastPrediction;
  modal.style.display = "flex";
};

closeModal.onclick = () => {
  modal.style.display = "none";
};
window.onclick = (e) => {
  if (e.target === modal) modal.style.display = "none";
};
