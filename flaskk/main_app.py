from flask import Flask, render_template, request
import nltk
import joblib
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from unidecode import unidecode

app = Flask(__name__)

# Load the model
model_load = joblib.load(filename="/home/leguibs/exo_cine/Brief_NLP_joblib_model.joblib")
classifier = model_load["classifier"]
vectorizer = model_load["vectorizer"]

# Initialize lemmatizer
lm = WordNetLemmatizer()

# Download necessary NLTK data
nltk.download("punkt")
nltk.download("stopwords")

def standardize_vectorize(comment: str):
    """Format the comment for prediction"""
    comment = comment.replace(r"http\S+", "")
    comment = comment.replace(r"●  ●  ●", "")
    comment = comment.replace(r"spoiler", "")
    comment = comment.replace(r":", " ")
    comment = comment.replace(r".", " ")
    comment = comment.replace(r",", " ")
    comment = unidecode(comment)
    comment = comment.lower()
    comment = nltk.word_tokenize(comment)
    comment = [word for word in comment if word.isalnum()]
    comment = [word for word in comment if word not in set(stopwords.words('french'))]
    comment = [lm.lemmatize(word) for word in comment]
    comment = ' '.join(comment)     
    comment = vectorizer.transform([comment])
    return comment

def prediction(comment, classifier):
    avis = {
        0 : 'Commentaire négatif',
        1 : 'Commentaire positif'
    }

    comment = standardize_vectorize(comment)

    return avis[classifier.predict(comment)[0]]

@app.route('/', methods=["GET", "POST"])  
def index():
    
    if request.method == "GET":  
        
        return render_template('index.html')
        
    if request.method == "POST":
        comment = request.form['textarea']
        pred = prediction(comment, classifier)

        return render_template('index.html', pred=pred)

if __name__ == "__main__":
    app.run(debug=True)