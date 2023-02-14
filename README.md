# Lean Backend

Built with Fastapi & MongoDB

## To run mongodb locally

### Recommended (Use docker to setup mongodb locally)

&nbsp;&nbsp;MacOS: Follow this guide, [link](https://www.code4it.dev/blog/run-mongodb-on-docker)

&nbsp;&nbsp;Windows: Follow this guide, [link](https://www.youtube.com/watch?v=NEPZqSvKx40&ab_channel=TalkingaboutComputerScience)

### If docker is not installed,

&nbsp;&nbsp;MacOS: Follow this guide, [link](https://docs.docker.com/desktop/install/mac-install/)

&nbsp;&nbsp;Windows: Follow this guide, [link](https://docs.docker.com/desktop/install/windows-install/)

&nbsp;&nbsp;After installing mongoDB, create a .env in lean-backend root directory and follow the format in .env.example

&nbsp;&nbsp;Change the MONGO_URI=mongodb://(username):(password)@localhost:(port)/?retryWrites=true

&nbsp;&nbsp;Use MongoDB Compass Client to access MongoDB with a GUI, [link](https://www.mongodb.com/try/download/compass)

&nbsp;&nbsp;Connect to MongoDB using the MONGO_URI above and create a db, note down the db name you input

&nbsp;&nbsp;Change the DB_NAME in .env to the db name of db you created.

## To start fastapi server

### Recommended (Use pipenv to manage python dependencies)

&nbsp;&nbsp;`git clone git@github.com:zihaolam/lean-backend.git`

&nbsp;&nbsp;`cd lean-backend`

&nbsp;&nbsp;`pip install --user pipenv`

&nbsp;&nbsp;`pipenv install`

&nbsp;&nbsp;`pipenv shell`

&nbsp;&nbsp;`yarn dev`
