document.addEventListener("DOMContentLoaded", async () => {
    const form = document.getElementById("quiz-form");
    const submitBtn = document.getElementById("submit-btn");
    
    try {
        const response = await fetch("https://your-backend.com/api/questions");
        const questions = await response.json();
        
        questions.forEach((q, index) => {
            const questionElement = document.createElement("div");
            questionElement.classList.add("question");
            questionElement.innerHTML = `<p>${index + 1}. ${q.text}</p>`;
            
            const optionsContainer = document.createElement("div");
            optionsContainer.classList.add("options");
            
            q.options.forEach(option => {
                const label = document.createElement("label");
                const input = document.createElement("input");
                input.type = "radio";
                input.name = `q${index}`;
                input.value = option;
                label.appendChild(input);
                label.appendChild(document.createTextNode(` ${option}`));
                optionsContainer.appendChild(label);
            });
            
            questionElement.appendChild(optionsContainer);
            form.appendChild(questionElement);
        });
    } catch (error) {
        console.error("Error loading questions:", error);
    }
    
    submitBtn.addEventListener("click", async () => {
        const formData = new FormData(form);
        const answers = Object.fromEntries(formData.entries());
        
        try {
            const response = await fetch("", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ answers })
            });
            const result = await response.json();
            alert(result.message || "Results submitted successfully!");
        } catch (error) {
            console.error("Error submitting answers:", error);
        }
    });
});