# plpgsql-deepdive
PL/pgSQL Exercise to solve challenges encounter in Application.

## Prerequisites
Ensure you have the following installed on your system:

- **Python** (version 3.11.4 or later) → [Download here](https://www.python.org/downloads/)
- **PostgreSQL**  → [Download here](https://www.postgresql.org/download/)

---

## Installation Guide

### 1️⃣ Clone the Repository
If using Git, open a terminal or command prompt and run:

```sh
git clone https://github.com/AkashDotPy/postgresql_excercise.git
cd postgresql_excercise
```

If not using Git, manually download and extract the project files.

### 2️⃣ Create a Virtual Environment (Recommended)
To avoid conflicts with system packages, create a virtual environment:

```sh
python -m venv venv
```

Activate the virtual environment:

- **macOS/Linux**:
  ```sh
  source venv/bin/activate
  ```
- **Windows**:
  ```sh
  venv\Scripts\activate
  ```

### 3️⃣ Install Dependencies
Run the following command to install required packages:

```sh
pip install -r requirements.txt
```

---

## Configuration

### 4️⃣ Set Up Environment Variables
Add database credentials in  `.env` file in the project root:

```ini
DB_HOST=your_host
DB_PORT=your_port
DB_NAME=your_db_name
DB_USER=your_user
DB_PASSWORD=your_password
```

---

## Running the Application

### 5️⃣ Start the Streamlit App
Execute the following command:

```sh
streamlit run app/main.py
```

This will start a local development server and provide a URL (e.g., `http://localhost:8501`) where you can access the app in your browser.

---

## Usage
- Navigate through the **sidebar** to access different pages:
  - **Home**: Overview of the application.
  - **Booking Summary**: Displays booking details for selected facilities.
  - **Search**: Allows searching through facility data.
- Select a facility from the sidebar dropdown to view usage hours and booking summaries.
- Interact with the data displayed using Streamlit’s built-in widgets.

---

## Troubleshooting

### Issue: Dependencies not installing?
- Ensure you're using the correct Python version:
  ```sh
  python --version
  ```
- Try upgrading pip:
  ```sh
  pip install --upgrade pip
  ```

### Issue: Database connection errors?
- Check your `.env` file for correct database credentials.
- Ensure the database server is running.



