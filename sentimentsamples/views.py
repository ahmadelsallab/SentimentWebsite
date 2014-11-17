from django.shortcuts import render
from django.template import RequestContext, loader
from django.views import generic

# Create your views here.
from django.http import HttpResponse
def main(request):
    # Get the query entered by the user
    #On first request there is no form data submitted so request.GET would not have any data. So doing request.GET['pub_date_from'] will fail. You shall use .get() method
    #query = request.GET['searchbox'] 
    try:
        query = request.GET['searchbox']
    except:
        # The first load will have no keys in GET dict.
        query = ""
    
    # Load the main page template
    template = loader.get_template('sentimentsamples/main.html')
    
    # Fill the query list
    query_list = ['One', 'Two', 'Three']
    # Render with the query
    context = RequestContext(request, {'query': query, 'query_list' : query_list})
   
    return HttpResponse(template.render(context))

