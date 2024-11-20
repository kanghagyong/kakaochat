import re
from flask import Flask, request, render_template_string
from collections import defaultdict
app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    print(request.method)
    return '''
        <h1>안녕하세요.</h1>
    '''

@app.route('/kakaochat/', methods=['GET', 'POST'])
def pybokakao2():
    if request.method == 'POST':
        # POST 요청에서 textarea 값 가져오기
        user_input = request.form.get('user_input')  # 'user_input'은 textarea의 name 값
        pattern = r'\[(.*?)\]\s\[(.*?)\]\s(.*)'
        pattern_del = r'---------------.*?---------------'
        # 작성자별 대화 내용을 저장할 딕셔너리
        conversations = defaultdict(list)
        # 유효성 체크
        if user_input:
            user_input = re.sub(pattern_del, '', user_input, flags=re.DOTALL) # 날짜 표시제거
            # 대화 내용 파싱
            lines = user_input.split('\n')
            for line in lines:
                match = re.match(pattern, line.strip())  # 각 줄을 정규 표현식에 맞춰서 추출
                if match:
                    author = match.group(1)  # 작성자
                    message = match.group(3)  # 대화 내용
                    conversations[author].append(message)

            # 작성자별로 내용을 출력하거나 저장
            msg = ""
            rows = len(conversations)
            heightSize = 1200
            for author, messages in conversations.items():
                if rows > 5 :
                    rows = 5
                    heightSize = 500
                tablecss = f"float:left;border:1px solid #000;max-height:{heightSize}px;overflow-y:auto;display:block;height:calc(100% - 200px);"
                msg = msg+f"<table style='width: calc( 100% / {rows}); {tablecss}'><tr><th>{author}의 대화</th></tr>"
                messa = ""
                for message in messages:
                    messa = messa+"<tr><td style='word-break: break-all;'>"+message+"</td></tr>"
                msg = msg +messa + "</table>"
            return f"사용자 입력: <br>{msg} <div><button type='button' style='width:calc(100% - 10px); padding:10px;margin:30px auto;' onclick='location.href = document.referrer;' >뒤로가기</button></div>"
        else:
            return "입력이 없습니다. 다시 시도해주세요."

    return '''
        <h1>카카오톡 대화 내용 입력</h1>
        <form method="POST" style="text-align:center;">
            <textarea name="user_input" rows="10" cols="200"  style="width:calc(100% - 10px);height:calc(100vh - 200px);"></textarea>
            <br><br><br>
            <input type="submit" style="width:calc(100% - 10px);padding:10px;" value="분리">
        </form>
    '''

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)