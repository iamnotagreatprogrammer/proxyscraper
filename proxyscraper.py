import sys
import csv
import subprocess
import os
import requests
def installDependencies():
    subprocess.check_call([sys.executable, "-m", "pip", "install", "bs4"])
installDependencies()
import tkinter as tk
from bs4 import BeautifulSoup
from tkinter.filedialog import asksaveasfile
from tkinter.filedialog import askopenfile
from tkinter import messagebox
from tkinter import *
from tkinter import filedialog

list_of_rows = [] # create list to contain scraped data

def deletelist():
    list_of_rows.clear() # used to delete scraped proxies when each different site is selected

def pingproxies():
    displayoutput.delete(1.0,  END)
    status = []
    proxiesfile =  filedialog.askopenfilename(initialdir="/home", title = "Select csv file containing proxies",filetypes = ((".csv files","*.csv"),)) # allow selection of CSV file containing proxies
    outputresults = filedialog.asksaveasfilename(title="Select filename and directory to save proxy test results to", defaultextension=".csv") # ask for location of new CSV file with test results
    with open(proxiesfile) as csvfile: # open csvfile containing the .csv file to test
        reader = csv.reader(csvfile)
        with open(outputresults, 'w', newline='') as csvoutput:
            output = csv.writer(csvoutput)
            for row in reader: # iterate via each row
                rep = os.system("ping " + row[0] + " -n 1") # ping all the values from the first column (containing the IP Address)
                if rep == 0:
                    status = 'is up' # if ping test returns successful then write IP address and is Up to text file
                    output.writerow([row[0]] + [row[1]] + [status])
                else:
                    status= 'is down' # if ping test returns successful then write IP address and is Down to text file
                    output.writerow([row[0]] + [row[1]] + [status])
            displayoutput.insert('end',"Proxies tested successfully, please check output file")


         # make sure to close text file and not keep open.

def saveproxy(): # function to ask user to input name of file containing the scraped proxies
    savelocation = filedialog.asksaveasfilename(title="Select filename and directory to save to", defaultextension=".csv")
    with open (savelocation + '.csv','w', newline='') as file:
        writer=csv.writer(file)
        writer.writerow(['IP','Port', 'Code', 'Country', 'Anonymity', 'Google', 'HTTPS', 'Last Checked']) # add column titles
        for row in list_of_rows:
            if any(field.strip() for field in row): # strip extra blank line between each output.
                writer.writerow(row)
        displayoutput.insert('end',"Proxies scraped and saved. Please check output file")

def makesoup(url): # pass url to beautifulsoup to parse html. Url is defined in menu for each site so code doesnt have to be repeated for each site
    page=requests.get(url)
    return BeautifulSoup(page.text,"lxml")

def proxyscrape(table): # scrape proxy data from table on site, add to list that was created earlier
    deletelist()
    for row in table.findAll('tr'):
        list_of_cells = []
        for cell in row.findAll('td'):
            text = cell.text.replace('&nbsp;', '')
            list_of_cells.append(text)
        list_of_rows.append(list_of_cells)
    saveproxy()

def scrapeproxies(url):
    displayoutput.delete(1.0,  END) # contains the parent  table attribute where proxy data is present
    soup=makesoup(url)
    proxyscrape(table = soup.find('table', attrs={'id': 'proxylisttable'}))


root = tk.Tk()
root.resizable(False, False)
root.geometry("400x250")
root.wm_title("Proxy Scraper")
site1 = tk.Button(text="Scrape SSLProxies.org", command= lambda: scrapeproxies(url = "https://www.sslproxies.org"))
site1.pack(anchor=CENTER)
site2 = tk.Button(text="Scrape FreeProxyList.net", command= lambda: scrapeproxies(url = "https://free-proxy-list.net"))
site2.pack(anchor=CENTER)
site3 = tk.Button(text="Scrape US-Proxy.org", command= lambda: scrapeproxies(url = "https://us-proxy.org"))
site3.pack(anchor=CENTER)
site4 = tk.Button(text="Scrape Socks-Proxy.net", command= lambda: scrapeproxies(url = "https://socks-proxy.net"))
site4.pack(anchor=CENTER)
site5 = tk.Button(text="Ping Test File containing proxies", command= lambda: pingproxies())
site5.pack(anchor=CENTER)
outputlabel = tk.Label(root, text = "Output")
displayoutput = Text(root)
outputlabel.pack()
displayoutput.pack()
displaylog = Text(root)

root.mainloop()

