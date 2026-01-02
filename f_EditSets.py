def consecutive_counter(df, index):
    """
    Sub-sub-function to determine how many consecutive questions meet a previously-specified criteria

    Returns 
    -> A string containing the consecutive question numbers separated by commas
    -> How many consecutive numbers are contained
    -> The max index of the question streak
    
    """
    # Create a list to store the question numbers in
    list_q_nums = []
    # Add in the first question number of the consecutive streak
    list_q_nums.append(df['Q_Num'].iloc[index])
    # As long as the question numbers are in the set and...
    # As long as the questions numbers are consecutive
    while ((index + 1 < len(df['Q_Num'])) and (df['Q_Num'].iloc[index + 1] == df['Q_Num'].iloc[index] + 1)):
        # Append the question number in the list
        list_q_nums.append(df['Q_Num'].iloc[index+1])
        # Increment the index number
        index += 1

    # Determine how many consecutive numbers are contained
    count_consecutive = len(list_q_nums)

    # Return 
    #-> A string containing all the numbers in the list
    #-> The number of consecutive questions contained
    #-> The new index
    return (', '.join(map(str, list_q_nums)), count_consecutive, index)

def edit_sets__concordance(df):
    """
    Sub-Function to...
    1. Create a dataframe conatining all concordance questions
    2. Throw a flag to the output if...
        -> There are more than 5 Concordance questions
        -> There are consecutive, non-10-point questions that are Concordance
        -> There is no Concordance question from a verse's context (ConcFV) when there is a Concordance question asking the quizzer to say the verse(s) (ConcQE)
        -> There is no Concordance question asking the quizzer to say the verse(s) (ConcQE) when there is a Concordance question from a verse's context (ConcFV)

    Returns a list of output messages
    
    """
    # Imports
    import re

    # Create a blank list to store any output
    output_list = []

    # For each set
    for i in range(df['Set_Num'].max()):
        # Create a sub dataframe containing all the concordance questions in the set
        df_conc = df.loc[(df['Set_Num'] == i+1) & (df['Concordance'] != '_')]
        # If the set has concordance questions
        if len(df_conc) > 0:
            # =-=-=-=-=-=-=-=-=-= CHECKS =-=-=-=-=-=-=-=-=-=
            # === Check if there are more than 5 concordance questions in the set ===
            # See if there are more than 5 concordance questions in the set
            if len(df_conc) > 5:
                # If so, throw a flag
                if i < 9:
                    # If the set number is single-digit, add a zero in front of it... for sorting purposes
                    output_list.append(f'<p>* SET 0{i+1} may have too many Concordance questions (<i>{len(df_conc)}x</i>) (<i>{', '.join(map(str, df_set['Q_Num']))}</i>). Consider moving some of these to other sets.</p>')
                else: # If not, keep the set number the same
                    output_list.append(f'<p>* SET {i+1} may have too many Concordance questions (<i>{len(df_conc)}x</i>) (<i>{', '.join(map(str, df_set['Q_Num']))}</i>). Consider moving some of these to other sets.</p>')

            # === Check if there are consecutive, non-10-point questions that are concordance ===
            # Create a sub-dataframe containing all the non-10-point questions
            df_non_10 = df.loc[(df['Set_Num'] == i+1) & (df['Pt_Val'] != 10)]
            # Create an index variable to run through the following 'while' loop
            j = 0
            # Create a list for storing the question numbers that meet this criteria
            list_q_nums = []
            # For all the questions in this dataset
            while j < len(df_non_10):
                # As long as we are still in the dataframe and...
                # If questions j and j+1 are both concordance
                while ((j+1 < len(df_non_10) and (df_non_10['Concordance'].iloc[j] != '_') and (df_non_10['Concordance'].iloc[j+1] != '_'))):
                    # Append the jth questin's number to the list
                    list_q_nums.append(df_non_10['Q_Num'].iloc[j])
                    # Increment j
                    j += 1
                # If not, see if there is anything in the list
                if list_q_nums:
                    # If so, append the last number in the consecutive streak
                    list_q_nums.append(df_non_10['Q_Num'].iloc[j])
                    if i < 9:
                        # If the set number is single-digit, add a zero in front of it... for sorting purposes
                        output_list.append(f'<p>* SET 0{i+1}: There are consecutive, non-10-point questions (<i>{', '.join(map(str, list_q_nums))}</i>) that are Concordance questions. Consider spreading these out.</p>')    
                    else: # If not, keep the number the same
                        output_list.append(f'<p>* SET {i+1}: There are consecutive, non-10-point questions (<i>{', '.join(map(str, list_q_nums))}</i>) that are Concordance questions. Consider spreading these out.</p>')
                # Increment j
                j += 1
            

            # === Check if there is no CONC_FV when there is CONC_QE ===
            # If there is a concordance question asking the quizzer to quote/give in essence verses, and...
            # If there is no concordance question asking the quizzer to quote/give in essence verses
            if (len(df_conc.loc[df_conc['Q_Intro'].str.contains(r'Q|E')]) > 0) and (len(df_conc.loc[df_conc['Q_Intro'].str.contains(r'Q|E')]) == len(df_conc['Q_Intro'])):
                # Throw a flag
                if i < 9:
                    # If the set number is single-digit, add a zero in front of it... for sorting purposes
                    output_list.append(f'<p>* SET 0{i+1} asks Concordance question(s) where quizzers need to give the verses, but it does not ask for questions from the verse context. Consider adding in some.</p>')
                else: # If not, keep the number the same
                    output_list.append(f'<p>* SET {i+1} asks Concordance question(s) where quizzers need to give the verses, but it does not ask for questions from the verse context. Consider adding in some.</p>')

            # === Check if there is no CONC_QE when there is CONC_FV ===
            # If there as a concordance question asking the quizzer from the verse's context, and...
            # If there is no concordance question asking the quizzer to quote/give in essence verses
            if (len(df_conc.loc[df_conc['Q_Intro'].str.contains(r'Q|E') == False]) > 0) and (len(df_conc.loc[df_conc['Q_Intro'].str.contains(r'Q|E') == False]) == len(df_conc['Q_Intro'])):
                # Throw a flag
                if i < 9:
                    # If the set number is single-digit, add a zero in front of it... for sorting purposes
                    output_list.append(f'<p>* SET 0{i+1} asks Concordance question(s) from the verse context, but does not ask a Concordance question requriing the quizzer to say the verses. Consider adding in some.</p>')    
                else: # If not, keep the number the same
                    output_list.append(f'<p>* SET {i+1} asks Concordance question(s) from the verse context, but does not ask a Concordance question requriing the quizzer to say the verses. Consider adding in some.</p>')

        # Else, throw a flag that there are NO Concordance questions in the set
        else:
            if i < 9:
                # If the set number is single-digit, add a zero in front of it... for sorting purposes
                output_list.append(f'<p>! SET 0{i+1} has NO Concordance questions.  Consider adding some from other sets.</p>')
            else: # If not, keep the number the same
                output_list.append(f'<p>! SET {i+1} has NO Concordance questions.  Consider adding some from other sets.</p>')

    # Return the output list
    return output_list

def edit_sets__type_of_question(df):
    """
    Sub-function to throw a flag if...
    -> There are multiple Unique Word questions
    -> There are multiple "of" phrase questions
    -> There are multiple Adjective questions
    -> There are multiple "According to *verse*" questions
    -> There are multiple "About/Describe" questions
    -> There are multiple "How does *verse* describe *noun*" questions

    Returns a list of output messages to concatenate to the overall output
    
    """
    # Imports
    import re

    # Create a blank list to store any output
    output_list = []

    # For each set
    for i in range(df['Set_Num'].max()):
        # Create a sub dataframe containing the questions in just this set... for ease of access
        df_set = df.loc[df['Set_Num'] == i+1]

        # =-=-=-=-=-=-=-=-=-= CHECKS =-=-=-=-=-=-=-=-=-=
        # === Check if there are multiple Unique Word questions ===
        if len(df_set.loc[df['Notes'] == 'Unique word']) > 1:
            # If so, throw a flag
            if i < 9:
                # If the set number is single-digit, add a zero in front of it... for sorting purposes
                output_list.append(f'<p>* SET 0{i+1} has multiple <i>Unique Word</i> related questions (<i>{', '.join(map(str, list(df_set.loc[df['Notes'] == 'Unique word', 'Q_Num'])))}</i>). Consider moving these around other sets.</p>')
            else: # If not, keep the number the same
                output_list.append(f'<p>* SET {i+1} has multiple <i>Unique Word</i> related questions (<i>{', '.join(map(str, list(df_set.loc[df['Notes'] == 'Unique word', 'Q_Num'])))}</i>). Consider moving these around other sets.</p>')

        # === Check if there are multiple "of" phrase questions ===
        if len(df_set.loc[df['Notes'] == '"of" phrase']) > 1:
            # If so, throw a flag
            if i < 9:
                # If the set number is single-digit, add a zero in front of it... for sorting purposes
                output_list.append(f'<p>* SET 0{i+1} has multiple <i>"of" phrase</i> questions (<i>{', '.join(map(str, list(df_set.loc[df['Notes'] == '"of" phrase', 'Q_Num'])))}</i>). Consider moving these around other sets.</p>')
            else: # If not, keep the number the same
                output_list.append(f'<p>* SET {i+1} has multiple <i>"of" phrase</i> questions (<i>{', '.join(map(str, list(df_set.loc[df['Notes'] == '"of" phrase', 'Q_Num'])))}</i>). Consider moving these around other sets.</p>')

        # === Check if there are multiple Adjective questions ===
        if len(df_set.loc[df['Notes'] == 'Adjective']) > 1:
            # If so, throw a flag
            if i < 9:
                # If the set number is single-digit, add a zero in front of it... for sorting purposes
                output_list.append(f'<p>* SET 0{i+1} has multiple <i>Adjective</i> related questions (<i>{', '.join(map(str, list(df_set.loc[df['Notes'] == 'Adjective', 'Q_Num'])))}</i>). Consider moving these around other sets.</p>')
            else: # If not, keep the number the same
                output_list.append(f'<p>* SET {i+1} has multiple <i>Adjective</i> related questions (<i>{', '.join(map(str, list(df_set.loc[df['Notes'] == 'Adjective', 'Q_Num'])))}</i>). Consider moving these around other sets.</p>')
        
        # === Check if there are multiple "According to *verse*" questions ===
        if len(df_set.loc[df['Notes'] == 'According to *verse*']) > 1:
            # If so, throw a flag
            if i < 9:
                # If the set number is single-digit, add a zero in front of it... for sorting purposes
                output_list.append(f'<p>* SET 0{i+1} has multiple "<i>According to *verse*</i>" questions (<i>{', '.join(map(str, list(df_set.loc[df['Notes'] == 'According to *verse*', 'Q_Num'])))}</i>). Consider moving these around other sets.</p>')
            else: # If not, keep the number the same
                output_list.append(f'<p>* SET {i+1} has multiple "<i>According to *verse*</i>" questions (<i>{', '.join(map(str, list(df_set.loc[df['Notes'] == 'According to *verse*', 'Q_Num'])))}</i>). Consider moving these around other sets.</p>')
        
        # === Check if there are multiple "About/Describe" questions ===
        if len(df_set.loc[df['Notes'].str.contains(r'About|Describe')]) > 1:
            # If so, throw a flag
            if i < 9:
                # If the set number is single-digit, add a zero in front of it... for sorting purposes
                output_list.append(f'<p>* SET 0{i+1} has multiple "<i>About/Describe</i>" questions (<i>{', '.join(map(str, list(df_set.loc[df['Notes'].str.contains(r'About|Describe'), 'Q_Num'])))}</i>). Consider moving these around other sets.</p>')
            else: # If not, keep the number the same
                output_list.append(f'<p>* SET {i+1} has multiple "<i>About/Describe</i>" questions (<i>{', '.join(map(str, list(df_set.loc[df['Notes'].str.contains(r'About|Describe'), 'Q_Num'])))}</i>). Consider moving these around other sets.</p>')
        
        # === Check if there are multiple "How does *verse* describe *noun*" questions ===
        if len(df_set.loc[df['Notes'] == 'How does *verse* describe ___']) > 1:
            # If so, throw a flag
            if i < 9:
                # If the set number is single-digit, add a zero in front of it... for sorting purposes
                output_list.append(f'<p>* SET 0{i+1} has multiple "<i>How does *verse* describe ___</i>" questions (<i>{', '.join(map(str, list(df_set.loc[df['Notes'] == 'How does *verse* describe ___', 'Q_Num'])))}</i>). Consider moving these around other sets.</p>')
            else: # If not, keep the number the same
                output_list.append(f'<p>* SET {i+1} has multiple "<i>How does *verse* describe ___</i>" questions (<i>{', '.join(map(str, list(df_set.loc[df['Notes'] == 'How does *verse* describe ___', 'Q_Num'])))}</i>). Consider moving these around other sets.</p>')

    # Return the output
    return output_list
    
def edit_sets__intro(df):
    """
    Sub-Function to throw a flag if
    - 3 consecutive questions have the same introductory remark
      -> except for Complete Answer
    - There are more than 2 Statement and Questions
    - There are more than 4 Scripture Text Questions

    Returns a list of output messages to concatenate to the overall output
    
    """
    # Imports
    import re

    # Create a blank list to store any output
    output_list = []

    # For each set
    for i in range(df['Set_Num'].max()):
        # Create a sub dataframe containing the questions in just this set
        #-> For ease of access
        df_set = df.loc[df['Set_Num'] == i+1]

        # =-=-=-=-=-=-=-=-=-= CHECKS =-=-=-=-=-=-=-=-=-=

        # === Check if there are 3 or more consecutive questions with the same introductory remark ===
        # ----> Except for complete answer

        # Create a list containing all the question introdoctory shorthands
        #-> Except Application Questions
        #--> S = Statement and Question
        #--> \d+ = Multiple-part Question
        #--> T = Scripture Text Question
        #--> Q = Quotation Question
        #--> E = Essence Question
        #--> C = Quotation/Essence Completion Question
        list_q_shorthands = ['S', r'\d+', 'T', 'Q', 'E', 'C']
        # For each shorthand
        for j in range(len(list_q_shorthands)):
            # Create a sub-sub dataframe containing all the questions with that question shorthand
            df_shorthand = df_set.loc[df_set['Q_Intro'].str.contains(list_q_shorthands[j])]
            # Reset k
            k = 0
            # For each question in the sub dataframe
            while k < len(df_shorthand['Q_Intro']):
                # Check if the next 2 question numbers are consecutive
                if ((k+2 < len(df_shorthand['Q_Intro'])) and (df_shorthand['Q_Num'].iloc[k+2] == df_shorthand['Q_Num'].iloc[k] + 2)):
                    # Call consecutive_counter() to determine how many consecutive questions there are
                    str_consec, cnt, k = consecutive_counter(df_shorthand, k)
                    # Figure out which introductory remark is being repeated
                    if j == 0:
                        repeated_intro = 'Statement and Question'
                    elif j == 1:
                        repeated_intro = 'Multiple-Part Question'
                    elif j == 2:
                        repeated_intro = 'Scripture-Text Question'
                    elif j == 3:
                        repeated_intro = 'Quotation/Quotation Completion Question'
                    elif j == 4:
                        repeated_intro = 'Essence/Essence Completion Question'
                    else: # j == 5
                        repeated_intro = 'Quotation Completion/Essence Completion Question'
                    # Send a flag to the output
                    if i < 9:
                        # If the set number is single-digit, add a zero in front of it... for sorting purposes
                        output_list.append(f'<p>* SET 0{i+1}: {cnt} consecutive questions (<i>{str_consec}</i>) have the same introductory remark (<i>{repeated_intro}</i>). Consider moving these around.</p>')
                    else: # If not, keep the number the same
                        output_list.append(f'<p>* SET {i+1}: {cnt} consecutive questions (<i>{str_consec}</i>) have the same introductory remark (<i>{repeated_intro}</i>). Consider moving these around.</p>')
                else:
                    k += 1
        
        # Create a sub-sub dataframe containing all the questions with that question shorthand
        df_shorthand = df_set.loc[df_set['A_Intro'].str.contains(r'\d+')]
        # Reset k
        k = 0
        # For each question in the sub dataframe
        while k < (len(df_shorthand['A_Intro'])):
            # Check if the next 2 question numbers are consecutive
            if ((k+2 < len(df_shorthand['A_Intro'])) and (df_shorthand['Q_Num'].iloc[k+2] == df_shorthand['Q_Num'].iloc[k] + 2)):
                # If so, call consecutive_counter() to determine how many consecutive questions there are
                str_consec, cnt, k = consecutive_counter(df_shorthand, k)
                # Send a flag to the output
                if i < 9:
                    # If the set number is single-digit, add a zero in front of it... for sorting purposes
                    output_list.append(f'<p>* SET 0{i+1}: {cnt} consecutive questions (<i>{str_consec}</i>) have the same introductory remark (<i>Multiple-Part Answer</i>). Consider moving these around.</p>')
                else: # If not, keep the number the same
                    output_list.append(f'<p>* SET {i+1}: {cnt} consecutive questions (<i>{str_consec}</i>) have the same introductory remark (<i>Multiple-Part Answer</i>). Consider moving these around.</p>')
            # If not, just increment k
            else:
                k += 1
 
        # === Check if there are more than 2 questions marked Statement and Question ===
        if (len(df_set.loc[df_set['Q_Intro'].str.contains('S', case = True)]) > 2):
            # If so, grab the question numbers of these questions and...
            q_nums = df_set.loc[(df_set['Q_Intro'].str.contains('S', case = True)), ('Q_Num')]
            # Throw a flag
            if i < 9:
                # If the set number is single-digit, add a zero in front of it... for sorting purposes
                output_list.append(f'<p>* SET 0{i+1} may have too many questions (<i>{', '.join(map(str, q_nums))}</i>) (<i>{len(q_nums)}x</i>) labeled as <i>Statement and Question</i>. Consider moving some of these to other sets.</p>')
            else: # If not, keep the number the same
                output_list.append(f'<p>* SET {i+1} may have too many questions (<i>{', '.join(map(str, q_nums))}</i>) (<i>{len(q_nums)}x</i>) labeled as <i>Statement and Question</i>. Consider moving some of these to other sets.</p>')

        # === Check if there are more than 4 questions marked Scripture Text Question ===
        if (len(df_set.loc[df_set['Q_Intro'].str.contains('T', case = True)]) > 4):
            # If so, grab the question numbers of these questions and...
            q_nums = df_set.loc[(df_set['Q_Intro'].str.contains('T', case = True)), ('Q_Num')]
            # Throw a flag
            if i < 9:
                # If the set number is single-digit, add a zero in front of it... for sorting purposes
                output_list.append(f'<p>* SET 0{i+1} may have too many questions (<i>{', '.join(map(str, q_nums))}</i>) (<i>{len(q_nums)}x</i>) labeled as <i>Scripture-Text Question</i>. Consider moving some of these to other sets.</p>')
            else: # If not, keep the number the same
                output_list.append(f'<p>* SET {i+1} may have too many questions (<i>{', '.join(map(str, q_nums))}</i>) (<i>{len(q_nums)}x</i>) labeled as <i>Scripture-Text Question</i>. Consider moving some of these to other sets.</p>')

    # Return the output list
    return output_list

def edit_sets__A(df):
    """
    Sub-Function to...
    1. Pull out all Chapter Analysis questions in a set
    2. Throw a flag to the output if...
        -> 2 consecutive questions have the Chapter Analysis introductory remark
        -> A set has NO Chapter Analysis
        -> A set has more than 3 Chapter Analysis questions
        -> A set has multiple of the same type of Chapter Analysis question

    Returns a list of output messages to concatenate to the overall output
    
    """
    # Imports
    import re

    # Create a blank list to store any output
    output_list = []

    # For each set
    for i in range(df['Set_Num'].max()):
        # Create a sub-dataframe containing the questions labeled Chapter Analysis in the set
        df_A = df.loc[
                        (df['Set_Num'] == i+1) &
                        (df['A_Intro'].str.contains('A', case = True))
                      ]

        # =-=-=-=-=-=-=-=-=-= CHECKS =-=-=-=-=-=-=-=-=-=
    
        # === Check if consecutive questions have the Chapter Analysis introductory remark ===
        # Create a set to store the question numbers in
        set_consec_questions = set()
        # For each question in the Chapter Analysis dataframe
        for j in range(len(df_A['Q_Num'])):
            # Check if questions j and j+1 are consecutive
            if ((j+1 < len(df_A['Q_Num'])) and (df_A['Q_Num'].iloc[j+1]) == ((df_A['Q_Num'].iloc[j]) + 1)):
                # If so, put both question numbers into the set
                set_consec_questions.add(df_A['Q_Num'].iloc[j])
                set_consec_questions.add(df_A['Q_Num'].iloc[j+1])
            else:
                # If not, check if the set has question numbers in it
                if len(set_consec_questions) != 0:
                    # If yes, send a message to the output
                    if i < 9:
                        # If the set number is single-digit, add a zero in front of it... for sorting purposes
                        output_list.append(f'<p>* SET 0{i+1}: Consecutive questions (<i>{', '.join(map(str, set_consec_questions))}</i>) are labeled as <i>Chapter Analysis</i>. Consider moving these around.</p>')
                    else: # If not, keep the number the same
                        output_list.append(f'<p>* SET {i+1}: Consecutive questions (<i>{', '.join(map(str, set_consec_questions))}</i>) are labeled as <i>Chapter Analysis</i>. Consider moving these around.</p>')
                # Reset the set
                set_consec_questions = set()

        # === Check if there are NO Chapter Analysis in the set ===
        # Check if the length of the current set's dataframe is zero
        if len(df_A) == 0:
            # If so, throw a flag
            if i < 9:
                # If the set number is single-digit, add a zero in front of it... for sorting purposes
                output_list.append(f'<p>! SET 0{i+1} has NO Chapter Analysis questions in it. Consider adding one.</p>')
            else: # If not, keep the number the same
                output_list.append(f'<p>! SET {i+1} has NO Chapter Analysis questions in it. Consider adding one.</p>')
            
        # === Check if the set has more than 3 Chapter Analysis quesitons ===
        # Check if the lengh of the current set's dataframe is more than three
        if len(df_A) > 3:
            # If so, throw a flag
            if i < 9:
                # If the set number is single-digit, add a zero in front of it... for sorting purposes
                output_list.append(f'<p>* SET 0{i+1} may have too many Chapter Analysis questions (<i>{', '.join(map(str, df_A['Q_Num']))}</i>) (<i>{len(df_A)}x</i>). Consider moving some to other sets.</p>')
            else: # If not, keep the number the same
                output_list.append(f'<p>* SET {i+1} may have too many Chapter Analysis questions (<i>{', '.join(map(str, df_A['Q_Num']))}</i>) (<i>{len(df_A)}x</i>). Consider moving some to other sets.</p>')

        # === Check if the set has more than one of the same type of Chapter Analysis === 
        # Check if each question's note is unique
        #-> The casted set of the dataframe will have only the unique values
        #-> Thus, if the lengths are the same, there are no duplicate notes.
        if len(df_A['Notes']) != len(set(df_A['Notes'])):
            # If they are not the same, we have duplicate notes.
            # Find the notes that are duplicated and the associated question numbers
            duped_notes = df_A[df_A.duplicated(['Notes'], keep = False)]
            # For each unique duplicated note
            for j in set(duped_notes['Notes']):
                # Find all the quesitons in the set with that note
                duped_note_questions = list(df_A.loc[(df['Notes'] == j), ('Q_Num')])
                # Send the flag to the output list
                if i < 9:
                    # If the set number is single-digit, add a zero in front of it... for sorting purposes
                    output_list.append(f'<p>* SET 0{i+1} has multiple (<i>{', '.join(map(str, duped_note_questions))}</i>) of the same type of Chapter Analysis question (<i>{j}</i>). Consider spreading these throughout other sets.</p>')
                else: # If not, keep the number the same
                    output_list.append(f'<p>* SET {i+1} has multiple (<i>{', '.join(map(str, duped_note_questions))}</i>) of the same type of Chapter Analysis question (<i>{j}</i>). Consider spreading these throughout other sets.</p>')
                

    # Return the output list
    return output_list

def edit_sets__references(df):
    """
    Sub-Function to...
    1. Pull out all references in a set
    2. Throw a flag to the output if...
       -> 2 questions are from the same verse
       -> 2 consecutive questions are from the same chapter
       -> 4 consecutive questions are from the same book in a multiple-book season

    Returns a list of output messages to concatenate to the overall output
    
    """
    # Imports
    import re

    # Create a blank list to store any output
    output_list = []

    # For each set in the dataframe
    for i in range(df['Set_Num'].max()):
        # Create a list for the book(s)
        list_books = []
        # Create a list for the chapters
        list_chapters = []
        # Create a list for the references
        list_refs = []
        # Grab all the references in this set
        #-> Store those references in a list
        list_refs_by_question = list(df.loc[(df['Set_Num'] == i+1), ('Ans_Reference')])
        # For each question's reference(s)
        for j in range(len(list_refs_by_question)):
            # Send the book(s) to the books list
            list_books += re.findall(r'[a-zA-Z]+', list_refs_by_question[j])
            # Send the chapters to the chapters list
            list_chapters += re.findall(r'(\d+):', list_refs_by_question[j])
            # Send the verse references to the references list
            list_refs += re.findall(r':(\d+)', list_refs_by_question[j])
        # Replace the list of complete references with the combination of the other three lists
        list_complete_refs = [(f'{list_books[j]} {list_chapters[j]}:{list_refs[j]}') for j in range(len(list_chapters))]
        
    # =-=-=-=-=-=-=-=-=-= CHECKS =-=-=-=-=-=-=-=-=-=
        # === Check if 2 questions are from the same verse ===
        # Create a list that will contain all the duplicated references
        list_refs_multiple_times = []
        # Count the number of times each reference appears
        for j in range(len(list_complete_refs)):
            count_ref = list_complete_refs.count(list_complete_refs[j])
            # Check if there is more than one instance of that reference
            if count_ref > 1:
                # If so, check if we found that reference already
                if (list_complete_refs[j] in list_refs_multiple_times) == False:
                    # If not, put that reference in the list
                    list_refs_multiple_times.append(list_complete_refs[j])
                    # Find all the questions in the set with that reference in the answer
                    list_questions_with_same_ref = list(df.loc[(
                                                                (df['Ans_Reference'].str.contains(list_complete_refs[j])) & 
                                                                (df['Set_Num'] == i+1)
                                                                ), ('Q_Num')])
                    # Write an output message letting the user know what questions have duplicate references
                    if i < 9:
                        # If the set number is single-digit, add a zero in front of it... for sorting purposes
                        output_list.append(f'<p>* SET 0{i+1}: Multiple questions (<i>{', '.join(map(str, list_questions_with_same_ref))}</i>) are coming from the same verse (<i>{list_complete_refs[j]}</i>). Consider moving some to other sets.</p>')
                    else: # If not, keep the number the same
                        output_list.append(f'<p>* SET {i+1}: Multiple questions (<i>{', '.join(map(str, list_questions_with_same_ref))}</i>) are coming from the same verse (<i>{list_complete_refs[j]}</i>). Consider moving some to other sets.</p>')


        # === Check if 2 consecutive questions are from the same chapter ===
        # Check if there are multiple chapters
        #-> Create a set containing all the chapters in it
        set_chs = set((f'{list_books[j]} {list_chapters[j]}') for j in range(len(list_chapters)))
        #-> Determine if there are any duplicates
        #-> Create a list of chapters
        list_chs = [(f'{list_books[j]} {list_chapters[j]}') for j in range(len(list_chapters))]
        #--> Compare the lengths of the set and the list
        if len(set_chs) != len(list_chs):
            # If so, iterate through each element in the set
            for ch in set_chs:
                # Determine if that element appears more than once in the list
                if list_chs.count(ch) > 1:
                    # If so, create a dataframe of all questions with that chapter
                    df_identical_chapter = df.loc[(df['Set_Num'] == i+1) & (df['Ans_Reference'].str.contains(ch))]
                    # Create an index to go through the following "while" loop
                    k = 0
                    # For each chapter in the dataframe
                    while k < len(df_identical_chapter):
                        # If this is not the last element of the list, and...
                        # If the question number of elements k and k+1 are consecutive
                        if (k+1 < len(df_identical_chapter)) and (df_identical_chapter['Q_Num'].iloc[k+1] == df_identical_chapter['Q_Num'].iloc[k] + 1):
                            # Call consecutive_counter() to determine how many consecutive questions there are
                            str_consec, cnt, k = consecutive_counter(df_identical_chapter, k)
                            # Send a flag to the output
                            if i < 9:
                                # If the set number is single-digit, add a zero in front of it... for sorting purposes
                                output_list.append(f'<p>* SET 0{i+1}: Consecutive questions (<i>{str_consec}</i>) are coming from the same chapter (<i>{ch}</i>). Consider moving some of these to other sets.</p>')
                            else: # If not, keep the question number
                                output_list.append(f'<p>* SET {i+1}: Consecutive questions (<i>{str_consec}</i>) are coming from the same chapter (<i>{ch}</i>). Consider moving some of these to other sets.</p>')
                        else: # If not, increment k
                            k += 1
       # If not, we are only coming from one chapter. Ignore this flag
    
        # === Check if 4 consecutive questions are from the same book in a multiple-book season ===
        # Check for multiple books in the set
        if len(set(list_books)) != 1:
            # If we have multiple books, for each book
            for bk in set(list_books):
                # Create a sub-dataframe of all questions in this set with that book
                df_bk = df.loc[(df['Set_Num'] == i+1) & (df['Ans_Reference'].str.contains(bk))]
                # Create an index variable to go through the following "while" loop
                k = 0
                # For each instance of the book
                while k < len(df_bk):
                    # Make sure that we aren't at the end of the file and...
                    # See if there are at least three consecutive questions from that book
                    if (k+2 < len(df_bk)) and (df_bk['Q_Num'].iloc[k+2] == df_bk['Q_Num'].iloc[k] + 2):
                        # If so, call consecutive_counter() to see how many consecutive questions we have
                        str_consec, cnt, k = consecutive_counter(df_bk, k)
                        # Send a flag to the output
                        if i < 9:
                            # If the set number is single-digit, add a zero in front of it... for sorting purposes
                            output_list.append(f'<p>* SET 0{i+1}: {cnt} consecutive questions (<i>{str_consec}</i>) are coming from the same book (<i>{bk}</i>). Consider moving some of these to other sets.</p>')
                        else: # If not, keep the question number
                            output_list.append(f'<p>* SET {i+1}: {cnt} consecutive questions (<i>{str_consec}</i>) are coming from the same book (<i>{bk}</i>). Consider moving some of these to other sets.</p>')
                    else: # If not, increment k
                        k += 1          
        # If there is only one book present, ignore this section
    
    # Return the output list of strings
    return output_list

def edit_sets(df):
    """
    Function to perform editing suggestions on the layout of any sets of questions inputted
    Throws a flag to the output when...
    A Reference Issue Occurs
    - 2 questions are from the same verse
    - 2 consecutive questions are from the same chapter
    - 4 consecutive questions are from the same book in a season where multiple books are present
    A Chapter Analysis Issue Occurs
    - Consecutive questions have the Chapter Analysis introductory remark
    - There are NO Chapter Analysis questions
    - There are more than 3 Chapter Analysis questions
    - There are multiple of the same type of Chapter Analysis question
      -> by chapter, by section, concordance, etc.
    An Introductory Remark Issue Occurs
    - 3 consecutive questions have the same introductory remark
      -> except for Complete Answer
    - There are more than 2 Statement and Questions
    - There are more than 4 Scripture Text Questions
    A Type-of-Question Issue Occurs
    - There are multiple Unique Word questions
    - There are multiple "of" phrase questions
    - There are multiple Adjective questions
    - There are multiple "According to *verse*" questions
    - There are multiple "About/Describe" questions
    - There are multiple "How does *verse* describe *noun*" questions
    A Concordance Issue Occurs
    - There are more than 5 Concordance questions
    - There are consecutive, non-10-point questions that are Concordance
    - There is no Concordance question from a verse's context (ConcFV) when there is a Concordance question asking the quizzer to say the verse(s) (ConcQE)
    - There is no Concordance question asking the quizzer to say the verse(s) (ConcQE) when there is a Concordance question from a verse's context (ConcFV)

    Returns a string variable containing all the editing messages outputted
    
    """
    # Imports
    import re

    # Create a counting variable to tally the number of suggestions found
    num_edits = 0
    # Create a blank list to combine all the output messages to
    output_set_list = []
    # Create an output string variable to pass on to the output
    #-> Make the first line a title indicating these are SET edits
    output_set_msg = '<b>===== Question Set Edits / Suggestions =====</b><p>'

    # Call edit_sets__references() to check for any issues with the references in a set
    output_list__references = edit_sets__references(df)
    # Add the number of fixes to the total number of fixes we have
    num_edits += len(output_list__references)
    # For each element in the output
    for i in range(len(output_list__references)):
        # Concatenate that line to the output string
        output_set_list.append(output_list__references[i])

    # Check if there are any Chapter Analysis questions
    if len(df.loc[df['A_Intro'].str.contains('A', case = True)]) > 0:
        # If so, call edit_sets__A() to make any checks regarding Chapter Analysis questions
        output_list__A = edit_sets__A(df)
        # Add the number of fixes to the total number of fixes we have
        num_edits += len(output_list__A)
        # For each element in the output
        for i in range(len(output_list__A)):
            # Concatenate that line to the output string
            output_set_list.append(output_list__A[i])

    # Call edit_sets__intro() to make any checks regarding the introductory remarks
    output_list__intro = edit_sets__intro(df)
    # Add the number of fixes to the total number of fixes we have
    num_edits += len(output_list__intro)
    # For each element in the output
    for i in range(len(output_list__intro)):
        # Concatenate that line to the output string
        output_set_list.append(output_list__intro[i])

    # Call edit_sets__type_of_question() to make any checks regarding the question's Notes column
    output_list__type_of_question = edit_sets__type_of_question(df)
    # Add the number of fixes to the total number of fixes we have
    num_edits += len(output_list__type_of_question)
    # For each element in the output
    for i in range(len(output_list__type_of_question)):
        # Concatenate that line to the output string
        output_set_list.append(output_list__type_of_question[i])

    # Check if there are any Concordance questions
    if 'Concordance' in df.columns:
        # If so, call edit_sets__concordance()
        output_list__concordance = edit_sets__concordance(df)
        # Add the number of fixes to the total number of fixes we have
        num_edits += len(output_list__concordance)
        # For each element in the output
        for i in range(len(output_list__concordance)):
            # Concatenate that line to the output string
            output_set_list.append(output_list__concordance[i])

    # Notify the user that we are done editing the sets
    print(f'-> Set editor finished with {num_edits} edits/suggestions found')

    # Sort all the output messages
    output_set_list.sort()
    # For each element in the list
    for i in range(len(output_set_list)):
        # Send that message to the output string
        output_set_msg += output_set_list[i]
    
    # Return the editing suggestions
    return output_set_msg
