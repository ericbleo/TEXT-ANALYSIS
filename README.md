# TEXT ANALYSIS APP

This is a small learning project. You type text in a web page. A Python server reads that text and sends back simple statistics (word count, sentiment, and more). The web page shows the results.

There are two parts:

- **`server`** — the “brain.” It runs on your computer and listens for requests.
- **`client`** — the web page you see in the browser. It talks to the server.

You need **both** running at the same time to use the app.

---

## What you need on your computer

1. **Python 3** (version 3.10 or newer is fine).  
   Check in a terminal: `python --version`  
   If that does not work, try: `py --version`

2. **Node.js** (the LTS version from the official website is best).  
   Check: `node --version` and `npm --version`

If any command is “not found,” install that tool first, then open a **new** terminal window and try again.

---

## One-time setup

### Server (Python)

1. Open a terminal.
2. Go into the server folder (change the path if yours is different):

   ```bash
   cd path/to/TEXT ANALYSIS/server
   ```

3. Install the Python packages this project uses:

   ```bash
   pip install fastapi uvicorn pydantic
   ```

   If `pip` fails, try: `python -m pip install fastapi uvicorn pydantic`

### Client (React)

1. Open a terminal.
2. Go into the client folder:

   ```bash
   cd path/to/TEXT ANALYSIS/client
   ```

3. Install the JavaScript packages:

   ```bash
   npm install
   ```

You only need to run these installs **once** (or again if you delete `node_modules` or change computers).

---

## How to run the project (every time)

Use **two** terminal windows: one for the server, one for the client.

### Terminal 1 — start the server

```bash
cd path/to/TEXT ANALYSIS/server
uvicorn main:app --reload
```

Leave this running. You should see messages that the server started.  
The API lives at: **http://localhost:8000**

You can open **http://localhost:8000/docs** in the browser to see all API routes and try them there (optional).

### Terminal 2 — start the web page

```bash
cd path/to/TEXT ANALYSIS/client
npm run dev
```

Leave this running. The terminal will print a local address (often **http://localhost:5173**).  
Open that address in your browser. That is your app.

---

## How to use the app

1. Make sure **both** terminals are still running (server + client).
2. In the browser, type or paste text in the **Input** box.
3. Click **Analyze text**.
4. Read the numbers and lists in the **Results** section.

If something goes wrong, read the error message in the browser or in the terminal where the server is running.

---

## If something does not work

**“Cannot connect” or the button does nothing**

- Is the **server** terminal still open and running?
- Is the URL in the browser the one **`npm run dev`** printed (usually port **5173**)?
- The server must allow requests from that address. This project is set up for **http://localhost:5173** by default.

**“Port already in use”**

- Another program is using that port. Close other copies of the server or client, or stop old terminals, then try again.

**Python says `uvicorn` is not found**

- Run: `python -m uvicorn main:app --reload`  
  (Run this **inside** the `server` folder.)

---

## Project folders (simple map)

| Folder   | What it is                          |
| -------- | ----------------------------------- |
| `server` | Python + FastAPI code (`main.py`)   |
| `client` | React + Vite web app                |

---

## Learning ideas

- Change the sample text and watch how **word count** and **sentiment** change.
- Open **http://localhost:8000/docs** and call **`POST /analyze`** with the same JSON the web page sends: `{"text": "your words here"}`.
- Read `server/main.py` slowly to see how each number is calculated.

That is enough to run and explore this project as a beginner.
