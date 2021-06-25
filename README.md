# proftest-back
class Assessment
   <br/>
  categories = []
<br/>
 
class Category
  <br/>
  #belongs to assessment
  <br/>
  scope
   <br/>
  beginning
   <br/>
  developing
   <br/>
  accomplished
   <br/>
  questions = []
<br/>

class Question
  <br/>
  category_id
   <br/>
  text
<br/>

class Answer
  <br/>
  question_id
  <br/>
  text
  <br/>
  is_right
 <br/>

class Feedback
  <br/>
  #таблица ассоциации - связывает юзера и assessment
  <br/>
  score
  <br/>
  proficiency
   <br/>
  section
<br/>
  
class Submission
  <br/>
  question
  <br/>
  answers
  <br/>
  user
  <br/>
  time_submitted
  
