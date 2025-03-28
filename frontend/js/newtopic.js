document.addEventListener('DOMContentLoaded', () => {
    const addTopicBtn = document.getElementById('add-topic');
    const container = document.querySelector('.container2');
    const inputs = container.querySelectorAll('input');

    const statusMessage = document.createElement('div');
    statusMessage.className = 'status-message';
    statusMessage.style.marginTop = '10px';
    statusMessage.style.fontFamily = 'Unbounded, sans-serif';
    container.appendChild(statusMessage);

    function showStatus(message, isError = false) {
        statusMessage.textContent = message;
        statusMessage.style.color = isError ? 'red' : 'green';
    }

    addTopicBtn.addEventListener('click', async () => {
        addTopicBtn.disabled = true;
        showStatus('Sending data...');

        const [shortTitle, achievement, selfEvaluation] = Array.from(inputs, input => input.value.trim());

        if (!shortTitle || !achievement || !selfEvaluation) {
            showStatus('Please fill in all fields.', true);
            addTopicBtn.disabled = false;
            return;
        }

        const courseData = {
            topic: shortTitle,
            destination: achievement,
            knows_now: selfEvaluation
        };

        try {
            const token = localStorage.getItem('token');
            const response = await fetch('/api/course', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    Authorization: `Bearer ${token}`
                },
                body: JSON.stringify(courseData)
            });

            if (!response.ok) {
                throw new Error(`Server error: ${response.status}`);
            }

            const result = await response.json();
            console.log('Data sent successfully:', result);
            window.location.href = '/main';
            inputs.forEach(input => input.value = '');
        } catch (error) {
            console.error('Error sending data:', error);
            showStatus('An error occurred. Please try again later.', true);
        } finally {
            addTopicBtn.disabled = false;
        }
    });
});
