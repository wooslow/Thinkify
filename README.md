## ⚠️ This project was created during a Hackathon by EPAM x EHU in less than 10 hours
#### Due to this, the code may not be fully optimized and could contain some issues. The main goal was to deliver an MVP product.

--- 

# Thinkify 🤖

![project](./preview.png)


Thinkify is an AI-powered platform designed to help you learn any topic by providing personalized study materials, quizzes, progress tracking, and motivation through streaks.
## Try it out

[Thinkify](https://thinkify.wooslow.dev/) - Live demo [https://thinkify.wooslow.dev/](https://thinkify.wooslow.dev/)

## Features
- **Personalized Study Materials**: Thinkify provides you with personalized study materials based on your learning preferences and progress.
- **Quizzes**: Test your knowledge with quizzes and track your progress.
- **Progress Tracking**: Track your progress and see how much you've learned.
- **Streaks**: Stay motivated with streaks and earn rewards.
- **AI-powered**: Thinkify uses AI to provide you with the best learning experience.

## Tech Stack
- **Frontend**: Html, CSS, JavaScript by [@edrdavid1](https://github.com/edrdavid1)
- **Backend**: Python, FastAPI, PostgreSQL, OpenAI API by [@wooslow](https://github.com/wooslow)

## How to run
1. Clone the repository
2. Install the dependencies `poetry install`
3. Create a `.env` file and add the following variables:
```
DATABASE_URL=
DATABASE_ALEMBIC_URL=
SECRET_KEY=
OPENAI_API_KEY=
```
4. Run the migrations `poetry run alembic upgrade head`
5. Run the server
