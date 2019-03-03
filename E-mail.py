#!/usr/bin/python
import smtplib
from email.mime.text import MIMEText

path = '/home/forward/Desktop/'          # Working path

#_______________________________________________________________________________________________
# Read main text file
def open_txt():
    txt_name = input('\n> Filename of text> ')
    try:
        t = open(f'{path}{txt_name}', 'r')
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
        c = open(f'{path}{contacts_name}', 'r')
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
    print('\n\t Choose Contacts input type')
    print('>[!] If you choose "contacts-list", than you have to upload list file')
    contact_type = input('"S" for single contact / "L" for contacts-list> ')
    if contact_type.upper() == 'S':
        string = True
        contact = input('> Input adress> ')
    elif contact_type.upper() == 'L':
        string = False
        contact = open_contacts()
    else :
        print('>[ERROR] Check out instruction')
        return

    # Call MIME & SENDER functions here
    obj_type = mime_object(text_file, contact, string)
    sender(obj_type)


#_______________________________________________________________________________________________
# Mime object
def mime_object(body_text, contacts, string):
    sender_mail = input('Input "From"> ')
    sbj = input('Input "subject"> ')
    if string:
        ls = []
        msg = MIMEText(body_text)
        msg['From'] = sender_mail
        msg['To'] = contacts
        msg['Subject'] = sbj
        ls.append(msg)
        return ls
    else:
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
def sender(mime_obj):
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
        sender(mime_obj)

    # Send messages
    scount = 0
    fcount = 0
    for msg in mime_obj:
        try:
            server.send_message(msg)
            print(str(scount + 1) + ' sent')
            scount += 1
        except:
            print(str(scount) + ' failed, continue...')
            fcount += 1
            continue

    server.quit()

    print(str(scount) + 'Message has been sent succesfully')
    print(str(fcount) + 'Message has been sent sent failed')

# info
def head_info():
	print('[*] \t About')
	print('[*] E-mail sender')
	print('[*] Using Google SMTP server')
	print('[*] Files must be only .txt')
	print('[*] \n ______________ Shell _______________\n')


################# MAIN ###################
head_info()
menu()