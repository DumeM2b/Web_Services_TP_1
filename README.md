# Web_Services_TP_1

Andrea MACHEDA

## Introduction
In this lab session, we focused on applying the concepts learned in class about building RESTful servers. The main objective was to create a RESTful API using Flask and interact with a PostgreSQL database. The lab was divided into several key parts:

1. **Setting up PostgreSQL**: We began by setting up a PostgreSQL database using Docker for containerization, which allowed us to quickly deploy and manage our database environment.

2. **Database Configuration**: Once the PostgreSQL database was set up, we configured it with PgAdmin, a web-based database administration tool, to create and manage our database and tables.

3. **Virtual Environment**: We created a virtual environment to isolate the dependencies of our project, ensuring a clean and reproducible development environment.

4. **API Development**: The core of the lab focused on developing a RESTful API. We followed two approaches:
   - **SQL Approach**: We first created the database tables (User and Application) using SQL queries and executed them in our PostgreSQL database with SQLAlchemy.
   - **ORM Approach**: Then, we explored the Object-Relational Mapping (ORM) concept by configuring SQLAlchemy with Flask. We defined models representing the database tables and interacted with the database using object-oriented programming, without writing explicit SQL queries.

5. **Populating the Database**: We utilized the Faker library to generate fake data and populate our database tables, simulating realistic data scenarios.

6. **Implementation of REST Methods**: We implemented the GET method to retrieve data from our API, allowing clients to access information about users and applications stored in the database.

7. **Optional: Endpoints for POST Method**: We discussed the implementation of additional endpoints for creating resource, enhancing the functionality of our API.

8. **Optional: Integration with a Web Application**: Finally, we explored the integration of our REST API into a Flask web application. We created a simple web page to display user information retrieved from the API.

## Conclusion
Overall, this lab provided hands-on experience in developing RESTful APIs with Flask and interacting with a PostgreSQL database. By understanding the concepts of containerization, database configuration, ORM, and API development, we gained valuable insights into building scalable and efficient web applications.
