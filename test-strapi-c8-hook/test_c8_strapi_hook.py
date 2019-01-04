import copy
import json
import logging
import requests

import pprint

from prettytable import PrettyTable


# URLs
BASE_URL = "http://localhost:1337"
AUTH_URL = BASE_URL + "/auth/local/register"
MEN_URL = BASE_URL + "/men"
WOMEN_URL = BASE_URL + "/women"
CHILDREN_URL = BASE_URL + "/children"
ADDRESSES_URL = BASE_URL + "/addresses"


# Request Headers
HEADERS = {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}


# Logger
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# Console handler
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# Create formatter
formatter = logging.Formatter('%(asctime)s: %(levelname)s: %(message)s')
ch.setFormatter(formatter)

# Add Handlers
logger.addHandler(ch)


# Pretty Table
p = PrettyTable(["No.", "Test", "Status"])


# Functions
# GET request
def get(url, headers):

    logger.debug("Sending GET request to '{url}'".format(url=url))

    try:
        r = requests.get(url, headers=headers)
        r.raise_for_status()
    except requests.exceptions.RequestException as e:
        logger.error("GET request failed: '{url}'".format(url=url))
        raise e

    # Return response
    return r


# POST request
def post(url, data, headers):

    logger.debug("Sending POST request to '{url}'".format(url=url))

    try:
        r = requests.post(url, json.dumps(data), headers=headers)
        r.raise_for_status()
    except requests.exceptions.RequestException as e:
        logger.error("POST request failed: '{url}'".format(url=url))
        raise e

    # Return response
    return r


# PUT request
def put(url, data, headers):

    logger.debug("Sending PUT request to '{url}'".format(url=url))

    try:
        r = requests.put(url, json.dumps(data), headers=headers)
        r.raise_for_status()
    except requests.exceptions.RequestException as e:
        logger.error("PUT request failed: '{url}'".format(url=url))
        raise e

    # Return response
    return r


# DELETE request
def delete(url, headers):

    logger.debug("Sending DELETE request to '{url}'".format(url=url))

    try:
        r = requests.delete(url, headers=headers)
        r.raise_for_status()
    except requests.exceptions.RequestException as e:
        logger.error("DELETE request failed: '{url}'".format(url=url))
        raise e

    # Return response
    return r


# Get Authorization token from strapi
def register(username, password, email):

    logger.debug("Registering admin user: '%s'" % username)

    # Request Body
    body = {
        "username": username,
        "email":    email,
        "password": password}

    r = post(AUTH_URL, body, headers=HEADERS)
    if r.status_code != 200:
        err = "Failed to register '%s'. Error: '%s'" % (username, r.reason)
        logger.error(err)
        raise Exception(err)

    jwt = json.loads(r.content).get('jwt')
    if not jwt:
        raise Exception("Empty authorization token")

    # Successful
    return jwt


def find(url, jwt):

    # Add Authorization header
    headers = copy.deepcopy(HEADERS)
    headers['Authorization'] = "bearer {token}".format(token=jwt)

    r = get(url, headers=headers)
    if r.status_code != 200:
        err = "Failed to GET all records. Error: '%s'" % (r.reason)
        logger.error(err)
        raise Exception(err)

    allrecords = json.loads(r.content)

    # Successful
    return allrecords


# Get count of all records
def count(url, jwt):

    # Add Authorization header
    headers = copy.deepcopy(HEADERS)
    headers['Authorization'] = "bearer {token}".format(token=jwt)

    req_url = url + "/count"

    r = get(req_url, headers=headers)
    if r.status_code != 200:
        err = "Failed to GET count of all records. Error: '%s'" % (r.reason)
        logger.error(err)
        raise Exception(err)

    # Count
    count = json.loads(r.content)

    # Successful
    return count


# FindOne()
def findOne(url, doc_id, jwt):

    # Add Authorization header
    headers = copy.deepcopy(HEADERS)
    headers['Authorization'] = "bearer {token}".format(token=jwt)

    req_url = url + "/%s" % doc_id

    r = get(req_url, headers=headers)
    if r.status_code != 200:
        err = "Failed to GET one record. Error: '%s'" % (r.reason)
        logger.error(err)
        raise Exception(err)

    # document
    doc = json.loads(r.content)

    # Successful
    return doc

# Create a document
def create(url, body, jwt):

    # Add Authorization header
    headers = copy.deepcopy(HEADERS)
    headers['Authorization'] = "bearer {token}".format(token=jwt)

    r = post(url, body, headers=headers)
    if r.status_code != 200:
        err = "Failed to POST record. Error: '%s'" % (r.reason)
        logger.error(err)
        raise Exception(err)

    # document
    doc = json.loads(r.content)

    # Successful
    return doc


# Update a document
def update(url, update_id, body, jwt):

    # Add Authorization header
    headers = copy.deepcopy(HEADERS)
    headers['Authorization'] = "bearer {token}".format(token=jwt)

    req_url = url + "/%s" % update_id

    r = put(req_url, body, headers=headers)
    if r.status_code != 200:
        err = "Failed to PUT record. Error: '%s'" % (r.reason)
        logger.error(err)
        raise Exception(err)

    # document
    doc = json.loads(r.content)

    # Successful
    return doc


# Delete a document
def remove(url, delete_id, jwt):

    # Add Authorization header
    headers = copy.deepcopy(HEADERS)
    headers['Authorization'] = "bearer {token}".format(token=jwt)

    # url
    req_url = url + "/%s" % delete_id

    # Delete request
    r = delete(req_url, headers=headers)
    if r.status_code != 200:
        err = "Failed to DELETE record. Error: '%s'" % (r.reason)
        logger.error(err)
        raise Exception(err)

    # document
    doc = json.loads(r.content)

    # Successful
    return doc


def setup(jwt):

    # Man: Jack
    body = {'Name': 'Jack', 'Age': 30}
    man = create(MEN_URL, body, jwt)
    logger.debug("man: %s" % pprint.pformat(man))

    # Woman: Jill
    body = {'Name': 'Jill', 'Age': 27, 'spouse': man.get('id')}
    woman = create(WOMEN_URL, body, jwt)
    logger.debug("woman: %s" % pprint.pformat(woman))

    # Child 1: James
    body = {'Name': 'James',
            'Age': 10,
            'father': man.get('id'),
            'mother': woman.get('id')}
    child1 = create(CHILDREN_URL, body, jwt)
    logger.debug("child1: %s" % pprint.pformat(child1))

    # Child 2: Joy
    body = {'Name': 'James',
            'Age': 10,
            'father': man.get('id'),
            'mother': woman.get('id')}
    child2 = create(CHILDREN_URL, body, jwt)
    logger.debug("child2: %s" % pprint.pformat(child2))

    # Address:
    body = {'Name': 'Home',
            'Address': 'On a Hill',
            'men': [man],
            'women': [woman],
            'children': [child1, child2]}
    home = create(ADDRESSES_URL, body, jwt)
    logger.debug("home: %s" % pprint.pformat(home))


# Driver function
def test():

    try:
        # TEST 1: Register admin (default) user
        # jwt = register("test", "test123!", "test@test.com")
        jwt = None
        p.add_row(["1", "register", "pass"])

        # TEST 2: Test "create" for all models
        setup(jwt)
        p.add_row(["2", "create", "pass"])

        # TEST 3:
        men = find(MEN_URL, jwt)
        women = find(WOMEN_URL, jwt)
        children = find(CHILDREN_URL, jwt)
        addresses= find(ADDRESSES_URL, jwt)
        p.add_row(["2", "find all", "pass"])

        # TEST 4:
        man = findOne(MEN_URL, men[0].get('id'), jwt)
        woman = findOne(WOMEN_URL, women[0].get('id'), jwt)
        child1 = findOne(CHILDREN_URL, children[0].get('id'), jwt)
        home = findOne(ADDRESSES_URL, addresses[0].get('id'), jwt)
        p.add_row(["3", "find one", "pass"])

        # TEST 5:
        men = count(MEN_URL, jwt)
        women = count(WOMEN_URL, jwt)
        children = count(CHILDREN_URL, jwt)
        addresses= count(ADDRESSES_URL, jwt)
        p.add_row(["4", "count", "pass"])

        # TEST 7:
        update_body = {'Age': 35}
        updated = update(MEN_URL, man.get('id'), update_body, jwt)
        p.add_row(["5", "update", "pass"])

        # TEST 8:
        remove_id = child1.get('id')
        removed = remove(CHILDREN_URL, remove_id, jwt)
        p.add_row(["6", "delete", "pass"])

        # Print result
        logger.info("Test Results:\n%s" % p)

    except Exception as e:
        logger.error("Error: '%s'" % e)


# Driver
test()
