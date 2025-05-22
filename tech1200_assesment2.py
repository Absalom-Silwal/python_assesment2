import re
from datetime import datetime
from dateutil.relativedelta import relativedelta


support_menus = {1:"Create a new ticket",2:"View all tickets",3:"Update ticket",4:"Exit"}
#priority_levels = ["high","medium","low"]
priority_levels =[
    {"label":"High","value":"High","description":"Critical Issues"},
    {"label":"Medium","value":"medium","description":"Moderate Issues"},
    {"label":"Low","value":"medium","description":"Minor Issues"}
]
#cloud_providers = ["aws",'azure',"gcp"]
cloud_providers = [
    {"label": "AWS", "description": "Amazon Web Services – scalable cloud computing services", "value": "aws"},
    {"label": "Azure", "description": "Microsoft Azure – cloud platform for building, testing, and managing apps","value": "azure"},
    {"label": "GCP", "description": "Google Cloud Platform – infrastructure, platform, and serverless computing","value": "gcp"}
]
#issue_types = ["access","performance","others"]
issue_types =[
    {"label": "Access", "description": "Unable to log in or insufficient permissions", "value": "access"},
    {"label": "Performance", "description": "Slow system, high latency, or degraded services", "value": "performance"},
    {"label": "Others", "description": "General or uncategorized issues", "value": "others"}
]
#statuses = ['open','closed']
statuses =[
    {"label": "Open", "description": "Issue is pending resolution", "value": "open"},
    {"label": "Closed", "description": "Issue has been resolved or dismissed", "value": "closed"}
]
#ticket_filter_options = ['all','status','priority','issue','provider']
ticket_filter_options =[
    {"label": "All", "description": "Show all tickets without filtering", "value": "all"},
    {"label": "Status", "description": "Filter tickets by their current status (Open/Closed)", "value": "status"},
    {"label": "Priority", "description": "Filter based on ticket urgency level", "value": "priority"},
    {"label": "Issue Type", "description": "Filter by the type of cloud issue reported", "value": "issue"},
    {"label": "Cloud Provider", "description": "Filter by cloud platform (AWS, Azure, GCP)", "value": "provider"}

]
#ticket_filter_date_options = ['This Month','Last 2 Month','Last 3 Month']
ticket_filter_date_options=[
    {"label": "This Month", "description": "Show tickets created in the current month", "value": "this_month"},
    {"label": "Last 2 Months", "description": "Show tickets from the last two calendar months","value": "last_2_months"},
    {"label": "Last 3 Months", "description": "Show tickets from the last three calendar months","value": "last_3_months"}
]

filter_config={
    "all":{
        "choices":None,
        "label":"Showing all tickets",
        "field":None
    },
    "status":{
        "choices":statuses,
        "label":"Ticket filtered based on {} Status",
        "field":"status"
    },
    "priority":{
        "choices":priority_levels,
        "label":"Ticket filtered based on {} Priority",
        "field":"priority"
    },
    "issue":{
        "choices":issue_types,
        "label":"Ticket filtered based on {} Issue",
        "field":"issue_type"
    },
    "provider":{
        "choices":cloud_providers,
        "label":"Ticket filtered based on {} Provider",
        "field":"cloud_provider"
    }
}

filter_date_config={
    "this_month":{
        "label":"This month",
        "offsets":[0]
    },
    "last_2_months":{
        "label":"Last 2 months",
        "offsets":[0,1]
    },
    "last_3_months":{
        "label":"Last 3 months",
        "offsets":[0,1,2]
    }
}
agree_list =['y','yes']
tickets = []

def showSupportMenus():
    print("\n--------------------------------------------Showing Cloud Support System Menus--------------------------")
    for i in support_menus.keys():
        print(f"{i}. {support_menus[i]}")
    return

def generateUniqueTicketId():
    presentDate = datetime.now()
    return 'Tkt-'+str(int(datetime.timestamp(presentDate)))

def stringFormatter(string):
    return string.lower().strip()

def dateFormatter(time_stamp,formatter):
    dt_object = datetime.strptime(stringFormatter(time_stamp), "%Y-%m-%d %H:%M:%S")
    return dt_object.strftime(formatter)

def isemailValid(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

def selectOption(options,prompt,return_str=True):
    print(f"{prompt.replace("{}","")}")
    for option_index in range(1,len(options)+1):
        option = options[option_index-1]
        print(f"{option_index}. {option['label']} - {option['description']}")
    choice = int(input(f"Enter the number of your choice(1-{len(options)})\n"))
    if choice < 1 or choice > len(options):
        print("Invalid choice.please try again")
        return False
    selected_choice = options[choice-1]
    #print(f"Your selected option is:{selected_choice['label']}\n")
    return selected_choice


def userInput(type,input_message):
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

def ticketFilter(ticket_list,filter_key,filter_value):
    return [ticket for ticket in ticket_list if ticket[filter_key]['value']== filter_value ]

def createNewTicket():
    print("----------------------- creating a new ticket-------------------------")
    unq_ticket_id = generateUniqueTicketId()
    submitter = userInput('str', "Enter your email: ")
    if not isemailValid(submitter):
        print('Invalid email')
        return False
    current_date_time_in_unix = datetime.now()
    created_date = current_date_time_in_unix.strftime("%Y-%m-%d %H:%M:%S")
    priority = selectOption(priority_levels,"Select Priority")
    cloud_provider = selectOption(cloud_providers,"Select cloud providers")
    issue_type = selectOption(issue_types,"Select issue types")
    resource_id = userInput('str', "Enter the resource ID: ")
    description = userInput('str', "Describe the issue: ")
    status = [status for status in statuses if status['value']=='open'][0]
    if False in (submitter, priority, cloud_provider, issue_type, resource_id, description):
        print("Ticket creation failed due to invalid input.")
        return False

    new_ticket = {
        "id": unq_ticket_id,
        "submitter": submitter,
        "priority": priority,
        "status": status,
        "cloud_provider": cloud_provider,
        "issue_type": issue_type,
        "resource_id": resource_id,
        "description": description,
        "resolution_notes": "",
        "issue_date": created_date,
        "resolved_date":""
    }
    #tickets.append(new_ticket)
    tickets.append(new_ticket)
    print("Ticket created successfully!")
    return True

def viewTickets():
    selected_option = selectOption(ticket_filter_options,'Select Ticket filter options')
    if selected_option:
        selected_option_value = selected_option['value']
        filter_choice= filter_config[selected_option_value]
        if filter_choice["field"] == None:
            #This is for all case
            filterTicketsBasedOnDate(tickets,filter_choice["label"])
            return
        choices = filter_choice["choices"]
        label = filter_choice["label"]
        field = filter_choice["field"]
        user_category_choice = selectOption(choices,filter_choice["label"])
        #filtered_list = [ticket for ticket in tickets if ticket[field]['value']==user_category_choice['value']]
        filtered_list = ticketFilter(tickets,field,user_category_choice['value'])
        label = label.replace("{}",user_category_choice['label'])
        filterTicketsBasedOnDate(filtered_list,label)
        return

def filterTicketsBasedOnDate(ticket_list,filter_prompt):
    date_choice = selectOption(ticket_filter_date_options,"Select Below Filtered Dates")
    current_month = datetime.strptime(datetime.now().strftime("%Y-%m"), "%Y-%m")
    month_list = []
    filter_date_range = date_choice['value']
    filter_date = filter_date_config[filter_date_range]
    label = filter_date["label"]
    offsets = filter_date["offsets"]
    month_list = [
            (current_month - relativedelta(months=offset)).strftime("%Y-%m")
            for offset in offsets
        ]
    filtered_tickets = [ticket for ticket in ticket_list if dateFormatter(ticket['issue_date'],"%Y-%m") in month_list]
    showAllTickets(filtered_tickets,filter_prompt+" of "+label)
    return


def showAllTickets(filtered_tickets,filter_prompt):
    print(f"------------------------------------{filter_prompt}-----------------------------------")
    if len(filtered_tickets)<= 0:
        print("Tickets not available")
        return
    for ticket in filtered_tickets:
        formatted_issued_date = dateFormatter(ticket['issue_date'],"%#d %B, %Y at %#I:%M %p")
        print(f"ID: {ticket['id']}")
        print(f"Priority: {ticket['priority']['value']}")
        print(f"Status: {ticket['status']['value']}")
        print(f"Issue Type: {ticket['issue_type']['value']}")
        print(f"Cloud Provider: {ticket['cloud_provider']['value']}")
        print(f"Description: {ticket['description']}")
        print(f"Issue Date: {formatted_issued_date}")
        if stringFormatter(ticket['status']['value']) == 'closed':
            formatted_resolved_date = dateFormatter(ticket['resolved_date'],"%#d %B, %Y at %#I:%M %p")
            print(f"resolved date: {formatted_resolved_date}")
        print('\n')

def updateExistingTicket():
    print("----------------------------Updating existing Ticket----------------------------------")
    if len(tickets)<=0:
        print("Tickets not available")
        return
    showAllTickets(tickets,"Showing All Tickets")
    ticket_id = userInput('str','Enter the id of the ticket which you want to update: ')
    if ticket_id:
        for ticket in tickets:
            if stringFormatter(ticket['id']) == stringFormatter(ticket_id):
                status_change = userInput('str','Would you like to change the status of this ticker(Y/N)')
                if stringFormatter(status_change) in agree_list:
                    updated_status = selectOption(statuses,'Select Status')
                    if updated_status:
                        ticket['status'] = updated_status
                        if updated_status['value'] == 'closed':
                            ticket['resolved_date'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                priority_change = userInput('str','Would you like to change the priority of this ticket(Y/N): ')
                if stringFormatter(priority_change) in agree_list:
                    updated_priority = selectOption(priority_levels,'Select Priorities')
                    if updated_priority:
                        ticket['priority'] = updated_priority
                print('Ticket updated Sucessfully')
                return
        print("Ticket not found")
        return
    return

interaction_count = 0
while True:
    if interaction_count != 0 and interaction_count % 3 == 0:
        show_unresolved_tickets = userInput('str','Want to see unresolved tickets(y/n)?')
        if show_unresolved_tickets in agree_list:
            status_filtered_list = ticketFilter(tickets, 'status', 'open')
            showAllTickets(status_filtered_list,'List of All Unresolved Tickets')
    showSupportMenus()
    user_choice = int(input("Enter the menu index(1-"+str(len(support_menus.keys()))+"):\n"))
    if user_choice < 1 or user_choice > len(support_menus.keys()):
        print("Invalid Index\n")
        continue
    if user_choice == 1:
        createNewTicket()
    elif user_choice == 2:
        viewTickets()
    elif user_choice == 3:
        updateExistingTicket()
    elif user_choice == 4:
        print("System is Closing...Goodbye!")
        break
    interaction_count += 1