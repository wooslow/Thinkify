document.addEventListener("DOMContentLoaded", function () {
    const container = document.querySelector(".cards-container");
  
    const loader = document.createElement("div");
    loader.textContent = "Loading...";
    loader.style.textAlign = "center";
    loader.style.fontSize = "18px";
    container.appendChild(loader);
  
    async function fetchData() {
      try {
            const token = localStorage.getItem("token");
            const response = await fetch("/api/courses", {
                method: "GET",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${token}`
                }
            });
        if (!response.ok)
          throw new Error(`Failed to load data: ${response.statusText}`);
  
        const data = await response.json();
        renderCards(data);
      } catch (error) {
        console.error("Error fetching data:", error);
        showError("No courses available. Please click below to add a course.");
      } finally {
        loader.remove();
      }
    }
  
    function renderCards(courses) {
      container.innerHTML = "";
      if (!courses.length) {
        showError("No courses available.<br> Please click below to add a course.");
        return;
      }
      const fragment = document.createDocumentFragment();
      courses.forEach((course) => {
        const card = document.createElement("div");
        card.classList.add("card");
        card.innerHTML = `
          <h4>${course.name} | ${course.passed_lessons}</h4>
          <p style="color: rgba(0,0,0,0.53);">${course.description}</p>
          <button class="start-btn" onclick="window.location.href='/learn/${course.id}/${course.passed_lessons}'">Continue</button>
          <button class="start-btn">Remove</button>
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
                        padding: 10,
                        paddingLeft: 100
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
    document.getElementById("customChart").style.marginLeft = "-30px"
});