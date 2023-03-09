function getNewFact(){
    let url = "https://catfact.ninja/fact";
    fetch(url)
    .then((response) => response.json())
    .then((data) => {

        let node = document.createElement('li');
        node.appendChild(document.createTextNode(data.fact));
        document.querySelector('ul').appendChild(node);
        } 
    );
}

function genderize(){
    let name = document.getElementById("name").value;
    let url = "https://api.genderize.io/?name=".concat(name);

    if(name == ""){
        alert("Missing data : Please type a name to see the gender");
        return;
    }
    
    fetch(url)
    .then((response) => response.json())
    .then((data) => {
        let result = `Result : ${name} is ${data.probability * 100 }% ${data.gender}`        
        
        let div = document.getElementById('result');
        div.removeChild(div.firstChild);
        
        const node = document.createElement("p");
        const textnode = document.createTextNode(result);
        node.appendChild(textnode);
        div.appendChild(node);

        document.getElementById('name').value = "";
        } 
    );
}
