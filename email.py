class Email:
    def __init__(self, email_address, subject_line, email_content):
        self.email_address = email_address
        self.subject_line = subject_line
        self.email_content = email_content
        self.has_been_read = False

    def mark_as_read(self):
        self.has_been_read = True


# Initialise an empty inbox to store email objects
inbox = []


def populate_inbox():
    # Creating sample emails and adding them to the inbox
    email1 = Email("sender1@example.com", "Welcome to HyperionDev!", "Hello! Welcome to our platform.")
    email2 = Email("sender2@example.com", "Great work on the bootcamp!", "You are doing a fantastic job.")
    email3 = Email("sender3@example.com", "Your excellent marks!", "Congratulations on your achievements.")
    
    inbox.extend([email1, email2, email3])


def list_emails():
    print("\nYour Inbox:")
    for idx, email in enumerate(inbox):
        read_status = "Read" if email.has_been_read else "Unread"
        print(f"{idx} [{read_status}] {email.subject_line}")


def read_email(index):
    if 0 <= index < len(inbox):
        email = inbox[index]
        print("\nEmail Details:")
        print(f"From: {email.email_address}")
        print(f"Subject: {email.subject_line}")
        print(f"Content: {email.email_content}")
        if not email.has_been_read:
            email.mark_as_read()
            print(f"\nEmail from {email.email_address} marked as read.\n")
    else:
        print("\nInvalid index. Please choose a valid email index.")


if __name__ == "__main__":
    populate_inbox()

    while True:
        print("\nEmail Simulator Menu:")
        print("1. Read an email")
        print("2. View unread emails")
        print("3. Quit application")

        choice = input("Enter your choice (1/2/3): ")

        if choice == "1":
            list_emails()
            email_index = int(input("\nEnter the index of the email you want to read: "))
            read_email(email_index)
        elif choice == "2":
            list_emails()
        elif choice == "3":
            print("\nThank you for using the Email Simulator. Goodbye!")
            break
        else:
            print("\nInvalid choice. Please enter 1, 2, or 3.")
