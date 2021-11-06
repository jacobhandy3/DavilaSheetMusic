import csv
import datetime
from django.http import HttpResponse

def export_to_csv(modelAdmin,request,queryset):
    """
    Added functionality to Django's model admin page where the query set data from a given model
    will be outputted to a csv file that will be downloaded by the client
    """
    #Initialize the response:
    #get info from associated model for content disposition
    opts = modelAdmin.model._meta
    # prepare content disposition in http response for csv files
    content_disp = "attachment;filename=%s.csv"%opts.verbose_name
    #create the response as a text/csv
    response = HttpResponse(content_type="text/csv")
    #set content disposition 
    response["Content-Disposition"] = content_disp

    #Prepare the csv file to be written:
    #create a csv writer with the response csv file
    writer = csv.writer(response)
    #get the header of the model as a list using the info from the associated model excl. table relationships
    header = [field for field in opts.get_fields() if not field.many_to_many and not field.one_to_many]
    #write the header to the response csv file
    writer.writerow([field.verbose_name for field in header])

    #Write to the csv file:
    data_row = []
    #loop through every object
    for obj in queryset:
        data_row = []
        #loop through each of its fields
        for field in header:
            #get the value
            value = getattr(obj,field.name)
            #if it is a timestamp, convert to string
            if isinstance(value,datetime.datetime):
                value = value.strftime("%m/%d/%Y")
            #append to list
            data_row.append(value)
        #write current row to response csv file
        writer.writerow(data_row)
    #return csv file as an http response
    return response
#names the function in model admin
export_to_csv.short_description = "Export to CSV"