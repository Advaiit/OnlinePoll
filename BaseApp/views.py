from django.shortcuts import render
from django.views import View
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from BaseApp.models import UserProfile, Question, Option
from django.contrib.auth.models import User
from BaseApp import content_util as c_util
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.
class HomeView(View):
    template_name = 'BaseApp/base.html'

    def get(self, request):
        return render(request, self.template_name, {'list_title':'Home', 'question_list':c_util.getTopQuestions(3)})

class AddPollView(View):
    template_name = "BaseApp/add_poll.html"
    ctxt = {'list_title':'Add Poll'}

    def get(self, request):
        if request.user.is_authenticated:
            return render(request, self.template_name, context=self.ctxt)

        return HttpResponseRedirect(reverse("base_app:Home"))


    def post(self, request):
        if request.user.is_authenticated:
            question_text = request.POST.get("question_text")
            question_topic = request.POST.get("question_topic")
            question_comments = request.POST.get("question_comments")

            option1 = request.POST.get("option1")
            option2 = request.POST.get("option2")
            option3 = request.POST.get("option3")
            option4 = request.POST.get("option4")

            currentUser, obj = UserProfile.objects.get_or_create(user=request.user)
            question = Question.objects.create(user=currentUser, question_text=question_text, question_topic=question_topic, question_comments=question_comments)
            question.save()

            if option1 != "":
                op1 = Option.objects.create(question=question, option_text=option1, vote_count=0)
                op1.save()

            if option2 != "":
                op2 = Option.objects.create(question=question, option_text=option2, vote_count=0)
                op2.save()

            if option3 != "":
                op3 = Option.objects.create(question=question, option_text=option3, vote_count=0)
                op3.save()

            if option4 != "":
                op4 = Option.objects.create(question=question, option_text=option4, vote_count=0)
                op4.save()

        return render(request, self.template_name, context=self.ctxt)

class PollView(View):
    template_name = "BaseApp/poll.html"

    def get(self, request, question_id):
        q = c_util.getQuestion(question_id)
        optionList = c_util.getOptions(q)
        ctxt = {'list_title':'Poll'}
        ctxt['question'] = q
        ctxt['optionList'] = optionList
        ctxt['disableDone'] = True

        if request.user.is_authenticated:
            currentUser, obj = UserProfile.objects.get_or_create(user=request.user)
            try:
                currentUser.questions.get(id=question_id)
            except ObjectDoesNotExist:
                ctxt['disableDone'] = False

        return render(request, self.template_name, context=ctxt)

    def post(self, request, question_id):
        q = c_util.getQuestion(question_id)
        optionList = c_util.getOptions(q)
        ctxt = {'list_title':'Poll'}
        ctxt['question'] = q
        ctxt['optionList'] = optionList
        ctxt['disableDone'] = True

        if request.user.is_authenticated:
            selected_option_id = request.POST.get("option")
            currentUser, obj = UserProfile.objects.get_or_create(user=request.user)
            option = Option.objects.get(id=selected_option_id)

            try:
                option.question.responders.get(id=currentUser.id)
            except ObjectDoesNotExist:
                option.question.responders.add(currentUser)
                option.vote_count += 1
                currentUser.user_points += 1
                option.save()
                currentUser.save()

        return render(request, self.template_name, context=ctxt)

class PollList(View):
    template_name = "BaseApp/poll_list.html"
    list_title = "List"
    ctxt = {'list_title':list_title}

    def get(self, request, question_topic=""):
        if question_topic is not "":
            self.ctxt['question_list'] = c_util.getQuestionsByTopic(question_topic)
            return render(request, self.template_name, context=self.ctxt)
        else:
            if request.user.is_authenticated:
                currentUser, obj = UserProfile.objects.get_or_create(user=request.user)
                self.ctxt['question_list'] = c_util.getQuestionsByUser(currentUser)
                return render(request, self.template_name, context=self.ctxt)
        return HttpResponseRedirect(reverse("base_app:Home"))

class PollSearch(View):
    template_name = "BaseApp/poll_search.html"
    list_title = "Search"

    def get(self, request):
        return render(request, self.template_name, context={'list_title':self.list_title})

    def post(self, request):
        searchQuery = request.POST.get("searchQuery")
        return render(request, self.template_name, context={'list_title':self.list_title, 'question_list':c_util.queryQuestions(searchQuery)})

class Profile(View):
    template_name = "BaseApp/profile.html"
    list_title =     list_title = "Profile"
    ctxt = {'list_title':list_title}

    def get(self, request):
        return render(request, self.template_name, context=self.ctxt)

def register(request):
    print("REGISTER CALLED")
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        email = request.POST.get("email")

        # TODO: Perform a check against same username
        if(False):
            return render(HttpResponse("User already exist. TODO: Display better"))

        if(password != request.POST.get("confirm-password")):
            return render(HttpResponse("Password doesnt match with confirm password (TODO: Display better)"))

        # TODO: Perform validations on form here

        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()

        user_profile = UserProfile.objects.create(user=user)

        if 'profile_pic' in request.FILES:
            print("FILE NAME: ")
            print(request.FILES['profile_pic'].name)
            request.FILES['profile_pic'].name = str(user_profile.id)+"_"+request.FILES['profile_pic'].name

            user_profile.profile_pic = request.FILES['profile_pic']

        user_profile.save()

        user = authenticate(username=username, password=password) # TODO: try after removing this line

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('base_app:Home'))
            else:
                return HttpResponse("Account Not Active todo: have a better display")
        else:
            return HttpResponse("Something is not right with signup login")

        return HttpResponse("Try pushing signup button")

    return HttpResponse("Try pushing sign up button 2")


def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse("base_app:Home"))
            else:
                return HttpResponse("Account Not Active todo: have a better display")
        else:
            print("Login Failed: username: {}, password: {}".format(username, password))
            return HttpResponse("Invalid Login Details")
    else:
        render(request, reverse("base_app:Home"), {'list_title':'Home'})


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse("base_app:Home"))
