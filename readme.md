# DailyDiet

You can access the website at [daily-diet-aut.herokuapp.com](https://daily-diet-aut.herokuapp.com/)
and the API is deployed on Heroku at [dailydiet-api.herokuapp.com](https://dailydiet-api.herokuapp.com/).

We're a small team focused on providing tools and support for people who want to take control of their nutrition. Given the saturation of information in the diet industry, we focus on more pragmatic elements of healthy eating such as planning and cooking.

## Features

1. **BMI and Daily Needed Calorie Calculator:**  
   Body Mass Index (BMI) is a value derived from the mass and height of a person. It can be an important thing to consider in someone's diet since it describes your current body situation (if you need to lose or gain weight).  
   A normal person's daily needed calorie can be calculated using personal data and it's the most important thing in a healthy diet.

2. **Receiving Diet Plans:**  
   We have implemented a dynamic-programming algorithm for constructing a relevant diet based on the user's needed calorie. The algorithm can be improved using more complex concepts (genetic, etc.).  
   The plan will mostly contain a breakfast, main dish, and a simpler meal. The number of meals can be selected by the user.

3. **Accounts Managing:**  
   We used JWT to create and manage users' accounts. Users must sign up and confirm their email in order to use our main features.  
   Users can also use a dashboard to review their daily diets for the past 5 days, or manage other things about their accounts.

4. **(Advanced) Searching Recipes:**  
   We have implemented Elasticsearch on our database. Our Elasticsearch allows users to not only search by the name of the foods but also provide the feature of an advanced search. The search can be expanded on food nutrition, cooking time, and ingredients in various categories. You can search for recipes you can make with the ingredients you already have at home.

5. **Blog:**  
   Our blog is where authenticated users and nutrition experts can publish their posts.  
   Posts are displayed in the blog timeline and can be accessed by category or author.

6. **Admin Panel:**  
   An admin is needed to maintain and modify our content and users.  
   Admins can edit (create/delete/edit) blog posts, recipes, and users.

## Technologies

1. **Back-end:**
   - FLASK
   - PostgreSQL (on AWS cluster)
   - JSON Web Tokens
   - Elasticsearch

2. **Front-end:**
   - Vue.JS
   - NUXT
   - BootstrapVue

3. **Deployment:**
   - We have deployed our project on every stage to maintain a stable product.
   - DailyDiet is deployed on Heroku, which is a cloud platform as a service supporting several programming languages for easy deployment of applications.

4. **iOS Application:**
   - Swift
   - Auto Layout
   - Fastlane
   - GitHub Action

## Setup and Run on local machine

1. Install packages with `pip install -r requirements.txt`

2. Set environment variable `DAILYDIET_ENV` to `Development`/`Testing`/`Production`  
   (default value is `Development` if you set nothing)

3. Copy `.env.example` to `.env` and fill in the keys

4. Run with `python app.py`
