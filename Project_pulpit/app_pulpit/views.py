from django.http import HttpResponse
from django.shortcuts import render
import pandas as pd 
import json 
import sqlite3
import csv
from django.views.generic import View
from django.shortcuts import redirect

def index(request):
    return HttpResponse("Hello, world!")

def about(request):
    return HttpResponse("About us")
  
# Create your views here. 
def Table(): 
    # Подключение к базе данных SQLite
    conn = sqlite3.connect('PubMedArticles-7.db')
    cursor = conn.cursor()
    # Выполнить SQL-запрос
    query = "SELECT * FROM ArticleStruct"
    cursor.execute(query)
    data = cursor.fetchall()
    print(data)
    # Записать данные в CSV-файл
    with open('output.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([i[0] for i in cursor.description])  # Write header
        writer.writerows(data)  # Write data rows
    # Закрыть подключение к базе
    conn.close()

    df = pd.read_csv("output.csv") 
  
    # parsing the DataFrame in json format. 
    json_records = df.reset_index().to_json(orient ='records') 
    data = [] 
    data = json.loads(json_records) 
    context = {'d1': data}
    return context 

  
def Data(request):
    if request.GET.get('table1'):
        context = Table()
    else:
        context = None
    
  
    return render(request, 'app_pulpit/table.html', context)
