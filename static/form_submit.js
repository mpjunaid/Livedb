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
      if (data.created) {
        handleResponse("New user code created. Please check your email:"+ email +" for the code. User code:"+data.key);
      } else {
        handleResponse("User code already exists. Email sent to "+ email +" with the existing code. User code:"+data.key);
      }
    })
    .catch(error => console.error('Error:', error));
  });