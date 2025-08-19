// Simplified example of the updated JavaScript
async function checkPassword() {
  const passResponse = await fetch('/key.txt');
  const correctPassword = await passResponse.text();
  
  const enteredPassword = document.getElementById("password-input").value;

  if (enteredPassword === correctPassword) {
    // Fetch the content from the separate file
    const response = await fetch('/section-content-downloads.html');
    const content = await response.text();
    
    // Display the content on the page
    document.getElementById("protected-content").innerHTML = content;
    document.getElementById("protected-content").style.display = "block";
    document.getElementById("password-gate-container").style.display = "none";
  } else {
    // Handle incorrect password
  }
}