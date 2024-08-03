from flask import Flask, request, jsonify
import language_tool_python
import nltk

# Descargar recursos de NLTK
nltk.download('punkt')

app = Flask(__name__)
tool = language_tool_python.LanguageTool('es')

# Conjunto de palabras ofensivas comunes en México
offensive_words = {
    "cabrón", "cabrona", "chingar", "chingado", "chingada", "chingón", "chingona",
    "puta", "puto", "putazo", "pendejo", "pendeja", "pendejada", "mierda", "verga"
    "joder", "jodido", "jodida", "coño", "culero", "culera", "pinche", "estúpido",
    "estúpida", "imbécil", "idiota", "perra", "zorra", "hijo de puta", "hija de puta",
    "hijo de perra", "hija de perra", "maricón", "maricona", "culer@", "tarado", "tarada", 
    "verga", "cagado", "cagada", "cabronazo", "chingaderas", "chingar", "chingate",
    "chingatelo", "chingatelos", "chingatela", "chingatelas", "putiza", "puto", "putazos",
    "putear", "pinchurriento", "pinchurrienta", "pendejete", "pendejote", "jodete",
    "jodanse", "mierdero", "mierdera", "jodete", "jodanse", "cojonudo", "cojonuda", 
    "pinchazo", "pinchazos", "chingaquedito", "chingaqueditos", "chingatumadre", 
    "chingatupadre", "chingatumadralos", "chingatumadralas", "chingatumadralo", 
    "chingatumadralas", "putamadre", "putamadralos", "putamadralas", "putamadralo", 
    "putamadralas", "cagón", "cagona", "cagapalos", "cagapalo", "pinchi", "pendejote",
    "pendejon", "pendejona", "culazo", "culera", "culerazo", "culeraza", "pendejin",
    "cagaste", "cagaras", "cagara", "mierditas", "mierdita", "cabroncete", "cabronceta",
    "cabroncetes", "cabroncetas", "chingadazo", "chingadazos", "pendejito", "pendejita",
    "pendejitos", "pendejitas", "verguiza", "verguizas", "chingadazo", "chingadazos", 
    "cabronazo", "cabronazos", "jodidazo", "jodidazos", "chinga", "chingas", "chingamos", 
    "chingan", "chingaron", "chingaste", "chingaremos", "chingaramos", "chingarían",
    "chingarás", "chingará", "chingaríamos", "chingaríamos", "chingarías", "chingarían",
    "chingarás", "chingaré", "chingaré", "chingaremos", "chingaramos", "chingados", 
    "chingadas", "pinchazo", "pinchazos", "pinchis", "pinchurriento", "pinchurrienta", 
    "pendejonazo", "pendejonaza", "pendejozo", "pendejoza", "cagones", "cagonas", "putotes",
    "putotas", "putones", "putonas", "cabronsotes", "cabronsotas", "chingoncitos", 
    "chingoncitas", "chingaqueditos", "chingaqueditas", "pendejotes", "pendejotas", 
    "cagaditos", "cagaditas", "cagonzotes", "cagonzotas", "cabronsitos", "cabronsitas"
}

def contains_profanity(text):
    """Verifica si el texto contiene alguna palabra ofensiva."""
    tokens = nltk.word_tokenize(text.lower())
    return any(token in offensive_words for token in tokens)

@app.route('/check', methods=['POST'])
def check_spelling():
    data = request.get_json()
    text = data.get('text', '')
    
    if not text:
        return jsonify({'error': 'No text provided'}), 400
    
    matches = tool.check(text)
    corrected_text = language_tool_python.utils.correct(text, matches)
    
    profanity_flag = contains_profanity(corrected_text)
    
    return jsonify({
        'corrected_text': corrected_text,
        'contains_profanity': profanity_flag
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
