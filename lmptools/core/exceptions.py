class SkipSnapshot(Exception):
    """
    Exception to be raised when a snapshot is skipped while parsing a dump file
    """

    def __init__(self, msg: str):
        super(SkipSnapshot, self).__init__()
        self.msg = msg

    def __str__(self):
        if self.msg:
            return f"SkipSnapshot, {self.msg}"
        else:
            return "Exception SkipSnapshot occurred"
