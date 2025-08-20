import sys

def hello(name=None):
    if name is None:
        name = "World"
    return f"Hello {name}"


def main():
    name = sys.argv[1] if len(sys.argv) > 1 else None
    print(hello(name))


if __name__ == "__main__":
    main()
