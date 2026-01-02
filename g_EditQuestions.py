def edit_questions__formality(df):
    """
    Sub function to check for formality issues within a question
    Throws a flag if...
    - Question number 1 is for 30 points
    - The first word of the actual question is lowercase
    - The question doesn't end with proper punctuation ('?' or '.')
    - The question asks for a "complete reference", but the chapter was given in the introductory remarks
    - The question asks for "references" without the word complete, but the chapter was not given in the introductory remarks
    - "According to *verse*" questions come from nowhere
      -> no chapter or section given in the introductory remarks
      -> Unless the chapter, section or book is given in the actual question or...
      -> The question is asking for the "opening/closing" verse
    - The number of part questions is the same as the number of part answers
      -> When the number of part questions/answers is more than 1

    Returns a list containing all the flags to send to the output
    
    """
    # Imports
    import re
    
    # Create a blank list to store all the flags into
    list_flags__formality = []

    # =-=-=-=-=-=-=-=-=-= CHECKS =-=-=-=-=-=-=-=-=-=

    # === Check if question 1 is a 30-point question ===
    # Check if there are any questions labeled question number 1 and...
    # Check if any of those questions are for 30 points
    if len(df.loc[(df['Q_Num'] == 1) & (df['Pt_Val'] == 30)]) > 0:
        # If so, throw a flag to the output
        #-> If there is only one question that meets this criteria
        if len(df.loc[(df['Q_Num'] == 1) & (df['Pt_Val'] == 30)]) == 1:
            # If so, send the output for one question
            list_flags__formality.append(f'<p>* Set {list(df.loc[((df['Q_Num'] == 1) & (df['Pt_Val'] == 30)), 'Set_Num'])[0]} question 1 is for 30 points. Consider moving this elsewhere in the set.</p>')
        else: # If not, send the output for multiple questions
            list_flags__formality.append(f'<p>* Sets (<i>{', '.join(map(str,df.loc[((df['Q_Num'] == 1) & (df['Pt_Val'] == 30)), 'Set_Num']))}</i>): Question number 1 is for 30 points. Consider moving this elsewhere in the set.</p>')

    # === Check if the first word of a question is lowercase ===
    # For each question
    for i in range(len(df)):
        # Grab the first word of each question
        first_word = df['Question'].iloc[i].split()[0]
        # Determine if the first word is lowercase
        if first_word == first_word.lower():
            # If so, grab the set number and question number of that question and...
            # Throw an output flag
            list_flags__formality.append(f'<p>! Set {df['Set_Num'].iloc[i]} question {df['Q_Num'].iloc[i]} starts with a lowercase word. This should be capitalized.</p>')
    
    # === Check if the question doesn't end with "?" or "." ===
    # For each question
    for i in range(len(df)):
        # Determine if the last character is a "?" or a "." or...
        # Determine if there is a "?" or a "." followed by a quotation mark or just whitespace
        #-> The quotation mark can appear at the end of something like a Scripture-Texst question
        #-> The whitespace can appear at the end of quotation/essence completion questions
        if not re.search(r'[.?][ "]*\Z', df['Question'].iloc[i]):
            # If this is not the case either, throw a flag
            list_flags__formality.append(f'<p>! Set {df['Set_Num'].iloc[i]} question {df['Q_Num'].iloc[i]} does not end with proper punctuation (<i>? .</i>). These should end the question.</p>')

    # === Check if the question asks for "complete reference", but the chapter was given in the introductory remarks ===
    # Check if there are any questions asking for "complete reference" and...
    # Check if any of those questions are coming from the chapter
    if len(df.loc[(df['Question'].str.contains('omplete reference')) & (df['Location'].str.contains('ch'))]) < 0:
        # If so, for each question
        for i in range(len(df.loc[(df['Question'].str.contains('omplete reference')) & (df['Location'].str.contains('ch'))])):
            # Grab the set number and the question number, and...
            # Throw a flag
            list_flags__formality.append(f'<p>* Set {df['Set_Num'].iloc[i]} quesiton {df['Q_Num'].iloc[i]} is asking for the "complete reference(s)" when the chapter is already given in the introductory remarks. This should just ask for the "references".</p>')

    # === Check if the question asks for only references, but the chapter is NOT in the introductory remarks ===
    # Check if there are any questions asking for "reference" that are NOT asking for "complete reference" and...
    # Check if those questions are coming from nowhere
    if len(df.loc[(df['Question'].str.contains('reference')) & (df['Question'].str.contains('omplete') == False) & (df['Location'] == '_')]) > 0:
        # If so, for each question
        for i in range(len(df.loc[(df['Question'].str.contains('reference')) & (df['Question'].str.contains('omplete') == False) & (df['Location'] == '_')])):
            # Grab the set number and the question number, and...
            # Throw a flag
            list_flags__formality.append(f'<p>* Set {df['Set_Num'].iloc[i]} quesiton {df['Q_Num'].iloc[i]} is asking for just the "reference(s)" when the chapter is not given. Either the chapter needs to be in the introductory remarks or the question needs to ask for "complete reference(s)".</p>')

    # === Check if "According to *verse*" questions are coming from nowhere
    # Check if there are any questions with the "According to *verse*" note and...
    # Check if any of those questions are coming from nowhere
    if len(df.loc[(df['Notes'] == 'According to *verse*') & (df['Location'] == '_')]) > 0:
        # If so, create a sub dataframe of all these instances
        df_acc = df.loc[(df['Notes'] == 'According to *verse*') & (df['Location'] == '_')]
        # For each question in the sub dataframe
        for i in range(len(df_acc)):
            # Check if the chapter or section is in the question itself, and...
            # Check if the question is asking for the opening/closing verse
            if 'chapter' not in df_acc['Question'].iloc[i] and 'section' not in df_acc['Question'].iloc[i] and 'opening' not in df_acc['Question'].iloc[i] and 'closing' not in df_acc['Question'].iloc[i]:
                # If neither of these conditions are met, throw a flag
                list_flags__formality.append(f'<p>! Set {df_acc['Set_Num'].iloc[i]} question {df_acc['Q_Num'].iloc[i]} gives no chapter for "According to *verse*" question. This should be added.</p>')

    # === Check if the number of part questions is the same as the number of part answers ===
    # Create a sub dataframe of all questions that are both multiple-part question and multiple-part answer
    df_mpq_mpa = df.loc[(df['Q_Intro'].str.contains(r'\d+')) & (df['A_Intro'].str.contains(r'\d+'))]
    # For each question in the sub dataframe
    for i in range(len(df_mpq_mpa)):
        # Determine if the number of questions is the same as the number of answers
        if re.findall(r'\d+', df_mpq_mpa['Q_Intro'].iloc[i]) == re.findall(r'\d+', df_mpq_mpa['A_Intro'].iloc[i]):
            # If so, throw a flag
            list_flags__formality.append(f'<p>! Set {df_mpq_mpa['Set_Num'].iloc[i]} question {df_mpq_mpa['Q_Num'].iloc[i]} has the same number of part questions as part answers (<i>{re.findall(r'\d+', df_mpq_mpa['Q_Intro'].iloc[i])[0]}</i>). The number of part answers needs to go away or be changed.</p>')

    # Return the list of flags
    return list_flags__formality


def edit_questions__sep_consec(df):
    """
    Sub function to deal with issues regarding separate and consecutive verses
    Throws a flag if...
    - A 10-point question is labeled as separate/consecutive verses
    - There are multiple verse references in the answer, but the question is not marked as separate/consecutive verses
      -> S, C, chs, secs, bks
    - The question is coming from separate verses, but is not marked as separate/consecutive verses
    - The question is marked as separate/consecutive verses, but there aren't multiple references in the answer
    - A standard quotation/essence question from multiple verses isn't labeled as "From # consecutive verses"
    - A standard quotation/essence question from multiple verses doesn't have the number of verses in the introductory remarks
    - A standard quotation/essence question from multiple verses is marked as a multiple-part question
    - The question is asking for the chapters/references of something, but the question IS marked as separate/consecutive verses

    Returns a list containing all the flags to send to the output
    
    """
    # Imports
    import re

    # Create a blank list to send the flags to
    list_flags__sep_consec = []

    # =-=-=-=-=-=-=-=-=-= CHECKS =-=-=-=-=-=-=-=-=-=
    # === Check if any 10-point questions are labeled as separate/consecutive verses
    # See if there are any 10-point questions labeled as separate/consecutiv verses
    if len(df.loc[(df['Pt_Val'] == 10) & (df['Location'].str.contains(r'S|C|chs|bks|secs', case = True))]) > 0:
        # If so, create a sub dataframe containing these questions
        df_sep_consec_10 = df.loc[(df['Pt_Val'] == 10) & (df['Location'].str.contains(r'S|C|chs|bks|secs', case = True))]
        # For each question in the sub dataframe
        for i in range(len(df_sep_consec_10)):
            # Send a flag to the output
            list_flags__sep_consec.append(f'<p>* Set {df_sep_consec_10['Set_Num'].iloc[i]} question {df_sep_consec_10['Q_Num'].iloc[i]} is a 10-point question coming from multiple verses. This is generally frowned upon even if the answers are short. Consider making this a 20/30-point question.</p>')
    
    # === Check if there are multiple verses in the answer, but the question doesn't indicate so ===
    # === Check if the question is coming from multiple verses, but the introductory marks don't mark it so ===
    # Create a sub dataframe of all questions with multiple references
    df_multi_ref = df.loc[df['Ans_Reference'].str.contains(r':[^:]+:')]
    # For each question in this sub dataframe
    for i in range(len(df_multi_ref)):
        # Determine if the question is not appropriately marked as separate/consecutive verses, and...
        # Determine if the question is not asking for the (complete) references
        if ('S' not in df_multi_ref['Location'].iloc[i]) and ('C' not in df_multi_ref['Location'].iloc[i]) and ('chs' not in df_multi_ref['Location'].iloc[i]) and ('secs' not in df_multi_ref['Location'].iloc[i]) and ('bks' not in df_multi_ref['Location'].iloc[i]) and ('reference' not in df_multi_ref['Question'].iloc[i]):
            # If both conditions are met, throw a flag
            list_flags__sep_consec.append(f'<p>! Set {df_multi_ref['Set_Num'].iloc[i]} question {df_multi_ref['Q_Num'].iloc[i]} has multiple references in the answer, but is not labeled as separate/consecutive verses. The label should be added.</p>')

    # === Check if the question is marked as separate/consecutve verses, but the answer is coming from one verse ===
    # Create a sub dataframe containing all questions marked as separate/consecutive verses
    df_sep_consec = df.loc[df['Location'].str.contains(r'S|C|bks|chs|secs', case = True)]
    # For each question in the sub dataframe
    for i in range(len(df_sep_consec)):
        # Check if there are multiple references in the answer
        if len(re.findall(':', df_sep_consec['Ans_Reference'].iloc[i])) < 2:
            # If not, throw a flag
            list_flags__sep_consec.append(f'<p>! Set {df_sep_consec['Set_Num'].iloc[i]} question {df_sep_consec['Q_Num'].iloc[i]} is labeled as separate/consecutive verses, but only one verse is in the answer. Either add verses or remove this introductory remark.</p>')

    # === Check if a standard quotation/essence question is from multiple verses, but isn't marked as such ===
    # === Check if a standard quotation/essence question from multiple verses doesn't have the number of verses marked ===
    # === Check if a standard quotation/essence question from multiple verses is marked as a multiple-part question ===
    # Grab a sub dataframe containing all standard quotation/essence questions and...
    # Make sure they are coming from multiple verses
    df_std = df.loc[(df['Notes'].str.contains('Standard')) & (df['Ans_Reference'].str.contains(r':[^:]+:'))]
    # For each question in the sub dataframe
    for i in range(len(df_std)):
        # Determine if the questions are labeled as separate/consecutive verses
        if ('S' not in df_std['Location'].iloc[i]) and ('C' not in df_std['Location'].iloc[i]):
            # If not, throw a flag
            list_flags__sep_consec.append(f'<p>! Set {df_std['Set_Num'].iloc[i]} question {df_std['Q_Num'].iloc[i]} MUST be labeled as separate/consecutive verses.</p>')
        # Determine if the questions have the number of verses in the introductory remarks
        if re.search(r'\d+', df_std['Location'].iloc[i]) == None:
            # If not, throw a flag
            list_flags__sep_consec.append(f'<p>! Set {df_std['Set_Num'].iloc[i]} question {df_std['Q_Num'].iloc[i]} MUST have the number of verses in the introductory remarks.</p>')
        # Determine if the questions are labeled as a multiple-part question
        if re.search(r'\d+', df_std['Q_Intro'].iloc[i]) != None:
            # If so, throw a flag
            list_flags__sep_consec.append(f'<p>! Set {df_std['Set_Num'].iloc[i]} question {df_std['Q_Num'].iloc[i]} must NOT be labeled as a multiple-part question.</p>')


    # === Check if a question asking for (complete) references is marked as separate/consecutive verses ===
    # Create a sub dataframe containing all questions asking for (complete) references
    df_complete_refs = df.loc[df['Question'].str.contains('reference')]
    # For each question in the sub dataframe
    for i in range(len(df_complete_refs)):
        # Determine if the questions are labeled as separate/consecutive verses
        if 'S' in df_complete_refs['Location'].iloc[i] or 'C' in df_complete_refs['Location'].iloc[i]:
            # If so, throw a flag
            list_flags__sep_consec.append(f'<p>! Set {df_std['Set_Num'].iloc[i]} question {df_std['Q_Num'].iloc[i]} asks for (complete) references, but it is labeled as separate/consecutive verses. The label needs to be removed.</p>')

    # Return the list of flags
    return list_flags__sep_consec


def edit_questions__scripture_text(df):
    """
    Sub function to flag issues on questions labeled as Scripture-Text
    Throws a flag if...
    - The word "quote," appears, but the question is not labeled Scripture Text
      -> Unless the questions is a Completion question or...
      -> the question has the phrase "end quote" indicating a Statement and Question
    - The question is labeled a Scripture Text question, but it doesn't have the word "quote" in it
    - The question is labeled a Scripture Text question, but it has a reference in the question
    - A Scripture Text question starts with the word "Referring", but doesn't have a pronoun in the Scripture Text part of the question
    - A Scripture Text question has a pronoun after the word "quote", but it doesn't start with "Referring"

    Returns a list containing all the flags to send to the output
    
    """
    # Imports
    import re

    # Create a blank list to store our output messages
    list_flags__scripture_text = []

    # =-=-=-=-=-=-=-=-=-= CHECKS =-=-=-=-=-=-=-=-=-=
    # === Check for questions with the word "quote," that aren't labeled Scripture-Text ===
    # Create a sub-dataframe containing all questions with "quote," in it and...
    #                                   no Scripture-Text or Completion questions
    df_quote = df.loc[(df['Question'].str.contains('quote,')) & (df['Q_Intro'].str.contains(r'T|C') == False)]
    # For each question in the sub dataframe
    for i in range(len(df_quote)):
        # Check if that question contains the phrase "end quote"
        if ('end quote' not in df_quote['Question'].iloc[i]) and ('end-quote' not in df_quote['Question'].iloc[i]):
            # If not, throw a flag
            list_flags__scripture_text.append(f'<p>! Set {df_quote['Set_Num'].iloc[i]} question {df_quote['Q_Num'].iloc[i]} may need to be labeled as a Scripture-Text question.</p>')

    # === Check for questions labeled as Scripture-Text that don't have the word "quote" ===
    # For each question labeled Scripture-Text without the word "quote,"
    for i in range(len(df.loc[(df['Q_Intro'].str.contains('T')) & (df['Question'].str.contains('quote,') == False)])):
        # Throw a flag
        list_flags__scripture_text.append(f'<p>! Set {df.loc[(df['Q_Intro'].str.contains('T')) & (df['Question'].str.contains('quote,') == False)]['Set_Num'].iloc[i]} question {df.loc[(df['Q_Intro'].str.contains('T')) & (df['Question'].str.contains('quote,') == False)]['Q_Num'].iloc[i]} is labeled as Scripture-Text but does not have a scripture text at the end of the question (denoted by "quote"). Consider adding this or removing the Scripture-Text introductory remark.</p>')

    # === Check for questions labeled Scripture-Text that have a verse reference in the question ===

    # === Check if a Scripture-Text starts with "Referring" but doesn't have a pronoun after "quote" ===

    # === Check if a Scripture-Text question has a pronoun after "quote" but doesn't start with "Referring" ===

    # Return the list of flag messages
    return list_flags__scripture_text


def edit_questions__statement(df):
    """
    Sub function to flag issues on questions labeled as Statement and Question
    Throws a flag if...
    - The question doesn't have a statement, but is labeled as a Statement and Question
    - The question is not labeled Statement and Question, but has a statement in the question

    Returns a list of flag messages to send to the output
    
    """
    # Imports
    import re

    # Create a blank list to store our output messages
    list_flags__statement = []

    # =-=-=-=-=-=-=-=-=-= CHECKS =-=-=-=-=-=-=-=-=-=
    # === Check if a question is labeled as Statement and Question but has NO statement ===
    # Create a sub dataframe containing all questions labeled as Statement and Question
    df_statement = df.loc[df['Q_Intro'].str.contains('S', case = True)]
    # For each question in the sub dataframe
    for i in range(len(df_statement)):
        # Check if there are either 2 periods or 1 period with 1 question mark
        if not re.search(r'[.][^.]+[.?]', df_statement['Question'].iloc[i]):
            # If not, throw a flag
            list_flags__statement.append(f'<p>! Set {df_statement['Set_Num'].iloc[i]} question {df_statement['Q_Num'].iloc[i]} is labeled as a Statement and Question, but no statement is present. Either add a statement or remove the introductory remark.</p>')

    # === Check if a question is NOT labeled as Statement and Question but has a statement ===
    # Create a sub dataframe of all questions with multiple punctuation (? of .) and...
    # Ensure that they are not questions ending with "..." (e.g. quotation/essence questions)
    df_multi_punct = df.loc[(df['Question'].str.contains(r'[.][^.]+[.?]')) & (df['Question'].str.contains(r'\.\.\.') == False)]
    # For each question in the sub dataframe
    for i in range(len(df_multi_punct)):
        # Check if the question is labeled as Statement and Question
        if re.search('S', df_multi_punct['Q_Intro'].iloc[i]) == None:
            # If not, throw a flag
            list_flags__statement.append(f'<p>! Set {df_multi_punct['Set_Num'].iloc[i]} question {df_multi_punct['Q_Num'].iloc[i]} appears to have a statement in the question, but the question is not labeled Statement and Question.  Consider adding this introductory remark.</p>')

    # Return the list of flags
    return list_flags__statement
    

def edit_questions(df):
    """
    Function to perform editing suggestions on the actual questions found in the input file
    Throws a flag to the output when...
    A Formality Issue Occurs
    - Question number 1 is for 30 points
    - The first word of the actual question is lowercase
    - The question doesn't end with proper punctuation ('?' or '.')
    - The question asks for a "complete reference", but the chapter was given in the introductory remarks
    - The question asks for "references" without the word complete, but the chapter was not given in the introductory remarks
    - "According to *verse*" questions come from nowhere
      -> no chapter, section, or book given in the introductory remarks
      -> Unless the chapter or section is given in the actual question or...
      -> The question is asking for the "opening/closing" verse
    - The number of part questions is the same as the number of part answers
      -> When the number of part questions/answers is more than 1
    A Separate/Consecutive Issue Occurs
    - A 10-point question is labeled as separate/consecutive verses
    - There are multiple verse references in the answer, but the question is not marked as separate/consecutive verses
      -> S, C, chs, secs, bks
    - The question is coming from separate verses, but is not marked as separate/consecutive verses
    - The question is marked as separate/consecutive verses, but there aren't multiple references in the answer
    - A standard quotation/essence question from multiple verses isn't labeled as "From # consecutive verses"
    - The question is asking for the chapters/references of something, but the question IS marked as separate/consecutive verses
    A Scripture-Text Issue Occurs
    - The word "quote," appears, but the question is not labeled Scripture Text
      -> Unless the questions is a Completion question or...
      -> the question has the phrase "end quote" indicating a Statement and Question
    - The question is labeled a Scripture Text question, but it doesn't have the word "quote" in it
    - The question is labeled a Scripture Text question, but it has a reference in the question
    - A Scripture Text question starts with the word "Referring", but doesn't have a pronoun in the Scripture Text part of the question
    - A Scripture Text question has a pronoun after the word "quote", but it doesn't start with "Referring"
    A Statement and Question Issue Occurs
    - The question doesn't have a statement, but is labeled as a Statement and Question
    - The question is not labeled Statement and Question, but has a statement in the question

    Returns a string variable containing all the editing messages outputted
    
    """
    # Imports
    import re

    # Create a counter variable to count how many edits we find
    num_edits = 0
    # Create a blank list to combine all the output messages to
    output_set_list = []
    # Create a variable to store any edit messages in
    #-> Add a title row indicating these are edits for the actual questions
    output_question_msg = '<b>===== Question Edits / Suggestions =====</b><p>'

    # Call edit_questions__formality() to check for any formality issues within a question
    output_question__formality = edit_questions__formality(df)
    # Add how many fixes we found to the total number of fixes
    num_edits += len(output_question__formality)
    # For each edit
    for i in range(len(output_question__formality)):
        # Append that edit to our total list of fixings
        output_set_list.append(output_question__formality[i])

    # Call edit_questions__sep_consec() to check for any issues regarding separate/consecutive verses
    output_question__sep_consec = edit_questions__sep_consec(df)
    # Add how many fixes we found to the total number of fixes
    num_edits += len(output_question__sep_consec)
    # For each edit
    for i in range(len(output_question__sep_consec)):
        # Append that edit to our total list of fixings
        output_set_list.append(output_question__sep_consec[i])

    # Call edit_questions__scripture_text() to check for any issues regarding Scripture-Text questions
    output_question__scripture_text = edit_questions__scripture_text(df)
    # Add how many fixes we found to the total number of fixes
    num_edits += len(output_question__scripture_text)
    # For each edit
    for i in range(len(output_question__scripture_text)):
        # Append that edit to our total list of fixings
        output_set_list.append(output_question__scripture_text[i])

    # Call edit_questions__statement() to check for any issues regarding Scripture-Text questions
    output_question__statement = edit_questions__statement(df)
    # Add how many fixes we found to the total number of fixes
    num_edits += len(output_question__statement)
    # For each edit
    for i in range(len(output_question__statement)):
        # Append that edit to our total list of fixings
        output_set_list.append(output_question__statement[i])

    # Notify the user how many edits we found
    print(f'-> Question editor finished with {num_edits} edits/suggestions found')

    # Sort all the output messages
    output_set_list.sort()
    # For each element in the list
    for i in range(len(output_set_list)):
        # Send that message to the output string
        output_question_msg += output_set_list[i]

    # Return the editing suggestions
    return output_question_msg
