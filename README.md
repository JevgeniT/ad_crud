## Quick Start 

```
# Install pip
$ python get-pip.py

# Install dependencies
$ python -m pip install -r requirements.txt

# Create DB
$ python
>> from app import db
>> db.create_all()
>> exit()

# Run Server (http://localhost:5000)
$ python start.py
```

## Endpoints

### Product
* GET     /product
* GET     /product/:id
* POST    /product
* PUT     /product/:id
* DELETE  /product/:id

### Category
* GET     /category
* GET     /category/:id
* POST    /category
* PUT     /category/:id
* DELETE  /category/:id

```json

# category POST PUT 
{ "category":"category_name"}


# product POST PUT
{ "product" : "product_name","category": 1}
```
