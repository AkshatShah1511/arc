document.getElementById("saveBtn").addEventListener("click", () => {
    const email = document.getElementById("email").value;
    const url = document.getElementById("url").value;
  
    chrome.runtime.sendMessage(
      {
        type: "SAVE_DATA",
        payload: { email, url }
      },
      (response) => {
        document.getElementById("status").textContent =
          response.message;
      }
    );
  });
  