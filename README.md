Welcome to the search-developers wiki!

# Discover developers (click on Master branch to see code)
live link: http://discover-devs.devprojectspro.com/

Developed a powerful platform that empowers developers to showcase their talent and gain global exposure. With a simple sign-up process, developers can create their personalized profiles, highlighting their skills and projects. They have the flexibility to launch their profiles, allowing users from all over the world to explore their work. A unique feature of our platform is the ability for developers to rate and comment on each other's projects, fostering a collaborative and supportive community. Additionally, we have integrated a messaging app directly into the platform, enabling seamless communication among users.

To ensure a robust and reliable infrastructure, we have deployed this web application using ElasticBeanstalk, S3, leveraging S3 for image storage and PostgreSQL for secure user data storage.

Created a Backend RESTful-API that allows users with certain permissions to make api call to the database. 
Non users are allowed to fetch data using the Get Method. However, only login user can POST, PUT and DELETE object using the api endpoint. 
Used JSON Web Token Authentication to authenticate users that want to use the API endpoint.

## # Deployement
* Created both a local and deployment docker file
* Packaged project with docker-compose
* Deployed project on AWS EC2 instance with docker-compose

## # Key features:
* create, edit, and delete profile
* add, edit, and remove skills and projects
* Access message inbox anytime and reply to requests
* Add links for all projects such as GitHub, Youtube, Website ect..
* API endpoint to fetch data with authentication.


![dev3](https://user-images.githubusercontent.com/83102811/212494450-9663958e-c436-4b99-8ec7-39848224e707.png)
![dev4](https://user-images.githubusercontent.com/83102811/212494453-9a78d114-9bc6-439f-8e5e-a2b9661359b2.png)
![dev1](https://user-images.githubusercontent.com/83102811/212494462-44e0aef7-4482-4678-af61-8a86626f860d.png)
![dev2](https://user-images.githubusercontent.com/83102811/212494464-74b410a0-c2b4-4f45-bcda-8689c587f74d.png)
