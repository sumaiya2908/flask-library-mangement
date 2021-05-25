let book_select = document.getElementById('book_name1');
let member_select = document.getElementById('member_name1');

book_select.addEventListener('change',(e) => {
    book_id = book_select.value

    fetch('/book/' + book_id).then(function(response){
        response.json().then(function(data){
            let optionHTML = member_select.innerHTML;
            for(let member of data.members){
                optionHTML += '<option value="' + member.id + '">'+member.member_name + '</options>'
            }
            member_select.innerHTML = optionHTML;
        })
    })
})
