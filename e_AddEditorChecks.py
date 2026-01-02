def getTheFile():
    """
    Function to 
    1. Grab the CSV file outputted by the question analyzing scripts
    2. Pass on the file to each editing function defined (where applicable)
    3. Create a file containing all the suggested edits found

    Returns file containing all the suggested edits found
    
    """
    # Imports
    import pandas as pd
    import f_EditSets
    import g_EditQuestions

    # Constants
    OUTPUT_FILE = 'OutputCSV.csv'

    # Notify the user that the editing process has begun
    print('--- Beginning to Edit ---\n')

    # Create a variable containing the editor's file contents
    editor_output = ''

    # Open the summarizer's output file
    with open(OUTPUT_FILE, 'r') as summarizer_file:
        # Create a data frame containing the file's contents
        df = pd.read_csv(summarizer_file, encoding = 'latin')

        # Check to see if we have actual sets or if we are dealing with a bunch of questions
        #-> Check if there is more than one set listed, or...
        #-> Check if there are exactly 20 quesitons (8 10s, 9 20s, and 3 30s) or...
        #-> Check if there are exactly 23 questions (9 10s, 10 20s, and 4 30s) - This includes substitute questions
        if ((df['Set_Num'].max() > 1) |
           (
                (df['Q_Num'].max() == 20) &
                (len(df.loc[df['Pt_Val'] == 10] == 8)) &
                (len(df.loc[df['Pt_Val'] == 20] == 9))
            ) |
            (
                (df['Q_Num'].max() == 23) &
                (len(df.loc[df['Pt_Val'] == 10] == 9)) &
                (len(df.loc[df['Pt_Val'] == 20] == 10))
            )
            ):
            # If one of these match, we have a set
            # Call edit_sets() to begin editing the question sets
            #-> Paste any edit suggestions to our output variable
            editor_output += f_EditSets.edit_sets(df)

            # Paste the findings to our output variable
        else:
            # If not, there are no sets to edit, we just move on
            print('No sets to edit')

        # Call edit_questions() to begin editing the actual questions
        #-> Paste any edit suggestions to our output variable
        editor_output += g_EditQuestions.edit_questions(df)

        # Return the edit messages
        return editor_output
