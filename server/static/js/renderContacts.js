//function renderContacts(list of contacts) {

    var contactList = document.createElement('ul'); //document.getElementById("contact-list");

    for (i = 0; i < 1; i++) { // for (i = 0; i < contacts.length; i++) {

    	var contactName = "rachel"; //getContactsFromDatabase()[i].username;
    	var contactId = contactName;
    	

		var row = document.createElement('li');
		if (i == 1) {
        	row.className = "panel panel-info list-group-item justify-content-between active contact text-primary";
        }
        else {
        	row.className = "panel panel-info list-group-item justify-content-between contact text-primary";
        }
        row.id = contactId;

        row.innerText = contactName;

        var dropdown = document.createElement('span');
        dropdown.className = "btn-group pull-right edit-button";

        var editButton = document.createElement('button');
        editButton.type = "button";
        editButton.className = "btn btn-default dropdown-toggle";
        editButton.setAttribute('data-toggle' , 'dropdown');
        //editButton.data-toggle = "dropdown";

        var editIcon = document.createElement('span');
        editIcon.className = "fa fa-pencil-square-o";
        editButton.appendChild(editIcon);

        dropdown.appendChild(editButton);
       
        var menu = document.createElement('ul');
        menu.className = 'dropdown-menu';
        menu.setAttribute('role', 'menu');


        var editName = document.createElement('li');
        editName.className = "open-edit-name-modal";
        editName.setAttribute('data-toggle', 'modal');
        editName.setAttribute('data-target', '#edit-name-modal');
        editName.setAttribute('data-id', contactId);

        var text = document.createElement('a');
        text.innerText = "Edit name";
        editName.appendChild(text);

        menu.appendChild(editName);

        var deleteConvo = document.createElement('li');
        deleteConvo.className = "delete-convo";
        deleteConvo.setAttribute('data-id', contactId);

        var text2 = document.createElement('a');
        text2.innerText = "Delete conversation";
        deleteConvo.appendChild(text2);

        menu.appendChild(deleteConvo);

        dropdown.appendChild(menu);  

        row.appendChild(dropdown);

        contactList.appendChild(row);

    	// <li class="panel panel-info list-group-item justify-content-between active contact text-primary" id= contactId>
    	// contactName

    	// <span class="btn-group pull-right edit-button">
	    //     <button type="button" class="btn btn-default dropdown-toggle" data-toggle="dropdown">
	    //       <span class="fa fa-pencil-square-o"></span>
	    //     </button>

	    //     <ul class="dropdown-menu" role="menu">
	    //         <li data-toggle="modal" data-target="#edit-name-modal" class="open-edit-name-modal" data-id= contactId><a href="#">Edit name</a></li>
	    //         <li class="delete-contact" data-id= contactId><a href="#">Delete contact</a>
	    //         </li>
	    //     </ul>
	    //   </span>

	    // </li>



	}

	console.log(contactList.innerHTML);

    console.log(document.getElementsByClassName('active contact')[0].id);

//}