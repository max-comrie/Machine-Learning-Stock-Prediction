console.log("JavaScript is working!");

const form = document.getElementById("stockForm");
const resultDiv = document.getElementById("result");
const viewDetailsBtn = document.getElementById("viewDetailsBtn");

const modal = document.getElementById("stockModal");
const modalContent = document.getElementById("modalContent");
const closeModal = document.getElementById("closeModal");

let lastPrediction = "";

// Helper to render chart-like data lists
function renderChart(dataArray, title, asArrows = false) {
  if (!dataArray || dataArray.length === 0) return "";

  return `
    <h3>${title}</h3>
    <div style="max-height: 200px; overflow-y: auto; border: 1px solid #ccc; padding: 10px; border-radius: 6px; background: #f9f9f9;">
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

  fetch(`http://localhost:5000/predict?ticker=${symbol}`)
    .then((res) => res.json())
    .then((data) => {
      if (data.error) {
        resultDiv.innerHTML = `Error: ${data.error}`;
        viewDetailsBtn.style.display = "none";
        return;
      }

      const tomorrow = new Date();
      tomorrow.setDate(tomorrow.getDate() + 1);
      const tomorrowFormatted = tomorrow.toLocaleDateString("en-US", {
        year: "numeric",
        month: "long",
        day: "numeric",
      });

      let directionText;
      if (data.predicted_price === 1) {
        directionText = `${data.ticker} is predicted to go up tomorrow (${tomorrowFormatted})`;
      } else if (data.predicted_price === 0) {
        directionText = `${data.ticker} is predicted to go down tomorrow (${tomorrowFormatted})`;
      } else {
        directionText = `Prediction unavailable.`;
      }

      resultDiv.innerHTML = `${directionText}<br />`;
      viewDetailsBtn.style.display = "inline-block";
      resultDiv.appendChild(viewDetailsBtn);

      // Build modal content
      lastPrediction = `
        <strong>Symbol:</strong> ${data.ticker}<br />
        <strong>Prediction:</strong> ${directionText}<br />
        <strong>Confidence:</strong> ${
          data.confidence >= 0.5
            ? data.confidence
            : 1 - data.confidence || "N/A"
        }<br />
        <strong>Timestamp:</strong> ${data.timestamp || "N/A"}<br /><br />
        ${renderChart((data.history || []).slice(-50), "Last 50 Days", true)}
      `;
    })
    .catch((err) => {
      // Now using the correct error variable "err"
      console.error(err);
      // Provide user feedback
      resultDiv.innerText = "Something went wrong.";
      viewDetailsBtn.style.display = "none";
    });
});

// Show modal on button click
viewDetailsBtn.onclick = () => {
  modalContent.innerHTML = lastPrediction;
  modal.style.display = "flex";
};

// Close modal
closeModal.onclick = () => {
  modal.style.display = "none";
};

window.onclick = (e) => {
  if (e.target === modal) {
    modal.style.display = "none";
  }
};
