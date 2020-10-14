from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt,csrf_protect
from yaksh.decorators import has_profile
from yaksh.models import QuestionPaper, AnswerPaper, Profile, Course, Update, CurrentAffair
from yaksh.models import LearningModule, Quiz
from yaksh.views import my_render_to_response, my_redirect
from rest_framework import status
from letsprepare.models import AvailableQuizzes, PaytmHistory
from letsprepare.serializers import AvailableQuizzesSerializer, ErrorSerializer
import json
from plotly.offline import plot
import plotly.graph_objs as go
from twilio.rest import Client
from random import randint
from online_test import settings
from django.utils import timezone
from django.db import IntegrityError

from yaksh.send_emails import generate_activation_key
from datetime import datetime, date
import razorpay

from dateutil.relativedelta import relativedelta

if settings.IS_DEVELOPMENT:
    key = settings.rzp_key_dev
    secret_key = settings.rzp_secret_key_dev
else:
    key = settings.rzp_key_prod
    secret_key = settings.rzp_secret_key_prod

client = razorpay.Client(auth=(key, secret_key))

tw_client = Client(settings.sid, settings.token)

def show_all_quizzes(request):
    user = request.user
    id = request.GET['id']
    try:
        availableQuizzes = json.loads(json.dumps(AvailableQuizzesSerializer(AvailableQuizzes.objects.filter(user=user, successful=True), many=True).data))
        availableQuizIds = [quiz['quiz'] for quiz in availableQuizzes]
    except:
        availableQuizIds = []
    module = LearningModule.objects.get(id = id)
    course = list(Course.objects.all())[0]
    quizzes = module.get_quiz_units()
    quizzes = sorted(quizzes, key=lambda item: int(item.quiz_code.split('_')[1]))
    try:
        answerpapers = AnswerPaper.objects.filter(user=request.user)
    except:
        answerpapers = []
    question_papers_attempted = [i.question_paper.id for i in answerpapers]
    question_papers_data = []
    for qz in quizzes:
        for qp in list(QuestionPaper.objects.filter(quiz=qz.id)):
            question_papers_data.append({
                'code' : qz.quiz_code,
                'name': qz.description,
                'duration': qz.duration,
                'total_questions': qz.questionpaper_set.get(quiz=qz.id).tot_questions(),
                'weightage': qz.weightage,
                'id': qp.id,
                'attempts' : question_papers_attempted.count(qp.id),
            })
            if qz.id in availableQuizIds or qz.is_free:
                question_papers_data[-1]['available'] = True
            else:
                question_papers_data[-1]['available'] = False

    context = {
        'module' : module.name,
        'module_id' : module.id,
        'course_id' : course.id,
        'user': user,
        'question_papers': question_papers_data
    }
    #return render(request, 'yaksh/all_question_papers.html', context)
    return render(request, 'portal_pages/all_question_papers.html', context)

def show_all_modules(request):
    user = request.user
    # exams = Exams.objects.all()
    modules_data = []
    try:
        availableQuizzes = json.loads(json.dumps(AvailableQuizzesSerializer(AvailableQuizzes.objects.filter(user=user, successful = True), many=True).data))
        availableQuizIds = [quiz['quiz'] for quiz in availableQuizzes]
    except:
        availableQuizIds = []
    for module in list(LearningModule.objects.all()):
        quizzes = module.get_quiz_units()
        has_quizzes = 0
        for quiz in quizzes:
            if quiz.id in availableQuizIds or quiz.is_free:
                has_quizzes += 1
        modules_data.append({'name' : module.description, 'id' : module.id,
                              'total_quizzes' : len(quizzes), 'has_quizzes' : has_quizzes })
    context = {
        'user': user, 'modules': modules_data,
        'title': 'ALL  AVAILABLE  MODULES'
    }
    #return my_render_to_response(request, "yaksh/all_modules.html", context)
    
    return my_render_to_response(request, "portal_pages/subjects.html", context)

def show_all_on_sale(request):
    user = request.user
    modules_data = []
    try:
        availableQuizzes = json.loads(json.dumps(AvailableQuizzesSerializer(AvailableQuizzes.objects.filter(user=user, successful=True), many=True).data))
        availableQuizIds = [quiz['quiz'] for quiz in availableQuizzes]
    except:
        availableQuizIds = []
    for module in list(LearningModule.objects.all()):
        quizzes = module.get_quiz_units()

        quizzes = sorted(quizzes, key=lambda item: int(item.quiz_code.split('_')[1]))
        quiz_data = []
        for quiz in list(quizzes):
            # calculating discount
            # start
            discoun = 0
            # if the discount has to be applied on the base of the module discount or want default discount.
            if module.apply_to_all_quiz == True or quiz.is_default_discount == True:
                discoun = module.discount
            else:
                discoun = quiz.discount
            # end
            quiz_data.append({'name': quiz.description, 'code' : quiz.quiz_code, 'price' : quiz.price*((100-discoun)/100), 'org_price' : quiz.price, 'id':quiz.id})
            if quiz.id in availableQuizIds or quiz.is_free:
                quiz_data[-1]['available'] = True
            else:
                quiz_data[-1]['available'] = False
        module_price = sum([quiz['price'] for quiz in quiz_data if not quiz['available']])
        modules_data.append({'name': module.description, 'id': module.id, 'quizzes': quiz_data, 'state': 'Active', 'org_price' : module_price *2, 'price' : module_price})

    context = {
        'user': user, 'modules': modules_data,
        'title': 'ALL  AVAILABLE  MODULES'
    }
    # return my_render_to_response(request, "yaksh/all_on_sale.html", context)
    return my_render_to_response(request, "buy/all_on_sale.html", context)

@csrf_exempt
@login_required
@has_profile
def assign_quizzes(request):
    results = json.loads(request.POST['data'])
    try:
        profile = Profile.objects.get(user = request.user)

        name = profile.user.first_name + ' ' + profile.user.last_name
        phone = profile.phone_number
        email = profile.user.email
        product = 'Tests'

        amount = sum([quiz.price for quiz in Quiz.objects.filter(id__in=[quiz for quiz in results['quizzes']])])

        order_amount = amount*100

        order_currency = 'INR'
        order_receipt = ''
        notes = {'': ''}

        # CREAING ORDER
        response = client.order.create(
            dict(amount=order_amount, currency=order_currency, receipt=order_receipt, notes=notes, payment_capture='0'))
        order_id = response['id']
        order_status = response['status']

        for quiz in results['quizzes']:
            data = {'user': request.user.id,
                    'quiz': quiz,
                    'order_id': order_id
                    }
            available_quizzes_serializer = AvailableQuizzesSerializer(data=data)
            if available_quizzes_serializer.is_valid():
                available_quizzes_serializer.save()

        context = {}
        if order_status == 'created':
            # Server data for user convinience
            context['product_id'] = product
            context['price'] = order_amount
            context['name'] = 'missionpcs'
            context['prefill[name]'] = name
            context['prefill[contact]'] = phone
            context['prefill[email]'] = email
            context['key_id'] = key

            # data that'll be send to the razorpay for
            context['order_id'] = order_id
            context['description'] = name
            if settings.IS_DEVELOPMENT:
                context['callback_url'] = 'http://127.0.0.1:8000/letsprepare/verify_payment/'
            else:
                context['callback_url'] = 'https://missionpcs.com/letsprepare/verify_payment/'
            url = 'https://api.razorpay.com/v1/checkout/embedded'
        # paytmParams, checksum, url = get_payment_params(results['amount'], profile.phone_number, request.user.id, request.user.email, order_id)
            return JsonResponse({'paymentParams': context, 'url' : url})

    except Exception as e:
        return my_render_to_response(request, '404.html')

@login_required
def show_results(request):
    answerpapers = AnswerPaper.objects.filter(user = request.user)
    question_papers_attempted = [i.question_paper for i in answerpapers]
    question_papers_data = []
    for qp in set(question_papers_attempted):
        question_papers_data.append({
            'code' : qp.quiz.quiz_code,
            'name': qp.quiz.description,
            'id': qp.id
        })
    fig = get_percentage_graph(question_papers_attempted,answerpapers)
    plot_div = plot(fig,
        output_type='div',config=dict(
                    displayModeBar=False,
                    dragMode=False,
                    scrollZoom=False,
                    staticPlot= True
                ), include_plotlyjs=False)
    fig2 = get_accuracy_graph(question_papers_attempted, answerpapers)
    plot_div2 = plot(fig2,
                    output_type='div', config=dict(
            displayModeBar=False,
            dragMode=False,
            scrollZoom=False,
            staticPlot=True
        ), include_plotlyjs=False)
    # return my_render_to_response(request, "yaksh/results.html", context={'question_papers' : question_papers_data, 'plot_div': plot_div, 'plot_div2': plot_div2,
    #                                                                      'course_id' : list(Course.objects.all())[0].id})
    return my_render_to_response(request, "upgradev001/results.html", context={'question_papers' : question_papers_data, 'plot_div': plot_div, 'plot_div2': plot_div2,
                                                                         'course_id' : list(Course.objects.all())[0].id})

def get_accuracy_graph(question_papers_attempted, answerpapers):
    attempt_dict = {}
    qa_tups = zip(question_papers_attempted,answerpapers)
    qa_tups_ordered = [qa for qa in sorted(qa_tups, key=lambda item: item[1].end_time)]
    for qp, ap in qa_tups_ordered:
        num_attempted = len(ap.questions_answered.all())
        if qp.quiz.quiz_code in attempt_dict.keys():
            if num_attempted == 0:
                attempt_dict[qp.quiz.quiz_code].append(0)
            else:
                attempt_dict[qp.quiz.quiz_code].append(round(((ap.marks_obtained)/len(ap.questions_answered.all())*100),2))
        else:
            attempt_dict[qp.quiz.quiz_code] = []
            if num_attempted == 0:
                attempt_dict[qp.quiz.quiz_code].append(0)
            else:
                attempt_dict[qp.quiz.quiz_code].append(round(((ap.marks_obtained)/len(ap.questions_answered.all()))*100,2))

    fy = []
    sy = []

    attempts = list(attempt_dict.keys())
    for uqp in attempts:
        try:
            fy.append(attempt_dict[uqp][0])
        except:
            fy.append(0)
        try:
            sy.append(attempt_dict[uqp][1])
        except:
            sy.append(0)

    trace1 = go.Bar(
        x=attempts,
        y=fy,
        text=[str(i) for i in fy],
        textposition='outside',
        name='Attempt 1',
        hoverinfo='skip'
    )
    trace2 = go.Bar(
        x=attempts,
        y=sy,
        text=[str(i) for i in sy],
        textposition='outside',
        name='Attempt 2',
        hoverinfo='skip'
    )

    data = [trace1, trace2]
    layout = go.Layout(barmode='group', yaxis=dict(range=[0, 108]))
    fig = go.Figure(data=data, layout=layout)
    return fig


def get_percentage_graph(question_papers_attempted, answerpapers):
    attempt_dict = {}
    qa_tups = zip(question_papers_attempted,answerpapers)
    qa_tups_ordered = [qa for qa in sorted(qa_tups, key=lambda item: item[1].end_time)]
    for qp, ap in qa_tups_ordered:
        if qp.quiz.quiz_code in attempt_dict.keys():
            attempt_dict[qp.quiz.quiz_code].append(ap.percent)
        else:
            attempt_dict[qp.quiz.quiz_code] = []
            attempt_dict[qp.quiz.quiz_code].append(ap.percent)

    fy = []
    sy = []

    attempts = list(attempt_dict.keys())
    for uqp in attempts:
        try:
            fy.append(attempt_dict[uqp][0])
        except:
            fy.append(0)
        try:
            sy.append(attempt_dict[uqp][1])
        except:
            sy.append(0)

    trace1 = go.Bar(
        x=attempts,
        y=fy,
        text=[str(i) for i in fy],
        textposition='outside',
        name='Attempt 1',
        hoverinfo='skip'
    )
    trace2 = go.Bar(
        x=attempts,
        y=sy,
        text=[str(i) for i in sy],
        textposition='outside',
        name='Attempt 2',
        hoverinfo='skip'
    )

    data = [trace1, trace2]
    layout = go.Layout(barmode='group', yaxis=dict(range=[0, 108]))
    fig = go.Figure(data=data, layout=layout)
    return fig

@csrf_exempt
@login_required
@has_profile
def report_error(request):
    data = json.loads(request.POST['data'])
    if len(data['error']) == 0:
        data['error'] = '_'
    try:
        error_serializer = ErrorSerializer(data=data)
        if error_serializer.is_valid():
            error_serializer.save()

        return JsonResponse({'SUCCESS': 'Thanks!!'}, status=status.HTTP_201_CREATED)

    except Exception as e:
        return JsonResponse({'error' : str(e)}, status=status.HTTP_400_BAD_REQUEST)

@csrf_protect
def send_otp(request):

    data = json.loads(request.POST['data'])
    number = data['number']
    if settings.IS_DEVELOPMENT == False:
        otp = randint(111111,999999)
        body = 'Hi there! Your OTP to register on missionpcs is : ' + str(otp)
        try:
            send_sms(body, number)
            return JsonResponse({'SENT': otp})
        except Exception as e:
            return JsonResponse({'NUMBER NOT VALID' : str(e)})
    else:
        otp = "000000"
        return JsonResponse({'SENT': otp})
def send_sms(body, number):
    message = tw_client.messages.create(
        body = body,
        from_= settings.twilio_number,
        to = number
    )


def index(request):
    
    
    # """Take the credentials of the user and log the user in."""
    # next_url = request.GET.get('next')
    courses = Course.objects.all()
    updates_result = Update.objects.order_by('-pubDate').filter(type='result')[:5]
    update_announcements = Update.objects.order_by('-pubDate').filter(type='announcement')[:5]
    admit_cards = Update.objects.order_by('-pubDate').filter(type='admit_card')[:5]
    this_month = datetime.now().month
    months_to_show = []
    today_dt = date.today()
    for i in range(0, 12):
        p_month = today_dt + relativedelta(months=-i)
        months_to_show.append(p_month)
    context = {'courses': courses, 'updates_result': updates_result, 'update_announcements': update_announcements, 'admit_cards': admit_cards, 'prev_months': months_to_show}
    if request.method == "POST":
        if request.POST["sub"] == "Sign In":
            username = request.POST["username"].lower()
            password = request.POST["password"]
            path_next = request.POST["next"]
            if len(username)==0 or len(password)==0:
                context["error"]:"Please Fill all the Fields"
                return my_render_to_response(request, 'index.html', context)
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return my_redirect(path_next)
            else:
                context["username"] = username
                context["error"]="Invalid username/password"
            return my_render_to_response(request, 'index.html', context)    
        if request.POST["sub"] == "Sign Up":
            username = request.POST["username"]
            password = request.POST["password"]
            email = request.POST["email"]
            confirmation = request.POST["confirmation"]
            firstname = request.POST["firstname"]
            lastname = request.POST["lastname"]
            country_code = request.POST["country_code"]
            phone_number = request.POST["phone-number"]
            
            context["username"] = username
            context["firstname"] = firstname
            context["lastname"] = lastname
            context["country_code"] = country_code
            context["phone_number"] = phone_number
            context["email"] = email
            if password != confirmation:
                context["regerror"] = "password doesn't match"
                return my_render_to_response(request, "index.html", context)
            # elif len(phone_number)!=10:
            #     context["regerror"] = "Phone number should be atleast 10 digits"
            #     return my_render_to_response(request, "index.html", context)
            try:
                new_user = User.objects.create_user(username, email, password)
                new_user.first_name = firstname
                new_user.last_name = lastname
                new_user.save()
            except IntegrityError:
                context["regerror"] = "Username already taken."
                return my_render_to_response(request, "index.html", context)
            
            new_profile = Profile(user=new_user)
            new_profile.country_code = country_code
            new_profile.phone_number = phone_number

            if settings.IS_DEVELOPMENT:
                new_profile.is_email_verified = True
            else:
                new_profile.is_email_verified = True
                new_profile.activation_key = generate_activation_key(
                    new_user.username)
                new_profile.key_expiry_time = timezone.now() + timezone.timedelta(
                    minutes=20)
            new_profile.save()
            new_user = authenticate(username=username, password=password)
            login(request, new_user)
            return my_redirect('/exam/select_exam')
            # if user_email and key:
            #     success, msg = send_user_mail(user_email, key)
            #     context = {'activation_msg': msg}
            #     return my_render_to_response(
            #         request,
            #         'yaksh/activation_status.html', context
            #     )
            #return index(request)

    if request.user.id == None:
        return my_render_to_response(request, "index.html", context)
    else:
        return my_redirect('/exam/login/?next=/letsprepare/show_modules/')

def detailed_news(request, ca_id):
    ca = CurrentAffair.objects.get(id=ca_id)
    context = {'ca': ca}
    return my_render_to_response(request, "portal_pages/detailed-news.html", context)

def current_affairs_all(request):
    this_month = datetime.now().month
    months_to_show = []
    today_dt = date.today()
    for i in range(0, 10):
        p_month = today_dt + relativedelta(months=-i)
        months_to_show.append(p_month)
    ca = CurrentAffair.objects.all().order_by("-pubDate")
    context = {'ca': ca, 'prev_months': months_to_show}
    return my_render_to_response(request, "portal_pages/current-affairs.html", context)

def current_affairs_month(request, month, year):
    this_month = datetime.now().month
    months_to_show = []
    today_dt = date.today()
    for i in range(0, 10):
        p_month = today_dt + relativedelta(months=-i)
        months_to_show.append(p_month)
    ca = CurrentAffair.objects.all().filter(pubDate__year=year).filter(pubDate__month=month).order_by("-pubDate")
    context = {'ca': ca, 'prev_months': months_to_show}
    return my_render_to_response(request, "portal_pages/current-affairs.html", context)


@csrf_exempt
def verify_payment(request):
    if request.method == "POST":

        data_dict = {}
        response = request.POST
        params_dict = {
            'razorpay_payment_id': response['razorpay_payment_id'],
            'razorpay_order_id': response['razorpay_order_id'],
            'razorpay_signature': response['razorpay_signature']
        }

        # VERIFYING SIGNATURE
        try:
            status = client.utility.verify_payment_signature(params_dict)
            data_dict['status_code'] = status
            # return data_dict
            orders = list(AvailableQuizzes.objects.filter(order_id=response['razorpay_order_id']))
            user = orders[0].user
            del data_dict['status_code']
            PaytmHistory.objects.create(user=user, **data_dict)
            for order in orders:
                order.successful = True
                order.save()
            return my_redirect('/letsprepare')
        except:
            return my_render_to_response(request, 'yaksh/404.html')
    return my_redirect('/letsprepare')