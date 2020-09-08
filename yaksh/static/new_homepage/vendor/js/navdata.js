document.addEventListener('DOMContentLoaded', () => {
    load_navdata();
})
function load_navdata(){
    const request = new XMLHttpRequest();
    request.open('GET', '/api/all_courses');
    request.onload = () => {
        const response = JSON.parse(request.response);
        for(res in response){
            let courseli = document.createElement('li');
            let courselink = document.createElement('a');
            courselink.href = "#a";
            courselink.textContent = response[res].name;
            courseli.appendChild(courselink);
            document.getElementById('courses-drop').appendChild(courseli);
            
            courseli = document.createElement('li');
            courselink = document.createElement('a');
            courselink.href = "#b";
            courselink.textContent = response[res].name
            courseli.appendChild(courselink)
            document.querySelector('#subjects-drop').appendChild(courseli)

            courseli = document.createElement('li');
            courselink = document.createElement('a');
            courselink.href = "#c";
            courselink.textContent = response[res].name
            courseli.appendChild(courselink)
            document.querySelector('#test-se-drop').appendChild(courseli)

            courseli = document.createElement('li');
            courselink = document.createElement('a');
            courselink.href = "#d";
            courselink.textContent = response[res].name
            courseli.appendChild(courselink)
            document.querySelector('#prev-year-drop').appendChild(courseli)
        }
    };
    request.send();
    // const request2 = new XMLHttpRequest();
    // request2.open('GET', '/api/get_subjects');
    // request2.onload = () => {
    //     const response2 = JSON.parse(request2.response);
    //     for(res in response2){
    //         let courseli = document.createElement('li');
    //         let courselink = document.createElement('a');
    //         courselink.href = "#";
    //         courselink.textContent = response2[res].name
    //         courseli.appendChild(courselink)
    //         document.querySelector('#subjects-drop').appendChild(courseli)
    //     }
    // };
    // request2.send();
}

function addtonav(dat){
    
    console.log(dat);
    document.getElementById('subjects-drop').appendChild(dat);
    console.log(dat)
}