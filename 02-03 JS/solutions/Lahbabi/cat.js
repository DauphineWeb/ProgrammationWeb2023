if(document.querySelector("#fact-button"))
{
const factButton = document.querySelector("#fact-button");
const factsDiv = document.querySelector("#facts");

factButton.addEventListener("click", async function() {
  try {
    const response = await fetch("https://catfact.ninja/fact");
    const data = await response.json();
    const fact = data.fact;

    const newFact = document.createElement("div");
    newFact.classList.add("fact");
    newFact.innerText = fact;
    factsDiv.prepend(newFact);
  } catch (error) {
    console.error(error);
  }
});
}


