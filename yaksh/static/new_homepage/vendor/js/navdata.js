document.addEventListener('DOMContentLoaded', () => {
    try{
        load_navdata();
    }
    catch(err) {
        console.log(err)
    }
    var x = window.matchMedia("(max-width: 991px)")
    screencheck(x);
    x.addListener(screencheck)
})
function load_navdata(){
    const request = new XMLHttpRequest();
    request.open('GET', '/api/all_courses');
    request.onload = () => {
        const response = JSON.parse(request.response);
        for(res in response){
            // Exams drop down

            let courseli = document.createElement('li');
            courseli.classList = "sub-dropdown";
            let courselink = document.createElement('a');
            courselink.href = "#a";
            courselink.textContent = response[res].name;
            courseli.appendChild(courselink);

            // subdropdown subject in exams
            let course_sub_drop_ul = document.createElement('ul');
            course_sub_drop_ul.classList = "sub-dropdown-content";
            course_sub_drop_a = document.createElement('a');
            course_sub_drop_a.href="#";
            course_sub_drop_a.textContent = "Subjects";
            
            course_sub_drop_ul.appendChild(course_sub_drop_a);
            course_sub_drop_a = document.createElement('a');
            course_sub_drop_a.href="#";
            course_sub_drop_a.textContent = "Test Series";
            course_sub_drop_ul.appendChild(course_sub_drop_a);
            
            course_sub_drop_a = document.createElement('a');
            course_sub_drop_a.href="#";
            course_sub_drop_a.textContent = "Previous Year Paper";
            course_sub_drop_ul.appendChild(course_sub_drop_a);
            
            course_sub_drop_a = document.createElement('a');
            course_sub_drop_a.href="#";
            course_sub_drop_a.textContent = "Announcements";
            course_sub_drop_ul.appendChild(course_sub_drop_a);
            courseli.appendChild(course_sub_drop_ul);

            // Sub Dropdown Test Series
            


            document.getElementById('courses-drop').appendChild(courseli);
            
            // subjects drop down
            courseli = document.createElement('li');
            courselink = document.createElement('a');
            courselink.href = "#b";
            courselink.textContent = response[res].name
            courseli.appendChild(courselink)
            document.querySelector('#subjects-drop').appendChild(courseli)

            // Tests Drop down
            courseli = document.createElement('li');
            courselink = document.createElement('a');
            courselink.href = "#c";
            courselink.textContent = response[res].name
            courseli.appendChild(courselink)
            document.querySelector('#test-se-drop').appendChild(courseli)
            
            // Previous Year Drop down
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

function screencheck(x) {
    userdrop = document.querySelector("#drop-user");
    if(x.matches){
        user_option = document.querySelector("#user_options");
        user_option.children[1].style.position ="absolute"
        console.log("yes")
        mob_user = document.querySelector("#mob-user");
        console.log(mob_user, userdrop)
        mob_user.appendChild(userdrop)

    }
    else{
        pc_user = document.querySelector("#pc-user");
        pc_user.appendChild(userdrop)
    }
}

