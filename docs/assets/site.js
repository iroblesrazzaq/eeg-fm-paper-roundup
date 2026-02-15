function norm(s) { return (s || "").toLowerCase(); }

function setupSearch() {
  const input = document.getElementById("searchBox");
  if (!input) return;

  input.addEventListener("input", () => {
    const q = norm(input.value);
    const cards = document.querySelectorAll(".card");
    for (const c of cards) {
      const hay = norm(c.getAttribute("data-hay"));
      c.style.display = hay.includes(q) ? "" : "none";
    }
  });
}

document.addEventListener("DOMContentLoaded", setupSearch);
