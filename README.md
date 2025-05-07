# Backend

## Setup Instructions

### 1-Clone the Repository

```bash
git clone https://github.com/Give-and-Grow/Backend.git
cd Backend
```

### 2-Create a Virtual Environment:

```bash
python -m venv venv
```

### 3-Activate the Virtual Environment:

    a-On Windows:

```bash
venv\Scripts\activate
```

    b-On MacOS/Linux:

```bash
source venv/bin/activate
```

### 4-Install Dependencies:

```bash
pip install -r requirements.txt
```

## Running the Application

### 1-Ensure the virtual environment is activated

### 2-Run the Flask app

```bash
python run.py
```

### 3-Open your browser and navigate to http://127.0.0.1:5000/ to see the app in action.

To stop the app, press

```bash
Ctrl+C
```

## Dependencies

### The project uses the following Python packages (listed in requirements.txt):

### To update dependencies, activate the virtual environment and run:

```bash
pip freeze > requirements.txt
```

### To update DataBase, activate the virtual environment and run:

```bash
flask db migrate -m "some comments"
flask db upgrade
```

## Contributing

### 1-Create a new branch for your changes

```bash
git checkout -b newBrnach
```

### 2-Make your changes and commit them

```bash
git add .
git commit -m "Your message"
```

### 3-Push to the branch

```bash
git push origin newBrnach
--Create Pull Request
--Merge Pull Request
git checkout main
git pull origin main
git branch -d newBrnach
git push origin --delete newBrnach
git checkout -b new-feature
```
