

// this javascript function handles the search query and pagination which ensure that when someone query semething, when they click the next button to see more of that query search that they are able
// to see it. it makes the search query and the pagination works toehter. allowing basically mutiple parameter search.

// get search query and page link
let searchForm = document.getElementById('searchForm');
let pageLink = document.getElementsByClassName('page-link');

// if there is a search for sumibitted or if a search query was requested, get the form, get all page, add an even listener to each and, get the pecific page number the
// the user request, and add that number to the form and give a name value. 

if (searchForm){
    for(let i = 0; pageLink.length > i; i++){
        pageLink[i].addEventListener('click', function (e) {
            e.preventDefault()
            // get data attribute, or the page number when someone click on it.
            let page = this.dataset.page
            // add didden search inout to form
            searchForm.innerHTML += `<input value=${page} name="page" hidden/>`
            // submit for
            searchForm.submit()

        })
    }

};

let tags = document.getElementsByClassName('project-tag');
     for (let i = 0; tags.length > i; i++){
         tags[i].addEventListener('click', (e)=> {
            let tagId = e.target.dataset.tag;
             let projectId = e.target.dataset.project;
            //  console.log('tagid', tagId,);
            //  console.log('ptojectId', projectId);
            fetch('http://127.0.0.1:8000/api/remove_tag/', {
                method:'DELETE',
                headers: {
                    'content-Type': 'application/JSON'
                },
                body: JSON.stringify({'project': projectId, 'tag': tagId})
            })
                .then(Response => Response.json())
                .then(data => {
                    e.target.remove()
                })
         })
     }