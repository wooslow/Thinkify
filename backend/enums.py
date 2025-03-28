PROMT_AI = """
Generate a structured learning course based on the following user input:

Course name: польский язык
Goal after completing the course: я хочу знать многие фрукты и овощи на польском языке
Current knowledge level: A1 немного знаю польский алфавит и некоторые слова

The response should be ONLY a structured JSON object like this:

{
    "course_name": "English Language",
    "course_short_description": "Beginner-level English course up to A1",
    "course_tasks": [
        {
            "task_name": "Lesson name",
            "task_description": "Detailed lesson content explaining the topic (up to 1500 characters)",
            "test_after_task": [
                {
                    "question": "A multiple-choice question",
                    "answers": ["Option 1", "Option 2", "Option 3", "Option 4"],
                    "type": "radio",
                    "correct_answer": 2
                },
                {
                    "question": "A question requiring user input",
                    "answers": [],
                    "type": "input",
                    "correct_answer": "None"
                }
            ]
        }
    ]
}

The course should be logically structured to help the user progress from their current knowledge level to the desired goal. Ensure a smooth learning curve, creating around 20 tasks with increasing complexity.
If you can't answer the question for some reason, you should return a json in the format {“error”: “Not Acsess”}.
ANSWER ONLY JSON!!
"""