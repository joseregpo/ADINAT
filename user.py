class User():

    def __init__(self, username=None, socket=None, state="afk", connected=False):
        if username is None:
            self.username = ""
        else:
            self.username = username
            
        if socket is None:
            self.socket = ""
        else:
            self.socket = socket

        self.state = state
        self.connected = connected

    def __str__(self):
        s = "Username : " + self.username + "\nSocket : " + str(self.socket) + "\nState : " + self.state
        return s
    
    def __eq__(self, user):
        return self.username == user.username and self.socket == user.socket
    
    def setState(self, state):
        self.state = state

    def getState(self):
        return self.state
    
    def setConnected(self, value):
        self.connected = value

    def getConnected(self):
        return self.connected
        
    def getSocket(self):
        return self.socket
    
    def getUsername(self):
        return self.username
