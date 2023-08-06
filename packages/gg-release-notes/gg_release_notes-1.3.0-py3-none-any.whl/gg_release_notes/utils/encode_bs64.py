import base64


def encode_env_file(path: str):
    """
    Encodes the .env file with base64 and prints it to the console.
    The output can be used in the .github/workflows/release_notes.yml file and needs to be saved as Github Actions Secret.
    """
    with open(path, "rb") as f:
        print(base64.b64encode(f.read()))


if __name__ == "__main__":
    encode_env_file(input("Enter the path to the .env file: "))
