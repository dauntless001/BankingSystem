from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User, Account, History
from .forms import AccountForm
import random
from django.contrib.auth.decorators import login_required

@login_required(login_url='/accounts/login')
def savemoney_view(request):
    qs = User.objects.get(username = request.user.username)
    token = random.randint(111111, 999999)
    if request.method == 'POST':
        amount = request.POST['amount']
        token = request.POST['token']
        parsed_token = request.POST['parsed_token']
        if int(token) != int(parsed_token):
            messages.info(request, 'Invalid Token')
            return redirect('accounts:savemoney')
        qs.account.acc_bal += int(amount)
        qs.save()
        History.objects.create(user=request.user, details=f'${amount} was deposited into your account')
        messages.info(request, f'{amount}, has been successfully Saved to your account')
        return redirect('accounts:dashboard')
    name = 'saveform.html'
    context = {
        'token':token
    }
    return render(request, name, context)

@login_required(login_url='/accounts/login')
def withdrawmoney_view(request):
    qs = User.objects.get(username = request.user.username)
    token = random.randint(111111, 999999)
    if request.method == 'POST':
        amount = request.POST['amount']
        token = request.POST['token']
        parsed_token = request.POST['parsed_token']
        if int(token) != int(parsed_token):
            messages.info(request, 'Invalid Token')
            return redirect('accounts:savemoney')
        if qs.account.acc_bal - int(amount) <0:
            messages.info(request, f'Insufficient Balance')
            return redirect('accounts:dashboard')
        qs.account.acc_bal -= int(amount)
        qs.save()
        History.objects.create(user=request.user, details=f'${amount} was withdrawn from your account')
        messages.info(request, f'{amount}, has been successfully Withdrawn from your account')
        return redirect('accounts:dashboard')
    name = 'saveform.html'
    context = {
        'token':token
    }
    return render(request, name, context)

@login_required(login_url='/accounts/login')
def transmoney_view(request):
    form = AccountForm(request.POST or None)
    name = 'transfer.html'
    context = {
        'form':form
    }
    return render(request, name, context)


@login_required(login_url='/accounts/login')
def transverify_view(request):
    if request.method == 'POST':
        account_num = request.POST['account_number']
        try:
            user = Account.objects.get(sec_num=account_num)
            messages.success(request, 'Account Found.')
            acc_details = user
            token = random.randint(111111, 999999)
            acc_num = account_num
        except:
            messages.info(request, 'Account Not Found!!!')
            return redirect('accounts:transfermoney')
    name = 'transverify.html'
    context = {
        'user_details':acc_details,
        'token' : token,
        'acc_num' : acc_num,
    }
    return render(request, name, context)


@login_required(login_url='/accounts/login')
def transcomplete_view(request):
    if request.method == 'POST':
        account_num = request.POST['acc_num']
        token = request.POST['token']
        parsed_token = request.POST['parsed_token']
        amount = request.POST['amount']
        if int(token) != int(parsed_token):
            messages.info(request, 'Invalid Token Please Try Again')
            return redirect('accounts:transfermoney')
        user = Account.objects.get(sec_num=int(account_num))
        qs = request.user
        if qs.account.acc_bal - int(amount) < 0:
            messages.info(request, 'Insufficient Funds')
            return redirect('accounts:dashboard')
        qs.account.acc_bal -= int(amount)
        qs.save()
        History.objects.create(user=request.user, details=f'You successfully transferred ${amount} to {user.sec_num}, {user.user.first_name} {user.user.last_name}')
        user.acc_bal += int(amount)
        user.save()
        History.objects.create(user=user.user, details=f'${amount} was successfully transferred from {qs.account.sec_num}, {qs.account.user.first_name} {qs.account.user.last_name}')
        messages.success(request, f'{amount} transferred successfully')
        return redirect('accounts:dashboard')


@login_required(login_url='/accounts/login')
def transaction_history(request):
    qs = History.objects.filter(user=request.user)
    name = 'history.html'
    context = {
        'qs' : qs
    }
    return render(request, name, context)