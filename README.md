# ![Django DRF Example App](project-logo.png)

> ### Example Django DRF codebase containing real world examples (CRUD, auth, advanced patterns, etc) that adheres to the [RealWorld](https://github.com/gothinkster/realworld-example-apps) API spec.

This repo is functionality complete — PR's and issues welcome!

## Installation

1. Clone this repository
2. `cd` into `conduit-django`: `cd productionready-django-api`.
3. Install [pyenv](https://github.com/yyuu/pyenv#installation).
4. Install [pyenv-virtualenv](https://github.com/yyuu/pyenv-virtualenv#installation).
5. Install Python 3.7.9: `pyenv install 3.7.9`.
6. Create a new virtualenv called `productionready`: `pyenv virtualenv 3.7.9 productionready`.
7. Set the local virtualenv to `productionready`: `pyenv local productionready`.
8. Reload the `pyenv` environment: `pyenv rehash`.

If all went well then your command line prompt should now start with `(productionready)`.

If your command line prompt does not start with `(productionready)` at this point, try running `pyenv activate productionready` or `cd ../productionready-django-api`. 

If pyenv is still not working, visit us in the Thinkster Slack channel so we can help you out.

---------

# RealWorld - Article History API 구현

Article의 변경사항(추가/수정/삭제)을 기록할 수 있는 기능을 추가하고, 이를 조회할 수 있는 History API를 구현.

History API는 해당 Article 작성자만 확인 가능해야한다.

추가한 기능에 대한 테스트 코드 작성한다.

Backend코드의 각 git history 유지하고 추가한 내용에 대해 commit한다.

## 구현
### 1. Base Backend Source
 * Django Rest Framework(Python3) 
   * original: https://github.com/gothinkster/django-realworld-example-app
   * fork: https://github.com/youbeebee/django-realworld-example-app

### 2. API Spec

**Get Article History**  

`GET /api/history`  

`Authentication Need`

인증된 사용자의 Article 생성, 수정, 삭제 History를 반환한다.  
반환되는 field는 Article의 작성자, 제목, Request 종류(Create(POST), Update(PUT), DELETE), Request Body, 요청한 시간이다. 

**Response Example**
```
{
    "count":2,
    "next":null,
    "previous":null,
    "results":[
    {
        "author":{
            "username":"u1648021644",
            "bio":"",
            "image":"https://static.productionready.io/images/smiley-cyrus.jpg",
            "following":false
        },
        "req":"DELETE",
        "title":"How to train your dragon",
        "body":"<QueryDict: {}>",
        "time":"2022-03-23T07:47:39.987005+00:00"
    },
    {
        "author":{
            "username":"u1648021644",
            "bio":"",
            "image":"https://static.productionready.io/images/smiley-cyrus.jpg",
            "following":false
        },
        "req":"PUT",
        "title":"How to train your dragon",
        "body":"{
            'article': {'body': 'With two hands'}
        }",
        "time":"2022-03-23T07:47:35.140653+00:00"
    }]
}
```

### 3. 코드 설명
#### History Model 작성(models.py)  

`History` Model은 `author`, `request`, `title`, `body` 정보를 가짐
 * `author`: API caller
 * `req`: 요청의 종류 Create(POST), Update(Put), Delete(DELETE)
 * `title`: `Article`의 제목
 * `body`: `request`의 내용

```
class History(TimestampedModel):
    author = models.ForeignKey(
        'profiles.Profile', on_delete=models.CASCADE, related_name='history'
    )

    req = models.TextField()
    title = models.TextField()
    body = models.TextField()

    def __str__(self):
        return self.author + ' History'
```

#### History Model에 대한 View 및 Serializer 작성(views.py, serializers.py)

```
class HistoryAPIView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = HistorySerializer
    queryset = History.objects.all()

    def get_queryset(self):
        user = self.request.user.profile

        return History.objects.filter(
            author=user
        )
```

API Permission은 `IsAuthenticated`로 설정해서 인증된 유저만 확인할 수 있도록 설정.

히스토리 정보는 `user`로 필터해서 본인이 요청했던 API만 볼 수 있게 설정.

Articles View의 `create()`, `update()`, `delete()`가 실행될 때 `History` 객체를 생성 후 저장하도록 구현. 

#### API url 등록(urls.py)

```
url(r'^history/?$', HistoryAPIView.as_view()),
```

## 실행 및 테스트
### 실행방법
1. Installation 문단 참고하여 pyenv 가상환경 (또는 기타 Python 가상환경) 세팅
2. `pip install -r requirements.txt`
2. DB 마이그레이션 `python manage.py migrate`
3. 웹서버 실행 `python manage.py runserver`
4. 웹 브라우저에서 `http://localhost:8000/api` 확인

### 테스트 방법
1. 웹서버 실행
2. `cd test`
3. Full API Test 방법  
RealWorld App의 모든 API + History API를 테스트한다.  
테스트 과정 중 새 유저 생성 후 아티클 생성, 수정, 삭제 1회씩 하므로 총 3개 History가 검색됨.
```
APIURL=http://localhost:8000/api ./run-api-tests.sh
``` 
4. History API만 테스트  
History API와 관련된 작업만 수행한다.  
아티클 생성 1회, 수정 2회, 삭제 1회 수행 후 `history` 호출.
```
APIURL=http://localhost:8000/api ./run-api-tests-history.sh
``` 
