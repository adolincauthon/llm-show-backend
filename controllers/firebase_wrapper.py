from firestore_model.model_firestore import Agent_Model


def set_user_message(asssitant, user, message):
    '''
    Sets a new message from assistant to user, updating both objects in firebase
    :param assistant: Reference to assistant's firebase record
    :param user:      Reference to user's firebase record
    :param message:   Message to send
    :returns bool:    Returns success of operation
    '''
    try:
        return True
    except:
        return False


def set_message_history(asssitant_obj, user_obj):
    '''
    Sets a new message from assistant to user, updating both objects in firebase
    :param assistant: Reference to assistant's firebase record
    :param user:      Reference to user's firebase record
    :param message:   Message to send
    :returns bool:    Returns success of operation
    '''
    try:
        model = Agent_Model()
        model.add_messages(asssitant_obj, user_obj)
        return True
    except Exception as e:
        print(e)
        return False


def get_message_history(assistant, user):
    '''
    Retrieves message history between assistant and user
    :param assistant: ID to asssitant's firebase record
    :param user:      ID to user's firebase recod
    :returns dict:    Returns dictionary containing asssistantMessages and userMessages lists
    '''
    model = Agent_Model()
    assistant_messages = []
    user_messages = []

    assistant_data = model.get_agent(assistant)

    inbox = assistant_data.get('inbox')
    user_messages.extend(inbox.get(user, []))
    outbox = assistant_data.get('outbox')
    assistant_messages.extend(outbox.get(user, []))

    return {'assistant_messages': assistant_messages, 'user_messages': user_messages}
