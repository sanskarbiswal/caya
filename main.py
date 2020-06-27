from flask import Flask, render_template, request, redirect, url_for
import csv, json
from tempfile import NamedTemporaryFile

app = Flask(__name__)
f_path = "data/components.csv"
f_path2 = "data/feed.csv"
logfeed = []
data_field = ['Category', 'Name', 'Quantity', 'Location', 'Stock']
active_search = ""
cData = None
############# Non-Flask Functions ####################
def does_comp_exist(compName, getData=False):
    with open(f_path, 'r') as f:
        reader = csv.reader(f)
        for line in reader:
            if line[1] == compName:
                if getData:
                    return line
                else:
                    return True
def feed_action(feedString="None"):
    import os
    global logfeed
    if os.path.exists(f_path2):
        with open(f_path2, 'r') as f:
            reader = csv.reader(f)
            for line in reader:
                logfeed.append(line)
    else:
        with open(f_path2, 'w', newline="") as f:
            writer = csv.writer(f)
            for i in range(0,12):
                logfeed.append(feedString)
            writer.writerows(logfeed)
    if feedString == "None":
        pass
    else:
        logfeed = [logfeed[-1]] + logfeed[:-1]
        logfeed[0] = feedString
        with open(f_path2, 'w', newline="") as f:
            writer = csv.writer(f)
            writer.writerows(logfeed)
        

def check_csv_data():
    import os
    if os.path.exists(f_path):
        pass
    else:
        data_field = ['Category', 'Name', 'Quantity', 'Location', 'Stock']
        with open(f_path,"w+", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(data_field)

def update_csv(data_field):
    import shutil
    tempfile = NamedTemporaryFile(mode='w', delete=False, newline="")
    with open(f_path, 'r', newline="") as f, tempfile:
        reader = csv.reader(f)
        writer = csv.writer(tempfile)
        for line in reader:
            if line[1] == data_field[1]:
                # update
                line = data_field
                writer.writerow(line)
            else:
                writer.writerow(line)
    shutil.move(tempfile.name, f_path)


############# FLASK Function #########################

@app.route('/')
@app.route('/index')
def index():
    global cData, logfeed
    check_csv_data()
    #feed_action("New Feed Repo Generated")
    return render_template('main.html', compData=cData)

@app.route('/add_comp', methods=['POST','GET'])
def add_comp():
    global logfeed
    if request.method == 'POST':
        category = request.form['inp_add_comp_category']
        compName = request.form['inp_add_comp_name']
        compQnty = request.form['inp_add_comp_qnty']
        compLoc  = request.form['inp_add_comp_loc']
        stock    = compQnty
        if(does_comp_exist(compName)):
            # TODO: update quantity
            pass
        else:
            # add component data as new field
            data_field = [category,compName, compQnty, compLoc, stock]
            with open(f_path, 'a+',newline="") as f:
                writer = csv.writer(f)
                writer.writerow(data_field)
            feed_action("Added "+compQnty+" : "+compName)
    return redirect(url_for('index', compData=None))

@app.route('/search_comp', methods=['POST'])
def search_comp():
    if request.method == 'POST':
        global active_search, cData
        compName = request.form['search_component'] 
        compData = does_comp_exist(compName, True)
        cData = compData
        active_search = compName
    return redirect(url_for('index', compData=cData))

@app.route('/borrow_comp', methods=['POST'])
def borrow_comp():
    if request.method == 'POST':
        global active_search, cData, logfeed
        compName = active_search
        compData = does_comp_exist(compName, True)
        compData[4] = str(int(compData[4]) - int(request.form['borrow_qty']))
        update_csv(compData)
        cData = compData
        feed_action("Borrowed "+request.form['borrow_qty']+" : "+compName)
    return redirect(url_for('index', compData=cData))


@app.route('/return_comp', methods=['POST'])
def return_comp():
    if request.method == 'POST':
        global cData, logfeed
        compName = request.form['compName']
        compData = does_comp_exist(compName, True)
        compData[4] = str(int(compData[4]) + int(request.form['ret_qty']))
        #print(compName, flush=True)
        update_csv(compData)
        cData = compData
        feed_action("Returned "+compName)
    return redirect(url_for('index', compData=cData))

if __name__ == "__main__":
    app.run(debug = True)

