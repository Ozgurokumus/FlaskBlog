# Flask Blog

`Flask Blog` is a Flask project with features:

- Personal profile creation and modification
- Post creation with categories
- Editable/deletable posts
- Posts are commentable
- You can also reply to other comments 

## How to start

 To start this blog, manually clone this repository. Project is ready to run (with some requirements). You need to clone and run:

```sh
$ mkdir FlaskBlog
$ cd FlaskBlog
$ git clone https://github.com/Ozgurokumus/FlaskBlog .
$ pip install -r requirements.txt
$ python app.py
```

Open http://127.0.0.1:5000/, create some posts, customize your profile and **have fun**.

## Request Examples

### API Resources

  - [GET /posts](#get-posts)
  - [GET /posts/[id]](#get-postsid)
  - [GET /categories](#get-categories)
  - [GET /categories/[categoryname]](#get-categoriescategoryname)
  - [GET /users](#get-users)
  - [GET /users/[username]](#get-usersusername)
  
### GET /posts

Example: http://127.0.0.1:5000/api/posts

Response body:
```
  {
    "posts": [
      {
        "author_username": "Hou", 
        "id": 1, 
        "title": "Something Fancy"
      }, 
      {
        "author_username": "Ranpo", 
        "category": "General", 
        "id": 2, 
      }
    ]
  }
```
### GET /posts/id

Example: http://127.0.0.1:5000/api/posts/1

Response body:
```
  {
    "post": {
      "author_username": "Hou", 
      "category": "Gaming", 
      "content": "Some text", 
      "id": 1, 
      "title": "Something Fancy"
    }
  }
```
### GET /categories

Example: http://127.0.0.1:5000/api/categories

Response body:
```
  {
    "categories": [
      "General", 
      "Sports", 
      "Gaming", 
      "News", 
      "TV", 
      "Memes", 
      "Travel", 
      "Music, Art & Design"
    ]
  }
```
### GET /categories/[categoryname]

Example: http://127.0.0.1:5000/api/categories/General

Response body:
```
  {
    "posts": [
      {
        "author_username": "Hou", 
        "category": "General", 
        "content": "Some text", 
        "id": 2, 
        "title": "Fancy Title"
      }, 
      {
        "author_username": "Rugz", 
        "category": "General", 
        "content": "More text", 
        "id": 3, 
        "title": "Cool Title"
      }
    ]
  }
```
### GET /users

Example: http://127.0.0.1:5000/api/users

Response body:
```
  {
    "users": [
      "Hou", 
      "Rugz"
    ]
  }
```
### GET /users/[username]

Example: http://127.0.0.1:5000/api/users/Hou

Response body:
```
  [
    {
      "user": {
        "facebook": "You haven't set your facebook adress ", 
        "id": 1, 
        "twitter": "You haven't set your twitter adress ", 
        "username": "Hou"
      }
    }, 
    {
      "posts": [
        {
          "author_username": "Hou", 
          "category": "Gaming", 
          "content": "Some text", 
          "id": 1, 
          "title": "Something Fancy"
        }, 
        {
          "author_username": "Hou", 
          "category": "General", 
          "content": "Some text", 
          "id": 2, 
          "title": "Fancy Title"
        }
      ]
    }
  ]
```
