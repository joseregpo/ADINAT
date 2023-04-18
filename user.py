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
        self.sharefile = {}
        self.requestSharefile = {}

    def __str__(self):
        s = "Username : " + self.username + "\nSocket : " + str(self.socket) + "\nState : " + self.state
        return s
    
    def __eq__(self, user):
        return self.username == user.username
    
    def __hash__(self):
        return self.socket.__hash__()

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
    
    def checkIfUserExistsInChannel(self, user):
        if user in self.channel:
            return True
        return False
    
    def addUserToRequestChannel(self, user):
        self.requestChannel.append(user)

    def removeUserFromRequestChannel(self, user):
        self.requestChannel.remove(user)

    def checkIfUserExistsInRequestChannel(self, user):
        if user in self.requestChannel:
            return True
        return False

    def getSharefile(self):
        return self.sharefile
    
    def addToSharefile(self, user, file):
        f = [file]        
        if user in self.sharefile.keys():
            self.sharefile[user].extend(f)
        else:
            self.sharefile[user] = f

    def getRequestSharefile(self):
        return self.requestSharefile
    
    def addToRequestSharefile(self, user, file):
        f = [file]        
        if user in self.requestSharefile.keys():
            self.requestSharefile[user].extend(f)
        else:
            self.requestSharefile[user] = f

    def removeFromRequestSharefile(self, user, file):
        for k,v in self.requestSharefile.items():
            if k == user and file in v:
                v.remove(file)
                return
            

    def checkIfFileExistsInRequestShareFile(self, user, file):
        for k,v in self.requestSharefile.items():
            if k == user and file in v:
                return True
        return False

        # for i in range (len(self.requestSharefile)):
        #     for k, v in i.items():
        #         if k == user:
        #             if file in v:
        #                 v.remove(file)
        #                 return
                        


