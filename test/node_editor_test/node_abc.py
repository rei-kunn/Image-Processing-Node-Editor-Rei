from abc import ABC, abstractmethod

class Node(ABC):
    @abstractmethod
    def add_node(self, parent, node_id, pos=[0, 0]):
        pass

    @abstractmethod
    def update(self):
        pass