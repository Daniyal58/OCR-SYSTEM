from flask import Blueprint, render_template,request,jsonify
import os,io
import pytesseract
from PIL import Image
from flask_login import login_required, current_user
from .models import Doc
from . import db
import spacy, pytz
from datetime import datetime

nlp = spacy.load("en_core_web_sm")

views = Blueprint('views',__name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    
    return render_template("Home.html",user = current_user)

@views.route('/extract-text', methods=['POST'])
def extract_text():
    if 'image' in request.files:
        uploaded_image = request.files['image']
        # Save the uploaded image to a temporary file
        image_path = 'temp_image.png'
        uploaded_image.save(image_path)
        # Perform OCR on the uploaded image
        extracted_text = pytesseract.image_to_string(Image.open(image_path))
        # Delete the temporary image file
        os.remove(image_path)
        return jsonify({'text': extracted_text})
    else:
        return jsonify({'error': 'No image file provided'})
    

@views.route('/process-text', methods=['POST'])
def process_text():
    extracted_text = request.json.get('text', '')
    
    # Process the extracted text using spaCy
    doc = nlp(extracted_text)

    # Extract important words
    important_words = [token.text for token in doc if token.pos_ in ['NOUN', 'PROPN']]
    
    # Return the important words as JSON
    return jsonify({'important_words': important_words})

@views.route('/remove_stopwords', methods=['POST'])
def remove_stopwords():
    # Get the text from the request
    text = request.json.get('text', '')
    

    # Process the text with SpaCy
    doc = nlp(text)

    # Remove stop words
    cleaned_text = ' '.join([token.text for token in doc if not token.is_stop])
    
    return jsonify({'cleaned_text': cleaned_text})

@views.route('/upload_image',methods=['POST'])
def upload_image():
    file = request.files['image']
    name = request.form.get('doc_name', '')
    user = request.form.get('user_id', '')
    time = datetime.now(pytz.utc)
    image_data = file.read()
    new_image = Doc(doc_name=name, image=image_data,date = time, user_id = user)
    db.session.add(new_image)
    db.session.commit()

    return jsonify({'message': 'Document uploaded successfully'})

@views.route('/get_user_documents', methods=['POST'])
def get_user_documents():
    user_id = request.json['user_id']
    documents = Doc.query.filter_by(user_id=user_id).all()
    doc_names = [doc.image for doc in documents]
  
    return jsonify({ 'documents':doc_names })

