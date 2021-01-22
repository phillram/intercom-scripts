# _______________________________________________________________
# Close all open Intercom conversations
# _______________________________________________________________

# _______________________________________________________________
# Importing requirements 
# _______________________________________________________________
import requests, json

# _______________________________________________________________
# Initializing variables
# Place your Intercom bearer token and administrator ID here
# _______________________________________________________________
intercom_api_key = ''
intercom_admin_id = ''

# _______________________________________________________________
# Search for open converations
# _______________________________________________________________
def retrieve_open_conversations():
    url = "https://api.intercom.io/conversations/search"
    headers = {
        'Authorization': intercom_api_key,
        'Content-Type': 'application/json'
    }

    # Search query for open conversations
    payload = """
        { "query": {
            "field": "state",
            "operator": "=",
            "value": "open"
            }
        }
    """

    # API call to get open conversations
    response = requests.request("POST", url, headers = headers, data = payload)

    # Parse the response to JSON
    response_data = response.json()

    # Initializing conversation ID array
    conversation_ids = []

    # Getting a list of the user IDs
    for i in response_data['conversations']:
        conversation_ids.append(i['id'])

    # Returns: list of conversation IDs & number of conversations which matched the query
    return conversation_ids, response_data['total_count']


# _______________________________________________________________
# Closing conversations found above
# _______________________________________________________________
def close_conversations(intercom_conversation_ids):

    headers = {
        'Accept': 'application/json',
        'Authorization': intercom_api_key,
        'Content-Type': 'application/json',
    }

    payload = "{ \n  \"message_type\": \"close\",\n  \"type\": \"admin\",\n  \"admin_id\":" + str(intercom_admin_id) +  ",\n  \"body\": \"\"\n}"

    # Use the conversation IDs found earlier to close out the 
    for i in intercom_conversation_ids:
        url = "https://api.intercom.io/conversations/" + str(i) + "/parts"
        response = requests.request("POST", url, headers = headers, data = payload)
        # Parse the response to JSON
        response_data = response.json()
        print('Conversation ' + str(response_data['id']) + ' is now ' + str(response_data['state']))

    return response.text


# _______________________________________________________________
# Running the functions above   
# Find open conversations, then close them out
# _______________________________________________________________

# Searching for open conversations
conversation_ids = retrieve_open_conversations()
print('Starting conversations: ' + str(conversation_ids[1]))

while conversation_ids[1]:
    # Closing those conversations
    close_conversations(conversation_ids[0])

    # Repeating the search
    conversation_ids = retrieve_open_conversations()
    print('Remaining conversations: ' + str(conversation_ids[1]))