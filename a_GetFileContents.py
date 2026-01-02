# Function being called by 'main.py'
def getTheFile():
    """
    Function to:
    1. Ask the user for a file (PDF, DOCX, TXT, RTF)
    2. Extract the text from that file
    3. Call 'b_SummarizeQuestions' to begin investigation of that file
    
    """
    # Imports
    from js import document
    from pyodide.ffi import create_proxy
    import io
    import b_SummarizeQuestions as summarize
    import e_AddEditorChecks as edit

    def handle_file(event):
        """
        Function to create the call to ask the user for a file
        
        """

        # Grab the file submitted by the user
        files = event.target.files

        # Make sure a file was correctly submitted
        if files.length == 0:
            # If not, return. There is nothing else we can do
            return

        # If so, grab the first file listed (which should be the only one listed)
        file = files.item(0)
        
        # Create a FileReader object to read in the file's bytes
        file_reader = __import__("js").FileReader.new()
        
        def on_load(e):
            """
            Function to:
            1. Send the file to the appropriate file decoder (PDF, DOCX, TXT, RTF)
            2. Call 'b_SummarizeQuestions' sending the files' contents
            
            """

            # Grab the file's bytes
            data = io.BytesIO(e.target.result.to_py())

            # Grab the file's name
            filename = file.name.lower()
    
            try:
                # Check if the file is of type PDF
                if filename.endswith(".pdf"):
                    # If so:
                    #-> Import PdfReader
                    from PyPDF2 import PdfReader
                    #-> Create a PdfReader object
                    reader = PdfReader(data)
                    #-> Write the file's contents to a variable
                    text = "\n".join([page.extract_text() or "" for page in reader.pages])
                    #-> Call 'b_SummarizeQuestions' sending that variable
                    summarize.summarize(text)

                # If not, check if the file is of type DOCX
                elif filename.endswith(".docx"):
                    # If so:
                    #-> Import python-docx
                    import docx
                    #-> Create a Document object
                    doc = docx.Document(data)
                    #-> Write the document's contents to a variable
                    text = "\n".join([p.text for p in doc.paragraphs])
                    #-> Call 'b_SummarizeQuestions' sending that variable
                    summarize.summarize(text)

                # If not, check if the file is of type TXT
                elif filename.endswith(".txt"):
                    # if so:
                    #-> Decode and send the byte data to the variable
                    text = data.read().decode("utf-8", errors="ignore")
                    #-> Call 'b_SummarizeQuestions' sending that variable
                    summarize.summarize(text)

                # If not, check if the file is of type RTF
                elif filename.endswith(".rtf"):
                    # If so:
                    #-> Import rtf_to_text from the "striprtf" library to decode the file's contents
                    from striprtf.striprtf import rtf_to_text
                    #-> Read in the decoded contents from the file
                    text = rtf_to_text(data.read().decode('utf-8', errors = 'ignore'))
                    # Call 'b_SummarizeQuestions' sending in that variable
                    summarize.summarize(text)

                # If the file type is none of the above, return
                else:
                    print('ERROR: File not acceptable')
                    print('Is your file of type PDF, TXT, RTF, or DOCX?')
                    return
                    
            except Exception as e:
                print('EXCEPTION: Failed to open your file')
                print(e)
                return

            # Call 'e_AddEditorChecks' to begin the editing processing once the file is read
            edit_str = edit.getTheFile()
            # Send any edits to the html page
            #-> Grab the html's output div for this
            edit_output = document.getElementById('edit_output')
            #-> Send the edits to this variable
            edit_output.innerHTML = f'<p>{edit_str}</p>'

        # Call the on_load function
        file_reader.onload = create_proxy(on_load)

        # Read the file as an Array Buffer
        file_reader.readAsArrayBuffer(file)

    # Add an event listener that will stall the program until the user enters a file
    document.getElementById("input_file").addEventListener("change", create_proxy(handle_file))
