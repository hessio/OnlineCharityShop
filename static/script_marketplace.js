// Get all the modal buttons
var modalBtns = document.querySelectorAll('.item');

// Add a click event listener to each modal button
modalBtns.forEach(function(btn) {
  btn.addEventListener('click', function() {
    // Get the modal ID from the data-modal attribute
    var modalId = btn.getAttribute('data-modal');
    //document.getElementById("test").innerHTML += modalId;
    //document.write(modalId);

    // Get the modal element
    var modal = document.querySelector(modalId);
    // Get the div element
    // var myDiv = document.getElementById('my-div');

    // Change the text of the div element
    // myDiv.innerHTML = 'Fuckign fuckers';
    
    // Display the modal
    modal.style.display = 'block';

    // Add a click event listener to the close button
    var closeBtn = modal.querySelector('.close-btn');
    //myDiv.innerHTML = "${closeBtn}" + closeBtn.textContent;
    closeBtn.addEventListener('click', function() {
      // Hide the modal
      // myDiv.innerHTML = 'button works';
      modal.style.display = 'none';
    });
  });
});


// Select all elements with an id attribute that starts with "title-item"
const title_items = document.querySelectorAll('#capitalised');

// Loop through each element and update its text content
title_items.forEach(element => {
  const text = element.innerText.trim();
  // console.log(text);
  const newText = text.charAt(0).toUpperCase() + text.slice(1);
  element.textContent = newText;
});



// const title_item = document.querySelectorAll('title-item');
// title_item.forEach(

// );
// var myDiv = document.getElementById('title-item');
// myDiv.innerHTML += 'help me'; //+ str;
// // console.log(str);
// // const str2 = str.charAt(0).toUpperCase() + str.slice(1);
