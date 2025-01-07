# <img src="./static/imgs/dd.png" alt="DD" style="width: 30px;" /> DD - Delete Duplicates

## What is this project

It allows you to verify if there are duplicated files in your file system. And, delete them if you want.

## How to run this project

1. Clone this project

```
git clone https://github.com/pepcmarques/deldup.git
```

2. Go to the `deldup` directory

```
cd deldup
```

3. Install a Python virtualenv

```
python -m venv .venv
```

4. Activate the `virtual environment`

```
source .venv/bin/activate     # For Linux or Mac

.venv/Scripts/activate.exe    # For Windows
```

5. Install dependencies

```
pip install -r requirements.txt
```

6. Run `DelDup`

```
python deldup.py
```

## The configuration file

The configuration file looks like the one below:

```json
{
  "home_dir": "/Users/YOUR_USER_HERE",
  "database_url": "sqlite:///./deldup.sqlite3",
  "mode": "none",
  "categories": {
    "images": {
      "code": "img",
      "ext": ["bmp", "gif", "jpg", "jpeg", "png", "tiff"]
    },
    "documents": {
      "code": "doc",
      "ext": ["doc", "docx", "odt", "ods", "ppt", "pptx", "pdf", "txt", "xls", "xlsx"]
    }
  }
}
```

| Key          | Description                                                            |
| ------------ | ---------------------------------------------------------------------- |
| home_dir     | Directory from which you want to recursively check files.              |
| database_url | url to connect to DB                                                   |
| mode         | DelDup mode (explained below)                                          |
| categories   | JSON structure that defines which files will be checked for duplicates |

### Modes

| Mode  | Description                                                    |
| ----- | -------------------------------------------------------------- |
| none  | Remove file visually only                                      |
| db    | Remove file entry from DB.                                     |
| fs    | Remove file from the file system.                              |
| │ all | Remove file entry from DB and remove file from the file system |

## How to use this project

The first time you run the project, it will create the configuration file and it will stops the execution.

The second time and you run the project, it will recursivelly check all the files and save entries in the database. This process takes a while.

After populating the DB, it will allow you to connect to it using your browser.

Open the browser and connect to `http://0.0.0.0:8000`

## Technologies used in this project

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![HTML](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![CSS](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-323330?style=for-the-badge&logo=javascript&logoColor=F7DF1E)

## How this project is organized

In the project root, you will find the main program `deldup.py`, `services.py`, and `settings.py`. There are other 4 (four) directories where you will find the code `app` (containing the database engine and models), `frontend` (not much), `backend` (api), and `static` (css, images, and JS code).

## How this project was implemented

I used Fastapi for the API and pure JavaScript to be able to run it anywhere. The beuty of it is to generate one executable with `pyinstaller`.

> I will prepare it asap for Mac, Linux, and Windows.

## Dependencies

Python

## How to contribute with this project

- Create an issue
- Wait for this issue to be assigned to you
- Develop the feature and make a PR

## Who contributed with this project

- [Paulo](https://github.com/pepcmarques)

## Contact Me

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://linkedin.com/in/pepcmarques)

## Do you need help?

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://linkedin.com/in/pepcmarques)

<!--
## Some docs that helped me creating this

[FastAPI + SQLModel + Alembic](https://testdriven.io/blog/fastapi-sqlmodel/)

[FastAPI + SQLModel + Alembic](https://github.com/testdrivenio/fastapi-sqlmodel-alembic/tree/main)

[FastAPI Compilation with PyInstaller](https://github.com/mohammadhasananisi/compile_fastapi)

[A minimal fastapi example loading index.html](https://stackoverflow.com/questions/65916537/a-minimal-fastapi-example-loading-index-html)

[Unlocking the Potential of FastAPI Sub-Applications for API Version Management](https://medium.com/@tarunrdhiraj/unlocking-the-potential-of-fastapi-sub-applications-for-api-version-management-f8df311574d0)
-->
