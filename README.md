# Lemon-Stand
## Description
This is a sales tracking and reporting system to help manage the incredible amounts of lemonade the staffs sell on a daily basis, and automatically calculate appropriate commissions for each hard-working sales staff.
## Design
![Diagram](/images/ER_Diagram.png)
## How to run the project
- Install Python 3+ from [Python official download website](https://www.python.org/downloads/)
- Upgrade `pip` to the latest version.
    - For Windows, go to the Search bar and type "Edit the system environment variables", click on it.
    - Go to the `Environment Variables`, then `Path` in "User Variables" and copy the link of Python script (..\Scripts\).
    - Paste the link in the terminal and do `cd <your_python_link>`. Then do `python -m pip install --upgrade pip`.
- Install `virtualenv` and `virtualenv` (recommended) in the command line.
    - For Linux: `pip install --user virtualenv` and `pip install vitualenvwrapper`.
    - For Windows: `pip install virtualenv` and `pip install virtualenvwrapper-win`.
- Clone the repository to your work directory.
- Make a virtual environment by typing `mkvirtualenv <your_virtualenv_name>`, then type `workon <your_virtualenv_name>`
- Then change directory to `/<your_work_directory/lemonademanager` and run `python manage.py runserver`
- For full instructions on how to download Django, visit [Django's instalation](https://docs.djangoproject.com/en/3.0/intro/install/)
## Pages
- Admin Page        : `http://localhost:8000/admin/` (Use `admin` as the username and password)
- Index Page        : `http://localhost:8000/sales/`
- Sales Entry Page  : `http://localhost:8000/sales/form`
- Report Page       : `http://localhost:8000/sales/report`
## Limitation
There are a lot of room for improventments in the project.
- In the Sale Entry Page, you can only submit one type of product for each sale.
- The design for the database is still suboptimal. (Need a better design to handle sale and commission)
