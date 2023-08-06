import webbrowser
import time
import requests

URL = "https://linkedin.com/in/siddheshkulthe"
recipient_email = "siddheshkulthe43@gmail.com"

social_list = []


def send_message():
    name = str(input("So, what can I call you: "))
    time.sleep(1)
    print(f"It's nice to meet you {name}!")
    time.sleep(1)
    message = str(input("Tell me your messsage here: "))
    time.sleep(1)
    print(f"Just so that Siddhesh can get back to you {name},")
    time.sleep(1)
    email = str(input("Please share me your email: "))
    vercel_url = "http://34.204.127.0:5001/"
    data = {"message": message, "email": email, "name": name}

    # Make the HTTP POST request to your Vercel app's endpoint
    response = requests.post(vercel_url, json=data)

    if response.status_code == 200:
        print("Thanks for reaching out.")
        print("I've successfully informed Siddhesh that you wanted to reach out!")
    else:
        print("Error sending message.")


def start():
    print("Hey yo! Nice to meet you :)")
    time.sleep(1)
    print("I'm a Freddy. Developed by Siddhesh Kulthe.")
    time.sleep(1)
    print("What would you like to do?\n")
    time.sleep(1)
    choice = int(
        input(
            "1. Send Siddhesh A Message \n2. Check out Siddhesh's LinkedIn \nEnter (1/2): "
        )
    )
    if choice == 1:
        send_message()
    elif choice != 1:
        print("\nCool! I'll lead you to his resume!")
        time.sleep(2)
        print("Btw, he's a super cool guy. Would really love to be friends with you :)")
        time.sleep(2)
        print("...")
        time.sleep(1)
        webbrowser.open(URL)
