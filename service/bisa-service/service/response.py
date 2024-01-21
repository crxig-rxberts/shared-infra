class Response:
    def __init__(self, status, message):
        self.status = status
        self.message = message

    @classmethod
    def success(cls, message="Success"):
        return cls("success", message)

    @classmethod
    def failure(cls, message="Failure"):
        return cls("failure", message)

    def to_dict(self):
        return {"status": self.status, "message": self.message}

    def __str__(self):
        return str(self.to_dict())
