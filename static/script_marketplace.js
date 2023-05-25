// Get all the modal buttons
var modalBtns = document.querySelectorAll('.item');

// Add a click event listener to each modal button
modalBtns.forEach(function(btn) {
  btn.addEventListener('click', function() {
    // Get the modal ID from the data-modal attribute
    var modalId = btn.getAttribute('data-modal');

    // Get the modal element
    var modal = document.querySelector(modalId);
    
    // Display the modal
    modal.style.display = 'block';

    // Add a click event listener to the close button
    var closeBtn = modal.querySelector('.close-btn');
    closeBtn.addEventListener('click', function() {
      // Hide the modal
      modal.style.display = 'none';
    });
  });
});


// Select all elements with an id attribute that starts with "title-item"
const title_items = document.querySelectorAll('#capitalised');

// Loop through each element and update its text content
title_items.forEach(element => {
  const text = element.innerText.trim();

  const newText = text.charAt(0).toUpperCase() + text.slice(1);
  element.textContent = newText;
});

