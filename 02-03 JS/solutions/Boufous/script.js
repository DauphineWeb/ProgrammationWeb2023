const factButton = document.getElementById("fact-button");
const factContainer = document.getElementById("fact-container");

factButton.addEventListener("click", function() {
  fetch("https://catfact.ninja/fact")
    .then(response => response.json())
    .then(data => {
      const factDiv = document.createElement("div");
      factDiv.classList.add("fact");
      factDiv.innerHTML = data.fact;
      factContainer.prepend(factDiv);

      setTimeout(() => {
        factDiv.classList.add("show-fact");
      }, 100);
    })
    .catch(error => console.error(error));
});