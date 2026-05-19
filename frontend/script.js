console.log("JS FILE LOADED");

const backend = "http://127.0.0.1:8000";

async function uploadPDF() {
  const file = document.getElementById("pdfFile").files[0];

  if (!file) {
    alert("Select a file first");
    return;
  }

  const formData = new FormData();
  formData.append("file", file);

  try {
    const res = await fetch(backend + "/upload", {
      method: "POST",
      body: formData
    });

    const data = await res.json();
    document.getElementById("status").innerText = data.message;

  } catch (error) {
    console.error("UPLOAD ERROR:", error);
    document.getElementById("status").innerText = "Upload failed";
  }
}

async function askQuestion() {
  const question = document.getElementById("question").value;

  if (!question) {
    alert("Please enter a question");
    return;
  }

  try {
    const res = await fetch(
      backend + "/ask?question=" + encodeURIComponent(question)
    );

    const data = await res.json();
    document.getElementById("answer").innerText = data.answer;

  } catch (error) {
    console.error("ASK ERROR:", error);
    document.getElementById("answer").innerText = "Error getting answer";
  }
}