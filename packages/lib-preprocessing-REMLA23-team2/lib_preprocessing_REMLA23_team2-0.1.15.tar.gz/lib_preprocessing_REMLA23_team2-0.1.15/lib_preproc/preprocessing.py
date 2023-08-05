import re
import nltk
from nltk.corpus import stopwords

nltk.download('stopwords')
all_stopwords = stopwords.words('english')
all_stopwords.remove('not')

def get_version():
    with open("VERSION", "r") as version_file:
        return version_file.read().strip()

def process_review(review: str):
    review = re.sub('[^a-zA-Z]', ' ', review)
    review = review.lower()
    review = review.split()
    review = [ps.stem(word) for word in review if not word in set(all_stopwords)]
    review = ' '.join(review)
    return review