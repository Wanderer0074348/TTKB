from openai import OpenAI

client = OpenAI()

response = client.responses.create(
     model = "gpt-4.1",
     input = "This is a sample text input"
)


if __name__ == "__main__":
     print("Hello World")