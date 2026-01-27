## Version 1.0.1
January 27th, 2026
### Features
- Added check for "According to *verse*" questions that come from a section
- Ordered outputs by Importance, then by Set Number, then by Question Number
-> These now have leading zeros where necessary
- Optimized set number ordering
-> Used format string properties instead of "if" statements

### Bug Fixes
* The flag for questions with multiple references in the answer but no indication in the introductory remarks was not accounting for Quotation/Essence Completion questions
* Counting the number of consecutive, non-concordance questions kept repeating itself causing too many output messages
* Fixed typo in flag message where questions are asking for only the reference when the chapter was not given
* Fixed typo in flag message where sets ask Concordance from the verse context but not by making quizzers say the verses
