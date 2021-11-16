import  urllib.request,json
from .models import Quotes



base_url = None
def configure_request(app):
  global base_url
  base_url=app.config['QUOTES_API']
  
  
def get_quotes():
  with urllib.request.urlopen(base_url)as url:
    quote_url = url.read()
    response = json.loads(quote_url)  
    
    quote_object =None
    
    if response:
      author = response.get('author')
      id = response.get('id')
      quote = response.get('quote')
      permalink= response.get('permalink')
      quote_object = Quotes(author,id,quote,permalink) 
      
  return quote_object    

