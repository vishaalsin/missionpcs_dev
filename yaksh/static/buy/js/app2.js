//Variables
const courses= document.querySelector('#courses-list'),
        shoppingCartContent= document.querySelector('#cart-content tbody'),
        clearCartBtn=document.querySelector('#clear-cart');
        checkoutCartBtn=document.querySelector('#cart-checkout');

let courses_to_buy = new Set();



//Listeners
loadEventListeners();


function loadEventListeners(){


    courses.addEventListener('click', buycourse);

    shoppingCartContent.addEventListener('click', removeCourse);

    clearCartBtn.addEventListener('click', clearCart);

    checkoutCartBtn.addEventListener('click', checkoutCart);

    document.addEventListener('DOMContentLoaded', getFromLocalStorage);

}





//Functions
console.log("HI")
function buycourse(e){
    console.log("Event Triggered")

    if(e.target.classList.contains('add-to-cart')){
        console.log('add-to-cart')
    if(e.target.classList.contains('quiz-on-sale')){
    const quiz_code = e.target.parentElement.parentElement.children[0].children[0].innerText.trim();
    if(courses_to_buy.has(quiz_code)){
        console.log("already present no need to add");
    }
    else {
        courses_to_buy.add(quiz_code);    
        console.log(courses_to_buy)
        let ibttn = e.target.parentElement.parentElement.children[3].firstElementChild
        ibttn.disabled = true
        ibttn.innerHTML = "Added to Cart"
        console.log(ibttn) 
        console.log("quiz_code", quiz_code)
        const quiz_price = e.target.parentElement.parentElement.children[0].children[2].innerText.trim().split('₹')[1].trim();
        console.log("price", quiz_price)
        const quiz_id = parseInt(e.target.parentElement.parentElement.children[1].innerText.trim());
        console.log("quiz_id", quiz_id)
        const quiz_availibility = e.target.parentElement.parentElement.children[2].innerText.trim();
        console.log("quiz_availability", quiz_availibility)
        if(quiz_availibility == 'False'){
        addIntoCart(quiz_code, quiz_price, quiz_id);
    }
    }
    }

    if(e.target.classList.contains('module-on-sale')){
    item_containers = e.target.parentElement.parentElement.children[1].children[0].children
    console.log(item_containers)
        for (var i = 0; i < item_containers.length; i++) {
            if (item_containers[i].classList.contains('card')){
                console.log("contains_card")
                const quiz_code = item_containers[i].firstElementChild.firstElementChild.firstElementChild.innerText.trim();
                if(courses_to_buy.has(quiz_code)){
                    console.log("already present no need to add");
                    continue;
                }
                else{
                    courses_to_buy.add(quiz_code)
                    ibttn = item_containers[i].firstElementChild.children[3].firstElementChild
                    ibttn.disabled = true
                    if(ibttn.innerHTML == "Add to Cart"){
                        console.log("inner Html", ibttn.innerHTML);
                        ibttn.innerHTML = "Added to Cart";
                    }
                    console.log(ibttn)
                }
                console.log("quiz-code", quiz_code)
                const quiz_price = item_containers[i].firstElementChild.firstElementChild.children[2].innerText.trim().split('₹')[1].trim();
                console.log("quiz_price", quiz_price)
                const quiz_id = parseInt(item_containers[i].firstElementChild.children[1].innerText.trim());
                console.log("quiz_id", quiz_id)
                const quiz_availibility = item_containers[i].firstElementChild.children[2].innerText.trim();
                console.log("quiz_availability", quiz_availibility)
                if(quiz_availibility == 'False'){
                addIntoCart(quiz_code, quiz_price, quiz_id);
                }
            }
}
    }


//    getCourseInfo(course);
    alert("Quizzes Added!!")
    }
}


function addIntoCart(quiz_code, quiz_price, quiz_id){
    const row= document.createElement('tr');
    row.innerHTML= ` 
    <tr>
    <td>
    ${quiz_code}</td>
    <td> ${quiz_price} </td>
    <td style = "display:none"> ${quiz_id} </td>
    <td> <a href ="#" class="fa fa-trash remove" data-id="${quiz_id}"></a> </td>


    </tr>

    `;
    shoppingCartContent.appendChild(row);

}

function removeCourse(e){

    if(e.target.classList.contains('remove')){
        
        to_rem = e.target.parentElement.parentElement.firstElementChild.innerText.trim()
        courses_to_buy.delete(to_rem)
        console.log(to_rem, courses_to_buy)
        e.target.parentElement.parentElement.remove();
        const addbtn = document.querySelectorAll("button").forEach((bt) => {
            
            if(bt.disabled){
                console.log("disabled", bt)
                let del_quiz_code = bt.parentElement.parentElement.children[0].children[0].innerText.trim();
                if(del_quiz_code == to_rem){
                    bt.disabled = false
                    console.log("button inner html", bt.innerHTML)
                    bt.innerHTML = "Add to Cart";
                }
                console.log(del_quiz_code)
            }
        });
        console.log(addbtn)
       
    
        }
}

function clearCart(e){
    shoppingCartContent.innerHTML='';
    courses_to_buy.clear();
    console.log(courses_to_buy);
    document.querySelectorAll("button").forEach((bt) => {
        if(bt.disabled){
            bt.disabled = false;
            bt.innerHTML = "Add to Cart";
        }
    })
}

function checkoutCart(e){
    items = e.target.parentElement.firstElementChild.tBodies[0].children;
    sum = 0
    console.log(items)
    quiz_ids = []
    for (var i = 0; i < items.length; i++) {
      sum += parseInt(items[i].cells[1].innerText.replace("Rs.", ""))
      quiz_ids.push(parseInt(items[i].cells[2].innerText))
    }
//    alert(sum)
    assign_quizzes(quiz_ids, sum)
//    window.location.href = "/letsprepare";
}

function assign_quizzes(quiz_ids, sum) {
    submitData = {'quizzes' : quiz_ids, 'amount' : sum}

    $.post("/letsprepare/assign_quizzes/",
  {
    data: JSON.stringify(submitData)
  },
  function(data, status){
    console.log("work")
    const row= document.createElement('form');
    row.name='myForm';
    row.method='POST';
    row.action=data['url'];

    for (var key in data['paymentParams']) {
        row.innerHTML += '<input type="hidden" name="' + key + '" value="' + data['paymentParams'][key] + '">'
        // check if the property/key is defined in the object itself, not in parent
        }
        document.body.appendChild(row);
        console.log(row)
         row.submit();
      });
    }







