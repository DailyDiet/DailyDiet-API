#Daily diet api documentation

##v1.0

### `/calculate/bmi`
method: `POST`

*input*: 
- height in centimiters
- weight in kilograms
```json
{
	"height":180,  
	"weight":80
}
```

*output*:
- `bmi_value` rounded up to 2 decimal points
- `bmi_status` one of **Underweight**, **Normal weight**, **Overweight** and **Obesity**
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
            "This field is required."
        ]
    }
}
```
