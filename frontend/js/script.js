document.addEventListener("DOMContentLoaded", function() {
    const container = document.querySelector(".cards-container");
    
    function createCard(title, description, buttonText) {
        const card = document.createElement("div");
        card.classList.add("card");
        
        const h4 = document.createElement("h4");
        h4.textContent = title;
        
        const p = document.createElement("p");
        p.textContent = description;
        
        const button = document.createElement("button");
        button.classList.add("start-butt");
        button.textContent = buttonText;
        
        card.appendChild(h4);
        card.appendChild(p);
        card.appendChild(button);
        
        container.appendChild(card);
    }
    
    // Пример добавления карточек
    createCard("Russian to A2", "Lorem Ipsum is simply dummy text of the printing and typesetting industry.", "15/30");
    createCard("Russian to B1", "Another example of dummy text for demonstration purposes.", "10/20");
});



document.addEventListener("DOMContentLoaded", function () {
    const ctx = document.getElementById("customChart").getContext("2d");

    new Chart(ctx, {
        type: "line",
        data: {
            labels: ["Day 1", "Day 5", "Day 10", "Day 15", "Day 20"],
            datasets: [{
                data: [0, 40, 60, 75],
                borderColor: "#ffffff", // Белая линия
                borderWidth: 3, // Толще для четкости
                tension: 0.4, // Плавная линия
                fill: false, // Без заливки
                pointRadius: 0 // Без точек
            }]
        },
        options: {
            responsive: true,
            animation: false, // Убираем бесконечную анимацию
            plugins: {
                legend: { display: false } // Без легенды
            },
            scales: {
                x: {
                    grid: {
                        display: false,
                        drawBorder: true
                    },
                    border: {
                        display: true,
                        width: 4, // Толщина оси X
                        color: "black" // Цвет оси X
                    },
                    ticks: { display: false }, // Убираем подписи оси X
                    title: {
                        display: true,
                        text: "lessons learned",
                        color: "black",
                        font: { size: 18, weight: "bold" },
                        padding: 10
                    }
                },
                y: {
                    grid: {
                        display: false,
                        drawBorder: true
                    },
                    border: {
                        display: true,
                        width: 4, // Толщина оси Y
                        color: "black" // Цвет оси Y
                    },
                    ticks: { display: false }, // Убираем подписи оси Y
                    title: {
                        display: true,
                        text: "response rate",
                        color: "black",
                        font: { size: 18, weight: "bold" },
                        padding: 10
                    }
                }
            }
        }
    });

    // Убираем фон, делая его прозрачным
    document.getElementById("customChart").style.background = "transparent";
});