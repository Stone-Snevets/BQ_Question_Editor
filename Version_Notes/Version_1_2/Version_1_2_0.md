## Version 1.2.0
Date Added: April 9, 2026
### Features
- Swapped order of sets and questions to edit
  -> Edits to questions hold a bit more importance than general edits to sets. So put the more important first
- Re-worded error messages to order them by set number, then by question number
- Boldened the set number and question number of each edit for better visualization
- Increased the number of "Statement and Question"s to three per round

### Bug Fixes
* Words that had pronouns in them (e.g. "fruit" has "it" in it) were being read in as having prououns in a scripture text
* Flags for multiple of same question type had mixed single and double quotation marks
* Questions ending with some quotation from scripture that didn't end with a question mark or period were being flagged as not ending with proper punctuation
  -> For example: a question asking for the verse that contains a specific exclamation
* Questions with forms of the word "mystery" in a scripture text were being flagged as having the pronoun "my" in the scripture text
* Questions asking for how someone addresses someone else were being flagged as a 10-point question asking for a "how"
