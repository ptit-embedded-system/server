# HOW TO RUN

- Create environment:

  Windows:

  ```bash
  python -m venv tfod
  ```

  Linux:

  ```bash
  python3 -m venv tfod
  ```

- Activate the environment:

  Linux/MacOS:

  ```bash
  . tfod/bin/activate
  ```

  Windows:

  ```bash
  .\tfod\Scripts\activate
  ```

- Install dependencies:

  ```bash
  python -m pip install --upgrade pip
  pip install ipykernel
  python -m ipykernel install --user --name=tfodj
  ```

- Create a folder in project with name `uploads`

- Run every cells in Install.ipynb

- Run flask:
  ```bash
  python app.py
  ```
