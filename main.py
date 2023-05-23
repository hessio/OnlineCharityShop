# main.py

from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
import os
from dotenv import load_dotenv
from square.client import Client
import uuid
import random
import time
import square
import flask

# Load environment variables from .env file
load_dotenv()

# Square API credentials
access_token = os.getenv('ACCESS_TOKEN') 
location_id = os.getenv('LOCATION_ID')

# Square API client object
square_client = Client(
    access_token=access_token,
    environment='sandbox'
)


main = Blueprint('main', __name__)


def attach_image(item_id, image_file):
    print(item_id, image_file)
    result = square_client.catalog.create_catalog_image(
        request = {
            "idempotency_key": str(uuid.uuid4()),#"2b43f799-ec35-467c-8283-bc0c9f36545e",
            # "file": str(f_stream),
            "object_id": item_id,
            "image": {
                "type": "IMAGE",
                "id": "#15",
                "image_data": {
                    "name": "testt",
                    "caption": "test"
                }
            }
        },
        image_file=image_file
    )
    print(result.body)
    return result.body['image']['id']


# Create an item in the Square catalog
def create_item(item_data):
    #print(item_data)
    try:
        # Use the Catalog API to create the item
        catalog_api = square_client.catalog
        #print(catalog_api)
        response = catalog_api.upsert_catalog_object(body=item_data)

        print('thihs the response ', str(response))
        # Return the item ID if successful
        if response.is_success():
            print(response.body)
            item_id = response.body['id_mappings'][0]['object_id']
            print(item_id)
            return item_id
        else:
            return None

    except Exception as e:
        print(e)
        return None


items = {"item1": {"Name": "toy1", "Price": "30", "Description": "This is a toy I had in my family for 3 generations and has served us well"},
"item2": {"Name": "toy2", "Price": "34", "Description": "This is a fun toy I had in my family for 5 yeasrs and has served us well"},
"item3": {"Name": "toy3", "Price": "35", "Description": "This had in my family and has served us well you're welcome eat shit"},
"item4": {"Name": "toy4", "Price": "36", "Description": "I had in my family has served us well"},
"item5": {"Name": "toy5", "Price": "37", "Description": "This us well"},
"item5": {"Name": "toy6", "Price": "38", "Description": "Change my mind"},
}

'''
# Create a route for creating an item
#@app.route('/create_marketplace_item', methods=['POST'])
def create_marketplace_item():
    # Parse request data

    item_data = {
        "idempotency_key": str(uuid.uuid4()),
        "object": {
        "type": "ITEM",
        "id": "#111",
        "item_data": {
          "name": "fuckinghellhatethisapi",
          "available_online": False,
          "available_for_pickup": True,
          "available_electronically": False,
          "variations": [
            {
              "type": "ITEM_VARIATION",
              "id": "#13131",
              "version": 11,
              "is_deleted": False,
              "item_data": {
                "name": "killmenow",
                "available_online": False,
                "available_for_pickup": True,
                "available_electronically": False
            },
              "item_variation_data": {
                "pricing_type": "FIXED_PRICING",
                "price_money": {
                  "amount": 100,
                  "currency": "EUR"
                },
                "track_inventory": True,
                "available_for_booking": False,
                "sellable": True,
                "stockable": False
              }
            }
          ]
        }
      }
    }

    # Create the item in the Square catalog
    item_id = create_item(item_data)

    # Return the item ID or an error message
    if item_id:
        return jsonify({"item_id": item_id}), 201
    else:
        return jsonify({"error": "Failed to create item"}), 500
'''

@main.route('/')
def index():
    #print('what the fuck')
    return render_template('index.html')

@main.route('/profile')
@login_required
def profile():
    #print(current_user.first_name)
    return render_template('profile.html', name=current_user.first_name)

@main.route('/post_ad', methods=['GET', 'POST'])
@login_required
def post_ad():
    if request.method == 'POST':
        title = request.form['title']
        price = request.form['price']
        desc = request.form['description']
        image = request.files['image']
        cwd = os.getcwd()
        print(cwd)
        image.save('project/uploads/' + image.filename)

        item_data = {
            "idempotency_key": str(uuid.uuid4()),
            "object": {
            "type": "ITEM",
            "id": "#111",
            "item_data": {
              "name": title,
              "available_online": False,
              "available_for_pickup": True,
              "available_electronically": False,
              "variations": [
                {
                  "type": "ITEM_VARIATION",
                  "id": "#"+str(random.randint(0, 9999)),
                  "version": 11,
                  "is_deleted": False,
                  "item_data": {
                    "name": title,
                    "available_online": False,
                    "available_for_pickup": True,
                    "available_electronically": False
                },
                  "item_variation_data": {
                    "pricing_type": "FIXED_PRICING",
                    "price_money": {
                      "amount": int(price),
                      "currency": "EUR"
                    },
                    "track_inventory": True,
                    "available_for_booking": False,
                    "sellable": True,
                    "stockable": False
                  }
                }
              ]
            }
          }
        }

        # Create the item in the Square catalog
        item_id = create_item(item_data)

        # print(item_id)

        # file_to_upload_path =  #"image_example_1.png" # Modify this to point to your desired file.
        f_stream = open('project/uploads/' + image.filename, "rb")
        print('project/uploads/' + image.filename)

        attach_image(item_id, f_stream)

        # # Return the item ID or an error message
        # if item_id:
        #     return jsonify({"item_id": item_id}), 201
        # else:
        #     return jsonify({"error": "Failed to create item"}), 500
    
    return render_template('post_ad.html')

@main.route('/create_order', methods=['POST', 'GET'])
def create_order():
    
    item_id = request.form.get('button_value')
    
    response = square_client.orders.create_order(
      body = {
        "order": {
          "location_id": location_id,
          "line_items": [
            {
              "quantity": "1",
              "catalog_object_id": item_id
            }
          ]
        },
        "idempotency_key": str(uuid.uuid4())
      }
    )
    price = "{:0.2f}".format(round((float(response.body['order']['line_items'][0]['base_price_money']['amount'])/100), 2))

    order_id = response.body['order']['id']
    # print('create order response: ', response.body)

    return render_template('payments.html', order_id=order_id, price=price)
    # if response.is_success():
    #     print(';;;;;;')
    #     # Return the payment status and id
    #     return flask.jsonify({
    #       'money': response.body['order']['line_items'][0]['base_price_money']['amount'],
    #       # 'payment_id': response.body['payment']['id']
    #     })
    # elif response.is_error():
    #     # Return the error message
    #     return flask.jsonify({
    #       'error': response.errors[0]['detail']
    #     })

    # time.sleep(1000)
    # return redirect(url_for('main.new_page')) #, price=price))

@main.route('/new_page', methods=['POST', 'GET'])
def new_page():
    data = request
    # print('this is the request: ' , data)
    return render_template('payments.html')

# Define a route to process the payment
@main.route('/payment', methods=['POST'])
def process_payment():
  # Get the nonce from the request body

  request_body = flask.request.get_json()
  nonce = request_body.get('sourceId')
  print('request body', request_body, '    ', nonce)

  result = square_client.orders.retrieve_order(
    order_id = request_body.get('order_id')
  )

  price = result.body['order']['line_items'][0]['base_price_money']['amount']
  print('this is hte order result', result.body['order']['line_items'][0]['base_price_money']['amount'])

  # Create a payment request with the nonce and amount
  payment_request = {
    'source_id': nonce,
    'amount_money': {
      'amount': price, # $1.00 charge
      'currency': 'EUR'
    },
    'idempotency_key': nonce # Use nonce as idempotency key
  }

  # Call the Payments API to create a payment
  response = square_client.payments.create_payment(payment_request)

  print(response)

  # Check if the payment was successful
  if response.is_success():
    # Return the payment status and id
    return flask.jsonify({
      'status': response.body['payment']['status'],
      'payment_id': response.body['payment']['id']
    })
  elif response.is_error():
    # Return the error message
    return flask.jsonify({
      'error': response.errors[0]['detail']
    })

@main.route('/completed_purchase', methods=["POST", "GET"])
def completed_purchase():
    # time.sleep(1000)
    print(request)
    return render_template('completed_purchase.html')

@main.route('/marketplace')
@login_required
def marketplace():

    result = square_client.catalog.search_catalog_objects(
      body = {
        "include_related_objects": True
      }
    )
    response = result.body['objects']
    related = result.body['related_objects']
    
    new_items = {}
    count = 0
    desc = ''
    image=''
    item_id=''
    
    for item in response:
        # print(item['item_data']['variations'][0]['id'])

        try:
            item_id = item['item_data']['variations'][0]['id']

        except:
            item_id='None'

        try:

            print('test', item['item_data']['image_ids'])
            image = related[0]['image_data']['url']

        except:
            image = '/static/placeholder.png'
            #print(item['id'])

        try:
            #print('Description: ', item['item_data']['description_plaintext'])
            desc=item['item_data']['description_plaintext']
        except:
            desc=''
            #print('no desc')
        #print('\n\n')
        # print(image)
        new_items['item'+str(count)] = {'Name': item['item_data']['name'], 
        'Price': item['item_data']['variations'][0]['item_variation_data']['price_money']['amount'],
        'Description': desc,
        'Image': image,
        'id': item_id
        }
        count += 1
    #print(new_items)

    return render_template('marketplace.html', items=new_items)
