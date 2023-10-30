#!/usr/bin/python

"""
This script allows you to send an email with provided content to a specified email address.
Warnings: 
1. In password.txt file you need to write an app 16-digit password that you generated in your 
Google account.
2. In content.txt file you need to write the content of you email.
"""

import argparse
import ssl
import smtplib

def get_info_from_file(fname, encoding='utf-8'):
    """
    Function to get information from a file.
    """
    with open(fname, encoding=encoding) as f:
        return f.read()

def send_email(smtp_server, smtp_port, context, from_addr, to_addrs, app_password, message):
    """
    Function to connect to the SMTP server and send the email.
    """
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls(context=context)
        server.login(from_addr, app_password)
        print(f"Sending email from - {from_addr}")
        server.sendmail(from_addr, to_addrs, message)
        print(f"Email sent to - {to_addrs}")
    except smtplib.SMTPAuthenticationError as e:
        print(f"Failed to authenticate. {e}")
    except smtplib.SMTPException as e:
        print(f"SMTP Exception occurred: {e}")
    finally:
        server.quit()

def main():
    """
    Main function to handle sending the email.
    """
    parser = argparse.ArgumentParser(description="Write your email, receive email, email subject and filename")
    parser.add_argument('-s', '--email_sender', required=True, help='Write your email')
    parser.add_argument('-r', '--email_receiver', required=True, help='Write receiver mail')
    parser.add_argument('-t', '--title', required=True, help='Write email subject')
    parser.add_argument('-f', '--content_filename', required=True, help='Write email content filename')
    args = parser.parse_args()

    smtp_port = 587
    smtp_server = "smtp.gmail.com"

    email_from = args.email_sender
    email_to = args.email_receiver
    title = args.title
    content = get_info_from_file(args.content_filename)

    app_password = get_info_from_file("password.txt")

    message = f"Subject: {title}\n\n{content}"

    context = ssl.create_default_context()

    send_email(smtp_server, smtp_port, context, email_from, email_to, app_password, message)


if __name__ == "__main__":
    main()
