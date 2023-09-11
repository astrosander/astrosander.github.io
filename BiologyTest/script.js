const button1 = document.getElementById("button1");
const button2 = document.getElementById("button2");
const output = document.getElementById("output");
var randomListIndex=1;
var randomItem;
var show; 

function getRandomElement() {
    document.getElementById("result").textContent = "";
    var list1 = ['O', 'C', 'H', 'N', 'Ca', 'P', 'K', 'S', 'Cl', 'Na', 'Mg'];
    var list2 = ['Fe', 'Zn', 'Cu', 'F', 'I', 'Mn', 'Co'];

    randomListIndex = Math.floor(Math.random() * 2); // 0 or 1

    if (randomListIndex === 0) {
        randomItem = list1[Math.floor(Math.random() * list1.length)];
        // document.getElementById("list-number").textContent = "1";
    } else {
        randomItem = list2[Math.floor(Math.random() * list2.length)];
        // document.getElementById("list-number").textContent = "2";
    }

    document.getElementById("random-element").textContent = randomItem;
    name = randomItem;
}

getRandomElement()

function A1() {
    if(randomListIndex === 0){
        document.getElementById("result").textContent = "OK";
        var textElement = document.getElementById("result");
        textElement.style.color = "green";
    }
    else{
        document.getElementById("result").textContent = "False";
        var textElement = document.getElementById("result");
        textElement.style.color = "red";
    }

}


function B1() {
    if(randomListIndex === 1){
        document.getElementById("result").textContent = "OK";
        var textElement = document.getElementById("result");
        textElement.style.color = "green";
    }
    else{
        document.getElementById("result").textContent = "False";
        var textElement = document.getElementById("result");
        textElement.style.color = "red";
    }
}

// button1.addEventListener("click", function() {
//     document.getElementById("random-element").textContent = "Button 1 was pressed. Task 2 performed.";
// });

// button2.addEventListener("click", function() {
//     document.getElementById("random-element").textContent = 21;
// });