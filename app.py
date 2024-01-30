from flask import Flask, render_template, request, session, url_for, redirect, flash
from functools import wraps
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import csv
import random
from sqlalchemy.sql.schema import ForeignKey

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:\\Users\\tyblu\\Desktop\\Final Year Project\\Programming & Coding\\project final Edition\\project11\\quiznova.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)
app.secret_key = "SecretQuizNovaKey "

#flask database integration with sqlalchemy
class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), nullable=False)
    email = db.Column(db.String(35), nullable=False)
    password = db.Column(db.String(20), nullable=False)
    role = db.Column(db.String(10), nullable=False)

    def __init__(self, name, email, password, role):
        self.name = name
        self.email = email
        self.password = password
        self.role = role

    def __repr__(self):
        return '<Content %s%s>' % self.name % self.password % self.email % self.role

class Quiz(db.Model):
    __tablename__ = 'quiz'
    
    Qid = db.Column(db.Integer, primary_key=True)
    QInstruction = db.Column(db.String, nullable=False)
    QTitle = db.Column(db.String(30), nullable=False)
    QCode = db.Column(db.String(6), nullable=False)
    QStatus = db.Column(db.Boolean, default=False, nullable=False)
    QStartDate = db.Column(db.String(20), nullable=False)
    QEndDate = db.Column(db.String(20), nullable=False)
    QTMark = db.Column(db.Integer, nullable=False)     
    QTQuestion = db.Column(db.Integer, nullable=False)  
    QAttempt = db.Column(db.Integer, nullable=False) 

    def __init__(self, QInstruction, QTitle, QCode, QStatus, QStartDate, QEndDate, QTMark, QTQuestion, QAttempt):
        self.QInstruction = QInstruction
        self.QTitle = QTitle
        self.QCode = QCode
        self.QStatus = QStatus
        self.QStartDate = QStartDate
        self.QEndDate = QEndDate
        self.QTMark = QTMark
        self.QTQuestion = QTQuestion
        self.QAttempt = QAttempt


    def __repr__(self):
        return '<Content %s%s>' % self.QInstruction % self.QTitle % self.QCode % self.QStatus % self.QStartDate % self.QEndDate % self.QTMark % self.QTQuestion % self.QAttempt

class QQuestion(db.Model):
    __tablename__ = 'qquestion'
    
    QQid = db.Column(db.Integer, primary_key=True)
    Qid = db.Column(db.Integer, db.ForeignKey('quiz.Qid'), nullable=False) 
    QQNum = db.Column(db.Integer, nullable=False)
    question = db.Column(db.String, nullable=False)
    QQType = db.Column(db.String(30), nullable=False)
    QQAOption = db.Column(db.String, nullable=False)
    QQACheck = db.Column(db.String, nullable=False) 
    QQTime = db.Column(db.Integer, nullable=False)
    QQMarks = db.Column(db.Integer, nullable=False)  

    def __init__(self, Qid, QQNum, question, QQType, QQAOption, QQACheck, QQTime, QQMarks):
        self.Qid = Qid
        self.QQNum = QQNum
        self.question = question
        self.QQType = QQType
        self.QQAOption = QQAOption
        self.QQACheck = QQACheck
        self.QQTime = QQTime
        self.QQMarks = QQMarks
       

    def __repr__(self):
        return '<Content %s%s>' % self.Qid % self.QQNum % self.question % self.QQType % self.QQAOption % self.QQACheck % self.QQTime % self.QQMarks

class Score(db.Model):
    __tablename__ = 'score'

    scoreid = db.Column(db.Integer, primary_key=True)
    id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    Qid = db.Column(db.Integer, db.ForeignKey('quiz.Qid'), nullable=False)
    QQNum = db.Column(db.Integer, nullable=False)
    userAns = db.Column(db.String, nullable=False)
    QAns = db.Column(db.String, nullable=False)
    quizTime = db.Column(db.Integer, nullable=False)
    QQStuMarks = db.Column(db.Integer, nullable=False)     
    QAttempted = db.Column(db.Integer, nullable=False)
    SQuestion = db.Column(db.String, nullable=False)

    def __init__(self, id, Qid, QQNum, userAns, QAns, quizTime, QQStuMarks, QAttempted, SQuestion):
        self.id = id
        self.Qid = Qid
        self.QQNum = QQNum
        self.userAns = userAns
        self.QAns = QAns
        self.quizTime = quizTime
        self.QQStuMarks = QQStuMarks
        self.QAttempted = QAttempted
        self.SQuestion = SQuestion

    def __repr__(self):
        return '<Content %s%s>' % self.id % self.Qid % self.QQNum % self.userAns % self.QAns % self.quizTime % self.QQStuMarks % self.QAttempted % self.SQuestion

class Ranking(db.Model):
    __tablename__ = 'ranking'
    
    rankingID = db.Column(db.Integer, primary_key=True)
    id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    Qid = db.Column(db.Integer, db.ForeignKey('quiz.Qid'), nullable=False)
    rankingTime = db.Column(db.Integer, nullable=False)
    rankingMark = db.Column(db.Integer, nullable=False)
    attempted = db.Column(db.Integer, nullable=False)
    rank = db.Column(db.Integer, nullable=False)

    def __init__(self, id, Qid, rankingTime, rankingMark, attempted, rank):
        self.id = id
        self.Qid = Qid
        self.rankingTime = rankingTime
        self.rankingMark = rankingMark
        self.attempted = attempted
        self.rank = rank

    def __repr__(self):
        return '<Content %s%s>' % self.id % self.Qid % self.rankingTime % self.rankingMark % self.attempted % self.rank

class Achievement(db.Model):
    __tablename__ = 'achievement'
    
    badgeID = db.Column(db.Integer, primary_key=True)
    id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    badgeName = db.Column(db.String, nullable=False)
    badgeImage = db.Column(db.String, nullable=False)

    def __init__(self, id, badgeName, badgeImage):
        self.id = id
        self.badgeName = badgeName
        self.badgeImage = badgeImage

    def __repr__(self):
        return '<Content %s%s>' % self.id % self.badgeName % self.badgeImage

with app.app_context():
    db.create_all()        





# login required decorator
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap

# Route for handling the login page logic
@app.route('/', methods=['GET', 'POST'])
def login():
    error = None

    if request.method == 'POST':
        user = User.query.filter_by(email=request.form['email'], password=request.form['password']).first()

        if not user:
            error = f'Invalid email or password {user}'

        else:
            session['logged_in'] = user.id 
            session['logged_in_username'] = user.name
            role = user.role

            if role == "Student":
                return student_Home()
            elif role == "Lecturer":
                return home()

    return render_template('login.html', error=error)

@app.route('/logout')
@login_required
def logout():
    session.pop('logged_in', None)
    session.pop('logged_in_username', None)
    flash('You were just logged in!')
    return redirect(url_for('login'))
    
@app.route('/home')
@app.route('/home/<int:page_num>')
@login_required
def home(page_num=1): 
    user = User.query.get(session['logged_in'])
    role = user.role
    #To prevent student from enter lecturer page
    if role == "Student":
        return student_Home()

    quizList = Quiz.query.paginate(per_page=10,page=page_num,error_out=True)
    return render_template('adminDashboard.html', user=user, date=datetime.now(),quizzes = quizList)
      
### Quiz Management ###
@app.route('/quiz_management')
@app.route('/quiz_management/<int:quiz_pgnum>')
@login_required
def quiz_management(quiz_pgnum=1):
    
    user = User.query.get(session['logged_in'])
    role = user.role
    #To prevent student from enter lecturer page
    if role == "Student":
        return student_Home()

    all_quizData = Quiz.query.all()
    boolR = False
    r = randomCode()

    while(boolR == False):
      code = Quiz.query.filter_by(QCode=r).first()
      if code == None:
          boolR = True
      else:
        r = randomCode()

    checkDate()

    #Pagination for table in HTML
    quizList = Quiz.query.paginate(per_page=10,page=quiz_pgnum,error_out=True)

    all_quizData = Quiz.query.all()
    return render_template('quizManagement.html', quizs = all_quizData, Qcode=r,quizzes=quizList, user=user)

def randomCode():
    r = ""
    while(len(r) != 6):
        sequence = random.randint(1,3)
        if sequence == 1:
            a=random.randint(65,90)
            r += chr(a)
        elif sequence == 2:
            b=random.randint(97,122)
            r += chr(b)
        else:
            r += str(random.randint(0,9))
    return r

def checkDate():
    all_quizData = Quiz.query.all()
    #check if the start date and time is reached
    for quiz in all_quizData:
        qid = quiz.Qid
        currentDateTime=datetime.now()
        split1 = str(currentDateTime).split(" ")
        currentDate = split1[0].split("-")
        currentTime = split1[1].split(":")

        savedDateTime=quiz.QStartDate
        split2 = str(savedDateTime).split(" ")
        savedDate = split2[0].split("-")
        savedTime = split2[1].split(":")

        savedEDateTime=quiz.QEndDate
        split3 = str(savedEDateTime).split(" ")
        savedEDate = split3[0].split("-")
        savedETime = split3[1].split(":")
        status = quiz.QStatus
        if int(savedDate[0])<int(currentDate[0]) and int(savedEDate[0])>int(currentDate[0]):
            status = True
        elif int(savedDate[0])<=int(currentDate[0]) and int(savedEDate[0])>=int(currentDate[0]):
            if int(savedDate[1])<int(currentDate[1]) and int(savedEDate[1])>int(currentDate[1]):
                status = True
            elif int(savedDate[1])<=int(currentDate[1]) and int(savedEDate[1])>=int(currentDate[1]):
                if int(savedDate[2])<int(currentDate[2]) and int(savedEDate[2])>int(currentDate[2]):
                    status = True
                elif int(savedDate[2])<=int(currentDate[2]) and int(savedEDate[2])>=int(currentDate[2]):
                    if int(savedTime[0])<int(currentTime[0]): 
                        status = True
                    elif int(savedTime[0])==int(currentTime[0]):
                        if int(savedTime[1])<=int(currentTime[1]):
                            status = True
                        else:
                            status = False
                    else:
                        status = False
                else:
                    status = False
            else:
                status = False
        else:
            status = False

        if int(savedEDate[0])==int(currentDate[0]) and int(savedEDate[1])==int(currentDate[1]) and int(savedEDate[2])==int(currentDate[2]):
            if int(savedETime[0])<int(currentTime[0]): 
                        status = False
            elif int(savedETime[0])==int(currentTime[0]):
                if int(savedETime[1])<=int(currentTime[1]):
                            status = False

        questions = QQuestion.query.filter_by(Qid=qid).count()
        if questions == 0:
            status = False

        quiz.QStatus = status
        db.session.commit()

    return None
    
@app.route('/submitQ', methods=['GET', 'POST'])
@login_required
def submitQuiz():
    user = User.query.get(session['logged_in'])
    role = user.role
    #To prevent student from enter lecturer page
    if role == "Student":
        return student_Home()

    if request.method == 'POST':
        quizName = request.form['name']
        quizStatus = request.form['status']
        quizCode = request.form['code']
        quizStart = request.form['start-date'] + " " + request.form['start-time']
        quizEnd = request.form['end-date'] + " " + request.form['end-time']
        quizAttempt = request.form['attempts']
        session['created_quiz_qcode'] = quizCode
        if quizStatus == "open":
            status = True
        else:
            status = False

        quiz = Quiz("None", quizName, quizCode, status, quizStart, quizEnd, 0, 0, quizAttempt)
        db.session.add(quiz)
        db.session.commit()
        
    return redirect(url_for('instructionCreate'))

@app.route('/editQ', methods=['GET', 'POST'])
@login_required
def editQuiz():
    user = User.query.get(session['logged_in'])
    role = user.role
    #To prevent student from enter lecturer page
    if role == "Student":
        return student_Home()

    if request.method == 'POST':
        currentData = Quiz.query.get(request.form.get('Qid'))
        quizTitle = request.form['name']
        quizStatus = request.form['status']
        if quizStatus == "open":
            status = True
        else:
            status = False
        currentData.QTitle = quizTitle
        currentData.QStatus = status
        db.session.commit()
        
    return redirect(url_for('quiz_management'))

@app.route('/deleteQuiz', methods = ['GET', 'POST'])
def delete_quiz_data():
    user = User.query.get(session['logged_in'])
    role = user.role
    #To prevent student from enter lecturer page
    if role == "Student":
        return student_Home()

    if request.method =='POST':

        currentData = Quiz.query.get(request.form.get('Qid'))
        currentData2 = QQuestion.query.filter_by(Qid=int(request.form['Qid'])).all()
        for x in currentData2:
            QQid = x.QQid
            deletedQQid = QQuestion.query.get(QQid)
            db.session.delete(deletedQQid)
        db.session.delete(currentData)
        db.session.commit()
 
    return redirect(url_for('quiz_management'))

@app.route('/instruction', methods=['GET', 'POST'])
@login_required
def instruction():
    user = User.query.get(session['logged_in'])
    role = user.role
    #To prevent student from enter lecturer page
    if role == "Student":
        return student_Home()

    #get quiz_id
    session['selected_quiz_id_instruction'] = request.form['Qid']
    quiz = Quiz.query.get(int(request.form['Qid']))
    instruction = quiz.QInstruction

    return render_template('instructionPage.html', instructions=instruction)

@app.route('/instructionCreate', methods=['GET', 'POST'])
@login_required
def instructionCreate():
    user = User.query.get(session['logged_in'])
    role = user.role
    #To prevent student from enter lecturer page
    if role == "Student":
        return student_Home()

    currentData = Quiz.query.filter_by(QCode=session['created_quiz_qcode']).first()
    qid = currentData.Qid
    session['selected_quiz_id_instruction'] = qid
    quiz = Quiz.query.get(int(qid))
    instruction = quiz.QInstruction

    return render_template('instructionPage.html', instructions=instruction)

@app.route('/saveInstruction', methods=['GET', 'POST'])
@login_required
def saveInstruction():
    user = User.query.get(session['logged_in'])
    role = user.role
    #To prevent student from enter lecturer page
    if role == "Student":
        return student_Home()

    if request.method == 'POST':
        quiz_id = int(session['selected_quiz_id_instruction'])
        instruction = request.form['instruction']
        quiz = Quiz.query.get(quiz_id)
        quiz.QInstruction = instruction
        db.session.commit()

    return redirect(url_for('toCreateQuestionPage'))

### Questions Management ###
@app.route('/quiz_search', methods = ['GET', 'POST'])
@login_required
def quiz_search():
    user = User.query.get(session['logged_in'])
    role = user.role
    #To prevent student from enter lecturer page
    if role == "Student":
        return student_Home()

    if request.method =='POST':
        session.pop('selected_quiz_question', None)
        session.pop('selected_quiz_question_mark', None)
        session['selected_quiz'] = request.form['Qid']
        quizQuestions = QQuestion.query.filter_by(Qid=int(request.form['Qid'])).all()
        quiz = Quiz.query.filter_by(Qid=int(request.form['Qid'])).first()
        instruction = quiz.QInstruction

    else:
        session.pop('selected_quiz_question', None)
        session.pop('selected_quiz_question_mark', None)
        qid = session['selected_quiz']
        quizQuestions = QQuestion.query.filter_by(Qid=int(qid)).all()
        quiz = Quiz.query.filter_by(Qid=int(qid)).first()
        instruction = quiz.QInstruction
 
    return render_template('/questionManagement.html', quizQuestions=quizQuestions, quiz=quiz, instructions=instruction)

@app.route('/quiz_questions_page')
@login_required
def quiz_questions_page():
    user = User.query.get(session['logged_in'])
    role = user.role
    #To prevent student from enter lecturer page
    if role == "Student":
        return student_Home()

    session.pop('selected_quiz_question', None)
    session.pop('selected_quiz_question_mark', None)
    session['selected_quiz'] = session['selected_quiz_id_instruction'] 

    quizQuestions = QQuestion.query.filter_by(Qid=int(session['selected_quiz_id_instruction'])).all()
    quiz = Quiz.query.filter_by(Qid=int(session['selected_quiz_id_instruction'])).first()
    instruction = quiz.QInstruction
 
    return render_template('/questionManagement.html', quizQuestions=quizQuestions, quiz=quiz, instructions=instruction)

@app.route('/saveInstructionQ', methods=['GET', 'POST'])
@login_required
def saveInstructionQ():
    user = User.query.get(session['logged_in'])
    role = user.role
    #To prevent student from enter lecturer page
    if role == "Student":
        return student_Home()

    if request.method == 'POST':
        quiz_id = int(session['selected_quiz'])
        instruction = request.form['instruction']
        quiz = Quiz.query.get(quiz_id)
        quiz.QInstruction = instruction
        db.session.commit()

    return redirect(url_for('quiz_search'))

@app.route('/createQuestion', methods = ['GET', 'POST'])
@login_required
def toCreateQuestionPage():
    user = User.query.get(session['logged_in'])
    role = user.role
    #To prevent student from enter lecturer page
    if role == "Student":
        return student_Home()

    if request.method=='POST':       
        qid = session['selected_quiz']  
        questions = db.session.query(QQuestion).filter(QQuestion.Qid==qid).count()
        quiz = db.session.query(Quiz).filter(Quiz.Qid==qid).first()
        qnum = questions + 1
    else:
        session['selected_quiz'] = session['selected_quiz_id_instruction'] 
        qid = session['selected_quiz']  
        questions = db.session.query(QQuestion).filter(QQuestion.Qid==qid).count()
        quiz = db.session.query(Quiz).filter(Quiz.Qid==qid).first()
        qnum = questions + 1

    return render_template('createQuestion.html', qnum=qnum, quiz=quiz)

@app.route('/createQuestion/submit', methods = ['GET', 'POST'])
@login_required
def submitCreatedQuestion():
    user = User.query.get(session['logged_in'])
    role = user.role
    #To prevent student from enter lecturer page
    if role == "Student":
        return student_Home()

    if request.method=='POST':
        qid = session['selected_quiz']
        time = request.form['hiddenTime'] #time in seconds
        type = request.form['hiddenType'] #type of quiz
        point = request.form['hiddenPoint'] #point of quiz
        qnum = request.form['qqnum'] #quiz number
        question = request.form['qquestion'] #question     
        answerText = request.form['answerText'] #question
        checkText = request.form['checkText'] #question
        
        quiz = Quiz.query.filter_by(Qid=qid).first()
        quizNum = int(quiz.QTQuestion) + 1
        quiz.QTQuestion = int(quizNum)
        quizScore = int(quiz.QTMark) + int(point)
        quiz.QTMark = int(quizScore)
        if type == "fill":
            checkText = answerText 
        qquestion = QQuestion(int(qid), int(qnum), question, type, answerText, checkText, int(time), int(point))
        db.session.add(qquestion)
        db.session.commit()

    return redirect(url_for('quiz_search'))

@app.route('/questionEdit', methods = ['GET', 'POST'])
@login_required
def question_edit():
    user = User.query.get(session['logged_in'])
    role = user.role
    #To prevent student from enter lecturer page
    if role == "Student":
        return student_Home()

    if request.method =='POST':
        session['selected_quiz_question'] = request.form['QQid']
        quesData = QQuestion.query.filter_by(QQid=int(request.form['QQid'])).first()
        session['selected_quiz_question_mark'] = quesData.QQMarks
        time1 = quesData.QQTime
        type1 = quesData.QQType
        point1 = quesData.QQMarks
        qnum1 = quesData.QQNum
        question = quesData.question
        ques = str(question).split() 
        question1 = ""
        if len(ques) != 1:
            for q in ques:
                question1 = question1 + q + "["
        else:
            question1 = ques[0]
        answerText = quesData.QQAOption
        ansT = str(answerText).split() 
        answerText1 = ""
        if len(ansT) != 1:
            for a in ansT:
                answerText1 = answerText1 + a + "["
        else:
            answerText1 = ansT[0]
        checkText1 = quesData.QQACheck

    return render_template('/editQuestion.html', time=time1, type=type1, point=point1, qnum=qnum1,
     question=question1, answerText=answerText1, checkText=checkText1)

@app.route('/questionEdit/submit', methods = ['GET', 'POST'])
@login_required
def submitEditedQuestion():
    user = User.query.get(session['logged_in'])
    role = user.role
    #To prevent student from enter lecturer page
    if role == "Student":
        return student_Home()

    if request.method=='POST':
        qid = session['selected_quiz']
        qqid = session['selected_quiz_question']
        qqmarks = session['selected_quiz_question_mark']
        questionSelected = QQuestion.query.filter_by(QQid=int(qqid)).first()

        time = request.form['hiddenTime'] #time in seconds
        type = request.form['hiddenType'] #type of quiz
        point = request.form['hiddenPoint'] #point of quiz
        question = request.form['qquestion'] #question  
        answerText = request.form['answerText'] #answer options
        checkText = request.form['checkText'] #answer check
        
        questionSelected.QQTime = int(time)
        questionSelected.QQType = type
        questionSelected.QQMarks = int(point)
        questionSelected.question = question
        questionSelected.QQAOption = answerText
        if type == "fill":
            checkText = answerText 
        questionSelected.QQACheck = checkText

        quiz = Quiz.query.filter_by(Qid=int(qid)).first()
        quizScore = int(quiz.QTMark) - int(qqmarks) + int(point)
        quiz.QTMark = int(quizScore)
        db.session.commit()
    return redirect(url_for('quiz_search'))

@app.route('/questionDelete', methods = ['GET', 'POST'])
@login_required
def question_delete():
    user = User.query.get(session['logged_in'])
    role = user.role
    #To prevent student from enter lecturer page
    if role == "Student":
        return student_Home()

    if request.method =='POST':
        qid = session['selected_quiz']
        quiz = Quiz.query.get(qid)
        numQ = quiz.QTQuestion
        numQ = numQ - 1
        quiz.QTQuestion = numQ
        currentData = QQuestion.query.get(request.form.get('QQid'))
        marks = currentData.QQMarks
        Tmarks = quiz.QTMark
        Tmarks = Tmarks - marks
        quiz.QTMark = Tmarks
        db.session.delete(currentData)
        currentData2 = QQuestion.query.filter_by(Qid=int(qid)).all()
        qqnum = 1
        for x in currentData2:
            x.QQNum = int(qqnum)
            qqnum = qqnum + 1
        db.session.commit()

    return redirect(url_for('quiz_search')) 

#### STUDENT MANAGEMENT ###
@app.route('/student_management/',methods=['GET','POST'],defaults={"page_num":1})
@app.route('/student_management/<int:page_num>',methods=['GET','POST'])
@login_required
def student_management(page_num):
    studentList = User.query.filter(User.role=="Student").paginate(per_page=10,page=page_num,error_out=True)
    user = User.query.get(session['logged_in'])
    role = user.role
    #To prevent student from enter lecturer page
    if role == "Student":
        return student_Home()

    if request.method == 'POST' and 'tag' in request.form:
       tag = request.form["tag"]
       search = "%{}%".format(tag)
       studentList = User.query.filter(User.name.like(search)).paginate(per_page=10, error_out=True)
       return render_template('manageStudent.html',students=studentList, tag=tag, user=user)
    return render_template('manageStudent.html', students = studentList,user=user)

@app.route('/registerStudent', methods=['GET', 'POST'])
@login_required
def index():
    user = User.query.get(session['logged_in'])
    role = user.role
    #To prevent student from enter lecturer page
    if role == "Student":
        return student_Home()

    data = []
    if request.method == 'POST':
        csvf = request.form['csvfile']
        data = []

        with open(csvf) as file:
            csvfile = csv.reader(file)
            for row in csvfile:
                
                database = row
                if database[1] != 'Email':
                    user = User.query.filter_by(name=database[0]).first()
                    email = User.query.filter_by(email=database[1]).first()
                    if user == None and email == None:
                        USER = User(str(database[0]), str(database[1]), str(database[2]), str(database[3]))
                        data.append(row)
                        db.session.add(USER)   
                         
            db.session.commit()     
        flash("Upload Successfully")

    return render_template('registerStudent.html', data=data)

@app.route('/add', methods = ['POST'])
@login_required
def add_student_data():
    user = User.query.get(session['logged_in'])
    role = user.role
    #To prevent student from enter lecturer page
    if role == "Student":
        return student_Home()

    if request.method == 'POST':
        currname = request.form['name']
        curremail = request.form['email']
        currpassword = request.form['password']
        checking = User.query.filter_by(name=currname).count()
        if checking == 0:
            currentData = User(currname, curremail, currpassword,'Student')
            db.session.add(currentData)
            db.session.commit()
            flash("Added Successfully", "success")    
        else:
            flash(currname + " already exist in the database.", "error")
 
        return redirect(url_for('student_management'))

@app.route('/edit_student_by_id',methods=['GET','POST'])
@login_required
def edit_student_data():
    user = User.query.get(session['logged_in'])
    role = user.role
    #To prevent student from enter lecturer page
    if role == "Student":
        return student_Home()

    if request.method =='POST':
        currentData = User.query.get(request.form.get('id'))
        currname = currentData.name
        newname = request.form['name']
        checking = User.query.filter_by(name=newname).count()
        if newname != currname:
            if checking == 0:
                currentData.name = request.form['name']
            else:
                flash(newname + " already exist in the database.", "error")
        currentData.email = request.form['email']
        db.session.commit()
        flash('Updated Successfully')
        return redirect(url_for('student_management'))

@app.route('/delete', methods = ['GET', 'POST'])
@login_required
def delete_student_data():
    user = User.query.get(session['logged_in'])
    role = user.role
    #To prevent student from enter lecturer page
    if role == "Student":
        return student_Home()

    if request.method =='POST':
        currentData = User.query.get(request.form.get('id'))
        id = currentData.id
        currentData2 = Score.query.filter_by(id=int(id)).all()
        currentData3 = Achievement.query.filter_by(id=int(id)).all()
        currentData4 = Ranking.query.filter_by(id=int(id)).all()
        for x in currentData2:
            scoreid = x.scoreid
            score = Score.query.get(scoreid)
            db.session.delete(score)
        for y in currentData3:
            badgeID = y.badgeID
            achievement = Achievement.query.get(badgeID)
            db.session.delete(achievement)
        for z in currentData4:
            rankingID = z.rankingID
            ranking = Ranking.query.get(rankingID)
            db.session.delete(ranking)
        db.session.delete(currentData)
        db.session.commit()
        refreshRanking()
        flash("Deleted Successfully", "error")
 
    return redirect(url_for('student_management'))

def refreshRanking():
    quizs = db.session.query(Quiz).all()
    for quiz in quizs:
        qid = quiz.Qid
        ranks = db.session.query(Ranking).filter(Ranking.Qid==qid).all()

        if ranks != None:
            rankMarks = []
            rankTIME = []
            rankList = []
            for x in ranks:
                rankMarks.append(x.rankingMark)
                rankTIME.append(x.rankingTime)
                rankList.append(0)
            rankNum = 1
            while rankNum != (len(rankMarks)+1):
                counter = 0
                tempRankMark = 0
                tempRankTime = 100
                for i in range(len(rankMarks)):
                    if rankList[i] == 0:
                        if rankMarks[i] > tempRankMark:
                            tempRankMark = rankMarks[i]
                            tempRankTime = rankTIME[i]
                            counter = i
                        elif rankMarks[i] == tempRankMark and rankTIME[i] <= tempRankTime:
                            tempRankTime = rankTIME[i]
                            tempRankMark = rankMarks[i]
                            counter = i
                rankList[counter] = rankNum
                rankNum = rankNum + 1
            counter2 = 0
            for x in ranks:
                x.rank = int(rankList[counter2])
                counter2 = counter2 + 1
            db.session.commit()
    return None
### ACCOUNT PAGE ###
@app.route('/accSetup', methods = ['GET', 'POST'])
@login_required
def accSetup(): 
    user = User.query.get(session['logged_in'])
    role = user.role
    #To prevent student from enter lecturer page
    if role == "Student":
        return student_Home()
        
    currentPassword = "DummyPWD"
    currentName = user.name
    currentEmail = user.email
    currentRole = user.role

    return render_template('account.html', password=currentPassword, name=currentName,
     email=currentEmail, role=currentRole)

@app.route('/editAccount', methods=['GET', 'POST'])
@login_required
def edit_account():
    user = User.query.get(session['logged_in'])
    role = user.role
    #To prevent student from enter lecturer page
    if role == "Student":
         return student_Home()

    if request.method == 'POST':
        user = User.query.get(session['logged_in'])
        if request.form['name'] == None or request.form['email'] == None:
            return redirect(url_for('accSetup'))
        else:
            currname = user.name
            newname = request.form['name']
            checking = User.query.filter_by(name=newname).count()
            if newname != currname:
                if checking == 0:
                    user.name = request.form['name']
            user.email = request.form['email']
            if request.form['changePw'] == "true":
                checkPassword = User.query.filter_by(id=session['logged_in'], password=request.form['password']).count()
                if checkPassword != 0:
                    if request.form['repassword'] == "" or request.form['conpassword'] == "":
                        return redirect(url_for('accSetup'))
                    elif request.form['repassword'] == request.form['conpassword']:
                        user.password = request.form['repassword']
            
            db.session.commit()

    return redirect(url_for('accSetup'))

@app.route('/viewStudentAttempt', methods = ['GET', 'POST']) 
@login_required
def viewStudentAttempt():
    user = User.query.get(session['logged_in'])
    role = user.role
    #To prevent student from enter lecturer page
    if role == "Student":
        return student_Home()

    if request.method == 'POST':
        qid = request.form['Qid']
        results = db.engine.execute("SELECT * from ranking INNER JOIN user ON ranking.id = user.id AND ranking.Qid = " +qid+ " order by rank;")
        quiz = Quiz.query.get(qid)

    return render_template('viewStudentAttempt.html', results=results, quiz=quiz)
 
@app.route('/viewStudentRanking',methods=['GET','POST'])
@login_required
def viewStudentRanking():
    user = User.query.get(session['logged_in'])
    role = user.role
    #To prevent student from enter lecturer page
    if role == "Student":
        return student_Home()

    if request.method == 'POST':
        user = User.query.get(session['logged_in'])
        qid = request.form['Qid']
        quiz = Quiz.query.get(qid)
        result = db.engine.execute("SELECT * from ranking INNER JOIN user ON ranking.id = user.id AND ranking.Qid = " +qid+ " order by rank;")
        rank1 = Ranking.query.filter_by(rank=1, Qid=qid).first()
        rank2 = Ranking.query.filter_by(rank=2, Qid=qid).first()
        rank3 = Ranking.query.filter_by(rank=3, Qid=qid).first()
        rankID = 0
        student1 = ""
        student2 = ""
        student3 = ""
        if rank1 != None:
            rankID = rank1.id
            student1 = User.query.get(rankID)    

        if rank2 !=None:
            rankID = rank2.id
            student2 = User.query.get(rankID)

        if rank3 !=None:
            rankID = rank3.id
            student3 = User.query.get(rankID)

    return render_template('/studentRanking.html', user=user, result=result, quiz=quiz, rank1=rank1, student1=student1, rank2=rank2, student2=student2, rank3=rank3, student3=student3)


### THIS FOR STUDENT MODE ###
@app.route('/studentHomepage')
@login_required
def student_Home():
    user = User.query.filter_by(id=session['logged_in']).first()
    quizs = Quiz.query.filter_by(QStatus=True).all()
    checkDate()
    get_Achievement()
    return render_template('/student_mode/studentHomepage.html', user=user, quizs=quizs)

@app.route('/studentAccount', methods = ['GET', 'POST'])
@login_required
def SAccSetup(): 
    user = User.query.get(session['logged_in'])

    return render_template('/student_mode/settingAcc.html', user=user)

@app.route('/editAcc',methods=['GET','POST'])
@login_required
def editAcc():
    if request.method == 'POST':
        user = User.query.get(session['logged_in'])
        if request.form['name'] == None or request.form['email'] == None:
            return student_Home()
        else:
            currname = user.name
            newname = request.form['name']
            checking = User.query.filter_by(name=newname).count()
            if newname != currname:
                if checking == 0:
                    user.name = request.form['name']
            user.email = request.form['email']
            if request.form['changePw'] == "true":
                checkPassword = User.query.filter_by(id=session['logged_in'], password=request.form['password']).count()
                if checkPassword != 0:
                    if request.form['repassword'] == "" or request.form['conpassword'] == "":
                        return student_Home()
                    elif request.form['repassword'] == request.form['conpassword']:
                        user.password = request.form['repassword']        
            db.session.commit()
    return student_Home()

### FOR GAME PLAY ###
@app.route('/enterCode')
@login_required
def enterCode():
    get_Achievement()
    checkDate()

    return render_template('/gameplay/enterCode.html')

def get_Achievement():
    allUser = User.query.all()
    for user in allUser:
        userid = user.id
        quizTaken = Ranking.query.filter_by(id=userid).count()
        if quizTaken == 1:
            badges = Achievement.query.filter_by(id=userid, badgeName="Attempt 1 Quiz").count()
            if badges == 0:
                currentData = Achievement(int(userid), "Attempt 1 Quiz", 'attempts1.jpeg')
                db.session.add(currentData)
                db.session.commit()
        elif quizTaken == 5:
            badges = Achievement.query.filter_by(id=userid, badgeName="Attempt 5 Quiz").count()
            if badges == 0:
                currentData = Achievement(int(userid), "Attempt 5 Quizzes", 'attempts5.jpeg')
                db.session.add(currentData)
                db.session.commit()
        elif quizTaken == 10:
            badges = Achievement.query.filter_by(id=userid, badgeName="Attempt 10 Quiz").count()
            if badges == 0:
                currentData = Achievement(int(userid), "Attempt 10 Quizzes", 'attempts10.jpeg')
                db.session.add(currentData)
                db.session.commit()
        elif quizTaken == 50:
            badges = Achievement.query.filter_by(id=userid, badgeName="Attempt 50 Quiz").count()
            if badges == 0:
                currentData = Achievement(int(userid), "Attempt 50 Quizzes", 'attempts50.jpeg')
                db.session.add(currentData)
                db.session.commit()
    
    allQuizData = Quiz.query.all()
    for quiz in allQuizData:
        qid = quiz.Qid
        quizName = quiz.QTitle
        currentDateTime=datetime.now()
        split1 = str(currentDateTime).split()
        currentDate = split1[0].split("-")
        currentTime = split1[1].split(":")

        savedEDateTime = quiz.QEndDate
        split3 = str(savedEDateTime).split()
        savedEDate = split3[0].split("-")
        savedETime = split3[1].split(":")
        status = True
        if int(savedEDate[0])<int(currentDate[0]):
            status = False
        elif int(savedEDate[0])<=int(currentDate[0]):      
            if int(savedEDate[1])<int(currentDate[1]):
                status = False
            elif int(savedEDate[1])<=int(currentDate[1]):
                if int(savedEDate[2])<int(currentDate[2]):
                    status = False
                elif int(savedEDate[2])<=int(currentDate[2]):
                    if int(savedETime[0])<int(currentTime[0]): 
                        status = False
                    elif int(savedETime[0])<=int(currentTime[0]):
                        if int(savedETime[1])<=int(currentTime[1]):
                            status = False

        if status == False:
            badgeTop1 = "Top1-" + quizName
            badgeTop3 = "Top3-" + quizName
            badgeTop10 = "Top10-" + quizName
            top1rank = Ranking.query.filter_by(Qid=qid, rank=1).first()
            top3rank = Ranking.query.filter(Ranking.Qid==qid, Ranking.rank<=3).all()
            top10rank = Ranking.query.filter(Ranking.Qid==qid, Ranking.rank<=10).all()
            badges = Achievement.query.filter_by(badgeName=badgeTop1).count()
            if badges == 0:
                if top1rank != None:
                    ids = top1rank.id
                    currentData = Achievement(int(ids), badgeTop1, 'top1.jpeg')
                    db.session.add(currentData)
                    db.session.commit()
            
            badges = Achievement.query.filter_by(badgeName=badgeTop3).count()
            if badges == 0:
                if top3rank != None:
                    for data in top3rank:
                        ids = data.id
                        badges = Achievement.query.filter_by(badgeName=badgeTop3, id=ids).count()
                        if badges == 0:
                            currentData = Achievement(int(ids), badgeTop3, 'top3.jpeg')
                            db.session.add(currentData)
                            db.session.commit()
            
            badges = Achievement.query.filter_by(badgeName=badgeTop10).count()
            if badges == 0:
                if top10rank != None:
                    for data in top10rank:
                        ids = data.id
                        badges = Achievement.query.filter_by(badgeName=badgeTop10, id=ids).count()
                        if badges == 0:
                            currentData = Achievement(int(ids), badgeTop10, 'top10.jpeg')
                            db.session.add(currentData)
                            db.session.commit()

    return None

@app.route('/start',methods=['GET','POST'])
@login_required
def start():
    user = User.query.get(session['logged_in'])
    if request.method == 'POST':
        code = request.form['code']
        if user.role == "Lecturer":
            quiz = Quiz.query.filter_by(QCode=code).first()
        else:
            quiz = Quiz.query.filter_by(QCode=code, QStatus=True).first()
        if quiz == None:
            status = "Wrong Code!"
            return render_template('/gameplay/enterCode.html', status=status)
        else:
            session['start_quiz_id'] = quiz.Qid 
            questions = QQuestion.query.filter_by(Qid=int(session['start_quiz_id'])).all()
            attempts = db.session.query(Ranking).filter(Ranking.Qid==int(session['start_quiz_id']), Ranking.id==int(session['logged_in'])).all()
            if attempts == None:
                t = 0
            else:
                t = 0
                for x in attempts:
                    tries = x.attempted
                    if tries >= t:
                        t = tries
            
            if t == quiz.QAttempt:
                log = "OutOfAttempts"
            else:
                log = "ok"

    return render_template('/gameplay/startPage.html', quiz=quiz, questions=questions, attempts=t, log=log) 

@app.route('/start/submit',methods=['GET','POST'])
@login_required
def submitReport():
    if request.method == 'POST':
        qid = session['start_quiz_id']
        user = db.session.query(User).filter(User.id==int(session['logged_in'])).first()
        questions = db.session.query(QQuestion).filter(QQuestion.Qid==qid).all()
        quizAttempted = db.session.query(Ranking).filter(Ranking.Qid==qid, Ranking.id==int(session['logged_in'])).count()
        quizAns = request.form['hiddenQuizReport']
        quizTotalTime = request.form['hiddenTotalTime']
        quizTotalPoint = request.form['hiddenTotalPoint']
        optionAns = quizAns.split("[}")
        quizTime = quizTotalTime.split(";")
        quizPoint = quizTotalPoint.split(";")
        quizAttempted = quizAttempted + 1
        totalTime = 0
        totalPoint = 0
        role = user.role

        if role == "Student":
            for qnum in range(len(questions)):
                qType = questions[qnum].QQType
                userAns = ""
                quesAns = ""
                totalTime = totalTime + int(quizTime[qnum])
                totalPoint = totalPoint + int(quizPoint[qnum])
                question = questions[qnum].question

                if qType == "radio":
                    aOptions = questions[qnum].QQAOption
                    cOptions = questions[qnum].QQACheck
                    aOption = aOptions.split(";")
                    cOption = cOptions.split(";")
                    for i in range(len(cOption)-1):
                        if cOption[i] == "True":
                            quesAns = aOption[i]
                    userAns = optionAns[qnum]
                elif qType == "fill":
                    aOptions = questions[qnum].QQAOption
                    aOption = aOptions.split(";")
                    for i in range(len(aOption)-1):               
                        quesAns = quesAns + aOption[i] + ";"
                    userAns = optionAns[qnum]
                elif qType == "checkbox":
                    aOptions = questions[qnum].QQAOption
                    cOptions = questions[qnum].QQACheck
                    aOption = aOptions.split(";")
                    cOption = cOptions.split(";")
                    ansOption = optionAns[qnum].split(",")
                    for i in range(len(aOption)-1):
                        if cOption[i] == "True":
                            quesAns = quesAns + aOption[i] + ";"

                        if ansOption[i] == "True":
                            userAns = userAns + aOption[i] + ";"
                elif qType == "Matching":
                    aOptions = questions[qnum].QQAOption
                    cOptions = questions[qnum].QQACheck
                    aOption = aOptions.split(";")
                    cOption = cOptions.split(";")
                    ansOption = optionAns[qnum].split(",")
                    for i in range(len(aOption)-1):           
                        quesAns = quesAns + aOption[i] + "=" + cOption[i] + ";"        
                        userAns = userAns + aOption[i] + "=" + cOption[i] + ";"
            
                scoreData = Score(int(session['logged_in']), int(qid), (qnum+1), userAns, quesAns, int(quizTime[qnum]), int(quizPoint[qnum]), quizAttempted, question)
                db.session.add(scoreData) 
            rankData = Ranking(int(session['logged_in']), int(qid), int(totalTime), int(totalPoint), quizAttempted, 0)
            db.session.add(rankData)
            db.session.commit()          
        qid = session['start_quiz_id']
        ranks = db.session.query(Ranking).filter(Ranking.Qid==qid).all()
            
        if ranks == None:
            session.pop('start_quiz_id', None)
            return render_template('/gameplay/enterCode.html')

        else:
            rankMarks = []
            rankTIME = []
            rankList = []
            for x in ranks:
                rankMarks.append(x.rankingMark)
                rankTIME.append(x.rankingTime)
                rankList.append(0)
            rankNum = 1
            while rankNum != (len(rankMarks)+1):
                counter = 0
                tempRankMark = 0
                tempRankTime = 100
                for i in range(len(rankMarks)):
                    if rankList[i] == 0:
                        if rankMarks[i] > tempRankMark:
                            tempRankMark = rankMarks[i]
                            tempRankTime = rankTIME[i]
                            counter = i
                        elif rankMarks[i] == tempRankMark and rankTIME[i] <= tempRankTime:
                            tempRankTime = rankTIME[i]
                            tempRankMark = rankMarks[i]
                            counter = i
                rankList[counter] = rankNum
                rankNum = rankNum + 1
            counter2 = 0
            for x in ranks:
                x.rank = int(rankList[counter2])
                counter2 = counter2 + 1
            db.session.commit()
            session.pop('start_quiz_id', None)

    return redirect(url_for('student_Home'))

@app.route('/ranking')
@login_required
def choiceRanking():
    user = User.query.get(session['logged_in'])
    quizs = Quiz.query.all()
    return render_template('/student_mode/choiceRanking.html', user=user, quizs=quizs)

@app.route('/rankViewMore',methods=['GET','POST'])
@login_required
def ranking():
    if request.method == 'POST':
        user = User.query.get(session['logged_in'])
        qid = request.form['Qid']
        quiz = Quiz.query.get(qid)
        result = db.engine.execute("SELECT * from ranking INNER JOIN user ON ranking.id = user.id AND ranking.Qid = " +qid+ " order by rank;")
        rankID = 0
        ranking = Ranking.query.filter_by(Qid=int(qid), id=int(session['logged_in'])).all()
        if ranking != None:
            for row in ranking:
                rankID = row.id
        studentName = User.query.get(rankID) 

        rank1 = Ranking.query.filter_by(rank=1, Qid=qid).first()
        rank2 = Ranking.query.filter_by(rank=2, Qid=qid).first()
        rank3 = Ranking.query.filter_by(rank=3, Qid=qid).first()
        student1 = ""
        student2 = ""
        student3 = ""
        if rank1 != None:
            rankID = rank1.id
            student1 = User.query.get(rankID)    

        if rank2 !=None:
            rankID = rank2.id
            student2 = User.query.get(rankID)

        if rank3 !=None:
            rankID = rank3.id
            student3 = User.query.get(rankID)

    return render_template('/ranking.html', user=user, result=result, quiz=quiz, rank1=rank1,
     student1=student1, rank2=rank2, student2=student2, rank3=rank3, student3=student3, studentName=studentName, ranking=ranking)

@app.route('/viewAttempt',methods=['GET','POST'])
@login_required
def viewAttempt():
    if request.method == 'POST':
        user = User.query.get(session['logged_in'])
        session['view_quiz_id'] = request.form['Qid']
        qid = request.form['Qid']
        quiz = Quiz.query.get(qid)
        rank = Ranking.query.filter_by(id=int(session['logged_in']), Qid=int(qid)).all()

    else:
        return student_Home()

    return render_template('/student_mode/viewAttemptsMark.html', user=user, rank=rank, quiz=quiz)

@app.route('/viewAttempt/reports',methods=['GET','POST'])
@login_required
def viewAttemptReport():
    if request.method == 'POST':
        user = User.query.get(session['logged_in'])
        session['view_quiz_report_id'] = request.form['Qid']
        qid = request.form['Qid']
        attempts = request.form['Attempt']
        score = Score.query.filter_by(id=int(session['logged_in']), Qid=int(qid), QAttempted=int(attempts)).all()
        questions = QQuestion.query.filter_by(Qid=int(qid)).all()
        quiz = Quiz.query.get(qid)
        
    else:
        return student_Home()

    return render_template('/student_mode/viewAttemptsReport.html', user=user, score=score, questions=questions, quiz=quiz)

@app.route('/batches')
@login_required
def batches():
    user = User.query.get(session['logged_in'])
    achievementQ1 = Achievement.query.filter_by(id=session['logged_in'], badgeName="Attempt 1 Quiz").first()
    achievementQ5 = Achievement.query.filter_by(id=session['logged_in'], badgeName="Attempt 5 Quizzes").first()
    achievementQ10 = Achievement.query.filter_by(id=session['logged_in'], badgeName="Attempt 10 Quizzes").first()
    achievementQ50 = Achievement.query.filter_by(id=session['logged_in'], badgeName="Attempt 50 Quizzes").first()
    achievements = Achievement.query.filter_by(id=session['logged_in']).all()
    
    return render_template('/student_mode/batches.html',user = user, Q1=achievementQ1,
     Q5=achievementQ5, Q10=achievementQ10, Q50=achievementQ50, achievements=achievements)

if __name__ == "__main__":
    app.run(debug=True)