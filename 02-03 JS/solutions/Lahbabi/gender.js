const submitButton = document.querySelector("#submit-button");

if (submitButton) {
  submitButton.addEventListener("click", function(event) {
    event.preventDefault();
    const nameInput = document.getElementById("name-input");
    const resultDiv = document.getElementById("result");
    const name = nameInput.value.trim();
    
    if (name !== "") {
      fetch(`https://api.genderize.io/?name=${name}`)
        .then(response => response.json())
        .then(data => {
          const gender = data.gender;
          const probability = data.probability * 100;
          let message = `The gender of ${name} is `;
          if (gender === "male") {
            message += `male with ${probability}% certainty.`;
          } else if (gender === "female") {
            message += `female with ${probability}% certainty.`;
          } else {
            message += `unisex or not found.`;
          }
          resultDiv.innerHTML = message;
        })
        .catch(error => {
          resultDiv.innerHTML = "Error fetching data. Please try again later.";
          console.error(error);
        });
    } else {
      resultDiv.innerHTML = "Please enter a name.";
    }
  });
}

