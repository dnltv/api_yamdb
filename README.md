### YaMDb project (group project of the 10th sprint of the Yandex.Practicum course)
### Description
The YaMDb project collects user reviews (`Review`) of works (`Title`).
The works are divided into categories: "_Books_", "_Films_", "_Music_".
The list of categories (`Category`) can be expanded (for example, you can add a category "*Fine Arts*" or "*Jewelry*").

Development Team:
- [Danil Treskov](https://github.com/dnltv)
- [Ioann Chimrov](https://github.com/ioann7)
- [Kirill Lesnichuk](https://github.com/ButtonSlayer)

The works themselves are not stored in YaMDb, you can't watch a movie or listen to music here.

In each category there are works: books, movies or music. For example, in the category "**_Books_**" there may be works "Winnie the Pooh and everything-everything-everything" and "Martian Chronicles", and in the category "**_Music_**" — the song "Just Now" by the group "Insects" and the second suite by Bach. A work can be assigned a genre from the preset list (for example, "**_Fairy Tale_**", "**_Rock_**" or "**_Arthouse_**"). Only the administrator can create new genres.

Grateful or outraged readers leave text reviews for the works (`Review`) and give the work a **rating** (in the range from one to ten). From the set of scores, the average score of the work is automatically calculated.

The full API documentation is located at the endpoint `/redoc`

### Technology Stack:
- Python 3.7
- Django 3.2
- DRF 3.12.4
- JWT 5.2.2

Full list in the file **requirements.txt**

### Launching a project in dev mode
- Clone the repository and go to it on the command line.
- Install and activate the virtual environment taking into account the Python 3.7 version (choose python at least 3.7):

```bash
py -3.7 -m venv venv
```

```bash
source venv/Scripts/activate
```

- Install all dependencies from the file **requirements.txt**

```bash
python -m pip install --upgrade pip
```

```bash
pip install -r requirements.txt
```

- Perform migrations:

```bash
python manage.py migrate --run-syncdb
```

If necessary, fill in the database with test data with the command:

```bash
python manage.py csv_to_db
```

Create a superuser, then change the role in the admin panel from `user` to `admin`:

```bash
python manage.py createsuperuser
```

Launching the project:

```bash
python manage.py runserver
```

### Examples of working with the API for all users

Detailed documentation is available at the endpoint `/redoc/`

For unauthorized users, working with the API is available in read mode, you will not be able to change or create anything.

```
Access rights: Available without a token.
GET /api/v1/categories/ - Getting a list of all categories
GET /api/v1/genres/ - Getting a list of all genres
GET /api/v1/titles/ - Getting a list of all works
GET /api/v1/titles/{title_id}/reviews/ - Getting a list of all reviews
GET /api/v1/titles/{title_id}/reviews/{review_id}/comments/ - Getting a list of all comments to the review
Access rights: Administrator
GET /api/v1/users/ - Getting a list of all users
```

### User roles

- **_Anonymous_** — can view descriptions of works, read reviews and comments.
- **_Authenticated user_ (`user`)** — can, like an Anonymous Person, read everything, additionally he can publish reviews and rate works (films / books / songs), can comment on other people's reviews; can edit and delete his reviews and comments. This role is assigned by default to each new user.
- **_Moderator_ (`moderator`)** — the same rights as an Authenticated User plus the right to delete any reviews and comments.
- **_Administrator_ (`admin`)** — full rights to manage all project content. Can create and delete works, categories and genres. Can assign roles to users.
- **_Django superuser_** — has administrator rights (admin)

### Registering a new user
Get a confirmation code to the transmitted `email`.
Access rights: Available without a token.
It is forbidden to use the name `"me"` as a `username`.
The fields `email` and `username` must be unique.

Registering a new user:

```
POST /api/v1/auth/signup/
```

```json
{
"email": "string",
"username": "string"
}
```

Getting a JWT token:

```
POST /api/v1/auth/token/
```

```json
{
"username": "string",
"confirmation_code": "string"
}
```

### Examples of working with the API for authorized users

Adding a category:

```
Access rights: Administrator.
POST /api/v1/categories/
```

```json
{
"name": "string",
"slug": "string"
}
```

Deleting a category:

```
Access rights: Administrator.
DELETE /api/v1/categories/{slug}/
```

Adding a genre:

```
Access rights: Administrator.
POST /api/v1/genres/
```

```json
{
"name": "string",
"slug": "string"
}
```

Deleting a genre:

```
Access rights: Administrator.
DELETE /api/v1/genres/{slug}/
```

Updating the publication:

```
PUT /api/v1/posts/{id}/
```

```json
{
"text": "string",
"image": "string",
"group": 0
}
```

Adding a work:

```
Access rights: Administrator.
You cannot add works that have not yet been released (the year of release cannot be more than the current one).

POST /api/v1/titles/
```

```json
{
"name": "string",
"year": 0,
"description": "string",
"genre": [
"string"
],
"category": "string"
}
```

Adding a work:

```
Access rights: Available without a token
GET /api/v1/titles/{titles_id}/
```

```json
{
"id": 0,
"name": "string",
"year": 0,
"rating": 0,
"description": "string",
"genre": [
{
"name": "string",
"slug": "string"
}
],
"category": {
"name": "string",
"slug": "string"
}
}
```

Partial updating of information about the work:

```
Access rights: Administrator
PATCH /api/v1/titles/{titles_id}/
```

```json
{
"name": "string",
"year": 0,
"description": "string",
"genre": [
"string"
],
"category": "string"
}
```

Partial updating of information about the work:
```
Access rights: Administrator
DEL /api/v1/titles/{titles_id}/
```

Similarly for `Titles`, `Reviews` and `Comments`.

### Working with users:

There are some restrictions on working with users.

Getting a list of all users:
```
Access rights: Administrator
GET /api/v1/users/ - Getting a list of all users
```

Adding a user:

```
Access rights: Administrator
The email and username fields must be unique.
POST /api/v1/users/ - Adding a user
```

```json
{
"username": "string",
"email": "user@example.com",
"first_name": "string",
"last_name": "string",
"bio": "string",
"role": "user"
}
```

Getting a user by `username`:

```
Access rights: Administrator
GET /api/v1/users/{username}/ - Getting a user by username
```

Changing user data by `username`:

```
Access rights: Administrator
PATCH /api/v1/users/{username}/ - Changing user data by username
```

```json
{
"username": "string",
"email": "user@example.com",
"first_name": "string",
"last_name": "string",
"bio": "string",
"role": "user"
}
```

Deleting a user by `username`:

```
Access rights: Administrator
DELETE /api/v1/users/{username}/ - Deleting a user by username
```

Getting your account details:

```
Access rights: Any authorized user
GET /api/v1/users/me/ - Getting their account data
```

Changing your account details:

```
Access rights: Any authorized user
PATCH /api/v1/users/me/ # Changing your account details
```

The project was implemented as part of the Yandex.Practicum course on Python developer specialization (back-end).

### Documentation
- http://127.0.0.1:8000/redoc/

### Authors:
- [Danil Treskov](https://github.com/dnltv)
- [Ioann Chimrov](https://github.com/ioann7)
- [Kirill Lesnichuk](https://github.com/ButtonSlayer)