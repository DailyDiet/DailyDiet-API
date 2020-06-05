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
        "results": [ "list views.."],
        "total_results_count": "count..."
}
```

*sample input*

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

----------

### `/blog/`

method: `GET`

*input*: **NONE**

*output*:

response code will be **200**

- return all posts

```json
{
  "1": {
    "category": null,
    "content": "I don't know :)\r\ncheck flask doc!",
    "slug": "how-to-use-flask",
    "summary": "",
    "title": "How To Use Flask?"
  },
  "2": {
    "category": "recepie",
    "content": "who konws!",
    "slug": "avalin-post-dailydiet",
    "summary": "pooof",
    "title": "How To Get Diet?"
  }
}
```

----------
