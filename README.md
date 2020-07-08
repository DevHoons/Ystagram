# 인스타그램 만들어보기

- #### Django 학습을 위해 유튜브 Dstagram 강의를 참고하였으며, Heroku에 배포 후 git과 연동하여 commit 후 push 하면 Heroku 서버에 바로 반영이 되게 하는 작업까지 진행
- #### 사용기술 : Django + Disqus + Heroku

---

# 프로젝트 생성법

#### 1. pip install pipenv : pip와 virtualenv를 동시에 사용하기 위한 패키지 설치

#### 2. pipenv --three : 파이썬3 프로젝트 생성

#### 3. pipenv shell : 가상환경 만들어주기

#### 4. pipenv install Django : 장고 설치

- (==x.x.x 처럼 버전을 명시 해주지 않으면 가장 최신 버전이 설치 됌)

#### 5. django-admin startproject config : 프로젝트 생성

- 효율적인 앱 구조화를 위하여 최상위 config 폴더 이름 변경
- 변경한 폴더 내의 manage.py와 config폴더를 밖으로 이동
- 변경한 폴더는 삭제
- 만약 manage.py를 열었을때 알람이 오지 않으면 extensions에서 python 을 설치해야 함!

#### 6. python manage.py migrate : 데이터베이스 업데이트

- 프로젝트 생성 후 Django에서 기본적으로 제공해주는 User Model을 업데이트 시켜주는 과정

#### 7. python manage.py runserver : 서버 가동

- https://127.0.0.1:8000/admin에 접속하여 로그인 페이지가 나오면 성공!
- Admin을 만들어주지 않았기 때문에 아래 명령어로 슈퍼유저 생성

#### 8. python manage.py createsuperuser : 슈퍼유저 생성

- 유저 생성 후 Admin 페이지에서 로그인 확인

#### 9. django-admin startapp photo : 앱 생성

---

# 기능

### 1. 모델 생성

- 사용자의 업로드를 위한 Photo 모델 생성
- 작성자는 Django User Model에 데이터가 있는 사람을 참조해야하기 때문에 ForeignKey를 이용
- 이미지와 텍스트 생성날짜 업데이트 날짜를 위한 모델 추가

### 2. List

<pre><code>
 def photo_list(request):
    photos = Photo.objects.all()
    ctx = {"photos": photos}
    return render(request, "list.html", ctx)
 </code></pre>

- Photo Model의 manage한테 모든 데이터를 받아서 photos에 담아주고 Context Value를 Template Value List에 담아서 Template 파일을 render하여 화면에 List를 출력

### 3. Create, Delete, Update

- Class Based View기반의 CreateView, DeleteView, UpdateView를 이용하여 model과 field, success_url을 각각 설정
- CreateView의 경우 form_valid 함수를 통해 입력된 데이터가 올바른지 판단
<pre><code>
def form_valid(self, form):
       form.instance.name_id = self.request.user.id
       if form.is_valid():
           form.instance.save()
           return redirect("/")
       else:
           return self.render_to_response({"form": form})
</code></pre>
- 작성자는 필수 field 이지만 field 목록에 없으므로 함수 안에서 form instance 안에 name_id에 로그인한 사람을 할당
- form의 instance 객체를 데이터베이스에 저장하여 root로 redirect해주거나 입력 받았던 form을 그대로 response 해주는 코드

### 4. 로그인, 로그아웃

- accounts 앱에서 urls.py를 만들고, LoginView, LogoutView를 이용하고 따로 View 설정을 해주지 않고 urls 설정을 통해서 Login, Logout 구현

### 5. 회원가입

- Django Form을 통해 구현 - Django Form : HTML의 Form을 대신해주는 역할을 하고, 데이터베이스에 저장할 내용을 형식이나 제약조건을 설정
<pre><code>
class SignUpForm(forms.ModelForm):
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Repeat Password", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email"]

    def clean_password2(self):
        data = self.cleaned_data
        if data["password"] != data["password2"]:
            raise forms.ValidationError("비밀번호가 일치하지 않습니다.")
        return data["password2"]
</code></pre>

- 비밀번호와 비밀번호확인을 위한 form 추가
- User Model을 받아와 입력 받을 fields를 결정해주는 Meta Class
- self.cleaned_data : 입력 받은 후 sql injection을 방지하기 위해 처리를 거친 Data를 data 변수에 담음
- 입력한 비밀번호들을 비교하여 error 혹은 return 해주는 조건문

### 6. 댓글

- 이 프로젝트에서는 Disqus를 이용

### 7. 접근제한

<pre><code>from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
</code></pre>

- Function Based View 는 decorators를 이용
- Class Based View 는 mixins를 이용
- 로그인 접근제한을 기준으로 해당 함수 위 @login_required 혹은 클래스 인자 앞에 LoginRequiredMixin 을 추가하면 된다.

---

# Heroku 배포 셋팅

#### - Heroku CLI 설치 후 터미널에서 Heroku 입력하여 설치 확인!

#### 1. pipenv install dj-database-url

- heroku에 업로드를 하면 데이터베이스를 업데이트를 하여 덮어씌워줌

#### 2. pipenv install gunicorn

- 업로드를 하면 webserver와 함께 구동을 담당하는 middleware 설치

#### 3. pipenv install whitenoise

- static 파일을 관리하기 위한 모듈

#### 4. pipenv install psycopg2-binary

- postgre를 사용하기위한 모듈

#### 5. pipenv run pip freeze

- 가상환경에 설치되어있는 목록을 보여준다.

#### 6. pipenv run pip freeze > requirements.txt

- 설치된 모듈을 텍스트 파일로 저장해준다.

#### 7. 프로젝트 setting.py 설정

- import dj_database_url
- DEBUG = False => 배포할땐 False로 설정해주어야 한다.
- ALLOWED_HOSTS = ["로컬서버URL", "Heroku서버URL"]
- MIDDLEWARE : 상단쪽에 모듈 추가 "whitenoise.middleware.WhiteNoiseMiddleware",
- DATABASES : DATABASES["default"].update(dj_database_url.config(conn_max_age=500)) 추가

#### 8. 터미널에 heroku login 입력 후 로그인하기

#### 9. heroku create name

- heroku 앱 생성

#### 10. git push heroku master

- heroku master에 업로드

#### 11. heroku run python manage.py migrate

- heroku 서버 데이터베이스 업데이트

#### 12. heroku run python manage.py createsuperusre

- heroku 서버 슈퍼유저 생성

#### 13. heroku open

- 서버 URL이 열림

### 링크: <https://django-ystagram.herokuapp.com/>
