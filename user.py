class User():

    def __init__(self, username=None, socket=None, state=None):
        if username is None:
            self.username = ""
        else:
            self.username = username
            
        if socket is None:
            self.socket = ""
        else:
            self.socket = socket

        if state is None:
            self.state = ""
        else:
            self.state = state

    def __str__(self):
        s = "Username : " + self.username + "\nSocket : " + str(self.socket) + "\nState : " + self.state
        return s
    
    def __eq__(self, user):
        return self.username == user.username and self.socket == user.socket
    
    def setConnected(self, state):
        self.state = state

    def getConnected(self):
        return self.state
        
    def getSocket(self):
        return self.socket
    
    def getUsername(self):
        return self.username
