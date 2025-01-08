from dataclasses import dataclass
@dataclass
class Geek:
    def __init__(self) -> None:
        self.domain = "geeksforgeeks.org"
        self.gato = "miau"


if __name__ == '__main__':
	geeks = Geek()
	print("Before deleting domain attribute from geeks object:")
	print(geeks.domain)
	delattr(geeks, "gato")
	print("After deleting domain attribute from geeks object:")
	# this will raise AttributeError if we try to access 'domain' attribute
	print(geeks)
