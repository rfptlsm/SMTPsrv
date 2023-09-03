from email.message import EmailMessage
import smtplib
import sys, getopt
import glob


def mailbox(argv, port=465, address='addresslist.txt', letter='letter.txt', attachment=None):
    try:
        opts, args = getopt.getopt(argv, "he:p:s:P:a:l:f:", ['email=', 'password=', 'server=', 'port=', 'address=', 'leter=', 'files=', 'help'])
    except getopt.GetoptError:
        print("-e --email <email>\n-p --pass <password>\n-s --server <smtp server>\n-P --port (default: 465)\n-a --address (default: addresslist.txt)\n-l --letter (default: letter.txt)\n-f --files <attachment>")
        sys.exit(2)
    
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print("-e --email <email>\n-p --pass <password>\n-s --server <smtp server>\n-P --port (default: 465)\n-a --address (default: addresslist.txt)\n-l --letter (default: letter.txt)\n-f --files <attachment>")
            sys.exit()
        elif opt in ("-e", "--email"):
            mail = arg
        elif opt in ("-p", "--pass"):
            password = arg
        elif opt in ("-s", "--server"):
            server = arg
        elif opt in ("-P", "--port"):
            port = arg
        elif opt in ("-a", "--address"):
            address = arg
        elif opt in ("-l", "--letter"):
            letter = arg
        elif opt in ("-f", "--files"):
            attachment = arg

    with open(address) as f:
        to_send = f.readlines()

    with open(letter) as f:
        title_msg = f.readline()
        title_msg.strip('\n')
        body_msg = f.read()

    msg = EmailMessage()
    msg["Subject"] = title_msg
    msg["From"] = mail
    msg["To"] = to_send  # ', '.join(to_send)
    msg.set_content(body_msg)

    if(attachment != None):
        dfiles = glob.glob(attachment)
        for files in dfiles:
            with open(files, 'rb') as f:
                data_file = f.read()
                data_name = f.name
                msg.add_attachment(data_file, maintype='application', subtype='octet-stream', filename=data_name)

    with smtplib.SMTP_SSL(server, port) as smtp:
        smtp.ehlo()
        smtp.login(mail, password)
        smtp.send_message(msg)

if __name__ == "__main__":
    mailbox(sys.argv[1:])