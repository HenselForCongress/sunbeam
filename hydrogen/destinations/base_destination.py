# hydrogen/destinations/base_destination.py
class DataDestination:
    def send_data(self, data):
        raise NotImplementedError("send_data must be implemented by subclasses.")
