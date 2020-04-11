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

*in case of errors*: response code will be **400**

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

*in case of errors*: response code will be **400**

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
