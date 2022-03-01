import smtplib, os, base64, random, string, pyautogui
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


########################################################################################################################
#       GLOBAL VARIABLES
########################################################################################################################
students = []

sender_email = ''
password = ''

path_0 = os.getcwd()
path = path_0 + '/Solutions'
if not os.path.exists(path):
    os.makedirs(path)
os.chdir(path)

#################################################################################
#   ENCRYPTION VARIABLES
alphabeat = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                 'u', 'v', 'w', 'x', 'y', 'z','0','1','2','3','4','5','6','7','8','9']
part_1_mssg = 'hello world. this is the first part of the message. the second part is encrypted using the base64. search online for ways to decode this kind of encryption.'

def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

#################################################################################
#   EMAIL VARIABLES


html = """\
<p>&nbsp;</p>
<p>&nbsp;</p>
<p><img style="display: block; margin-left: auto; margin-right: auto;" src="https://wallpapertag.com/wallpaper/full/2/c/0/522422-full-size-mr-robot-wallpapers-1920x1080.jpg" alt="" width="612" height="268" /><br />&nbsp;&nbsp;</p>
<h1 style="text-align: center;">HACKING CHALLENGE: PYTHON MASTERS</h1>
<h4>&nbsp;</h4>
<h4>&nbsp;</h4>
<p style="text-align: center;">You received a mysterious message from an unknown source and you want to decypher it.</p>
<p style="text-align: center;">First of all, you see the message is split in two parts (Part I i Part II).</p>
<p style="text-align: center;">You suspect the first part begins with the words <em>Hello World</em>.</p>
<p style="text-align: center;">You have no clue about Part II. We will assume you need to decode Part I to decode Part II...</p>
"""

par_beg = '<p style="text-align: center;">'
par_end = '</p>'

########################################################################################################################
#       MAIN LOOP
########################################################################################################################

#####################################################################################
#   SET UP
print('Wellcome to the Hacking Challenge creator')
while True:
    usr_entry = input('Please, enter the email address of your student (if there are no more students enter 0): ')
    if usr_entry == '0':
        break
    else:
        students.append(usr_entry)
print('I will create a directory in ', path_0, ' named Solutions with all the data you require to assess the challenge.')
sender_email = input("Please, enter the sender's email (IMPORTANT. This email account needs to have low security set up. Preferably gmail):  ")
#password = getpass.getpass(prompt='Please, enter the password of this account: ',stream=None)
password = pyautogui.password(text='Please, enter the password of this account: ', title='', default='', mask='*')

#####################################################################################
#   LOOP THROUGH ALL STUDENTS

for id in students:
    #################################################################################
    #   ENCRYPT MESSAGES

    #############################################################
    #   Part I

    tex_name = id + '.txt'
    file_1 = open(tex_name, 'w')
    plain_msg = part_1_mssg
    plain_msg_split = list(plain_msg)

    encrypt_msg_split = []
    sparator = ''

    phase = random.randint(5, 29)
    for i in range(0, len(plain_msg_split)):
        isletter = False
        for j in range(0, len(alphabeat)):
            if plain_msg_split[i] == alphabeat[j]:
                isletter = True
                encrypt_msg_split.append(alphabeat[(j + phase) % 36])
        if isletter is False: encrypt_msg_split.append(plain_msg_split[i])
    encrypt_msg = sparator.join(encrypt_msg_split)


    #file_1.write(encrypt_msg)

    mail_body = html + par_beg + 'Part I:' + par_end + par_beg + encrypt_msg + par_end

    #############################################################
    #   Part II
    flag = str(get_random_string(10))

    part_2_mssg = "You have successfully completed the challenge " + id + ". You have to hand in this flag you have found to your teacher. Congratulations!\nFlag: " + flag

    encodedBytes = base64.b64encode(part_2_mssg.encode("utf-8"))
    encodedStr = str(encodedBytes, "utf-8")

    mail_body = mail_body + par_beg + 'Part II:' + par_end + par_beg + encodedStr + par_end

    #############################################################
    #   Build Assessment File

    file_1.write('Student: '+id+'\n\n\n')
    file_1.write('Decrypted message:\n\nPartI\n'+part_1_mssg+'\n\nPart II\n'+part_2_mssg+'\n\n')
    file_1.write('Encrypted message:\n\nPart I\n'+encrypt_msg+'\n\nPart II\n'+encodedStr+'\n\n')
    file_1.write('Flag: '+flag)

    #################################################################################
    #   SEND E-MAIL
    rec_email = id
    message = MIMEMultipart("alternative")
    message["Subject"] = "You Have Been Hacked"
    message["From"] = "Mr. Robot"
    message["To"] = rec_email

    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(mail_body, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part1)

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_email, password)
    print('Login success')
    server.sendmail(sender_email, rec_email, message.as_string())
    print('Email sent')
    file_1.close()