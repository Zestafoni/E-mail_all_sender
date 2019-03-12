#!/usr/bin/python
import smtplib
from email.mime.text import MIMEText

path = '/home/forward/Desktop/'          # Working path

#_______________________________________________________________________________________________
# Read main text file
def open_txt():
    txt_name = input('\n> Filename of text> ')
    try:
        t = open(f'{txt_name}', 'r')
        txt = t.read()
        t.close()
        return txt
    except:
        print('>[Error] Check out filename and try again')
        open_txt()

#______________________________________________________________________________________________
# Read contacts
def open_contacts():
    contacts_name = input('\n> Filename of contacts> ')
    try:
        c = open(f'{contacts_name}', 'r')
        contacts = [x.replace('\n', '') for x in c]
        c.close()
        return contacts
    except:
        print('>[Error] Check out filename and try again')
        open_contacts()

#_______________________________________________________________________________________________
# Shell type menu      
def menu():
    #1-- text input type
    print('\n\t Choose body-text input type!')
    text_type = input('> "U" for upload file / "M" for manual> ')
    if text_type.upper() == 'U':
        text_file = open_txt()
    elif text_type.upper() == 'M':
        text_file = input('> Input text: \n')
    else:
        print('>[ERROR] Check out instruction')
        return

    #2-- contact input type
    print('\n\t Upload Contacts')
    string = False
    contact = open_contacts()
    
    # Call MIME & SENDER functions here
    people = mime_object(text_file, contact)
    sender(people)


#_______________________________________________________________________________________________
# Mime object
def mime_object(body_text, contacts):
    sender_mail = input('Input "From": ')
    sbj = input('Input "Subject": ')
    contacts_list = []
    for each in contacts:
        msg = MIMEText(body_text)
        msg['From'] = sender_mail
        msg['To'] = each
        msg['Subject'] = sbj
        contacts_list.append(msg)
    return contacts_list


#_______________________________________________________________________________________________
# Sender function
def sender(people):
    uname = input('Enter username: ')
    pwr = input('Enter password: ')

    # Mail server connection
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587) 
    except:
        print('>[ERROR] Server conection error, try again later')
    server.starttls()
    try:
        server.login(uname, pwr)
    except:
        print('[!] Invalid username or password')
        sender(people)

    # Send messages
    scount = 0
    fcount = 0
    for msg in people:
        try:
            server.send_message(msg)
            print(str(scount + 1) + ' sent')
            scount += 1
        except:
            print(str(scount) + ' failed, continue...')
            fcount += 1
            continue

    server.quit()

    print(str(scount) + ' Message has been sent succesfully')
    print(str(fcount) + ' Failed')

# info
def head_info():
	print('[*] \t ')
	print('[*] E-mail sender')
	print('[*] Using Google SMTP server')
	print('[*] \n')


################# MAIN ###################
head_info()
menu()