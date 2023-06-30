class MockProcess():
    def __init__(self, pid, name) -> None:
        self.info = {"pid": pid, "name": name}
        self.running = True

    def kill(self):
        self.running = False
        pass