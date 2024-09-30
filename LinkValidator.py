class LinkValidator:
    def __init__(self, domain, disallows):
        self.domain = domain
        self.disallows = disallows

    def can_follow_link(self, url):
        if not url.startswith(self.domain):
            return False

        for path in self.disallows:
            if url.startswith(self.domain + path):
                return False
        return True