from BaseApp.models import UserProfile, Question, Option

# TODO: Write a method to return user preferred list based using sessions

def getTopQuestions(n): # TODO: Have some specific params for selecting top questions
    qList = Question.objects.all()
    l = len(qList)

    if(l < n):
        n = l

    return qList[:3]

def queryQuestions(searchQuery):
    if searchQuery is None or searchQuery == "":
        return None

    return Question.objects.filter(question_text__contains=searchQuery)

def getQuestionsByUser(user):
    if user is None:
        return None

    return Question.objects.filter(user=user)

def getQuestion(question_id):
    if question_id is None:
        return None

    return Question.objects.get(id=question_id)

def getOptions(question):
    return list(Option.objects.filter(question=question))

def getQuestionsByTopic(question_topic):
    if question_topic is None:
        return None

    return Question.objects.filter(question_topic=question_topic)
