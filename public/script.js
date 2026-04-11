const input = document.querySelector("input");
const btnAnalyze = document.querySelector("button:nth-of-type(1)");
const btnPdf = document.querySelector("button:nth-of-type(2)");

// 👉 ANALYSE
btnAnalyze.addEventListener("click", async () => {
  const product = input.value;

  if (!product) {
    alert("Entre un produit !");
    return;
  }

  try {
    const res = await fetch("/analyze", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ product })
    });

    const data = await res.json();

    alert(
      "Produit: " + data.product +
      "\nStatut: " + data.status +
      "\nDanger: " + data.danger
    );

  } catch (error) {
    alert("Erreur serveur");
  }
});

// 👉 PDF
btnPdf.addEventListener("click", () => {
  const product = input.value;

  if (!product) {
    alert("Entre un produit !");
    return;
  }

  window.open(`/pdf/${product}`, "_blank");
});