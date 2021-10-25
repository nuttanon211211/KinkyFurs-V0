from transformers import pipeline
import os
from flask import send_from_directory
from flask import Flask , request

text_generation = pipeline('text-generation' , model='sparki/kinkyfurs-gpt2')

def stripEnd(sen):
    if "." in sen:
        return '.'.join(sen.split('.')[:-1])+'.'
    else:
        return sen
        
def ans1(qes):
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
    return """<style>
    .input-element{
    font-size: 2em;
    width: 30em;
	}
	p{
	font-size: 2em;
	}
	img {
  width: 20%;   
	}
	.center {
  display: block;
  margin-left: auto;
  margin-right: auto;
  width: 25%;
  }

    </style> 
    <img src="static/Luby.png" alt="Luby" class='center'>
    <p>"""+ans1("Hello") + """</p>
    
    <form method="POST">
    <input class="input-element" name="text">
    <input type="submit">
</form>"""

@app.route('/',methods = ['POST'])
def my_form_post():
    q = request.form['text']
    return """<style>
    .input-element{
    font-size: 2em;
    width: 30em;
	}
	p{
	font-size: 2em;
	}
	img {
  width: 20%;   
    }
    .center {
  display: block;
  margin-left: auto;
  margin-right: auto;
  width: 25%;
   }
    </style> 
    <img src="static/Luby.png" alt="Luby" class="center">
    <p>"""+ans1(q) + """</p>
    
    <form method="POST">
    <input class="input-element" name="text">
    <input type="submit">
</form>"""
                               
app.run(host = '0.0.0.0',port="8080",debug=True)
