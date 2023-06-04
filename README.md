# HOW TO RUN

- Create environment:

  Windows:

  ```bash
  python -m venv venv
  ```

  Linux:

  ```bash
  python3 -m venv venv
  ```

- Activate the environment:

  Linux/MacOS:

  ```bash
  source venv/bin/activate
  ```

  Windows:

  ```bash
  .\venv\Scripts\activate
  ```

- Install dependencies:

  ```bash
  python -m pip install --upgrade pip
  pip install jupyter ipykernel
  python -m ipykernel install --user --name=venv
  ```

- Create a folder in project with name `uploads` (if receive file server)

- Run command to run notebook with kernel of virtual environment:

  ```bash
  jupyter notebook
  ```

  This will open Jupyter Notebook in web browser.

- Choose the notebook named Install.ipynb.

- Run every cells in Install.ipynb

- Run flask:
  ```bash
  python app.py
  ```
