from flask import Flask, render_template, request, redirect, url_for, jsonify
import csv, json, time, os
from tempfile import NamedTemporaryFile

app = Flask(__name__)
f_path = "data/components.csv"
f_path2 = "data/feed.csv"
f_path3 = "data/users.txt"
logfeed = []
data_field = ['Category', 'Name', 'Quantity', 'Location', 'Stock']
active_search = ""
cData = None
components = []
# Load all Components
with open(f_path,'r') as f:
    reader = csv.reader(f)
    for line in reader:
        components.append(line[1])
# Load All Logs
if os.path.exists(f_path2):
    feed = []
    with open(f_path2, 'r') as f:
        rd = csv.reader(f)
        for line in rd:
            feed.append(line)
    if len(feed) < 8:
        feed_len = len(feed)
    else:
        feed_len = 8
    for i in range(0,feed_len):
        logfeed.append(feed[i])
else:
    with open(f_path2, 'w', newline="") as f:
        pass

#components = json.dumps(components)
############# Non-Flask Functions ####################
def comUpdate():
    global components
    components = []
    # Load all Components
    with open(f_path,'r') as f:
        reader = csv.reader(f)
        for line in reader:
            components.append(line[1])
        
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
    t = list(time.localtime())
    date = str(t[2]) +"-"+ str(t[1]) +"-"+ str(t[0])
    global logfeed
    if feedString == "None":
        pass
    else:
        if len(logfeed) != 0:
            #logfeed.append()
            if len(logfeed) == 8:
                logfeed.pop()
            logfeed.insert(0, [feedString, date])
            #logfeed = [logfeed[-1]] + logfeed[:-1]
            print(logfeed)
            #logfeed[0] = [feedString, date]
        else:
            logfeed.append([feedString, date])
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
    comUpdate()
    #feed_action("New Feed Repo Generated")
    return render_template('main.html', compData=cData, comp=components, feedData = logfeed)

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
            comUpdate()
    return redirect(url_for('index', compData=None, comp=components, feedData = logfeed))

@app.route('/search_comp', methods=['POST'])
def search_comp():
    if request.method == 'POST':
        global active_search, cData
        compName = request.form['search_component'] 
        compData = does_comp_exist(compName, True)
        cData = compData
        active_search = compName
        comUpdate()
    return redirect(url_for('index', compData=cData, comp=components, feedData = logfeed))

@app.route('/borrow_comp', methods=['POST'])
def borrow_comp():
    if request.method == 'POST':
        global active_search, cData, logfeed
        compName = active_search
        compData = does_comp_exist(compName, True)
        compData[4] = str(int(compData[4]) - int(request.form['borrow_qty']))
        update_csv(compData)
        cData = compData
        comUpdate()
        feed_action("Borrowed "+request.form['borrow_qty']+" : "+compName)
    return redirect(url_for('index', compData=cData, comp=components, feedData = logfeed))


@app.route('/return_comp', methods=['POST'])
def return_comp():
    if request.method == 'POST':
        global cData, logfeed
        compName = request.form['compName']
        compQnty = request.form['ret_qty']
        compData = does_comp_exist(compName, True)
        compData[4] = str(int(compData[4]) + int(request.form['ret_qty']))
        if compData[4] <= compData[2]:
            #print(compName, flush=True)
            update_csv(compData)
            cData = compData
            feed_action("Returned "+compQnty+" "+compName)
            comUpdate()
    return redirect(url_for('index', compData=cData, comp=components, feedData = logfeed))

@app.route('/autocomplete', methods=['GET'])
def autocomplete():
    search = request.args.get('search-bar')
    app.logger.debug(search)
    return jsonify(json_list=components)

@app.route('/download_csv_report')
def download_csv_report():
    global cData, components, logfeed
    feed_action("CSV Output File Generated")
    path = os.path.realpath(f_path2)
    os.startfile(path)
    return redirect(url_for('index', compData=cData, comp=components, feedData = logfeed))

if __name__ == "__main__":
    app.run(debug = True)

