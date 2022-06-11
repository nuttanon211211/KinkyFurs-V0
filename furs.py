from transformers import pipeline
import os
from flask import send_from_directory
from flask import Flask , request

text_generation = pipeline('text-generation' , model='sparki/kinkyfurs-gpt2')
STYLE_BLOCK = """<style>

body {
  background-position: center center;
  background-attachment: fixed;
  background-size: cover;
}

.test {

  max-width: 50%;
  height: auto;

}

img {
  display: block;
  margin-left: auto;
  margin-right: auto;

  width: 50%;

  max-width: 100%;
  height: auto;


  }

p {
  font-size: 1.5em;
}

.input-element {
  font-size: 1.5em;
}


  input[type=submit] {
  background-color: deeppink;
  color: white;
  border: 3px solid deepskyblue;
  padding: 10px 20px;
  text-align: center;

  border-radius: 8px;
  font-weight: bold;
  display: inline-block;

  }

  input[type=submit]:hover, input[type=submit]:active {
  background-color: deepskyblue;

  }

    </style> """

def stripEnd(sen):
    if "." in sen:
        return '.'.join(sen.split('.')[:-1])+'.'
    else:
        return sen
        
def ans1(qes):
    # Debug only
    #return "Debug Mode"

    prefix_text = qes
    #print(prefix_text)
    generated_text= text_generation(prefix_text, max_length=50, num_beams=5,no_repeat_ngram_size=2,early_stopping=True)
    #print(generated_text[0]['generated_text'])
    if '\n\n' in generated_text[0]['generated_text']:
        return stripEnd(generated_text[0]['generated_text'].split("\n\n")[1])
    else:
        return stripEnd(generated_text[0]['generated_text'])

#while True:        
#    q = input()
#    ans = ans1(q)
#    print(ans)


app = Flask(__name__)

@app.route('/static/<file>')
def bg(file):
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               file, mimetype='image/png')


@app.route('/')
def favicon():
    return """<!DOCTYPE html>
  <head>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Furry Assistant</title>
  """ + STYLE_BLOCK + """
  </head>

    <img src="static/Luby.png" alt="Luby">
    <p>"""+ans1("Hi,") + """</p>
    
    <form method="POST">
    <input class="input-element" name="text">
    <input type="submit" value="send">
</form>"""

@app.route('/',methods = ['POST'])
def my_form_post():
    q = request.form['text']
    return """<!DOCTYPE html>
  <head>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Furry Assistant</title>
    """ + STYLE_BLOCK + """
  </head>

    <img src="static/Luby.png" alt="Luby">
    <p>"""+ans1(q) + """</p>
    
    <form method="POST">
    <input class="input-element" name="text">
    <input type="submit" value="send">
</form>"""
                               
app.run(host = '0.0.0.0',port="8080",debug=True)
