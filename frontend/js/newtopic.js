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

        const topicData = {
            shortTitle,
            achievement,
            selfEvaluation
        };

        try {
            const response = await fetch('/your-server-endpoint', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(topicData)
            });

            if (!response.ok) {
                throw new Error(`Server error: ${response.status}`);
            }

            const result = await response.json();
            console.log('Data sent successfully:', result);
            showStatus('Data sent successfully!');
            inputs.forEach(input => input.value = '');
        } catch (error) {
            console.error('Error sending data:', error);
            showStatus('An error occurred. Please try again later.', true);
        } finally {
            addTopicBtn.disabled = false;
        }
    });
});
