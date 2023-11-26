def set_user_message(asssitant, user, message):
    '''
    Sets a new message from assistant to user, updating both objects in firebase
    :param assistant: Reference to assistant's firebase record
    :param user:      Reference to user's firebase record
    :param message:   Message to send
    :returns bool:    Returns success of operation
    '''
    return True


def get_message_history(assistant, user):
    '''
    Retrieves message history between assistant and user
    :param assistant: Reference to asssitant's firebase record
    :param user:      Reference to user's firebase recod
    :returns dict:    Returns dictionary containing asssistantMessages and userMessages lists
    '''
    assistantMessages = []
    userMessages = []
    return {'assistantMessages': assistantMessages, 'userMessages': userMessages}
