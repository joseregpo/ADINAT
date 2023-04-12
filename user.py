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
        self.channel = []
        self.requestChannel = []
        self.sharefile = []
        self.requestSharefile = []

    def __str__(self):
        s = "Username : " + self.username + "\nSocket : " + str(self.socket) + "\nState : " + self.state
        return s
    
    def __eq__(self, user):
        return self.username == user.username
    
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
    
    def setUsername(self, new_username):
        self.username = new_username

    def getChannel(self):
        return self.channel
    
    def addUserToChannel(self, user):
        self.channel.append(user)

    def getRequestChannel(self):
        return self.requestChannel
    
    def addUserToRequestChannel(self, user):
        self.requestChannel.append(user)

    def removeUserFromRequestChannel(self, user):
        self.requestChannel.remove(user)

    def getSharefile(self):
        return self.sharefile
    
    def addToSharefile(self, user, file):
        d = {}
        f = [file]
        d[user].extend(f)
        self.sharefile.append(d)

    def getRequestSharefile(self):
        return self.requestSharefile
    
    def addToRequestSharefile(self, user, file):
        d = {}
        f = [file]
        d[user].extend(f)
        self.requestSharefile.append(d)

    def removeFromRequestSharefile(self, user, file):
        for i in range (len(self.requestSharefile)):
            for k, v in i.items():
                if k == user:
                    if file in v:
                        v.remove(file)
                        return
                        



