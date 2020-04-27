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

- access_token
- refresh_token

```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1ODc5ODI1OTgsIm5iZiI6MTU4Nzk4MjU5OCwianRpIjoiZGRjOTJmMjMtMGUwZS00ZGYxLWIzMTgtYjdiM2NlNmYyZTMyIiwiZXhwIjoxNTg3OTgzNDk4LCJpZGVudGl0eSI6Im1vaGFtbWFkaG9zc2Vpbi5tYWxla3BvdXJAZ21haWwuY29tIiwiZnJlc2giOnRydWUsInR5cGUiOiJhY2Nlc3MifQ.MQey2So6HvQyO6HH9yWJjbb0-EgoUPVvFofo8B0mhPw",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1ODc5ODI1OTgsIm5iZiI6MTU4Nzk4MjU5OCwianRpIjoiMjA0NTYwNjktZDMwZi00NjM5LWJkZTktYThkMWNjYmIzN2I4IiwiZXhwIjoxNTkwNTc0NTk4LCJpZGVudGl0eSI6Im1vaGFtbWFkaG9zc2Vpbi5tYWxla3BvdXJAZ21haWwuY29tIiwidHlwZSI6InJlZnJlc2gifQ.IdMv78GnD4vUH6BlgdzPYPFw_04Hz7M150LqRv4drXc"
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

1- response code will be **400**

```json
{
  "errors": {
    "confirm_password": [
      "passwords must match"
    ],
    "new_password": [
      "Field must be between 6 and 25 characters long."
    ]
  }
}
```

2- response code will be **401**

```json
{
  "msg": "Token has expired"
}
```

3- response code will be **403**

```json
{
  "error": "Old password does not match."
}
```

4- response code will be **422**

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
