# Installation
1. pip install -f requirements.txt
2. ./manage.py migrate
3. ./manage.py createsuperuser
4. ./manage.py runserver

# sample cURL request
```
curl --location --request POST --user admin:password 'http://127.0.0.1:8000/api/v1/calculateDeliveryFee' \
--header 'Accept: application/json; indent=4' \
--form 'cart_value="1"' \
--form 'delivery_distance="2"' \
--form 'number_of_items="3"' \
--form 'time="2021-01-16T13:00:00Z"'
```