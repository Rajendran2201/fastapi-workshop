# CIT Hands-On

This repository contains a FastAPI application for hands-on experimentation.

## Getting Started

Follow the steps below to set up and run the application locally.

### 1. Clone the Repository

```
git clone https://github.com/tarunkumark/CIT-Hands-On.git
cd CIT-Hands-On
```

### 2. Create a Virtual Environment

Use Python's built-in `venv` module to create a virtual environment:

```
python -m venv env
```

Activate the virtual environment:

- On Windows:
  ```
  .\env\Scripts\activate
  ```
- On macOS/Linux:
  ```
  source env/bin/activate
  ```

### 3. Install Dependencies

Install the required packages listed in `requirements.txt`:

```
pip install -r requirements.txt
```

### 4. Run the Application

Start the FastAPI app using `uvicorn`:

```
uvicorn app:app --reload
```

The `--reload` flag enables automatic reloads on code changes (useful during development).

### 5. Access the Application

Once running, access the app in your browser at:

```
http://127.0.0.1:8000
```

Interactive API documentation is available at:

```
http://127.0.0.1:8000/docs
```

##
