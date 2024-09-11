function handleResponse(response) {
    const responseDiv = document.getElementById('response');
    responseDiv.innerHTML = response;
  }
  
  const form = document.getElementById('signup-form');
  form.addEventListener('submit', (event) => {
    console.log("Open JS file")
    event.preventDefault(); // Prevent default form submission behavior
    const formData = new FormData(form);
    const email = formData.get('email');

    fetch('/sign_up', {
      method: 'POST',
      body: formData
    })
    .then(response => response.json())
    .then(data => {
      console.log(data.message)
      if (data.user_status) {
        handleResponse("New user code created. "+ data.message);
      } else {
        handleResponse("User code already exists. "+ data.message);
      }
    })
    .catch(error => console.error('Error:', error));
  });