# Class LinkValidator to determine valid links
class LinkValidator:

# Initiates self
    
    def __init__(self, domain, disallows):
        self.domain = domain
        self.disallows = disallows

# Determines if the link can be followed. Doesn't allow to go past bounds of the domain
    
    def can_follow_link(self, url):
        if not url.startswith(self.domain):
            return False

        for path in self.disallows:
            if url.startswith(self.domain + path):
                return False
        return True
