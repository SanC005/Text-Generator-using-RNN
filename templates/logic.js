const inputBox = document.querySelector('.inputBox')
const btn = document.querySelector('.btn')
btn.addEventListener('click', (e)=> {

    console.log(inputBox.value);
 generate(inputBox.value)

})

async function generate(query) {
  console.log("heyyy")
//     fetch("http://127.0.0.1:5000/generate", {
//   method: "POST",
//   mode: 'cors',
//   body: JSON.stringify({
//     "query":"I had seen little of Holmes lately"
//   }),
//   headers: {
//     "Content-type": "application/json; charset=UTF-8"
//   }
// })
//   .then((response) => response.json())
//   .then((json) => console.log(json));
    

  

}






async function lol(query) {
    fetch("http://127.0.0.1:5000/", {
  method: "GET",
  mode: 'cors',
  
  headers: {
    "Content-type": "application/json; charset=UTF-8"
  }
})
  .then((response) => response.json())
  .then((json) => console.log(json));
    
}
console.log(inputBox)

console.log(inputBox.value)