import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

recipient_list = ['googlegroup1@mail.com', 'googlegroup1@mail.com']
sender_mail = 'sender@mail.com'


def send_mail(mail_type, phone, feedback=''):
    """
    Function is used for sending the mail when the user is created and the user gives feedback
    the type of the mail is decided by mail_type of the argument.
    """
    phone = str(phone[0:5] + '*****' + phone[10:])
    if mail_type == 'FEEDBACK':
        with open('templates/feedback.html', 'r') as template:
            html = ''.join(template.readlines())
            message = Mail(
                from_email=sender_mail,
                to_emails=recipient_list,
                subject=mail_type,
                html_content=html.format(phone=phone, feedback=feedback))

    elif mail_type == 'NEW USER':
        with open('templates/welcome.html', 'r') as template:
            html = ''.join(template.readlines())
            message = Mail(
                from_email=sender_mail,
                to_emails=recipient_list,
                subject=mail_type,
                html_content=html.format(phone=phone))
    else:
        print("Please check the mail_type before sending mail")
        return
    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
        if response.status_code == 202:
            print('send successfully')
    except Exception as e:
        print(e)


