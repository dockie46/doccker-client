class DockerContainer:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __str__(self):
        return f"DockerContainer(id={self.id}, name={self.name})"


class DockerImage:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __str__(self):
        return f"DockerImage(id={self.id}, name={self.name})"
