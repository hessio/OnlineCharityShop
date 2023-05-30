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
import openai

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

openai.api_key = os.getenv("OPEN_AI_KEY")


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

    try:
        # Use the Catalog API to create the item
        catalog_api = square_client.catalog

        response = catalog_api.upsert_catalog_object(body=item_data)

        # Return the item ID if successful
        if response.is_success():
            # print(response.body)
            item_id = response.body['id_mappings'][0]['object_id']
            print(item_id)
            return item_id
        else:
            return None

    except Exception as e:
        print(e)
        return None

@main.route('/')
def index():
    #print('what the fuck')
    return render_template('index.html')

@main.route('/profile')
@login_required
def profile():
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
              ],
              "description_html": desc,
            }
          }
        }

        # Create the item in the Square catalog
        item_id = create_item(item_data)

        f_stream = open('project/uploads/' + image.filename, "rb")
        print('project/uploads/' + image.filename)

        attach_image(item_id, f_stream)
        print(current_user.id)
        # attach_user(current_user.)
    
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
    price = "{:0.2f}".format(round((float(response.body['order']['line_items'][0]['base_price_money']['amount'])), 2))

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
      'amount': price,
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


# Define a route to process the payment
@main.route('/get_details', methods=['POST'])
def process_user_details():

  request_body = flask.request.get_json()
  # order_id = request_body.get('order_id')
  
  cust_result = square_client.customers.retrieve_customer(
    customer_id = current_user.square_cust_id,
  )

  order_result = square_client.orders.retrieve_order(
    order_id = request_body.get('order_id')
  )

  print('order result: ', order_result.body['order']['line_items'][0]['base_price_money']['amount'])

  print('this is hte order result', cust_result.body['customer']['address'])

  address = [cust_result.body['customer']['address']['address_line_1'], cust_result.body['customer']['address']['address_line_2']]
  return flask.jsonify({
        'amount': str(order_result.body['order']['line_items'][0]['base_price_money']['amount']),
        'billingContact': {
            'addressLines': address,
            'familyName': cust_result.body['customer']['given_name'],
            'givenName': cust_result.body['customer']['family_name'],
            'email': cust_result.body['customer']['email_address'],
            'country': 'IE',
            'phone': cust_result.body['customer']['phone_number'],
            'region': 'DUB',
            'city': 'Dublin',
        },
        'currencyCode': 'EUR',
        'intent': 'CHARGE',
    })

@main.route('/completed_purchase', methods=["POST", "GET"])
def completed_purchase():
    # time.sleep(1000)
    print(request)
    return render_template('completed_purchase.html')

@main.route('/ai_update', methods=['POST'])
def process_openai_request():
    try:
        message = request.json['message']

        ai_prompt = 'You are a an AI language model and I want you to rewrite this description for me to make the item I am selling more appealing to potential buyers here is the description: "' + message + '"'
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": ai_prompt}]
        )
        response = completion.choices[0].message

        return flask.jsonify({'response': response})
    except Exception as e:
        print(e)
        return flask.jsonify({'error': 'An error occurred'}), 500

@main.route('/marketplace')
@login_required
def marketplace():

    result = square_client.catalog.search_catalog_objects(
      body = {
        "include_related_objects": True,
        "include_deleted_objects": False,
      }
    )
    response = result.body['objects']
    related = result.body['related_objects']
    
    new_items = {}
    count = 0
    desc = ''
    image=''
    item_id=''
    price_money = ''

    print(related)
    
    for item in response:

        try:
            item_id = item['item_data']['variations'][0]['id']

        except:
            item_id='None'

        try:
            print('test', item['item_data']['image_ids'])
            for rel in related:
                if rel['id'] == item['item_data']['image_ids'][0]:
                    image = rel['image_data']['url']

        except:
            image = '/static/placeholder.png'
            #print(item['id'])

        try:
            print('price test', item['item_data']['variations'][0]['item_variation_data']['price_money']['amount'])
            price_money = item['item_data']['variations'][0]['item_variation_data']['price_money']['amount']

        except:
            price_money = ''

        try:
            print('Description: ', item['item_data']['description_plaintext'])
            desc=item['item_data']['description_plaintext']
        except:
            desc=''

        print(image)
        new_items['item'+str(count)] = {'Name': item['item_data']['name'], 
        'Price': price_money, #item['item_data']['variations'][0]['item_variation_data']['price_money']['amount'],
        'Description': desc,
        'Image': image,
        'id': item_id
        }
        count += 1
    

    return render_template('marketplace.html', items=new_items)
