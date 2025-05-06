
import datetime
support_menus = {1:"create a new ticket",2:"view all tickets",3:"update ticket"}
tickets = []

def showSupportMenus():
    for i in support_menus.keys():
        print(f"{i}. {support_menus[i]}")
    return

def generateUniqueTicketId():
    presentDate = datetime.datetime.now()
    return int(datetime.datetime.timestamp(presentDate))

def stringFormatter(string):
    return string.lower().strip()

def promptInputer(type,input_message):
    type = stringFormatter(type)
    user_input = ''
    if type == 'int':
        user_input = int(input(input_message))
    else:
        user_input = input(input_message)
        user_input = stringFormatter(user_input)
    if user_input:
        return user_input
    else:
        print('Invalid user input')
        return False

def inputValidator(input):
    return True
def createNewTicket():
    new_ticket = {
        "id": "CLD-2024-001",
        "submitter": "user@company.com",
        "date": "2024-01-15 14:30",
        "priority": "High",
        "status": "Open",
        "cloud_provider": "AWS",
        "issue_type": "Access",
        "resource_id": "i-1234567890abcdef0",
        "description": "Cannot SSH into EC2 instance",
        "resolution_notes": ""
    }
    unq_ticket_id = generateUniqueTicketId()
    if priority := promptInputer('str',"Enter the priority for this ticket"):
        print(priority)




while True:
    showSupportMenus()
    menu_index = int(input("Enter the menu index(1-"+str(len(support_menus.keys()))+"):\n"))
    if menu_index < 1 or menu_index > len(support_menus.keys()):
        print("Invalid Index\n")
        continue
    if menu_index == 1:
        print("----------------------- creating a new ticket-------------------------")
        createNewTicket()
