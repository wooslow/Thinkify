document.addEventListener("DOMContentLoaded", function () {
    const container = document.querySelector(".cards-container");
  
    const loader = document.createElement("div");
    loader.textContent = "Loading...";
    loader.style.textAlign = "center";
    loader.style.fontSize = "18px";
    container.appendChild(loader);
  
    async function fetchData() {
      try {
        const response = await fetch("/courses");
        if (!response.ok)
          throw new Error(`Failed to load data: ${response.statusText}`);
  
        const data = await response.json();
        renderCards(data);
      } catch (error) {
        console.error("Error fetching data:", error);
        showError("Failed to load cards. Please try again later.");
      } finally {
        loader.remove();
      }
    }
  
    function renderCards(courses) {
      container.innerHTML = "";
      if (!courses.length) {
        showError("No courses available.");
        return;
      }
      const fragment = document.createDocumentFragment();
      courses.forEach((course) => {
        const card = document.createElement("div");
        card.classList.add("card");
        card.innerHTML = `
          <h4>${course.name}</h4>
          <p>${course.description}</p>
          <p><strong>Author:</strong> ${course.author}</p>
          <p><strong>Passed Lessons:</strong> ${course.passed_lessons}</p>
          <button class="start-btn">Start Course</button>
        `;
        fragment.appendChild(card);
      });
      container.appendChild(fragment);
    }
  
    function showError(message) {
      container.innerHTML = `<p style="color: red; text-align: center;">${message}</p>`;
    }
  
    function debounce(func, delay = 300) {
      let timeout;
      return function (...args) {
        clearTimeout(timeout);
        timeout = setTimeout(() => func(...args), delay);
      };
    }
  
    const fetchDebounced = debounce(fetchData, 500);
    fetchDebounced();
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