import pandas as pd 
import numpy as np
from admin_api.models import Lead
from auth_api.models import User, Employee


def assign_leads():
    employees = Employee.objects.filter(type="sales")
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
            
    return "hello"


def get_leads(lead_sheet):
    df = pd.read_excel(lead_sheet)
    df = df.to_numpy()
    for row in df:
        name,  contact = row
        source = 'A'
        # print(f'row details: {name} {contact} {source}')
        
        lead = Lead(
            name=name,
            contact_number=contact,
            source=source
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
    
    leads = Lead.objects.all()    
    assign_leads()                
    return leads