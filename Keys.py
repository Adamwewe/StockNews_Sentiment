from dotenv import dotenv_values

def environment_vars(path):
    """
    Args:
        path (str): path to respective .env file
    returns:
        cred (dict): k/v pair dictionary returning sensitive data
    """


    return dotenv_values(path)
