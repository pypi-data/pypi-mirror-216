
[![Downloads](https://static.pepy.tech/badge/librairy)](https://pepy.tech/project/librairy)
[![Current Release Version](https://img.shields.io/github/release/librairy/driver.svg?style=flat-square&logo=github)](https://github.com/librairy/driver/releases)
[![pypi Version](https://img.shields.io/pypi/v/claimer.svg?style=flat-square&logo=pypi&logoColor=white)](https://pypi.org/project/librairy/)
# librAIry Driver

## Introduction

*librAIry driver* simplifies the integration process and empowers developers to leverage the powerful [librAIry system](https://librairy.eu/) for managing and analyzing large-scale multilingual documents. With its easy-to-use driver implementation and comprehensive features, the module facilitates efficient document management, language-specific processing, and information retrieval from the librAIry system. 

### Key Features:

- **Easy Integration**: The module offers a straightforward integration process for developers. It provides a well-documented and easy-to-use driver implementation that connects with the librAIry system. Developers can quickly incorporate the librAIry functionalities into their own applications or systems without significant overhead.

- **Document Management**: With the librAIry-Driver, managing large-scale multilingual documents becomes effortless. The driver provides methods for document ingestion, enabling users to import documents in various formats such as PDF, plain text, Word documents, and more. It also offers functionalities for organizing and categorizing the documents within the librAIry system.

- **Multilingual Support**: The driver enables seamless handling of multilingual documents. It leverages librAIry's AI capabilities to automatically detect the language of each document, allowing for effective organization and processing of multilingual content. Users can work with documents in different languages without the need for language-specific configurations.

- **Search and Retrieval**: The librAIry-Driver facilitates efficient search and retrieval of information from the document collection. It provides methods to perform keyword-based searches, enabling users to find relevant documents quickly. The driver utilizes librAIry's natural language processing capabilities to enhance search accuracy and provide more precise results.

- **Language-Specific Analysis**: It includes functionalities for language-specific analysis of documents. Developers can utilize the driver to perform tasks such as language identification, sentiment analysis, entity extraction, topic modeling, and keyword extraction. These capabilities help uncover valuable insights and facilitate advanced data processing on multilingual documents.

- **Question-Answering Functionality**: librAIry now incorporates question-answering functionality. Developers can utilize the driver to build applications that can answer questions based on the content of the document collection. This feature enables users to extract specific information or find answers to their queries within the multilingual documents.

- **Performance Optimization**: Our system focuses on performance optimization to handle large-scale document collections effectively. It utilizes efficient algorithms and techniques to ensure fast processing and response times. The driver is designed to handle millions of documents efficiently, making it suitable for projects with substantial document repositories.

- **Customization and Extensibility**: The module offers a flexible and extensible architecture. Developers can customize the driver implementation to suit specific requirements or extend its functionalities to incorporate additional features. It provides a solid foundation for integrating librAIry into existing workflows or building new applications on top of it.


## Installation

To install the package, run:
```bash
pip install librairy
```

## Use

```python
from librairy import bookshelf

#
# Request an API key at http://librairy.eu

my_bookshelf = bookshelf.connect(credentials="<API_KEY>")

books = [
    {
    "document_id": "1",
    "text": "Lions are large carnivorous felines found in grasslands and savannas.",
    "description": "Source: National Geographic"
    }, {
    "document_id": "2",
    "text": "Dolphins are highly intelligent marine mammals known for their playful behavior and strong social bonds.",
    "description": "Source: World Wildlife Fund"
    },{
    "document_id": "3",
    "text": "Elephants are the largest land animals, characterized by their long trunks and distinctive ivory tusks.",
    "description": "Source: Smithsonian's National Zoo"
    },{
    "document_id": "4",
    "text": "Penguins are flightless birds that thrive in cold Antarctic regions, often forming large colonies for breeding.",
    "description": "Source: BBC Earth"
    }
]
for book in books:
    my_bookshelf.add(book)

```

### Make Questions

The librAIry system encompasses a powerful **question answering functionality** that allows users to extract precise answers from a vast collection of documents. With this cutting-edge feature, librAIry empowers users to ask specific questions and receive accurate responses, enabling efficient information retrieval and knowledge discovery. 

```python
# make a question
resp = my_bookshelf.ask("What abilities have the dolphins shown?")
print(resp)

# OUTPUT:
# [
#   {
# 	'value': 'highly intelligent',
# 	'evidence': {
# 		    'text': 'Dolphins are highly intelligent marine mammals known for their playful behavior and strong social bonds.',
# 		    'document_id': 'c81e728d-9d4c-2f63-6f06-7f89cc14862c',
# 		    'description': 'Source: World Wildlife Fund',
# 		    'start': 13,
# 		    'end': 31,
# 		    'score': 0.54
# 	    }
#   }
# ]

```

### Search by Semantic

Unlike traditional keyword-based searching, librAIry takes searching to a whole new level with its advanced semantic searching functionality. By harnessing the power of artificial intelligence and natural language processing, librAIry goes beyond simple keyword matching to **understand the context, meaning, and relationships within your multilingual document collection**. This means you can perform more sophisticated searches that capture the true intent behind your query, allowing you to uncover relevant information that may not be explicitly captured by keywords alone. With librAIry's semantic searching, you can explore concepts, analyze document similarities, identify related topics, and gain a deeper understanding of your document collection like never before. Experience the next generation of searching with librAIry and unlock a world of valuable insights hidden within your multilingual documents.

```python
# search from the meaning of a term
resp = my_bookshelf.query("ocean")
print(resp)

# OUTPUT:
#  [
#   {
#  	'text': 'Dolphins are highly intelligent marine mammals known for their playful behavior and strong social bonds.',
#  	'document_id': 'c81e728d-9d4c-2f63-6f06-7f89cc14862c',
#  	'description': 'Source: World Wildlife Fund',
#  	'score': 0.61551234126091
#   }, {
#  	'text': 'Penguins are flightless birds that thrive in cold Antarctic regions, often forming large colonies for breeding.',
#  	'document_id': 'a87ff679-a2f3-e71d-9181-a67b7542122c',
#  	'description': 'Source: BBC Earth',
#  	'score': 0.6150351762771606
#   }
#  ]

```

### Collect Documents

librAIry offers a groundbreaking feature that streamlines the process of collecting documents from external sources, starting with scientific articles in the current version and expanding to encompass other sources in the future. With this cutting-edge functionality, librAIry eliminates the manual effort of sourcing and curating documents by automatically gathering relevant scientific articles from trusted repositories and publishers. This automated document collection ensures an up-to-date and diverse corpus, allowing researchers, academics, and knowledge seekers to access a comprehensive collection of scientific literature effortlessly. Stay at the forefront of research and expand your knowledge with librAIry's automatic document collection, empowering you to explore a wide range of sources without the hassle of manual aggregation.

```python
from librairy.collector import semscholar

papers = semscholar.Semantic_Scholar()
papers.add_author(name="Carlos Badenes-Olmedo", id="1413809069")

# interval: collect documents every `interval` minutes
# initial_delay: wait `initial_delay` minutes the first time
my_bookshelf.collect(papers, interval=5, initial_delay=0)
```

The ability of librAIry to automatically collect scientific articles from external sources, combined with its question answering functionality, revolutionizes research and knowledge discovery by providing researchers with a curated corpus of scientific literature and the means to extract precise insights. This powerful combination accelerates research, enables informed decision-making, bridges knowledge gaps, and fosters collaboration, empowering scientists to make breakthrough discoveries and advance scientific understanding.


```python
# make a question
resp = my_bookshelf.query("What is librAIry?")
print(resp)

# OUTPUT:
# [
#   {
#       'value': 'a novel architecture to store, process and analyze large collections of textual resources', 
#       'evidence': 
#           {
#               'text': 'We present librAIry, a novel architecture to store, process and analyze large collections of textual resources, integrating existing algorithms and tools into a common, distributed, high-performance workflow', 
#               'document_id': '498f9faf-c782-5728-5ba0-da972810df33', 
#               'description': "**'Distributing Text Mining tasks with librAIry'**, Carlos Badenes-Olmedo,José Luis Redondo García,Óscar Corcho, *ACM Symposium on Document Engineering*, 2017", 
#               'start': 21, 
#               'end': 110, 
#               'score': 0.7
#           }
#   }
# ]

```