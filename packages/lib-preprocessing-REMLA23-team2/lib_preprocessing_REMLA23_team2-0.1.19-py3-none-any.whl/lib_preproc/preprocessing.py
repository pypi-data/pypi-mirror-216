import re
import nltk
import pkg_resources
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

nltk.download('stopwords')
all_stopwords = stopwords.words('english')
all_stopwords.remove('not')

ps = PorterStemmer()

# def get_version():
#     with open("VERSION", "r") as version_file:
#         return version_file.read().strip()
    
def get_version():
    try:
        return pkg_resources.get_distribution("lib_preprocessing_REMLA23_team2").version
    except pkg_resources.DistributionNotFound:
        return None
    
__version__ = get_version()

def process_review(review: str):
    review = re.sub('[^a-zA-Z]', ' ', review)
    review = review.lower()
    review = review.split()
    review = [ps.stem(word) for word in review if not word in set(all_stopwords)]
    review = ' '.join(review)
    return review