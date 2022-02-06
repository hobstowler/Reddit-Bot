# Author: Hobs Towler
# Date: 2/4/2022
# Description: Provides methods for getting refresh token using Praw API.

import praw as pr
import socket
import sys
import random
import webbrowser


def get_refresh_token(cid, secret, scopes=None):
    """
    Gets a refresh token with provided client Id and Client Secret. Will launch web browser and read data from browser.
    Args:
        cid ([type]): Client ID
        secret ([type]): Client Secret
        scopes ([type], optional): Authorization scopes for instance of Reddit. If None/default, uses 'identity' and 'read' scopes.

    Returns: None
    """
    if scopes is None:
        scopes = ['identity','read']

    reddit = pr.Reddit(
        client_id = cid,
        client_secret = secret,
        redirect_uri = 'http://localhost:8080',
        user_agent = 'test by u/pytesterbot'
    )

    state = str(random.randint(0, 65000))
    auth_url = reddit.auth.url(scopes, state, "permanent")
    webbrowser.open(auth_url)
    #print("open this in your browser:", auth_url)

    client = receive_connection()
    data = client.recv(1024).decode('utf-8')
    param_tokens = data.split(" ", 2)[1].split("?", 1)[1].split('&')
    params = {
        key: value for (key, value) in [token.split("=") for token in param_tokens]
    }

    if state != params["state"]:
        send_message(
            client,
            f"State mismatch. Expected: {state}, recieved: {params['state']}",
        )
        return 1
    elif "error" in params:
        send_message(client, params['error'])
        return 1
    
    refresh_token = reddit.auth.authorize(params["code"])
    #print(refresh_token)
    send_message(client, f"Refresh token: {refresh_token}")
    return refresh_token

def receive_connection():
    """
    Opens a connection to listen on localhost:8080
    Returns: client
    """
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('localhost', 8080))
    server.listen(1)
    client = server.accept()[0]
    server.close()
    return client

def send_message(client, message):
    client.send(f"HTTP/1.1 200 OK\r\n\r\n{message}".encode('utf-8'))
    client.close()
    
if __name__ == "__main__":
    #get_refresh_token()
    pass