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
import shutil


TheConfigurationFile = 'F:\\Users\\dudeo\\AppData\\Local\\Programs\\Python\\Python39\\dist\\Config.txt'

logFile = 'NISA.txt'
configTXT = TheConfigurationFile
the_site = 'https://store.nisamerica.com/collections/preorder?sort_by=manual&filter.v.availability=1&filter.v.price.gte=&filter.v.price.lte='
the_short_site = 'store.nisamerica.com/preorders?product_list_limit=45'

def write(log, text, datetime_option):
    if datetime_option:
        logger = open(log, 'w')
        now = datetime.now()
        dt_string = now.strftime("%m/%d/%Y %I:%M:%S %p")
        logger.write(dt_string + '\n')
        print(text)
        logger.write(text + '\n')
        logger.close()
    else:
        logger = open(log, 'w')
        logger.write(text + '\n')
        logger.close()

def append(log, text, datetime_option):
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
    time.sleep(time2wait)
    
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
            if (desiredLines[i] == separators[spot]) or (desiredLines[i]+'\n' == separators[spot]) or (desiredLines[i].__contains__(separators[spot])):
                separatorIs[spot] = i
                print(i, desiredLines[i])
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

def contains_console(string):
    string_list = string.split('\n')
    sep = '?????????????????????????????????????????????????????????????????????????'
    list_of_consoles = get_lines_between_separator(sep, configTXT)
    new_string = ''
    for string in string_list:
        if string.__contains__('Ignored'):
            pass
        elif string == 'Coming':
            pass
        else:
##            for console in list_of_consoles:
##                if string.__contains__(console):
##                    new_string = new_string + string + '\n'
            new_string = new_string + string + '\n'
    return new_string
    #return string

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
            if (bs_response.__contains__(line_no_space)):# and ((bs_response.__contains__('PS5')) or (bs_response.__contains__('(')) or (bs_response.__contains__('Switch'))):
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
    #print(string)
    string = string.replace('9 - $', '9 $')
##    for index_of_character_in_string in range(0, len(string)):
##        try:
##            if string[index_of_character_in_string] == '$':
##                characters = str(string[index_of_character_in_string]) + str(string[index_of_character_in_string+1]) + str(string[index_of_character_in_string+2]) + str(string[index_of_character_in_string+3]) + str(string[index_of_character_in_string+4])+str(string[index_of_character_in_string+5])+str(string[index_of_character_in_string+6])
##                #print(characters)
##                string = string.replace(characters, '')
##        except:
##            pass
    for cents in range(0, 100000):
        dollar = str(format(round(cents / 100, 2), '.2f'))
        dollar = '$' + dollar
        if string.__contains__(dollar):
            #print(dollar)
            string = string.replace(dollar, '')
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
    string = string.replace('Sale price', '')
    string = string.replace('Preorder', '')
    string = string.replace('View Product', '')
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


def try_to_fix(msg):
    msg = str(msg)
    if msg.lower().__contains__('not find a suitable'):
        path = msg.replace('Could not find a suitable TLS CA certificate bundle, invalid path: ', '')
        path = path.replace('\\cacert.pem', '')
        path = path.strip()
        missing_dir = 'F:\\Users\\dudeo\\AppData\\Local\\Programs\\Python\\Python39\\certifi'
        try:
            shutil.copytree(missing_dir, path)
            return True
        except Exception as err:
            append(logFile, 'well I tried'+str(err), True)
            print(err)
            return False
    else:
        return False

#Checker
def NISA(counter, past):
    s = past
    try:
        append(logFile, s, True)
    except Exception as stry:
        append(logFile, str(stry)+' --> roughly line 360', True)
    try:
        s_array = str(s)
        s_array = s_array.split('\n')
        split = 1
    except:
        print('can not split')
        split = 0
    #s = 9
    #get the sites from the configuration file
    print(the_site)
    msg = 'There is a new available limited edition preorder at NISA! Check out ' + the_short_site
    try:
        response = requests.get(the_site)
        site = str(response)
    except Exception as fucked:
        text = 'Its fucked.  Error is {}'.format(fucked)
        append(logFile, text, True)
        fixed = try_to_fix(fucked)
        if fixed:
            try:
                response = requests.get(the_site)
                site = str(response)
            except Exception as err:
                site = 'Fucked'
                append(logFile, 'It said fixed but still errored: '+str(err), True)
        else:
            site = 'Fucked'
            response = '11037 Fuck me 11037'
        print('FUCKED')
    if site != "Fucked":
        logger = open(logFile, 'a')
        now = datetime.now()
        dt_string = now.strftime("%m/%d/%Y %I:%M:%S %p")
        logger.write('\n')
        logger.write(dt_string + '\n')
        logger.write(str('NISA got response\n'))
        logger.close()
        bs_response = BeautifulSoup(response.text, "lxml")
        bs_response = bs_response.body
    else:
        logger = open(logFile, 'a')
        now = datetime.now()
        dt_string = now.strftime("%m/%d/%Y %I:%M:%S %p")
        logger.write('\n')
        logger.write(dt_string + '\n')
        logger.write(str('NISA could not get a response\n'))
        logger.close()
        bs_response = None#BeautifulSoup(response.text, "lxml")
        bs_response = None#bs_response.body
    #print(bs_response)
    if bs_response == None:
        append(logFile, 'The body response is None', True)
        NoneResponse = True
        bs_response = 'None'
    else:
        bs_response = bs_response.find(class_='product-list__inner').getText()
        bs_response = str(bs_response)
        bs_response = remove_unnecessary_shit(bs_response)
        NoneResponse = False
    #print(bs_response)
    #exit()
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
            string_with_old_stuff_removed = string_with_old_stuff_removed.replace(game.strip(), 'Ignored')
        string_with_old_stuff_removed = contains_console(string_with_old_stuff_removed)
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
            if NoneResponse:
                try:
                    email('store.nisamerica.com/preorders?product_list_limit=45 seems to be down')
                except:
                    email('store.nisamerica.com/preorders?product_list_limit=45 seems to be down')
                logger = open(logFile, 'a')
                now = datetime.now()
                dt_string = now.strftime("%m/%d/%Y %I:%M:%S %p")
                logger.write('\n')
                logger.write(dt_string + '\n')
                logger.write('NISA is down.  Will wait an additional 39.96 minutes\n')
                print('Will wait an additional 39.96 minutes')
                logger.close()
                time.sleep(60*60*.666)
            else:
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
                except Exception as mainerr:
                    msg = 'There was a main() error on NISA. Maybe check store.nisamerica.com/preorders?product_list_limit=45'
                    email(msg + '\n' + str(mainerr))
                    logger = open(logFile, 'a')
                    now = datetime.now()
                    dt_string = now.strftime("%m/%d/%Y %I:%M:%S %p")
                    logger.write('\n')
                    logger.write(dt_string + '\n')
                    logger.write('There was a main() error. \n' + '\n')
                    logger.close()
                past = today
                daycount = daycount + 1
        if count == 0:
            print('short sleep')
            time.sleep(secrets.randbelow(7))
        else:
            time.sleep(secrets.randbelow(777))
        clear_out_log_file(logFile, 4444444, 4)
        if count == 0:
            print('shorter sleep')
            time.sleep(6)
        else:
            time.sleep(666)
        count = count + 1
        #print(count)

        
if __name__ == '__main__':
    main()
