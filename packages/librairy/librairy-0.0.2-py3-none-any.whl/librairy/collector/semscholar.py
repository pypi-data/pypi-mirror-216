import json

class Semantic_Scholar():

    def __init__(self):        
        self.authors = {'authors':[]}

    def get_id(self):
        return "semscholar"

    def add_author(self,name,id):
        author = {
            'name':name,
            'id':id
        }
        self.authors['authors'].append(author)

    def get_parameters(self):
        return json.dumps(self.authors)