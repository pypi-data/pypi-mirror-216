#usando de exemplo: https://github.com/Slimakoi/Amino.py/blob/master/amino/lib/util/objects.py


class AuthorProfile:
    def __init__(self, data):
        self.json = data
        self.Username = None
        self.PublicFlags = None
        self.id = None
        self.GlobalName = None
        self.Discriminator = None
        self.AvatarDecoration = None
        self.AvatarUrl = None
      
    @property
    def AuthorProfile(self):
        self.Username = self.json.get('username')
        self.PublicFlags = self.json.get('public_flags')
        self.id = self.json.get('id')
        self.GlobalName = self.json.get('global_name')
        self.Discriminator = self.json.get('discriminator')
        self.AvatarDecoration = self.json.get('avatar_decoration')
        try:
            self.AvatarUrl = f"https://cdn.discordapp.com/avatars/{self.id}/{self.json.get('avatar')}"
        except:
            self.AvatarUrl = None

        return self


class MessageContent:
  def __init__(self, data):
    self.json = data
    
  @property
  def MessageContent(self):
    self.Event = self.json.get('t')
    self.Message = self.json.get('d').get('content')
    self.Author = AuthorProfile(self.json.get('d').get('author')).AuthorProfile
    self.id = self.json.get('d').get('id')
    self.timestamp = self.json.get('d').get('timestamp')
    self.MentionEveryone = self.json.get('d').get('mention_everyone')

    return self