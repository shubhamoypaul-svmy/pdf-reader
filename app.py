from flask import Flask, render_template,request,send_file,redirect
from werkzeug.utils import secure_filename
import os
import PyPDF2 

UPLOAD_FOLDER = 'uploads/'
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in {'pdf'}
def fun(path,v):

# creating a pdf file object 
    try:
        pdfFileObj = open(path, 'rb') 

  
# creating a pdf reader object 

        pdfReader = PyPDF2.PdfFileReader(pdfFileObj) 

        
# printing number of pages in pdf file 

        #print(pdfReader)

        P=[]
        P2=[]
        l=pdfReader.numPages-1
        for i in range(l):
            pageObj = pdfReader.getPage(i)
  
     # extracting text from page 

            Text=pageObj.extractText()
            a=Text.split()[0:v]
            pageObj = pdfReader.getPage(i+1)

  
     # extracting text from page 

            Text2=pageObj.extractText()
            b=Text2.split()[0:v]
            P.append(a==b)
            if P[-1]==False :
                P2.append(i)
            #print(a==b)
        pdfFileObj.close()  
        from PyPDF2 import PdfWriter, PdfReader
        pages_to_keep = P2 # page numbering starts from 0
        infile = PdfReader(path) 
        output = PdfWriter()

        for i in pages_to_keep:
            p = infile.pages[i] 
            output.add_page(p)

        with open('convert.pdf', 'wb') as f:
            output.write(f)
        return("done")
         
        
    except ValueError:
      print("Oops!  That was no valid number.  Try again...")

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/data',methods = ['POST', 'GET'])
def data():
    if request.method == 'POST':
      file = request.files['file']
      v=request.form.get('value', type=int)
      if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        fuck=os.path.join(app.config['UPLOAD_FOLDER'],filename)
        fun(fuck,v)
      return render_template('covert.html',result="/convert.pdf",v=v)
@app.route('/download')
def download():
    path1 = app.config['UPLOAD_FOLDER']
    dir_list = os.listdir(path1)
    t=os.path.join(path1,dir_list[-1])
    if os.path.isfile(t):
        os.remove(t)
    return send_file("/convert.pdf", as_attachment=True,)





if __name__ == "__main__":  
    app.run(debug=True)




    # importing the required libraries
