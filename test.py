import requests
import json
import random
from bs4 import BeautifulSoup
from uuid import uuid4
import csv
from random import uniform
from config import USER_CREDENTIALS

class Test(object):

    """
    Base class for page objects.
    """

    def __init__(self):
        """
        Initialize the Task set.
        """
        super(Test, self).__init__()
        self.session = requests.Session()
        self.hostname = "https://test.cheetay.pk/"

    def _check_page_response(self, response, response_string):
        """
        Check whether a response was successful.
        """
        if response.status_code != 200:
            raise Exception(
                'API request failed with following error code: ' +
                str(response.status_code)
            )

        page_response = response.text
        try:
            assert response_string in page_response
        except:
            raise Exception("Page response is not correct")

    def get_cheetay(self):
        url= self.hostname
        cookies= self.session.get(url).cookies

        auth_data = {
            'csrftoken': cookies['csrftoken'],
            'basketid': cookies['basket_id'],
            'sessionid': cookies['sessionid']
        }
        return auth_data


    def login(self, user):
        """
        Authenticate the user.
        :param username: The user's username.
        :param password: The user's password.
        """
        url = self.hostname
        self.session.get(url)
        csrf = self.session.cookies['csrftoken']
        basketid = self.session.cookies['basket_id']
        sessionid = self.session.cookies['sessionid']


        post_url = self.hostname  + "v3/oscarapi/login/"

        # import pdb; pdb.set_trace()
        params = {
            "username": user,
            "password": "cheetay"
            }
        headers = {
            'Server': 'nginx/1.4.6 (Ubuntu)',
            'Date': 'Thu, 28 Oct 2019 09:32:18 GMT',
            'Content-Type': 'application/json',
            'Vary': 'Accept, Cookie',
            'Connection': 'keep-alive',
            'X-Frame-Options': 'SAMEORIGIN',
            'Allow': 'GET, POST, DELETE, HEAD, OPTIONS',
            'Set-Cookies': 'session_id={}; expires=Thu, 22-Oct-2020 09:32:18 GMT; Max-Age=31449600; Path=/'.format(sessionid),
            'Set-Cookies': 'csrftoken={}; expires=Thu, 05-Dec-2019 09:32:18 GMT; httponly; Max-Age=3628800; Path=/'.format(csrf),
            'Set-Cookies': 'basket_id={}; Path=/'.format(basketid)
        }
        response = self.session.post(post_url, data=json.dumps(params), headers=headers)
        return response

    def search_partners(self):
        post_url = self.hostname+ 'v3/oscarapi/search/'

        params = {
            "area_id": 262,
            "city_id": 1,
            "area_name": "Thokar Niaz Beg",
            "page_size":20,
            "page":1,
            "food_query":"",
            "cuisines_filter":"",
            "sort_query":1
        }

        headers = {
            'Server': 'nginx/1.4.6 (Ubuntu)',
            'Date': 'Thu, 28 Oct 2019 09:32:18 GMT',
            'Content-Type': 'application/json',
            'Referer': 'https://test.cheetay.pk/',
            'Vary': 'Accept, Cookie',
            'Connection': 'keep-alive',
            'X-Frame-Options': 'SAMEORIGIN',
            'Allow': 'GET, POST, DELETE, HEAD, OPTIONS',
            'X-CSRFToken': self.session.cookies['csrftoken'],
            'Set-Cookies': 'basket_id={}; Path=/'.format(self.session.cookies['basket_id'])
        }
        response = self.session.post(post_url, data=json.dumps(params), headers=headers)
        print (response.text)

        partners = response.json()['data']['partners']
        total_partners = len(partners)

        random_partner = partners[random.randint(0,total_partners)]
        partner_code = random_partner['code']
        print (partner_code)

        url = self.hostname + 'v3/oscarapi/restaurants/{}?area_id=262'.format(partner_code)
        res = self.session.get(url)

        products = res.json()['data']['products'][0]['products']
        products_length = len(products)

        # import pdb;
        # pdb.set_trace()
        single_random_product = products[random.randint(0, products_length)]
        product_id = single_random_product['id']
        basket_url = self.hostname + 'v3/oscarapi/basket/add-product/?multi_vender=true&area_id=262'

        params_basket = {
            "url": "/oscarapi/products/{}/".format(product_id),
            "quantity": 1,
            "instructions": ""
        }

        basket_response = self.session.post(basket_url,data=json.dumps(params_basket), headers=headers )
        print  (basket_response.text)
        # import pdb;
        # pdb.set_trace()
        return res

    def checkout(self):
        url = self.hostname + 'v2/oscarapi/checkout/'
        headers = {
            'Server': 'nginx/1.4.6 (Ubuntu)',
            'Date': 'Thu, 28 Oct 2019 09:32:18 GMT',
            'Content-Type': 'application/json',
            'Vary': 'Accept, Cookie',
            'Connection': 'keep-alive',
            'X-Frame-Options': 'SAMEORIGIN',
            'Allow': 'GET, POST, DELETE, HEAD, OPTIONS',
            'X-CSRFToken': self.session.cookies['csrftoken'],
            # 'Set-Cookies': 'basket_id={}; Path=/'.format(self.session.cookies['basket_id'])
        }

        params = {
            "basket":"/oscarapi/baskets/{}/".format(self.session.cookies['basket_id']),
            "delivery_type":"economy",
            "address_id": 209274,
            "extras":"nothing",
            "tip": 0,
            "shipping_address":{
                "country":"/oscarapi/countries/PK/",
                "phone_number":"",
                "first_name": "Abdul",
                "last_name": "Azeem",
                "line1": "Thokar Niaz Beg",
                "line2": "",
                "line3": "",
                "line4": "Karachi"
            },
            "source":"Android-App",
            "category":"food",
            "payment_method":"COD",
            "order_instructions":""
        }

        re = self.session.post(url, data=json.dumps(params), headers=headers)
        return re

    def signup(self):
        url = self.hostname
        r = self.session.get(url)
        soup = BeautifulSoup(r.text)
        token = soup.find('input', {'name': 'csrfmiddlewaretoken'})['value']
        # print token
        # import pdb; pdb.set_trace()
        csrf = r.cookies['csrftoken']
        # print csrf
        # import pdb; pdb.set_trace()
        # basketid = self.session.cookies['basket_id']
        # sessionid = self.session.cookies['sessionid']

        post_url = self.hostname + 'accounts/login/'
        headers = {
            'Host': 'test.cheetay.pk',
            'Origin': 'https://test.cheetay.pk',
            'Referer': 'https://test.cheetay.pk/',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Connection': 'keep-alive',
            'X-Frame-Options': 'SAMEORIGIN',
            'Accept': '*/*',
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': csrf,
            # 'Cookie': 'sessionid={0}; csrftoken={1}; basket_id={2}'.format(
            #     sessionid, csrf, basketid),

        }
        random_ = uuid4().hex[0:10]
        email = 'chetay_lt_{}@nowhere.com'.format(random_)
        print(email)
        params = {
            'csrfmiddlewaretoken': token,
            'registration-first_name': 'first_name',
            'registration-last_name': 'second_name',
            'registration-email': email,
            'registration-phone_number': '+92322{}'.format(random.randint(1000000, 4000000)),
            'registration-password1': 'cheetay',
            'registration-password2': 'cheetay',
            'referral-user-code': '',
            'registration_submit': '1'
        }
        re = self.session.post(post_url, data=params, headers=headers)
        # if re == 200:
        self._check_page_response(re, '"status": true')


        # import pdb; pdb.set_trace()

        # return re.text
        # return [email, re, token]

    def add_address(self):
        url = self.hostname + 'v3/oscarapi/address/add/'
        x, y = uniform(-180, 180), uniform(-90, 90)
        tok = self.session.cookies['csrftoken']

        params = {
            'latitude': random.randint(11, 60),
            'longitude': random.randint(60, 99),
            "line1" : "Dummy detail Address from the user",
            "label": "Home",

        }

        headers = {
            'Content-Type': 'application/json',
            'X-CSRFToken': tok,
            'Server': 'nginx/1.4.6 (Ubuntu)',
            # 'Host': 'beta.cheetay.pk',
            # 'Origin': 'https://beta.cheetay.pk',
            'Referer': 'https://test.cheetay.pk',
            # 'Vary': 'Accept, Cookie',
            # 'Connection': 'keep-alive',
            # 'X-Frame-Options': 'SAMEORIGIN',
            # 'Allow': 'POST, OPTIONS',
            # 'X-CSRFToken': tok,
            # 'X-Requested-With': 'XMLHttpRequest',
            # 'sessionid': self.session.cookies['sessionid'],
            # 'Cookie': 'csrftoken={0}; sessionid={1}; city_name=Lahore; city_id=1;'.format(tok, self.session.cookies['sessionid']),
            'Set-Cookie': 'basket_id={}; Path=/'.format(self.session.cookies['basket_id']),
            # 'Set-Cookie': 'sessionid={}; Path=/'.format(self.session.cookies['sessionid'])
        }

        res = self.session.post(url, headers=headers, data=json.dumps(params))
        return res

    def get_user_addresses(self):
        ur1l = 'https://test.cheetay.pk/accounts/profile/?active=saved-addresses#'
        print (self.session.get(ur1l))

        url = self.hostname + 'v2/address/user-addresses/'
        header = {
            'Set-Cookies': 'basket_id={}; Path=/'.format(self.session.cookies['basket_id'])
        }
        r =self.session.get(url, headers=header)
        return r

    def search_partner1s(self):
        post_url = self.hostname + 'v3/oscarapi/search/'

        params = {
            "area_id": 262,
            "city_id": 1,
            "area_name": "Thokar Niaz Beg",
            "page_size": 20,
            "page": 1,
            "food_query": "",
            "cuisines_filter": "",
            "sort_query": 1
        }

        headers = {
            'Server': 'nginx/1.4.6 (Ubuntu)',
            'Date': 'Thu, 28 Oct 2019 09:32:18 GMT',
            'Content-Type': 'application/json',
            'Referer': 'https://test.cheetay.pk/',
            'Vary': 'Accept, Cookie',
            'Connection': 'keep-alive',
            'X-Frame-Options': 'SAMEORIGIN',
            'Allow': 'GET, POST, DELETE, HEAD, OPTIONS',
            'X-CSRFToken': self.session.cookies['csrftoken'],
            'Set-Cookies': 'basket_id={}; Path=/'.format(self.session.cookies['basket_id'])
        }
        response = self.session.post(post_url, data=json.dumps(params), headers=headers)
        return response.text

    def addbasket(self):
        post_url = self.hostname + 'v3/oscarapi/basket/add-product/?multi_vender=true&area_id=412'
        body = {
            "url": "/oscarapi/products/181484/",
            "quantity": 1,
            "instructions": ""
        }
        headers = {
            'Server': 'nginx/1.4.6 (Ubuntu)',
            'Date': 'Thu, 28 Oct 2019 09:32:18 GMT',
            'Content-Type': 'application/json',
            'Referer': 'https://test.cheetay.pk/',
            'Vary': 'Accept, Cookie',
            'Connection': 'keep-alive',
            'X-Frame-Options': 'SAMEORIGIN',
            'Allow': 'GET, POST, DELETE, HEAD, OPTIONS',
            'X-CSRFToken': self.session.cookies['csrftoken'],
            'Set-Cookies': 'basket_id={}; Path=/'.format(self.session.cookies['basket_id'])
        }
        response = self.session.post(post_url, data=json.dumps(body), headers=headers)
        print (response.text)

    def foodtiles(self):

        post_url = self.hostname + 'v3/oscarapi/food-tiles/?area_id=412'
        body = {
            "area": 412,
            "page": 1
        }
        headers = {
            'Server': 'nginx/1.4.6 (Ubuntu)',
            'Date': 'Thu, 28 Oct 2019 09:32:18 GMT',
            'Content-Type': 'application/json',
            'Referer': 'https://test.cheetay.pk/',
            'Vary': 'Accept, Cookie',
            'Connection': 'keep-alive',
            'X-Frame-Options': 'SAMEORIGIN',
            'Allow': 'GET, POST, DELETE, HEAD, OPTIONS',
            'X-CSRFToken': self.session.cookies['csrftoken'],
            'Set-Cookies': 'basket_id={}; Path=/'.format(self.session.cookies['basket_id'])
        }
        response = self.session.post(post_url, data=json.dumps(body), headers=headers)
        print (response.text)

    def restaurantDetail(self):

        get_url = self.hostname + 'v3/oscarapi/restaurants/karachi-kanteen?area_id=412'
        # body = {
        #     "area": 412,
        #     "page": 1
        # }
        # headers = {
        #     'Server': 'nginx/1.4.6 (Ubuntu)',
        #     'Date': 'Thu, 28 Oct 2019 09:32:18 GMT',
        #     'Content-Type': 'application/json',
        #     'Referer': 'https://test.cheetay.pk/',
        #     'Vary': 'Accept, Cookie',
        #     'Connection': 'keep-alive',
        #     'X-Frame-Options': 'SAMEORIGIN',
        #     'Allow': 'GET, POST, DELETE, HEAD, OPTIONS',
        #     'X-CSRFToken': self.session.cookies['csrftoken'],
        #     'Set-Cookies': 'basket_id={}; Path=/'.format(self.session.cookies['basket_id'])
        # }
        response = self.session.get(get_url)
        print (response.text)







import time
cheetay = Test()
# print cheetay.signup().text
# assert '"status": true' in '{"status": true, "message": "Success", "data": null}'
# with open('fake.csv', 'wb') as csv_out:
#     for _ in range(100):
#         r = cheetay.signup()
#         email = r[0]
#         print r[1]
#         writer = csv.writer(csv_out)
#         writer.writerow([email])
#         time.sleep(2)


#
# ap =cheetay.login('chetay_lt_4b95402caf@nowhere.com')
# t = cheetay.search_partner1s()
# # t = str(t)
# print type(t)
# print t
# assert '"status":true' in t
# cheetay.foodtiles()
# cheetay.restaurantDetail()
# cheetay.addbasket()

for _ in range(200):
    cheetay.signup()
    time.sleep(3)


# sub = cheetay.add_address()
# print sub.text
# add = cheetay.get_user_addresses()
# print add.text
# # sub = cheetay.add_address()
# # import pdb; pdb.set_trace()
#
# for user in USER_CREDENTIALS:
#     print user
#     # credentials = random.choice(USER_CREDENTIALS)
#     # USER_CREDENTIALS.remove(credentials)
#     # email = credentials[0]
#     ap = cheetay.login(user[0])
#     # print index
#     sub = cheetay.add_address()
#     print sub
#     print sub.text
#     sub = cheetay.get_user_addresses()
#     print sub.text
#     import pdb; pdb.set_trace()
#     time.sleep(1)


# b = cheetay.search_partners()
# c = cheetay.checkout()
# print c.text
# print a.text
# print b.text
# import pdb;pdb.set_trace()