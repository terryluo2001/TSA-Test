# TSA-Test
A full stack application allowing CRUD of tasks. 

Inside this directory, is a directory which is a Vite app frontend implemented using React.js and Typescript.
As well as this, there is a backend directory which is a Python flask app backend.
Since I was busy, I started this project today and used Claude to help me code a majority of this, using Playwright MCP to help do the testing. However, I still proofread my code in order to make sure I understand what Claude is writing and to ensure that there are no hidden bugs. 

Since I used Claude to code in React.js, I was mostly focussed on functionality rather than styling.

Set up instructions

To run the frontend. Go inside TSA-frontend:
cd TSA-frontend

Install the packages:
npm install

Run the Vite App using npm run dev

To run the backend. Go inside TSA-backend:
cd TSA-backend

run python app.py

In the future, I would make some time to start this project earlier, and also use less AI for the frontend so I can understand the code better and be able to fix the styling myself. This is something I've been working on by making AI do small things at a time and taking the time to proof read the code in intervals each time.

My database details are:
DB_HOST=61.69.238.31
DB_PORT=3306
DB_USER=root
DB_PASSWORD=
DB_NAME=todolist_db