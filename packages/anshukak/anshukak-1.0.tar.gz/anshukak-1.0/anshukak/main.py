import requests
import pyperclip

def copy_content_to_clipboard(url):
    response = requests.get(url)
    if response.status_code == 200:
        content = response.text
        pyperclip.copy(content)
        print("success.")
    else:
        print("failed")

def main():
    name = input("Enter a name: ")
    url = f"https://raw.githubusercontent.com/Pranavkak/help/main/{name}.txt"
    copy_content_to_clipboard(url)

if __name__ == "__main__":
    main()
