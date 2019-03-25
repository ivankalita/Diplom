from django.shortcuts import render, redirect
from django.conf import settings
from django.http import HttpResponse, HttpResponseNotFound, FileResponse
from django.core.files.storage import FileSystemStorage

from .forms import UserForm, DocumentForm
from .models import Banner, Document, Table_IP_OS, Table_Port, DownloadProof
import shodan, os, subprocess


#for Parsing
from .nmap import report_parser



###
from libnmap.process import NmapProcess
from libnmap.parser import NmapParser
import json


SHODAN_API_KEY = "7ZJZ7j5N6OOkruWF7gEgC0rRC4fDZgid"

api = shodan.Shodan(SHODAN_API_KEY)

def home(request):
    documents = Document.objects.all()
    proofs = DownloadProof.objects.all()
    data = {'documents': documents, 'proofs': proofs}
    return render(request, 'banner/home.html', context=data)   


def banner_list(request):
    if (request.method == 'POST'):
        name = request.POST.get('webserver')
        try:
            results = api.search(name)
            for index, result in enumerate(results['matches']):
                ban = Banner(ip_str = result['ip_str'])#, data = result['data'])
                ban.save()
                if index == 5:
                    break
            banners = Banner.objects.all()
            return render(request, 'banner/list.html', {'results': banners})
        except shodan.APIError as e:
            return HttpResponse("<h2>Error, {0}</h2>".format(e))
    else:
        userform = UserForm()
    return render(request, 'banner/banner_list.html', {'form': userform})



def simple_upload(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        path_to_xml = 'C:\\Users\\Admin\\Desktop\\Search\\media\\' + filename
        try:
            BD_Nmap = report_parser(path_to_xml)
            for record in BD_Nmap:
                ip = record['IP']
                os = record['hostname']
                table_ip = Table_IP_OS(ip = ip, os = os)
                table_ip.save()
                if record['services'] != '':
                    for serv in record['services']:
                        port = serv['port']
                        service = serv['service']
                        banner = serv['ban']
                        table_port = Table_Port(ip = table_ip, port = port, service = service, banner = banner)
                        table_port.save()
        except Exception as e:
            return HttpResponse("<h2>Error, {0}</h2>".format(e))
    else: 
        return render(request, 'banner/simple_upload.html')

    ip_os = Table_IP_OS.objects.all()
    return render(request, 'banner/list.html', {'results': ip_os})


def view_list(request):
    ip_os = Table_IP_OS.objects.all()
    return render(request, 'banner/list.html', {'results': ip_os})
    
def view_banner(request, id): #Функция отображения информации о баннере
    try:
        #ban = Table_Port.objects.get(id=id)
        ip_os = Table_IP_OS.objects.get(id=id)
        ban=ip_os.table_port_set.all()
        data = {'results': ip_os, 'banners': ban}
        return render(request, 'banner/list_banner.html', context=data)
    except Table_Port.DoesNotExist:
        return HttpResponseNotFound('<h2>Info at this IP doesn`t Exist</h2>')   

def model_form_upload(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = DocumentForm()
    return render(request, 'banner/upload.html', {
        'form': form
    })


def delete(request, id):
    try:
        proof = DownloadProof.objects.get(id=id)
        proof.delete()
        return redirect('home')
    except Document.DoesNotExist:
        return HttpResponseNotFound('<h2>Documnet not found</h2>')

def open_file(request, id):
    proof = DownloadProof.objects.get(id = id)
    return HttpResponse("<p>{0}</p>".format(proof.document))

def test(request):
    full_query = []
    ans = (request.POST.get('main_search'), request.POST.get('group_country'), request.POST.get('group_city'), request.POST.get('group_os'), request.POST.get('group_port'))
    prop = ('','country:', 'city:', 'os:', 'post:')
    for iter in range(len(ans)):
        if ans[iter] != None:
           full_query.append(prop[iter] + ans[iter])
    full_query = '  '.join(full_query)
    try:
        results = api.search(full_query)
        for result in results['matches']:
            ban = Banner(ip_str = result['ip_str'])
            ban.save()
        banners = Banner.objects.all()
        return HttpResponse("<h2>Succes, {0}</h2>".format(full_query))#render(request, 'banner/list.html', {'results': banners})
    except shodan.APIError as e:
        return HttpResponse("<h2>Error, {0}</h2>".format(e))
    return render(request, 'banner/list.html')

def graph(request):
    return render(request, 'banner/graph.html')

def check_proof(request, id):
    if request.method == 'POST':
        query = request.POST.get('fairquery')
        limit = int(request.POST.get('limit'))
        id = int(request.POST.get('port_id'))
        try:
            #for Vulners.com
            from .getsploit import  start
            start(query, limit, id)
            return redirect('home')
        except Exception  as e:
            return HttpResponseNotFound('<h2>Document isn`t found {0}</h2>'.format(e))
