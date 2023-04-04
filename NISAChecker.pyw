import time
import smtplib
import requests
from bs4 import BeautifulSoup
from bs4 import SoupStrainer
from datetime import datetime
import os
from os.path import exists
import secrets
from email.message import EmailMessage


TheConfigurationFile = 'F:\\Users\\dudeo\\AppData\\Local\\Programs\\Python\\Python39\\dist\\Config.txt'

logFile = 'NISA.txt'
configTXT = TheConfigurationFile

def write(log, text, datetime_option):
    if datetime_option:
        logger = open(log, 'w')
        now = datetime.now()
        dt_string = now.strftime("%m/%d/%Y %I:%M:%S %p")
        logger.write(dt_string + '\n')
        logger.write(text + '\n')
        logger.close()
    else:
        logger = open(log, 'w')
        logger.write(text + '\n')
        logger.close()

def append():
    if datetime_option:
        logger = open(log, 'a')
        now = datetime.now()
        dt_string = now.strftime("%m/%d/%Y %I:%M:%S %p")
        logger.write(dt_string + '\n')
        logger.write(text + '\n')
        logger.close()
    else:
        logger = open(log, 'a')
        logger.write(text + '\n')
        logger.close()
        
def better_sleep(time2wait):
    start = time.time()
    while((time.time()-start)<time2wait-.00042):
        time.sleep(1)
#Get email and password
def login_info():
    configFile = open(TheConfigurationFile, 'r')
    config = str(configFile.read())
    email = config.split('Email: ')
    email = email[1].split('Password: ')
    password = str(email[1].strip())
    email = str(email[0].strip()).strip()
    try:
        server = config.split('Server: ')[1]
        server = str(server.split('Email: ')[0].strip())
    except:
        print('its the server')
    try:
        port = config.split('Port: ')[1]
        port = port.split('Server: ')[0].strip()
        port = int(str(port))
    except:
        print('port also fucked up')
    try:
        app = config.split('App Pass: ')[1]
        app = app.split('Port: ')[0].strip()
        app = str(app)
    except:
        print('port also fucked up')
    configFile.close()
    return email, password, server, port, app


#email function
def email(sites):
    myEmail, myPass, theServer, thePort, theAppPassword = login_info()
    configFile = open(configTXT, 'r')
    raw_emails = configFile.readlines()
    configFile.close()
    notDone = 1
    x = 0
    #Get the list of emails for pokemon
##    while notDone > 0:
##        bad = 0
##        for line in range(0, len(raw_emails)-x, 1):
##            if ((str(raw_emails[line]).__contains__('@')) and ((str(raw_emails[line]).__contains__('.')))):
##                if (str(raw_emails[line]).__contains__('Email')):
##                    try:
##                        raw_emails[line] = raw_emails[line+1]
##                        raw_emails[line+1] = 0
##                    except:
##                        raw_emails[line] = 0
##                else:                    
##                    raw_emails[line] = str(raw_emails[line]).strip()
##            else:
##                try:
##                    raw_emails[line] = raw_emails[line+1]
##                    raw_emails[line+1] = 0
##                except:
##                    raw_emails[line] = 0
##                bad = 1
##        x=x+1
##        if bad == 0:
##            notDone = 0
##        #print(raw_emails)
##        
##    the_emails = []
##    for i in range(0, len(raw_emails), 1):
##        if raw_emails[i] != 0:
##            the_emails.append(raw_emails[i])
##            print(the_emails[i])
    #email myself
    try:
        server = smtplib.SMTP_SSL(theServer, thePort)
        server.login(myEmail, theAppPassword)
        msge = EmailMessage()
        msge.set_content(sites)
        server.send_message(msge, from_addr=myEmail, to_addrs=myEmail)
        server.quit()
    except:
        better_sleep(1)
        logger = open(logFile, 'a')
        now = datetime.now()
        dt_string = now.strftime("%m/%d/%Y %I:%M:%S %p")
        logger.write('\n')
        logger.write(dt_string + '\n')
        logger.write(str('Failed to send email to me!'))
        logger.close()
        #email the poke peeps
##    for i in range(0, len(the_emails), 1):
##        try:
##            server = smtplib.SMTP_SSL(theServer, thePort)
##            server.login(myEmail, theAppPassword)
##            msge = EmailMessage()
##            msge.set_content(sites)
##            server.send_message(msge, from_addr=myEmail, to_addrs=str(the_emails[i]))
##            server.quit()
##        except:
##            better_sleep(1)
##            logger = open(logFile, 'a')
##            now = datetime.now()
##            dt_string = now.strftime("%m/%d/%Y %I:%M:%S %p")
##            logger.write('\n')
##            logger.write(dt_string + '\n')
##            logger.write(str('Failed to send email to ' + str(the_emails[i]) + '!'))
##            logger.close()

def get_lines_between_separator(starting_separator, TheConfigFile=configTXT, ending_separator=''):
    #Opens config file and returns a list of every line betwix the separators
    starting_separator = str(starting_separator)
    if ending_separator == '':
        ending_separator = starting_separator
    else:
        ending_separator = str(ending_separator)
    spot = 0
    separatorIs = [5, 9]
    logger = open(TheConfigFile, 'r')
    desiredLines = logger.readlines()
    separators = [starting_separator, ending_separator]
    #print(desiredLines)
    for i in range(10, len(desiredLines)): #Finds starting and ending lines with relevant info
        if spot > 1:
            pass
        else:
            if desiredLines[i] == separators[spot]:
                separatorIs[spot] = i
                spot = spot + 1
                if spot == 3:
                    i = 2*2*2*2*2*2*2*2*2*2*2*2*2*2*2*2*2*2*2*2*2*2*2*2*2*2*2*2*2
    i = 0
    stuff_between_separators = []
    for i in range(separatorIs[0]+1, separatorIs[1]):#Checks through each line between first and second separator
        #print(i)
        line_no_space = desiredLines[i].split('\n')[0]
        line_no_space = str(line_no_space.rstrip())
        stuff_between_separators.append(line_no_space)
    return stuff_between_separators

def check_if_relavent(separator, have_or_have_not, TheFileOfConfiguration, bs_response):
    #Check for special temporary key words
    spot = 0
    separatorIs = [5, 9]
    logger = open(TheFileOfConfiguration, 'r')
    desiredInfoSeparators = separator + '\n'
    desiredLines = logger.readlines()
    logger.close()
    #print(desiredLines)
    for i in range(10, len(desiredLines)):
        if desiredLines[i] == desiredInfoSeparators:
            separatorIs[spot] = i
            spot = spot + 1
            if spot == 3:
                i = 2*2*2*2*2*2*2*2*2*2*2*2*2*2*2*2*2*2*2*2*2*2*2*2*2*2*2*2*2
    i = 0
    sendEmail = 0
    if have_or_have_not == 'have':
        for i in range(separatorIs[0]+1, separatorIs[1]):
            #print(i)
            line_no_space = desiredLines[i].split('\n')[0]
            line_no_space = line_no_space.strip()
##            print('1****')
##            print(line_no_space)
##            print('1****1')
            if (bs_response.__contains__(line_no_space)) and ((bs_response.__contains__('PS5')) or (bs_response.__contains__('PS4')) or (bs_response.__contains__('Switch'))):
                logger = open(logFile, 'a')
                now = datetime.now()
                dt_string = now.strftime("%m/%d/%Y %I:%M:%S %p")
                logger.write('\n')
                logger.write(dt_string + '\n')
                logger.write(str(line_no_space + ' limited edition is up for preorder'))
                logger.close()
                print(line_no_space)
                #print(desiredLines[i])
                sendEmail = 1
                i = 2*2*2*2*2*2*2*2*2*2*2*2*2*2*2*2*2*2*2*2*2*2*2*2*2*2*2*2*2 + separatorIs[1]
    if have_or_have_not == 'have not':
        for i in range(separatorIs[0]+1, separatorIs[1]):
            #print(i)
            line_no_space = desiredLines[i].split('\n')[0]
            line_no_space = line_no_space.strip()
            if not (bs_response.__contains__(line_no_space)):
                #print(desiredLines[i])
                sendEmail = 1
                i = 2*2*2*2*2*2*2*2*2*2*2*2*2*2*2*2*2*2*2*2*2*2*2*2*2*2*2*2*2 + separatorIs[1]
    return sendEmail

def clear_out_log_file(file_that_logs_info, maximum_size_in_bytes, divisor_number):
    text_file_size = os.path.getsize(file_that_logs_info)
    if text_file_size > maximum_size_in_bytes:
##        print('too big')
##        print(text_file_size)
        logger_lines = []
        #read lines first
        logger = open(file_that_logs_info, 'r')
        logger_lines = logger.readlines()
        logger.close()
        #write most of the lines
        logger = open(file_that_logs_info, 'w')
        for number, line in enumerate(logger_lines):
            if number > (len(logger_lines)/divisor_number) or number == 0:
                logger.write(line)
        logger.close()

def remove_unnecessary_shit(string):
    for index_of_character_in_string in range(0, len(string)):
        try:
            if string[index_of_character_in_string] == '$':
                characters = str(string[index_of_character_in_string]) + str(string[index_of_character_in_string+1]) + str(string[index_of_character_in_string+2]) + str(string[index_of_character_in_string+3]) + str(string[index_of_character_in_string+4])+str(string[index_of_character_in_string+5])+str(string[index_of_character_in_string+6])
                #print(characters)
                string = string.replace(characters, '')
        except:
            pass
    string = string.replace('Compare', '')
    string = string.replace('Add to Cart', '')
    string = string.replace('Summer', '')
    string = string.replace('Fall', '')
    string = string.replace('Spring', '')
    string = string.replace('January', '')
    string = string.replace('February', '')
    string = string.replace('March', '')
    string = string.replace('April', '')
    string = string.replace('June', '')
    string = string.replace('May', '')
    string = string.replace('July', '')
    string = string.replace('August', '')
    string = string.replace('September', '')
    string = string.replace('October', '')
    string = string.replace('November', '')
    string = string.replace('December', '')
    string = string.replace('Early', '')
    string = string.replace('Available', '')
    string = string.replace('Late', '')
    string = string.replace('USD', '')
    for i in range(2022, 2097):
        year = str(i)
        try:
            string = string.replace(year, '')
        except:
            pass
    for i in range(32, 1, -1):
        day = str(i) + '/'
        day_comma = str(i) + ','
        try:
            string = string.replace(day, '')
        except:
            pass
        try:
            string = string.replace(day_comma, '')
        except:
            pass
    for i in range(13, 1, -1):
        month = str(i) + '/'
        month_comma = str(i) + ','
        try:
            string = string.replace(month, '')
        except:
            pass
        try:
            string = string.replace(month_comma, '')
        except:
            pass
    string = string.replace('\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n', '\n')
    string = string.replace('\n\n\n', '\n')
    string = string.replace('\n\n', '\n')
    string = string.replace('         ', '')
    string = string.replace('		', '')
    string = string.replace('  ', '')
    string = string.replace('\n\n\n', '\n')
    string = string.replace('\n\n', '\n')
    string = string.replace('  ', '')
    string = string.replace('\n ', '\n')
    string = string.replace('\n\n', '\n')
    string = string.replace(' \n', '\n')
    string = string.replace('\n\n', '\n')
##    print('1------')
##    print(string)
##    print('------2')
    return string
                    

#Checker
def NISA(counter, past):
    s = past
    try:
        s_array = str(s)
        s_array = s_array.split('\n')
        split = 1
    except:
        print('can not split')
        split = 0
    #s = 9
    #get the sites from the configuration file
    the_site = 'https://store.nisamerica.com/preorders?product_list_limit=45'
    print(the_site)
    the_short_site = 'store.nisamerica.com/preorders?product_list_limit=45'
    msg = 'There is a new available limited edition preorder at NISA! Check out ' + the_short_site
    try:
        response = requests.get(the_site)
        site = str(response)
    except Exception as fucked:
        text = 'Its fucked.  Error is {}'.format(fucked)
        write(logFile, text, True)
        site = 'Fucked'
        print('FUCKED')
    if site != "Fucked":
        logger = open(logFile, 'a')
        now = datetime.now()
        dt_string = now.strftime("%m/%d/%Y %I:%M:%S %p")
        logger.write('\n')
        logger.write(dt_string + '\n')
        logger.write(str('NISA got response'))
        logger.close()
    bs_response = BeautifulSoup(response.text, "lxml")
    bs_response = bs_response.body.main.find(class_='products wrapper grid products-grid').getText()
    bs_response = str(bs_response)
    bs_response = remove_unnecessary_shit(bs_response)
    #print(bs_response)
    #s = 6
    if bs_response == s:
        #there was no change to the site
        #print('no change')
        s = bs_response
        sendEmail = 0
        #sendEmail = 1 # comment out this line
    else:
        #Gotta make sure the order was not shuffled
        string_with_old_stuff_removed = bs_response
        if split == 1:
            for title_index in range(0, len(s_array)):
                if( (str(s_array[title_index]) == '') or (str(s_array[title_index]) == ' ') or (str(s_array[title_index]) == '  ') ):
                    pass
                else:
                    temp_text = str(s_array[title_index]).replace(' \n', '')
                    temp_text = str(s_array[title_index]).replace('\n ', '')
                    if temp_text[len(temp_text)-1] == '\n':
                        temp_text = temp_text.replace('\n', '')
##                    print('..')
##                    print(temp_text)
##                    print('..')
                    string_with_old_stuff_removed = string_with_old_stuff_removed.replace(temp_text, '')
                    string_with_old_stuff_removed = remove_unnecessary_shit(string_with_old_stuff_removed)
        ignore_games_separator = ';;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;'
        ignore_games = get_lines_between_separator(ignore_games_separator)#, TheConfigFile=configTXT, ending_separator='')
        print('ignored games list:\n{}'.format(str(ignore_games)))
        print('string_with_old_stuff_removed before ignored games list:\n{}'.format(string_with_old_stuff_removed))
        for game in ignore_games:
            string_with_old_stuff_removed.replace(game, 'Ignored')
        sep = '`````````````````````````````````````````````````````````````````````````'
        #print('stuff:\n' + string_with_old_stuff_removed)
        print('string_with_old_stuff_removed after ignored games list:\n{}'.format(string_with_old_stuff_removed))
        sendEmail = check_if_relavent(sep, 'have', TheConfigurationFile, string_with_old_stuff_removed)
        print('sendEmail = ' + str(sendEmail))
        s = bs_response
                    
        #sendEmail = 1 # comment out this line
    if counter > 0:
        if sendEmail == 1:
            #print('sending email')
            try:
                email(str(msg)+'\n\n'+string_with_old_stuff_removed+'\n\n'+str(s))
            except:
                email(str(msg))
            logger = open(logFile, 'a')
            now = datetime.now()
            dt_string = now.strftime("%m/%d/%Y %I:%M:%S %p")
            logger.write('\n')
            logger.write(dt_string + '\n')
            logger.write('New Limited Edition!\n')
            logger.close()
        else:
            #print('not sending email')
            logger = open(logFile, 'a')
            now = datetime.now()
            dt_string = now.strftime("%m/%d/%Y %I:%M:%S %p")
            logger.write('\n')
            logger.write(dt_string + '\n')
            logger.write('No New Info\n')
            logger.close()
    else:
        logger = open(logFile, 'a')
        now = datetime.now()
        dt_string = now.strftime("%m/%d/%Y %I:%M:%S %p")
        logger.write('\n')
        logger.write(dt_string + '\n')
        logger.write('Just started.  Not sending the email. \n')
        logger.close()
        pastsoup = s
    msg = 'Go to: '
    sendEmail = 0
    return s


def main():
    #email('This is a test.  Current BDSP events are Shayman.  Connect to Mystery Gift internet.  Starting April 1st to April 30th connect to MG internet and get Darkrai.  I love you a ton and once I finish school I promis Ill have more game time for you <3')
    z = 0
    count = 0
    daycount = count
    past = 0
    if(exists(logFile)):
        pass
    else:
        logger = open(logFile, 'w')
        logger.write('This is the log of stuff:' + '\n')
        logger.close()
    while z < 30:
        # should do the initializing
        # wont send email.  Just doing set up
        if count == 0:
            past_soup = NISA(count,  past)
        #now the set up is done do the check for real
        if count > 0:
            now = datetime.now()
            today = now.strftime("%S")
            if today == 'deez nuts':
                print('there is something really wrong')
            else:
                try:
                    past_soup = NISA(count, past_soup)
                except:
                    msg = 'There was a main() error on NISA. Maybe check Nippon Ichi Software America'
                    email(msg)
                    logger = open(logFile, 'a')
                    now = datetime.now()
                    dt_string = now.strftime("%m/%d/%Y %I:%M:%S %p")
                    logger.write('\n')
                    logger.write(dt_string + '\n')
                    logger.write('There was a main() error. \n' + '\n')
                    logger.close()
                past = today
                daycount = daycount + 1
        time.sleep(secrets.randbelow(777))
        clear_out_log_file(logFile, 4444444, 4)
        count = count + 1
        #print(count)

        time.sleep(666)
        
if __name__ == '__main__':
    main()








