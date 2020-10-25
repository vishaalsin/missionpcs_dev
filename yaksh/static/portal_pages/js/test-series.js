document.addEventListener("DOMContentLoaded", ()=>{
    for(let i=2; i<6; i++){
        console.log(`id_test${i}`);
        
        document.querySelector(`#id_test${i}`).parentElement.style.display = "none";
        document.querySelector(`#id_test_date${i}_month`).parentElement.style.display = "none";

    }
    let i=2;
    add_more = document.querySelector("#add_more");
    add_more.onclick = (e) => {
        e.preventDefault()
        if(i==5){
            add_more.style.display = "none"
            p_later = document.createElement('p')
            p_later.textContent = "You can add more tests after Saving the changes"
            add_more.parentElement.appendChild(p_later)
        }
        document.querySelector(`#id_test${i}`).parentElement.style.display = "block";
        document.querySelector(`#id_test_date${i}_month`).parentElement.style.display = "block";
        i++;
    }
})