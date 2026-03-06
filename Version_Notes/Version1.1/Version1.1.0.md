## Version 1.1.0
Date Added: March 6, 2026
### Features
- Added new flags for sets:
  - A set contains multiple "Reference of section" questions
  - A set contains consecutive "Statement and Question" questions
  - A set contains multiple Quotation/Essence Completion questions
  - A set contains multiple Standard Quotation/Essence questions
  - There are 3 consecutive questions of the same point value in a set
  - There are more than 4 Quotation/Essence [completion] questions in a set
- Added new flags for questions:
  - Question number 1 in a set is a Concordance question
  - A question is asking for multiple verses but only have one reference listed
    -> This stems off a bug in the question writer program that condenses a chunk of verses under one reference
  - A Quotation question doesn't ask the quizzer to "quote" a verse(s)
  - An Essence / Essence Completion question doesn't have the word "essence" in it
  - A question has a 1-word scripture text
  - A question starts with the word "Referring" but doesn't give any referral in the scripture text
  - A question has a pronoun in the scripture text, but doesn't refer the quizzer who/what that pronoun is
  - A question starts with "Referring to ___" but isn't labeled a Scripture Text question
  - A 10-point question asks "how" or "did what" rather than having the verb in the actual question

### Bug Fixes
* Question flag for questions asking for [complete] references marked as separate/consecutive verses had the wrong variable to iterate through
  -> This was causing "indexer out-of-bounds" errors
* Question flag for questions asking for [complete] references marked as separate/consecutive verses was not accounting for quotation/essence questions
  -> These can ask for both the verse and reference. In this case, the flag shouldn't be raised
* Question variables ending with a whitespace were being flagged as not ending with "?" or "."
* Flag for question number 1 being concordance wasn't accounting for sets with no concordance
