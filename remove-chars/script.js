var inputTextarea = document.getElementById("inputString");

inputTextarea.addEventListener("keydown", function(event) {
  if (event.ctrlKey && event.keyCode === 13) { // 13 is the key code for Enter
    event.preventDefault(); // Prevent the default Enter key behavior
    modifyAndCopy();
  }
});

function modifyAndCopy() {
  var input = document.getElementById("inputString").value;
 
  var modifiedString = input.replace(/[\n]+/g, " ").replace(/[0-9]/g, "");

  var tempTextarea = document.createElement("textarea");
  tempTextarea.value = modifiedString;
  document.body.appendChild(tempTextarea);
  tempTextarea.select();
  document.execCommand("copy");
  document.body.removeChild(tempTextarea);
  document.getElementById("myText").textContent = ""

  var myTextElement = document.getElementById("myText");
  myTextElement.textContent = "";
  myTextElement.textContent = "“" + modifiedString + "”\nhas been add to the clipboard";
}