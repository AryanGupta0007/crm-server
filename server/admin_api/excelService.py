from django.db import transaction
import pandas as pd 
import numpy as np
from admin_api.models import Lead, LeadBoardScore, LeadAccountStatus, LeadOperationStatus, LeadSaleStatus
from auth_api.models import User, Employee
import time 

def assign_leads():
    employees = Employee.objects.filter(type="sales")
    time3 = time.time()
    for employee in employees:
        unassigned_leads = Lead.objects.filter(assigned_to=None).all()
        try:
            i = int(employee.allot)
        except:
            i=5
        new_leads = unassigned_leads[:i]
        for lead in new_leads:
            print(f"{lead} assigned to {employee.user}")
            lead.assigned_to = employee.user       
    time4 = time.time()
    print(f'time taken to assign leads {time4-time3}s')
    return "hello"

@transaction.atomic
def get_leads(lead_sheet):
    df = pd.read_excel(lead_sheet)
    df = df.to_numpy()
    i = 0
    time1 = time.time()
    for row in df:
        
        name,  contact, source = row
        print(f'{i} row details: {name} {contact} {source}')
        
        lead = Lead(
            name=name,
            contact_number=contact,
            source=source
            )
        lead_board_score = LeadBoardScore(
            lead=lead
        )
        lead_account_status = LeadAccountStatus(
            lead=lead
        )
        lead_sale_status = LeadSaleStatus(
            lead=lead
        )
        lead_operation_status = LeadOperationStatus(
            lead=lead
        )
        
        if (Lead.objects.filter(contact_number=contact).exists()):
            print('lead assigned to a user')
            existing_lead = Lead.objects.filter(contact_number=contact).first()
            print(existing_lead.name)
            if (existing_lead.assigned_to):
                assigned_to = existing_lead.assigned_to
                lead.assigned_to = assigned_to
                print(assigned_to)
            existing_lead.delete()   
        lead.save()
        lead_account_status.save()
        lead_board_score.save()
        lead_sale_status.save()
        lead_operation_status.save()
        i += 1
    time2 = time.time()
    print(f'time taken to assign leads {time2-time1}s')
    leads = Lead.objects.all()    
    assign_leads()                
    return leads