async function uploadPDF() {
    const fileInput = document.getElementById("pdfFile");
    const file = fileInput.files[0];

    if (!file) {
        alert("Please select a file");
        return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
        const response = await fetch("http://127.0.0.1:5000/upload", {
            method: "POST",
            body: formData
        });

        const data = await response.json();

        if (data.text) {
            document.getElementById("outputText").innerText = data.text;
        } else {
            alert(data.error);
        }

    } catch (error) {
        console.error("Error:", error);
    }
}