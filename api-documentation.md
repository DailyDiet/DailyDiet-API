# DailyDiet API Documentation

## v1.0

### `/calculate/bmi`

method: `POST`

*input*:

- height in centimeters
- weight in kilograms

```json
{
  "height":180,  
  "weight":80
}
```

*output*:

- `bmi_value` rounded up to 2 decimal points
- `bmi_status` one of **Underweight**, **Normal weight**, **Overweight** or **Obesity**

```json
{
  "bmi_status": "Normal weight",
  "bmi_value": 24.69
}

```

*in case of errors*:

response code will be **400**

```json
{
  "errors": {
    "height": [
      "This field is required."
    ],
    "weight": [
      "Number must be between 20 and 150."
    ]
  }
}
```

----------

### `/calculate/calorie`

method: `POST`

*input*:

- goal one of **lose_weight**, **maintain** or **build_muscle**
- gender one of **male** or **female**
- height in centimiters
- weight in kilograms
- age in years
- activity level one of **sedentary**, **lightly**, **moderately**, **very** or **extra**

```json
{
  "goal":"maintain",
  "gender":"male",
  "height":180,  
  "weight":80,
  "age":21,
  "activity":"lightly"
}
```

*output*:

- `calorie` is integer number

```json
{
  "calorie": 2638
}

```

*in case of errors*:

response code will be **400**

```json
{
  "errors": {
    "activity": [
      "Invalid value, must be one of: sedentary, lightly, moderately, very, extra."
    ],
    "age": [
      "This field is required."
    ],
    "gender": [
      "Invalid value, must be one of: male, female."
    ],
    "goal": [
      "Invalid value, must be one of: lose_weight, maintain, build_muscle."
    ],
    "height": [
      "Number must be between 50 and 210."
    ],
    "weight": [
      "Number must be between 20 and 150."
    ]
  }
}
```

----------

### `/users/signup`

method: `POST`

*input*:

- full_name
- email
- password
- confirm_password

```json
{
  "full_name": "Arnold Schwarzenegger",
  "email": "arnold.schwarzenegger@gmail.com",
  "password": "p@$$word123",
  "confirm_password": "p@$$word123"
}
```

*output*:

response code will be **201**

- `msg` is string

```json
{
  "msg": "Account created successfully!"
}

```

*in case of errors*:

response code will be **400**

```json
{
  "errors": {
    "email": [
      "Email already registered."
    ]
  }
}
```

or

```json
{
  "errors": {
    "confirm_password": [
      "Passwords must match."
    ],
    "email": [
      "Invalid email address."
    ],
    "password": [
      "Field must be between 6 and 25 characters long."
    ]
  }
}
```

----------

### `/users/signup/confirmation/<token>`

method: `GET`

*input*: **NONE**

*output*:

response code will be **204**

- The server successfully processed the request and is not returning any content.

*in case of errors*:

1- response code will be **404**

```json
{
  "error": "User not found."
}
```

2- response code will be **400**

```json
{
  "error": "The confirmation link is invalid or has expired."
}
```

or

```json
{
  "error": "Account already confirmed. Please login."
}
```

----------

### `/users/signin`

method: `POST`

*input*:

- email
- password

```json
{
  "email": "arnold.schwarzenegger@gmail.com",
  "password": "p@$$word123"
}
```

*output*:

response code will be **200**

- is_active
- access_token
- refresh_token

```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1OTEzODEwOTYsIm5iZiI6MTU5MTM4MTA5NiwianRpIjoiYWViMjY5MDktYzUxZS00NTM0LTk0NWEtMzZkYzEwZjNiMjdhIiwiZXhwIjoxNTkxMzgxOTk2LCJpZGVudGl0eSI6Im1vaGFtbWFkaG9zc2Vpbi5tYWxla3BvdXJAZ21haWwuY29tIiwiZnJlc2giOnRydWUsInR5cGUiOiJhY2Nlc3MifQ.8iSlZyW2pQN-OzDiSUe7LKbgX6iS6CNOsPMUGZfhf-s",
  "is_active": true,
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1OTEzODEwOTYsIm5iZiI6MTU5MTM4MTA5NiwianRpIjoiMDA5N2E1M2ItYWI4Yi00YzAwLTkxZjUtZTgwNmNkNWFjNTRmIiwiZXhwIjoxNTkzOTczMDk2LCJpZGVudGl0eSI6Im1vaGFtbWFkaG9zc2Vpbi5tYWxla3BvdXJAZ21haWwuY29tIiwidHlwZSI6InJlZnJlc2gifQ.TpuHN33fO66LWVZktvYr10VGoDWwONJkPaC6WgywgQM"
}
```

*in case of errors*:

1- response code will be **403**

```json
{
  "error": "Email or Password does not match."
}
```

2- response code will be **400**

```json
{
  "errors": {
    "email": [
      "Invalid email address."
    ]
  }
}
```

----------

### `/users/auth`

method: `PUT`

*input*:

Authorization Header:

- Bearer \<refresh token>

Body:

- None

*output*:

response code will be **200**

- access_token

```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1ODc5OTQ1NDYsIm5iZiI6MTU4Nzk5NDU0NiwianRpIjoiZmU0YTE2MjUtNDFkMi00MjljLTlhZDItNmFlZDYyM2MzZDUwIiwiZXhwIjoxNTg3OTk1NDQ2LCJpZGVudGl0eSI6Im1vaGFtbWFkaG9zc2Vpbi5tYWxla3BvdXJAZ21haWwuY29tIiwiZnJlc2giOmZhbHNlLCJ0eXBlIjoiYWNjZXNzIn0.9Cybw84QcwAuxxPGoEhURAHFUTQpIK3A9N8TxE38NMw"
}
```

*in case of errors*:

1- response code will be **422**

```json
{
  "msg": "Signature verification failed"
}
```

or

```json
{
  "msg": "Invalid header string: 'utf-8' codec can't decode byte 0x9a in position 15: invalid start byte"
}
```

or

```json
{
  "msg": "Not enough segments"
}
```

2- response code will be **401**

```json
{
  "msg": "Token has expired"
}
```

----------

### `/users/signup/resendConfrimation`

method: `GET`

*input*:

Authorization Header:

- Bearer \<access token>

Body:

- None

*output*:

response code will be **200**

- `msg` is string

```json
{
  "msg": "A new confirmation email has been sent."
}

```

*in case of errors*:

1- response code will be **422**

```json
{
  "msg": "Signature verification failed"
}
```

or

```json
{
  "msg": "Invalid header string: 'utf-8' codec can't decode byte 0x9a in position 15: invalid start byte"
}
```

or

```json
{
  "msg": "Not enough segments"
}
```

2- response code will be **401**

```json
{
  "msg": "Token has expired"
}
```

----------

### `/users/signup/modify`

method: `PATCH`

*input*:
Authorization Header:

- Bearer \<access token>

Body:

- old_password
- new_password
- confirm_password

```json
{
  "old_password": "p@$$word123",
  "new_password": "123456",
  "confirm_password": "123456"
}
```

*output*:

response code will be **204**

- The server successfully processed the request and is not returning any content.

*in case of errors*:

1- response code will be **401**

```json
{
  "msg": "Token has expired"
}
```

2t- response code will be **422**

```json
{
  "msg": "Signature verification failed"
}
```

or

```json
{
  "msg": "Invalid header string: 'utf-8' codec can't decode byte 0x9a in position 15: invalid start byte"
}
```

or

```json
{
  "msg": "Not enough segments"
}
```

----------

### `/users/signout`

method: `PATCH`

*input*:

- None

*output*:

response code will be **204**

- The server successfully processed the request and is not returning any content.

----------

### `/users/get_user

method: `GET`

*input*:
Authorization Header:

- Bearer \<access token>

Body:

- None

*output*:

response code will be **200**

```json
{
  "confirmed": "False",
  "email": "mohammadhossein.malekpour@gmail.com",
  "full_name": "Mohammad Hossein Malekpour"
}
```

*in case of errors*:

1- response code will be **401**

```json
{
  "msg": "Token has expired"
}
```

----------

### `/foods/recipe/<int:id>`

method: `GET`

recipe and foods detailed information

*input*:
URL:

- food id

*sample input*:

```
/foods/recipe/33480
```

*output*:

response code will be **200**

- The server successfully processed the request and it's returning the recipe in this format.

- image id is **0** if image is a placeholder 

```json
{
  "author_id": 1,
  "category": "sandwich",
  "cook_time": 0,
  "date_created": "2020-05-07 15:10:07",
  "description": "Peanut butter + jelly",
  "directions": [],
  "food_name": "Big PB&J Sandwich",
  "id": 33482,
  "images": [
    {
      "id": 7,
      "image": "https://images.eatthismuch.com/site_media/img/33482_ldementhon_aa377c57-35b0-42c5-8c8e-930bd04c1fd3.png",
      "thumbnail": "https://images.eatthismuch.com/site_media/thmb/33482_ldementhon_aa377c57-35b0-42c5-8c8e-930bd04c1fd3.png"
    },
    {
      "id": 2665,
      "image": "https://images.eatthismuch.com/site_media/img/33482_Mirkatt_572cebe5-c1b7-441e-af28-0530524b3039.png",
      "thumbnail": "https://images.eatthismuch.com/site_media/thmb/33482_Mirkatt_572cebe5-c1b7-441e-af28-0530524b3039.png"
    },
    {
      "id": 7744,
      "image": "https://images.eatthismuch.com/site_media/img/33482_larrystylinson_e7a30dfb-b79e-417a-94ca-bde7a294fb54.png",
      "thumbnail": "https://images.eatthismuch.com/site_media/thmb/33482_larrystylinson_e7a30dfb-b79e-417a-94ca-bde7a294fb54.png"
    },
    {
      "id": 10535,
      "image": "https://images.eatthismuch.com/site_media/img/33482_FoodWorks_0b2e4aa6-9ff6-4d87-9a18-5a594126ed96.png",
      "thumbnail": "https://images.eatthismuch.com/site_media/thmb/33482_FoodWorks_0b2e4aa6-9ff6-4d87-9a18-5a594126ed96.png"
    },
    {
      "id": 10833,
      "image": "https://images.eatthismuch.com/site_media/img/33482_AziyaAlen_5fc51b0a-5f53-4067-bc31-1fb2aaa7db10.png",
      "thumbnail": "https://images.eatthismuch.com/site_media/thmb/33482_AziyaAlen_5fc51b0a-5f53-4067-bc31-1fb2aaa7db10.png"
    },
    {
      "id": 10932,
      "image": "https://images.eatthismuch.com/site_media/img/33482_LuizDGarcia_4de5ff13-1b71-4950-a0e7-d82f3bc502b4.png",
      "thumbnail": "https://images.eatthismuch.com/site_media/thmb/33482_LuizDGarcia_4de5ff13-1b71-4950-a0e7-d82f3bc502b4.png"
    },
    {
      "id": 10933,
      "image": "https://images.eatthismuch.com/site_media/img/33482_LuizDGarcia_e2a6df38-a718-4ab3-bf84-a7c9a6bda253.png",
      "thumbnail": "https://images.eatthismuch.com/site_media/thmb/33482_LuizDGarcia_e2a6df38-a718-4ab3-bf84-a7c9a6bda253.png"
    },
    {
      "id": 13194,
      "image": "https://images.eatthismuch.com/site_media/img/33482_jennmrqz_cdebca3a-ec99-447b-ad97-150d5fc4f03a.png",
      "thumbnail": "https://images.eatthismuch.com/site_media/thmb/33482_jennmrqz_cdebca3a-ec99-447b-ad97-150d5fc4f03a.png"
    },
    {
      "id": 48032,
      "image": "https://images.eatthismuch.com/site_media/img/33482_NarendrasinhChimansinhVadajiya_7c880813-aafa-4d4e-8ac7-850da878c56f.png",
      "thumbnail": "https://images.eatthismuch.com/site_media/thmb/33482_NarendrasinhChimansinhVadajiya_7c880813-aafa-4d4e-8ac7-850da878c56f.png"
    },
    {
      "id": 73768,
      "image": "https://images.eatthismuch.com/site_media/img/33482_%D8%BA%D8%B1%D9%83%D8%B2%D9%85%D8%A7%D9%86%D9%83_d02706f3-e94c-415e-ba9c-bf78dc7e1b9c.png",
      "thumbnail": "https://images.eatthismuch.com/site_media/thmb/33482_%D8%BA%D8%B1%D9%83%D8%B2%D9%85%D8%A7%D9%86%D9%83_d02706f3-e94c-415e-ba9c-bf78dc7e1b9c.png"
    },
    {
      "id": 73769,
      "image": "https://images.eatthismuch.com/site_media/img/33482_%D8%BA%D8%B1%D9%83%D8%B2%D9%85%D8%A7%D9%86%D9%83_ad5fac6b-64a8-4309-9ba3-71e3e5e8dcc0.png",
      "thumbnail": "https://images.eatthismuch.com/site_media/thmb/33482_%D8%BA%D8%B1%D9%83%D8%B2%D9%85%D8%A7%D9%86%D9%83_ad5fac6b-64a8-4309-9ba3-71e3e5e8dcc0.png"
    },
    {
      "id": 160621,
      "image": "https://images.eatthismuch.com/site_media/img/33482_JunidAli_d79d7a2d-d532-4e9a-9072-4f7075105c9b.png",
      "thumbnail": "https://images.eatthismuch.com/site_media/thmb/33482_JunidAli_d79d7a2d-d532-4e9a-9072-4f7075105c9b.png"
    },
    {
      "id": 270080,
      "image": "https://images.eatthismuch.com/site_media/img/33482_tabitharwheeler_6cd5f22c-a4fa-476b-abba-c9c9a42c3c3c.jpg",
      "thumbnail": "https://images.eatthismuch.com/site_media/thmb/33482_tabitharwheeler_6cd5f22c-a4fa-476b-abba-c9c9a42c3c3c.jpg"
    }
  ],
  "ingredients": [
    {
      "amount": 2.0,
      "food": {
        "food_name": "Whole-wheat bread",
        "id": 4025,
        "nutrition": {
          "calories": 70.56,
          "carbs": 11.9,
          "fats": 0.98,
          "proteins": 3.49
        },
        "primary_thumbnail": "https://images.eatthismuch.com/site_media/thmb/4025_erin_m_a7dde43d-5764-4eca-aaab-6446ec28f15e.png"
      },
      "grams": 56.0,
      "preparation": null,
      "units": "slice"
    },
    {
      "amount": 4.0,
      "food": {
        "food_name": "Peanut butter",
        "id": 3594,
        "nutrition": {
          "calories": 188.48,
          "carbs": 6.9,
          "fats": 15.98,
          "proteins": 7.7
        },
        "primary_thumbnail": "https://images.eatthismuch.com/site_media/thmb/3594_ldementhon_05f99dd7-43d4-4f2a-8127-789b8d75ecfc.png"
      },
      "grams": 64.0,
      "preparation": null,
      "units": "tbsp"
    },
    {
      "amount": 2.0,
      "food": {
        "food_name": "Apricot jam",
        "id": 4715,
        "nutrition": {
          "calories": 48.4,
          "carbs": 12.88,
          "fats": 0.04,
          "proteins": 0.14
        },
        "primary_thumbnail": "https://images.eatthismuch.com/site_media/thmb/4715_erin_m_8a36f44a-cae6-4617-987a-f4bacbb45bea.png"
      },
      "grams": 40.0,
      "preparation": null,
      "units": "tbsp"
    }
  ],
  "nutrition": {
    "calories": 614.88,
    "carbs": 63.49,
    "fats": 34.02,
    "proteins": 22.66
  },
  "prep_time": 5,
  "primary_image": "https://images.eatthismuch.com/site_media/img/33482_tabitharwheeler_6cd5f22c-a4fa-476b-abba-c9c9a42c3c3c.jpg",
  "primary_thumbnail": "https://images.eatthismuch.com/site_media/thmb/33482_tabitharwheeler_6cd5f22c-a4fa-476b-abba-c9c9a42c3c3c.jpg",
  "servings": 1,
  "source": "eatthismuch.com",
  "tag_cloud": "gluten Apricot jam Whole-wheat bread Sweets \"Big PB&J Sandwich\" Soy and Legume Products Baked Products Peanut butter"
}
```

*in case of errors*:

1- if food doesn't exist in the database, response code will be **404**

```json
{
  "error": "food not found."
}
```

2- if recipe doesn't exist, response code will be **404**

```json
{
  "error": "recipe not found."
}
```

----------

### `/foods/<int:id>`

method: `GET`

food summarized information

*input*:
URL:

- food id

*sample input*:

```
/foods/33480
```

*output*:

response code will be **200**

- The server successfully processed the request and it's returning food summary in this format.

```json
{
  "id": 33482,
  "category": "sandwich",
  "image": "https://images.eatthismuch.com/site_media/img/33482_tabitharwheeler_6cd5f22c-a4fa-476b-abba-c9c9a42c3c3c.jpg",
  "thumbnail": "https://images.eatthismuch.com/site_media/thmb/33482_tabitharwheeler_6cd5f22c-a4fa-476b-abba-c9c9a42c3c3c.jpg",
  "title": "Big PB&J Sandwich",
  "nutrition": {
      "calories": 615,
      "fat": 34.0,
      "fiber": 8.6,
      "protein": 22.7}
}
```

*in case of errors*:

1- if food doesn't exist in the database, response code will be **404**

```json
{
  "error": "food not found."
}
```

----------

### `/foods/search`

method: `GET`

recipe and foods detailed information

*input*:
GET method parameters:

- query: text to search
- page:pagination page, default value is 1
- page:items per page, default value is 10

*sample input*:

```
/foods/search?query=pasta&page=1&per_page=5
```

*output*:

response code will be **200**

- total results count in the elasticsearch
- food sample view of foods found int the search ordered by relevance

```json
{
        "results": [ "list of simple views.."],
        "total_results_count": "count..."
}
```

*sample output*

```json
{
  "results": [
    {
      "category": "pasta",
      "id": 384279,
      "image": "https://images.eatthismuch.com/site_media/img/384279_erin_m_77a48297-f148-454d-aa02-fdd277e70edf.png", 
      "nutrition": {
        "calories": 476,
        "fat": 8.6,
        "fiber": 1.6,
        "protein": 17.7
      },
      "thumbnail": "https://images.eatthismuch.com/site_media/thmb/384279_erin_m_77a48297-f148-454d-aa02-fdd277e70edf.png", 
      "title": "Pasta, Corn & Artichoke Bowl"
    },
    {
      "category": "pasta",
      "id": 1493432,
      "image": "https://images.eatthismuch.com/site_media/img/1093241_Billie7_1975_f6db1d3f-2bed-4c82-bf10-e343b9dc8314.jpeg", 
      "nutrition": {
        "calories": 591,
        "fat": 15.8,
        "fiber": 4.7,
        "protein": 16.7
      },
      "thumbnail": "https://images.eatthismuch.com/site_media/thmb/1093241_Billie7_1975_f6db1d3f-2bed-4c82-bf10-e343b9dc8314.jpeg", 
      "title": "Spaghetti with Mushrooms, Garlic and Oil"
    },
    {
      "category": "other",
      "id": 907167,
      "image": "https://images.eatthismuch.com/site_media/img/907167_tabitharwheeler_915ad93b-213d-4b3d-bcc2-e0570b833af3.jpg", 
      "nutrition": {
        "calories": 309,
        "fat": 7.2,
        "fiber": 8.6,
        "protein": 16.1
      },
      "thumbnail": "https://images.eatthismuch.com/site_media/thmb/907167_tabitharwheeler_915ad93b-213d-4b3d-bcc2-e0570b833af3.jpg", 
      "title": "Pasta with Red Sauce and Mozzarella"
    },
    {
      "category": "pasta",
      "id": 905979,
      "image": "https://images.eatthismuch.com/site_media/img/905979_tabitharwheeler_82334d46-99b8-428d-aa16-4bdd9c3008cd.jpg", 
      "nutrition": {
        "calories": 423,
        "fat": 12.3,
        "fiber": 4.0,
        "protein": 24.2
      },
      "thumbnail": "https://images.eatthismuch.com/site_media/thmb/905979_tabitharwheeler_82334d46-99b8-428d-aa16-4bdd9c3008cd.jpg", 
      "title": "Spaghetti with Meat Sauce"
    },
    {
      "category": "pasta",
      "id": 45500,
      "image": "https://images.eatthismuch.com/site_media/img/45500_simmyras_43adc56f-d597-4778-a682-4ddfa9f394a3.png", 
      "nutrition": {
        "calories": 285,
        "fat": 18.0,
        "fiber": 0.9,
        "protein": 15.4
      },
      "thumbnail": "https://images.eatthismuch.com/site_media/thmb/45500_simmyras_43adc56f-d597-4778-a682-4ddfa9f394a3.png", 
      "title": "Rigatoni with Brie, Grape Tomatoes, Olives, and Basil"
    }
  ],
  "total_results_count": 1211
}
```

*in case of errors*:

1- if you don't pass query parameter in the url

response code will be **422**

```json
{
            "error": "query should exist in the request"
}
```

2- if per_page value is more than 50

response code will be **422**

```json
{
            "error": "per_page should not be more than 50"
}
```

3- if search is timed out.

status code will be **408**
```json
{
            "error": "search request timed out."
}
```

----------

### `/blog/`

method: `GET`

*input*: **None**

*output*:

response code will be **200**

- return all posts

```json
{
"1": {
    "author_email": "yasi_ommi@yahoo.com",
    "author_fullname": "Ken Adams",
    "category": "category",
    "content": "post content",
    "current_user_mail": "mohammadhossein.malekpour@gmail.com",
    "slug": "some-slug",
    "summary": "post summery",
    "title": "sample post"
  },
  "10": {
    "author_email": "imanmalekian31@gmail.com",
    "author_fullname": "iman123",
    "category": "asd",
    "content": "asd",
    "current_user_mail": "mohammadhossein.malekpour@gmail.com",
    "slug": "asdss",
    "summary": "asdsss",
    "title": "asdss"
  },
  "11": {
    "author_email": "imanmalekian31@gmail.com",
    "author_fullname": "iman123",
    "category": "asd",
    "content": "asdasd",
    "current_user_mail": "mohammadhossein.malekpour@gmail.com",
    "slug": "asdasd",
    "summary": "asdas",
    "title": "asdasd"
  }
}
```

----------

### `/blog/<string:slug>`

method: `GET`

*input*:

pass query parametr in URL

*output*:

response code will be **200**

```json
{
  "author_email": "mohammadhossein.malekpour@gmail.com",
  "author_fullname": "Mohammad Hossein Malekpour",
  "category": "recepie",
  "content": "who konws!",
  "post_id": 2,
  "slug": "avaliwern-post-dailywrdiet",
  "summary": "pooof",
  "title": "How To Get Diet?"
}
```

*in case of errors*:

response code will be **404**

```json
{
  "error": "post not exist!"
}
```

----------

### `/blog/posts/new/`

method: `POST`

*input*:

Authorization Header:

- Bearer \<access token>

Body:

- category
- content
- slug
- summary
- title

```json
{
  "category": "recepie",
  "content": "who konws!",
  "slug": "dovomi-podsasdt-daasdilywrdiet",
  "summary": "pooof",
  "title": "How asdToqwewdasde Get Diet?"
}
```

*output*:

response code will be **200**

```json
{
  "msg": "Post created successfully"
}
```

*in case of errors*:

response code will be **400**

```json
{
  "error": {
    "title": [
      "This field is required."
    ]
  }
}
```

----------

### `/posts/delete/<int:post_id>/`

method: `DELETE`

*input*:

pass query parametr in URL

Authorization Header:

- Bearer \<access token>

*output*:

response code will be **204**

- No content

*in case of errors*:

response code will be **403**

```json
{
  "error": "access denied!"
}
```

----------

### `/blog/posts/user`

method: `GET`

*input*:

Authorization Header:

- Bearer \<access token>

*output*:

response code will be **200**

```json
{
  "2": {
    "author_email": "mohammadhossein.malekpour@gmail.com",
    "author_fullname": "Mohammad Hossein Malekpour",
    "category": "recepie",
    "content": "who konws!",
    "current_user_mail": "mohammadhossein.malekpour@gmail.com",
    "slug": "avaliwern-post-dailywrdiet",
    "summary": "pooof",
    "title": "How To Get Diet?"
  },
  "3": {
    "author_email": "mohammadhossein.malekpour@gmail.com",
    "author_fullname": "Mohammad Hossein Malekpour",
    "category": "recepie",
    "content": "who konws!",
    "current_user_mail": "mohammadhossein.malekpour@gmail.com",
    "slug": "dovomi-post-dailywrdiet",
    "summary": "pooof",
    "title": "How Toqwewe Get Diet?"
  },
  "4": {
    "author_email": "mohammadhossein.malekpour@gmail.com",
    "author_fullname": "Mohammad Hossein Malekpour",
    "category": "recepie",
    "content": "who konws!",
    "current_user_mail": "mohammadhossein.malekpour@gmail.com",
    "slug": "dovomi-post-daasdilywrdiet",
    "summary": "pooof",
    "title": "How Toqwewdasde Get Diet?"
  }
}
```

----------

### `/foods/diets`

method: `GET`

*input*:

GET parameters:

- page
- per_page

Authorization Header:

- Bearer \<access token>

*sample input*:
```
localhost:5000/foods/diets?page=1&per_page=2
```

*output*:

response code will be **200**

*sample output*:
```json
[
  {
    "diet": [
      {
        "category": "breakfast",
        "id": 905755,
        "image": "https://images.eatthismuch.com/site_media/img/905755_Shamarie84_a50c2b94-934f-4326-9af3-0e0f04d7b10f.png",
        "nutrition": {
          "calories": 443,
          "fat": 18.6,
          "fiber": 6.2,
          "protein": 17.9
        },
        "thumbnail": "https://images.eatthismuch.com/site_media/thmb/905755_Shamarie84_a50c2b94-934f-4326-9af3-0e0f04d7b10f.png",
        "title": "Peach Yogurt Parfait"
      },
      {
        "category": "mostly_meat",
        "id": 940743,
        "image": "https://images.eatthismuch.com/site_media/img/325467_simmyras_cbf011a4-a8ef-4fac-b4bc-bcdd1f8770d4.png",
        "nutrition": {
          "calories": 1633,
          "fat": 84.7,
          "fiber": 8.8,
          "protein": 112.4
        },
        "thumbnail": "https://images.eatthismuch.com/site_media/thmb/325467_simmyras_cbf011a4-a8ef-4fac-b4bc-bcdd1f8770d4.png",
        "title": "Ham and Cheese Chicken Roll-ups"
      },
      {
        "category": "breakfast",
        "id": 983905,
        "image": "https://images.eatthismuch.com/site_media/img/233507_ashleigh_c_hughes_9eab40e4-c8ad-488f-a381-f6e9342ed72d.png",
        "nutrition": {
          "calories": 214,
          "fat": 18.7,
          "fiber": 1.4,
          "protein": 9.3
        },
        "thumbnail": "https://images.eatthismuch.com/site_media/thmb/233507_ashleigh_c_hughes_9eab40e4-c8ad-488f-a381-f6e9342ed72d.png",
        "title": "Eggs & Greens"
      }
    ],
    "time": "Fri, 12 Jun 2020 13:56:25 GMT"
  }
]
```

in case of errors:

- Logged in user is `NULL`

*output*:

response code will be **404**

```json
{
       "error": "user not found"
}
```

------------

### `/foods/search/ingredient`
text-search between ingredients in order to choose some of them to include in a recipe.
(but it's not excluded to this)

method: `GET`

*input*:
GET method parameters:

- query: text to search
- page:pagination page, default value is 1
- page:items per page, default value is 10

*sample input*:

```
/foods/search/ingredient?query=Mango
```

*output*:

response code will be **200**

- total results count in the elasticsearch
- ingredients info ordered by relevance

```json
{
        "results": [ "list of simple views.."],
        "total_results_count": "count..."
}
```

*sample output*:

```json
{
  "results": [
    {
      "food_name": "Frozen Mango", 
      "id": 163245, 
      "nutrition": {
        "calories": 70.0, 
        "carbs": 19.0, 
        "fats": 0.0, 
        "proteins": 1.0
      }, 
      "primary_thumbnail": "https://images.eatthismuch.com/site_media/thmb/163245_simmyras_81adf045-0657-4bd9-8603-af3740b0e540.png"
    }, 
    {
      "food_name": "Mango Chutney", 
      "id": 448267, 
      "nutrition": {
        "calories": 25.0, 
        "carbs": 7.0, 
        "fats": 0.0, 
        "proteins": 0.0
      }, 
      "primary_thumbnail": "https://images.eatthismuch.com/site_media/thmb/448267_RedHawk5_6af04abe-c233-4908-83ed-6891e6306fc6.png"
    }, 
    {
      "food_name": "Mango Juice", 
      "id": 85585, 
      "nutrition": {
        "calories": 30.0, 
        "carbs": 7.0, 
        "fats": 0.0, 
        "proteins": 0.0
      }, 
      "primary_thumbnail": "https://img.icons8.com/color/2x/grocery-bag.png"
    }
  ], 
  "total_results_count": 3
}
```


*in case of errors*:

1- if you don't pass query parameter in the url

response code will be **422**

```json
{
            "error": "query should exist in the request"
}
```

2- if per_page value is more than 50

response code will be **422**

```json
{
            "error": "per_page should not be more than 50"
}
```

3- if search is timed out.

status code will be **408**
```json
{
            "error": "search request timed out."
}
```

---------

### `/foods/search`
advanced search in foods

method: `POST`

*input*:

```json
{
            "text": "text_to_search",
            "category" : "one of [mostly_meat, appetizers,drink,main_dish,sandwich,dessert,breakfast,protein_shake,salad,pasta,other]" ,
            "ingredients": ["list of ingredient ids"],
            "calories":{
                "min":"optional",
                "max":"optional"
            },
            "carbs": {
                "min":"optional",
                "max":"optional"
            } , 
            "fats":  {
                "min":"optional",
                "max":"optional"
            },
            "proteins": {
                "min":"optional",
                "max":"optional"
            } , 
            "cook_time":{
                "min":"optional",
                "max":"optional"
            }  ,
            "prep_time": {
                "min":"optional",
                "max":"optional"
            } , 
            "total_time": {
                "min":"optional",
                "max":"optional"
            }, 
            "page": "pagination page number (default is 1)" ,
            "per_page": "pagination per_page count (default is 10)"
}
```
*output*:
response code will be **200**

- total results count in the elasticsearch
- food sample view of foods found int the search ordered by relevance

```json
{
        "results": [ "list of simple views.."],
        "total_results_count": "count..."
}
```
*in case of errors*:

1- if you don't pass query parameter in the url

response code will be **422**

```json
{
            "error": "some query should exist in the request"
}
```

2- if per_page value is more than 50

response code will be **422**

```json
{
            "error": "per_page should not be more than 50"
}
```

3- if search is timed out.

status code will be **408**
```json
{
            "error": "search request timed out."
}
```

*sample input 1*:
```json
{
	"text":"avocado",
	"calories":{
		"min":200
	},
	"cook_time":{
		"min":20,
		"max":30
	}
}
```

*sample output 1*:
```json
{
    "results": [
        {
            "category": "breakfast",
            "id": 906721,
            "image": "https://images.eatthismuch.com/site_media/img/270860_mensuramjr_cd47fe9f-edb6-42cd-bcb0-766f8eaa3914.png",
            "nutrition": {
                "calories": 393,
                "fat": 34.2,
                "fiber": 13.5,
                "protein": 10.3
            },
            "thumbnail": "https://images.eatthismuch.com/site_media/thmb/270860_mensuramjr_cd47fe9f-edb6-42cd-bcb0-766f8eaa3914.png",
            "title": "Avocado Egg Bake"
        },
        {
            "category": "pasta",
            "id": 1015979,
            "image": "https://img.icons8.com/color/7x/spaghetti.png",
            "nutrition": {
                "calories": 935,
                "fat": 41.7,
                "fiber": 9.7,
                "protein": 49.5
            },
            "thumbnail": "https://img.icons8.com/color/2x/spaghetti.png",
            "title": "Creamy Chicken Avocado Pasta"
        },
        {
            "category": "sandwich",
            "id": 906763,
            "image": "https://images.eatthismuch.com/site_media/img/906763_JoseBaltazar_b00f5694-fd97-4f90-bc91-290a5d72257d.jpg",
            "nutrition": {
                "calories": 675,
                "fat": 36.1,
                "fiber": 16.9,
                "protein": 50.8
            },
            "thumbnail": "https://images.eatthismuch.com/site_media/thmb/906763_JoseBaltazar_b00f5694-fd97-4f90-bc91-290a5d72257d.jpg",
            "title": "Chicken and Avocado Sandwich"
        },
        {
            "category": "mostly_meat",
            "id": 905623,
            "image": "https://images.eatthismuch.com/site_media/img/264808_tharwood_e5e0c43d-bbf4-4006-875f-a0e48fef3302.png",
            "nutrition": {
                "calories": 260,
                "fat": 18.1,
                "fiber": 3.4,
                "protein": 19.5
            },
            "thumbnail": "https://images.eatthismuch.com/site_media/thmb/264808_tharwood_e5e0c43d-bbf4-4006-875f-a0e48fef3302.png",
            "title": "Ham, Egg, and Cheese Cupcake"
        },
        {
            "category": "sandwich",
            "id": 211831,
            "image": "https://images.eatthismuch.com/site_media/img/211831_ZenKari_967deee5-b5c2-4cf1-8544-9ff7757b0931.png",
            "nutrition": {
                "calories": 1184,
                "fat": 54.3,
                "fiber": 29,
                "protein": 33.6
            },
            "thumbnail": "https://images.eatthismuch.com/site_media/thmb/211831_ZenKari_967deee5-b5c2-4cf1-8544-9ff7757b0931.png",
            "title": "Nutribullet Portabella Burgers"
        }
    ],
    "total_results_count": 10
}
```

*sample input 2*:
```json
{
	"text":"avocado"
}
```

*sample output 2*:
```json
{
    "results": [
        {
            "category": "other",
            "id": 390740,
            "image": "https://images.eatthismuch.com/site_media/img/390740_erin_m_11094712-ba5d-4c9b-b0ad-278907f8d1e5.png",
            "nutrition": {
                "calories": 541,
                "fat": 42.2,
                "fiber": 13.9,
                "protein": 26.1
            },
            "thumbnail": "https://images.eatthismuch.com/site_media/thmb/390740_erin_m_11094712-ba5d-4c9b-b0ad-278907f8d1e5.png",
            "title": "Baked Seafood Stuffed Avocados"
        },
        {
            "category": "main_dish",
            "id": 943329,
            "image": "https://images.eatthismuch.com/site_media/img/331372_bbebber_dacfd09e-5d58-4e24-bdeb-1dc6ce82b16c.png",
            "nutrition": {
                "calories": 145,
                "fat": 10.8,
                "fiber": 6.8,
                "protein": 2.1
            },
            "thumbnail": "https://images.eatthismuch.com/site_media/thmb/331372_bbebber_dacfd09e-5d58-4e24-bdeb-1dc6ce82b16c.png",
            "title": "Strawberry Salsa Stuffed Avocados"
        }
    ],
    "total_results_count": 418
}
```

*sample input 3*:
```json
{
	"ingredients":[4914 ,2057,2042]
}
```

*sample output 3*:
found foods contain all the ingredients that we have given ids.
```json
{
    "results": [
        {
            "category": "pasta",
            "id": 57154,
            "image": "https://img.icons8.com/color/7x/spaghetti.png",
            "nutrition": {
                "calories": 2701,
                "fat": 69.7,
                "fiber": 39.3,
                "protein": 102.8
            },
            "thumbnail": "https://img.icons8.com/color/2x/spaghetti.png",
            "title": "Pasta Puttanesca"
        }
    ],
    "total_results_count": 1
}
```