var inputSearch = document.getElementById('input-search');
var batches = document.querySelectorAll('.batch');
var people = document.querySelectorAll('.batch ul li');

inputSearch.onkeyup = function(){
    var value = inputSearch.value.toLowerCase();
    for (var i = 0; i < batches.length; i++){
        var batch = batches[i];
        batch.classList.add('hide');
    }
    for (var i = 0; i < people.length; i++){
        var person = people[i];
        person.classList.add('hide')
        var children = person.children[0].children;

        for (var j = 0; j < children.length; j++){
            var child = children[j];
            var classes = child.classList;

            if(classes.contains('pseudonym') || classes.contains('real-name')){
                var innerHTML = child.innerHTML.toLowerCase()

                // contains search string
                if(innerHTML.indexOf(value) > -1){
                    // show person
                    person.classList.remove('hide');

                    // show batch
                    person.parentNode.parentNode.classList.remove('hide');
                }
            }
        }
    }
}