from django.shortcuts import render
from django.template import RequestContext, loader
from django.views import generic

# Create your views here.
from django.http import HttpResponse
from sentimentsamples.models import Opinion

from TwitterCrawler.TwitterCrawler import  *
import sys
#import os
#os.environ["PYTHONPATH"] = ("..\\..\\sentimentanalysis")
#sys.path.append("C:\\Non_valeo\\Research\\PostDoc\\Sentiment Analysis\\Code\\sentimentanalysis")
#sys.path.append("..\\..\\sentimentanalysis")
from datasetbuilder.DatasetBuilder import DatasetBuilder
from languagemodel.LanguageModel import LanguageModel   
from featuresextractor.FeaturesExtractor import FeaturesExtractor
from classifiers.Classifier import Classifier

twitterCrawler = None
polarityStyle = {'Positive' : 'alert alert-success', 'Negative' : 'alert alert-danger', 'Neutral' : 'alert alert-warning'}

# Start the DatasetBuilder
#-------------------------
# Configurations file xml of the dataset builder
import os
print(os.getcwd())
configFileDatasetBuilder = "sentimentanalysis\\configurations\\Configurations_DatasetBuilder.xml"

datasetSerializationFile = "sentimentanalysis\\output_results\\results_tweets.bin"

# Initialize the DatasetBuilder from serialization file
datasetBuilder = DatasetBuilder(configFileDatasetBuilder, [], datasetSerializationFile)

# Start the LanguageModel
#-------------------------
# Configurations file xml of the language model
configFileLanguageModel = "sentimentanalysis\\configurations\\Configurations_LanguageModel-lexicon.xml"

#positiveLangModelTxtLoadFile = ".\\LanguageModel\\Input\\Eshrag-positive.txt"
positiveLangModelTxtLoadFile = "sentimentanalysis\\input_data\\positive.txt"
#negativeLangModelTxtLoadFile = ".\\LanguageModel\\Input\\Eshrag-negative.txt"
negativeLangModelTxtLoadFile = "sentimentanalysis\\input_data\\negative.txt"
stopWordsFileName = "sentimentanalysis\\input_data\\stop_words.txt"
# The serialization file to save the model
languageModelSerializationFile = "sentimentanalysis\\LanguageModel\\Output\\language_model.bin"

# Start the LanguageModel:

# Initialize the LanguageModel
languageModel = LanguageModel(configFileLanguageModel, stopWordsFileName, [], [], [])
languageModel.LoadSentimentLexiconModelFromTxtFile(positiveLangModelTxtLoadFile, 1)
languageModel.LoadSentimentLexiconModelFromTxtFile(negativeLangModelTxtLoadFile, -1)

# Start the FeaturesExtractor:
#-----------------------------
# Configurations file xml of the features extractor
configFileFeaturesExtractor = "sentimentanalysis\\configurations\\Configurations_FeaturesExtractor-Lexicon.xml"
exportFileName = "sentimentanalysis\\\output_results\\features.txt"
 


# Start the Classifier:
#----------------------
# The serialization file to save the features
configFileClassifier = "sentimentanalysis\\configurations\\Configurations_Classifier-lexicon.xml"





def main(request):
    
    # Handle the query
    #--------------------    
    try:
        # Get the query entered by the user
        query = request.GET['searchbox']
        
        # Start the TwitterCrawler
        import os        
        BASE_DIR = os.path.dirname(os.path.dirname(__file__))
        configFileCrawler = os.path.join(BASE_DIR, 'TwitterCrawler','Configurations', 'Configurations.xml')
        twitterCrawler = TwitterCrawler(configFileCrawler, None, None, None)
        results = twitterCrawler.SearchQueryAPI(query, -1, -1)
        print('Crawling finished')
        #showsome(query)
        
        # Update the DB
        for result in results:
            datasetBuilder.trainSet = []
            datasetBuilder.trainSet.append({'label': 'Positive', 'text':result['text']})
            # Initialize the FeaturesExtractor
            testFeaturesExtractor = FeaturesExtractor(configFileFeaturesExtractor, [], [], languageModel, datasetBuilder.trainSet)
            testFeaturesExtractor.ExtractLexiconFeatures()
            classifier = Classifier(configFileClassifier, [],  None, None, testFeaturesExtractor.features, testFeaturesExtractor.labels)
            sentiment_lexicon_predicted = classifier.LexiconPredict(testFeaturesExtractor.features[0])
            print(sentiment_lexicon_predicted)
            #sentiment_lexicon_predicted = 1
            opinion = Opinion(text=result['text'], sentiment=sentiment_lexicon_predicted, source_url='https://twitter.com/search?q='+query)        
            opinion.save()
        
    except Exception as e:
        # No query entered
        query = ""
            
    # Render the response
    #--------------------   
            
    # Load the main page template
    template = loader.get_template('sentimentsamples/main.html')
    
    # Fill the query list
    opinion_list = Opinion.objects.order_by('text')[:1000]
    
    # Render with the query
    context = RequestContext(request, {'query': query, 'opinion_list' : opinion_list})
   
    return HttpResponse(template.render(context))

import json
import urllib.request, urllib.parse

def showsome(searchfor):
  query = urllib.parse.urlencode({'q': searchfor})
  url = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&%s' % query
  search_response = urllib.request.urlopen(url)
  search_results = search_response.read().decode("utf8")
  results = json.loads(search_results)
  data = results['responseData']
  print('Total results: %s' % data['cursor']['estimatedResultCount'])
  hits = data['results']
  print('Top %d hits:' % len(hits))
  for h in hits: print(' ', h['url'])
  print('For more results, see %s' % data['cursor']['moreResultsUrl'])
