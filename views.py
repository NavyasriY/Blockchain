from django.shortcuts import render
from django.template import RequestContext
from django.contrib import messages
from django.http import HttpResponse
from django.conf import settings
import os
import json
from web3 import Web3, HTTPProvider

global contract, web3
contract = None

def saveVote(candidate, name, symbol, voter, aadhar):
    global contract, web3
    if contract == None:
        blockchain_address = 'http://127.0.0.1:9545'
        # Client instance to interact with the blockchain
        web3 = Web3(HTTPProvider(blockchain_address))
        # Set the default account (so we don't need to set the "from" for every transaction call)
        web3.eth.defaultAccount = web3.eth.accounts[0]
        # Path to the compiled contract JSON file
        compiled_contract_path = 'EVoting.json'
        # Deployed contract address (see `migrate` command output: `contract address`)
        deployed_contract_address = '0x80c7cBe6C2412412583eAB748679f29008D64eCF'
        with open(compiled_contract_path) as file:
            contract_json = json.load(file)  # load contract info as JSON
            contract_abi = contract_json['abi']  # fetch contract's abi - necessary to call its functions
        file.close()
        # Fetch deployed contract reference
        contract = web3.eth.contract(address=deployed_contract_address, abi=contract_abi)
    # Call contract function (this is not persisted to the blockchain)
    msg = contract.functions.markVote(candidate, name, symbol, voter, aadhar).transact()
    tx_receipt = web3.eth.waitForTransactionReceipt(msg)
    return str(msg)


def getVote(candidate):
    global contract, web3
    if contract == None:
        blockchain_address = 'http://127.0.0.1:9545'
        # Client instance to interact with the blockchain
        web3 = Web3(HTTPProvider(blockchain_address))
        # Set the default account (so we don't need to set the "from" for every transaction call)
        web3.eth.defaultAccount = web3.eth.accounts[0]
        # Path to the compiled contract JSON file
        compiled_contract_path = 'EVoting.json'
        # Deployed contract address (see `migrate` command output: `contract address`)
        deployed_contract_address = '0x80c7cBe6C2412412583eAB748679f29008D64eCF'
        with open(compiled_contract_path) as file:
            contract_json = json.load(file)  # load contract info as JSON
            contract_abi = contract_json['abi']  # fetch contract's abi - necessary to call its functions
        file.close()
        # Fetch deployed contract reference
        contract = web3.eth.contract(address=deployed_contract_address, abi=contract_abi)
    message = contract.functions.getCount(candidate).call()
    return message

def CastVoteAction(request):
    if request.method == 'POST':
        candidate_id = request.POST.get('t1', False)
        voter = request.POST.get('t2', False)
        aadhar = request.POST.get('t3', False)
        if candidate_id == "1":
            saveVote(1,"Rahul Gandhi","Hand",voter,aadhar)
        if candidate_id == "2":
            saveVote(2,"Narendar Modi","Lotus",voter,aadhar)
        if candidate_id == "3":
            saveVote(3,"Akhilesh Yadav","Cycle",voter,aadhar)
        context= {'data':'Your vote saved inside Ethereum'}
        return render(request, 'index.html', context)    


def AdminLogin(request):
    if request.method == 'POST':
        username = request.POST.get('username', False)
        password = request.POST.get('password', False)
        if username == 'admin' and password == 'admin':
            context= {'data':'Welcome Admin'}
            return render(request, "AdminScreen.html", context)
        else:
            context= {'data':'Invalid username'}
            return render(request, 'Admin.html', context)

def index(request):
    if request.method == 'GET':
       return render(request, 'index.html', {})

def ViewCount(request):
    if request.method == 'GET':
       return render(request, 'ViewCount.html', {})    

def Admin(request):
    if request.method == 'GET':
       return render(request, 'Admin.html', {})

def Vote(request):
    if request.method == 'GET':
        output = '<table border=1 align=center width=100%>'
        font = '<font size="" color="white">'
        arr = ['Candidate ID','Candidate Name','Symbol','Cast Your Vote']
        output += "<tr>"
        for i in range(len(arr)):
            output += "<th>"+font+arr[i]+"</th>"
        output += "<tr><td>"+font+"1"+"</td>"
        output += "<td>"+font+"Rahul Gandhi"+"</td>"
        output+='<td><img src=/static/symbols/congress.png height=100 width=100/></td>'
        output+='<td><a href=\'CastVote?t1=1\'><font size=3 color=white>Click Here</font></a></td></tr>'
        output += "<tr><td>"+font+"2"+"</td>"
        output += "<td>"+font+"Narendar Modi"+"</td>"
        output+='<td><img src=/static/symbols/bjp.png height=100 width=100/></td>'
        output+='<td><a href=\'CastVote?t1=2\'><font size=3 color=white>Click Here</font></a></td></tr>'
        output += "<tr><td>"+font+"3"+"</td>"
        output += "<td>"+font+"Akhilesh Yadav"+"</td>"
        output+='<td><img src=/static/symbols/samajvadi.png height=100 width=100/></td>'
        output+='<td><a href=\'CastVote?t1=3\'><font size=3 color=white>Click Here</font></a></td></tr>'         
        context= {'data':output}        
        return render(request, 'Vote.html', context)

def CastVote(request):
    if request.method == 'GET':
        candidate = request.GET.get('t1', False)
        output = '<TR><TH align="left"><font size="" color="white">Candidate&nbsp;ID<TD><Input type=text name="t1" value="'+candidate+'" class="form-control" readonly></TD></TR>'
        context= {'data1':output}        
        return render(request, 'CastVote.html', context)

def ViewCountAction(request):
    if request.method == 'POST':
        candidate = request.POST.get('t1', False)
        count = getVote(int(candidate))
        #print(str(count)+"==========================================="))
        output = '<table border=1 align=center width=100%>'
        font = '<font size="" color="white">'
        arr = ['Candidate ID','Candidate Name','Symbol','Total Votes Received']
        output += "<tr>"
        for i in range(len(arr)):
            output += "<th>"+font+arr[i]+"</th>"
        if candidate == "1":
            output += "<tr><td>"+font+"1"+"</td>"
            output += "<td>"+font+"Rahul Gandhi"+"</td>"
            output+='<td><img src=/static/symbols/congress.png height=100 width=100/></td>'
            output+='<td><font size=3 color=white>'+str(count)+'</font></a></td></tr>'
        if candidate == "2":
            output += "<tr><td>"+font+"2"+"</td>"
            output += "<td>"+font+"Narendar Modi"+"</td>"
            output+='<td><img src=/static/symbols/bjp.png height=100 width=100/></td>'
            output+='<td><font size=3 color=white>'+str(count)+'</font></a></td></tr>'
        if candidate == "3":
            output += "<tr><td>"+font+"3"+"</td>"
            output += "<td>"+font+"Akhilesh Yadav"+"</td>"
            output+='<td><img src=/static/symbols/samajvadi.png height=100 width=100/></td>'
            output+='<td><font size=3 color=white>'+str(count)+'</font></a></td></tr>'         
        context= {'data':output}        
        return render(request, 'ViewResult.html', context)
    

    
