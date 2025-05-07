
from datetime import datetime


support_menus = {1:"create a new ticket",2:"view all tickets",3:"update ticket"}
priorities = ["high","medium","low"]
cloud_providers = ["aws",'azure',"gcp"]
issue_types = ["access","performance","others"]
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

def selectOption(options,prompt):
    print(f"{prompt}")
    for option_index in range(1,len(options)+1):
        print(f"{option_index}. {options[option_index-1]}")
    selected_index = int(input(f"Enter the number of your choice(1-{len(options)})\n"))
    if selected_index < 1 or selected_index > len(options):
        return False
    print(f"Your selected option is: {options[selected_index-1]}\n")
    return options[selected_index-1]


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
        return False


def createNewTicket():
    print("----------------------- creating a new ticket-------------------------")
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
    submitter = promptInputer('str', "Enter your email: ")
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    priority = selectOption(priorities,"Select Priority")
    cloud_provider = selectOption(cloud_providers,"Select cloud providers")
    issue_type = selectOption(issue_types,"Select issue types")
    resource_id = promptInputer('str', "Enter the resource ID: ")
    description = promptInputer('str', "Describe the issue: ")

    if False in (submitter, priority, cloud_provider, issue_type, resource_id, description):
        print("Ticket creation failed due to invalid input.")
        return False

    new_ticket = {
        "id": unq_ticket_id,
        "submitter": submitter,
        "date": date,
        "priority": priority,
        "status": "Open",
        "cloud_provider": cloud_provider,
        "issue_type": issue_type,
        "resource_id": resource_id,
        "description": description,
        "resolution_notes": ""
    }

    tickets.append(new_ticket)
    print("Ticket created successfully!")
    return True

def showAllTickets():
    print("------------------------------------Showing All tickets-----------------------------------")
    if len(tickets)<= 0:
        print("Tickets not available")
        return
    for ticket in tickets:
        print(ticket)
        print(f"id: {ticket['id']}")
        print(f"status: {ticket['status']}")
        print(f"description: {ticket['description']}")
        print(f"issue date: {ticket['date']}\n")




while True:
    showSupportMenus()
    menu_index = int(input("Enter the menu index(1-"+str(len(support_menus.keys()))+"):\n"))
    if menu_index < 1 or menu_index > len(support_menus.keys()):
        print("Invalid Index\n")
        continue
    if menu_index == 1:
        createNewTicket()
    elif menu_index == 2:
        showAllTickets()