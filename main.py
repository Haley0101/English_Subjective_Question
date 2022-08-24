import sqlite3, datetime, random
from flask import *

app = Flask(__name__)
app.config["PERMANENT_SESSION_LIFETIME"] = datetime.timedelta(minutes=10)
app.secret_key = 'haley-duddjwebserver'

def sql_check():
    try:
        db = sqlite3.connect("./data/Haley.db")
        SQL = db.cursor()
        return db, SQL
    except:
        return False, False

def eng_String():
    db, SQL = sql_check()
    if db == False: return False
    try:
        SQL.execute('SELECT engA1, engA2, engA3 FROM eng_String WHERE num_id = 1')
        result = SQL.fetchone()
    except Exception as e:
        print(e)
        return False
    result_A1 = str(random.sample((str(result[0]).replace(',', '')).split(), len((str(result[0]).replace(',', '')).split()))).replace("[", '').replace("'", '').replace("]", '')
    result_A2 = str(random.sample((str(result[1]).replace(',', '')).split(), len((str(result[1]).replace(',', '')).split()))).replace("[", '').replace("'", '').replace("]", '')
    result_A3 = str(random.sample((str(result[2]).replace(',', '')).split(), len((str(result[2]).replace(',', '')).split()))).replace("[", '').replace("'", '').replace("]", '')
    print(result_A1, result_A2, result_A3)
    return result_A1, result_A2, result_A3

def eng_check(id_num: int = None, text: str = None):
    if text is None or id_num is None: return False
    db, SQL = sql_check()
    if db == False: return False
    try:
        SQL.execute('SELECT engA1, engA2, engA3 FROM eng_String WHERE num_id = 1')
        result = SQL.fetchone()
    except:
        return False
    if result[id_num] == text:
        return True
    else:
        return False


@app.route('/', methods = ['POST', 'GET'])
def home():
    if request.method == 'POST':
        session['username'] = request.form['username']
        session['usernumber'] = request.form['classnum']
        if session['username'] == 'admin' and session['usernumber'] == '040728':
            return redirect(url_for('admin'))
        return redirect(url_for('home'))
    elif request.method == 'GET':
        if 'username' in session:  # session안에 username이 있으면 로그인
            return redirect(url_for('input_test'))
    return render_template('/home.html') # 로그인이 안될 경우


@app.route('/input-test', methods = ['POST', 'GET'])
def input_test():
    if request.method == "GET":
        if 'username' not in session:
            return redirect(url_for('home'))
        print(eng_String())
        eng_Q1, eng_Q2, eng_Q3 = eng_String()
        if eng_String() == False:
            return render_template('/result_page.html', _result = '오류가 발생 하였습니다. 데이터')
        return render_template('/inputs_web.html', eng_Q1 = eng_Q1, eng_Q2 = eng_Q2, eng_Q3 = eng_Q3)
    elif request.method == 'POST':
        engQ1, engQ2, engQ3 = request.form['engQ1'], request.form['engQ2'], request.form['engQ3']
        if eng_check(0, engQ1) == True: view_resultQ1 = '정답' 
        else: view_resultQ1 = '오답'
        if eng_check(1, engQ2) == True: view_resultQ2 = '정답' 
        else: view_resultQ2 = '오답'
        if eng_check(2, engQ3) == True: view_resultQ3 = '정답' 
        else: view_resultQ3 = '오답'
        return f'{engQ1} - {view_resultQ1}<br>{engQ2} - {view_resultQ2}<br>{engQ3} - {view_resultQ3}'


@app.route('/admin-page')
def admin():
    if request.method == "GET":
        if 'username' not in session:
            return render_template('/home.html')
        if session['username'] != 'admin' and session['usernumber'] != '040728':
            if 'username' in session:
                return redirect(url_for('input_test'))
            return redirect(url_for('home'))
        return render_template('/admin_page.html')


@app.route('/eng-stringinputjsonload', methods = ['POST'])
def eng_stringinputjsonload():
    if request.method == 'POST':
        db, SQL = sql_check()
        if db == False: return render_template('/result_page.html', _result = '오류가 발생 하였습니다. <br>데이터 불러오는 중 에러발생')
        engA1, engA2, engA3 = request.form['engA1'], request.form['engA2'], request.form['engA3']
        try:    
            SQL.execute(f'UPDATE eng_String SET engA1 = "{engA1}" WHERE num_id = 1')
            SQL.execute(f'UPDATE eng_String SET engA2 = "{engA2}" WHERE num_id = 1')
            SQL.execute(f'UPDATE eng_String SET engA3 = "{engA3}" WHERE num_id = 1')
            db.commit()
            _result = '성공적으로 수정이 완료 되었습니다.'
        except Exception as e:
            _result = f'일시적인 서버 오류로 실행이 최소 되었습니다.\n{e}'
        return render_template('/result_page.html', _result = _result)


@app.route('/test-result/<result>')
def test_result(result):
    str(result).replace('<>', '<br>')
    return render_template('/result_page.html', _result = result)


@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('usernumber', None)
    return redirect(url_for('home'))


app.run(host='0.0.0.0', port=2022)