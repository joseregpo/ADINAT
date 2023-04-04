class User():

    def __init__(self, username=None, socket=None):
        if username is None:
            self.username = ""
        else:
            self.username = username
            
        if socket is None:
            self.socket = ""
        else:
            self.socket = socket

    def __str__(self):
        s = "Username : " + self.username + "\nSocket : " + str(self.socket)
        return s
    
    def __eq__(self, user):
        return self.username == user.username and self.socket == user.socket
        
    def getSocket(self):
        return self.socket
    
    def getUsername(self):
        return self.username
