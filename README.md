# mini-sec-master
tutorial repo for a mini full-stack security master project

# Intro

In 20 steps, we will build a full-stack webapp that allows a user to type in any stock ticker and see its matching company name, description, and current price. We will use the [FMP API](https://financialmodelingprep.com/) to get financial data, pytest for unit testing, ruff for linting, and docker for containerization.

# Conditions of Satisfaction

It is helpful for me when working on development projects to first think about what conditions must be satisfied in order for the project to be considered complete. After it is clear what a "working program" must do, the development process becomes much more organized.

For this project, the conditions of satisfaction are simple:
*Client-Facing*
1. [ ] User can enter any stock ticker into a search box
2. [ ] Upon submission, the app **accurately** displays:
   - [ ] Company name
   - [ ] Company description
   - [ ] Current stock price
   - [ ] OR an error message if the ticker is invalid
*Internal*
3. [ ] The app has a passing and comprehensive unit test suite
4. [ ] The code passes linting with ruff
5. [ ] The app runs in a Docker container

# Lay of the Land

Before doing anything, your project structure will look like the following:

```bash
mini-sec-master/
├── .env # where the FMP API key is stored
├── Dockerfile # for containerization
├── docker-compose.yml # makes spinning up and down easier
├── requirements.txt
├── pyproject.toml # for linter config
├── README.md
├── app/ # where the full-stack app is
│   ├── __init__.py
│   ├── api/ # where the API is
│   │   ├── __init__.py
│   │   └── fmp_client.py # where the FMP API method you will make (to get company data) goes
│   └── frontend/ # where the frontend app you will make goes
│       └── app.py # where the frontend app will go
└── tests/ # where the unit tests you will make go
    └── test_fmp_client.py # where the unit tests for the FMP API method will go
```

Take a moment to familiarize yourself with the project structure. This framework is common - it will seem overwhelming if you don't stop to understand it before proceeding.

# Step-by-Step Instructions

*Preferably on a new branch. . .*

## Step 1: Install the requirements

run the following in terminal
```bash
pip install -r requirements.txt
```

## Step 2: Set up the .env file

create a .env file in the root directory and add the following:
```bash
FMP_API_KEY=<your-api-key>
```

once you have added the API key, remember to add the .env file to the .gitignore file so that it is not committed to the repository.

## Step 3: Understand the project structure

Re-read the Lay of the Land section above.

## Step 4: Read the FMP Documentation

Read the [FMP API documentation](https://site.financialmodelingprep.com/developer/docs/stable) to understand how to use the API.
*Hint:* use the [Company Profile endpoint](https://site.financialmodelingprep.com/developer/docs/stable#profile-symbol)

## Step 5: Run a test query on the API endpoint to understand the structure of the data

With your endpoint and API key, run the query in your browser with an example ticker. This will allow you to understand the structure of the data we will be working with.

Also see what happens if you give the API invalid inputs (iow what errors should we expect).

## Step 6: Start your test suite

In test_fmp_client.py, there’s a basic test asserting that your method raises NotImplementedError. Try running the tests:

```bash
pytest
```

The tests should fail because we haven't implemented the method yet.

*Note:* you will notice that the method raises a NotImplementedError, which is a type of Exception. The test expects that a ValueError is raised, which is also a type of Exception. This highlights the importance of not using the ambiguous Exception type in tests, because if we had, our test would have passed even though nothing has been implemented yet. [illustration](https://en.wikipedia.org/wiki/Roll_Safe)

## Step 7: Build out your test suite

Think about the problem and build out a test suite that satisfies the conditions of satisfaction. Try to think of some edge cases.

*What data is expected to be returned by the API? What data would we consider an error if we received it from FMP?*

*Are there any user inputs that we should reject before even making the API call?*

## Step 8: Implement the method

Now that you've finished your test suite, you can start on implementing the api method.

Do this where you see:

```python
def get_company_data_for_ticker(ticker: str):
    """
    Fetch the company name, company description, and current stock price for `ticker`.
    """
    raise NotImplementedError()
```

## Step 9: Get your tests to pass

It is rare for a first implementation to pass all the tests (unless the test suite is insufficient). You will likely have to make multiple iterations of testing and debugging before completing the method.

## Step 10: Run the linter

Use ruff to check if you have any linting errors:

```bash
ruff check
```

Then use the fixing tool to try and fix them:

```bash
ruff check --fix
```

Then use the formatting tool:

```bash
ruff format
```

Make any changes necessary to satisfy the linter.

## Step 11: Commit your code so far

Run `status` to review all your changes, then add them and provide a helpful commit message.

# Intermission

The next couple steps will be about setting up the containerization of the app. During these steps, you will be able to see the starter streamlit application working.

## Step 12: Setup Dockerfile and docker-compose.yml for API

Create a Dockerfile in the root directory that looks like this:

```dockerfile
FROM python:3.11-slim  # this tells us what base docker image to use. the docker community is vast and has done most of the work for us, all we have to do is decide what code to pull in and what requirements to add on top of the image
WORKDIR /code  # this is the working directory for the container. similar to how when you open file explorer, you are taken to your desktop
COPY requirements.txt ./  # this copies the requirements.txt file from your device into the container
RUN pip install -r requirements.txt  # this instructs the container to install the dependencies in the requirements.txt file
COPY app ./app  # this copies the app directory from your device into the container
COPY .env .env  # this copies the .env file from your device into the container
CMD ["streamlit", "run", "app/frontend/app.py", "--server.port=8501", "--server.address=0.0.0.0"]  # you can pass commands as a list of arguments to the CMD function. this list of commands instructs the container to run streamlit (and passes it the file location, port, and address (in this case, localhost))
```

Also make a docker-compose.yml file in the root directory that looks like this:

```yaml
version: "3.9"  # this is the version of the docker compose file format
services:
  app:
    build: .
    ports:
      - "8501:8501"  # this is a port mapping, which maps (left side) the port on your device (8501) to (right side) the port on the container (8501)
    env_file:
      - .env
```

## Step 13: Run your app in Docker

Build and start the container:

```bash
docker-compose up --build
```

## Step 14: Test the app locally

You should be able to see the basic starter app at `http://localhost:8501`.

If your implementation was successful, you will see the results of quering company data for AAPL with the method you implemented in the previous step.

## Step 15: Implement the frontend

Now, you can start working on the frontend. A basic streamlit application has been setup for you:

```python
"""
Streamlit UI for our mini security master.
"""

import streamlit as st
from app.api.fmp_client import get_company_data_for_ticker

st.title("📈 Mini Security Master")

# ticker = st.text_input("Enter a stock ticker", value="AAPL", max_chars=10) . . .

aapl_data = get_company_data_for_ticker("AAPL")

st.write(aapl_data)
```

Remember that your frontend implementation must satisfy the conditions of satisfaction. Unit testing (with pytest) of your frontend implementation is not necessary.

## Step 16: Manually test your frontend

Restart your docker containers and test out your implementation. Try inputting different tickers, an erroneous ticker, etc and see what happens.

## Step 17: Lint your code

Repeat the linting steps from Step 11.

## Step 18: Commit your frontend implementation

Run `status` to review all your changes, then add them and provide a helpful commit message.

## Step 19: Open a pull request

Open a pull request and request a review.

## Step 20: Post-approval

Congratulations, you now know how to build a full-stack webapp with python, docker, pytest, ruff, streamlit, and the FMP API. According to [indeed](https://www.indeed.com/career/full-stack-developer/salaries), you have just raised the floor of your salary to $120,000.

*Optional*

## (Optional) Step 21: Restart from scratch and let an LLM do the work

Note: use cursor or another IDE that supports LLM integration for this. Use a reasoning model.

1. Check out main so that you are starting from scratch.

2. Open a conversation with an LLM of your choice and give it the below prompt

The point of including this step is to show you just how useful reasoning models are at coding tasks like this. What took you many minutes likely took the LLM under two minutes to complete in full. It also probably made a more comprehensive test suite, added better documentation, etc compared to your implementation.

The point is not just to highlight the benefits of using an LLM in development. Review the LLM's implementation after it has finished. Depending on the model you used, it is likely that the model used libraries or techniques that are foreign to you. However, the implementation probably works and the frontend app probably runs smoothly. If the LLM was able to do a better job than you in a quicker timeframe, what is the point of learning how to do this ourselves anyway?

The truth is that you can get away with most coding tasks using an LLM IF you have precise instructions (we had 20 very precise steps), guardrails (we used linting, testing, etc), and clear COS. The truth is also that the quick gratification vibe coding gives us naturally incentivizes us to get lazy on the instruction set, guardrails, and COS over time. This leads to sneaky errors in LLM implementation that compound over time and become difficult to debug and stressful to fix. The errors are often not an issue with the LLMs implementation, but rather an issue with what you asked it to do in the first place.

Be aware of the tradeoffs and try to vibe code responsibly.

```
Below is a ready-to-paste prompt you can drop between the trailing triple-backticks in your README. It’s tuned for Cursor’s Autopilot: the model will work step-by-step, write tests first, keep ruff clean, and containerize everything exactly as the walkthrough specifies.

````text
You are an expert Python full-stack engineer and teacher working inside the **mini-sec-master** repo.

**Mission**  
Execute Steps 1 – 20 of the README to deliver a production-ready, fully-tested, ruff-clean, Dockerized Streamlit app that lets a user enter any stock ticker and receive its company name, description, and current price (or a graceful error).

---

### Global working rules
1. **TDD first.** Expand the unit-test suite before writing production code; keep `pytest` green at every commit.  
2. **Incremental commits.** Commit after each major milestone with clear messages (e.g. `feat(api): implement get_company_data_for_ticker`).  
3. **Lint hygiene.** `ruff check`, `ruff check --fix`, then `ruff format` must report zero issues before every commit.  
4. **Follow the README structure and filenames exactly.**

---

### Detailed implementation checklist

#### 1 – Dependencies & environment  
* Install everything from `requirements.txt`.  
* Expect `FMP_API_KEY` in a root `.env`; raise a clear error if missing.

#### 2 – `get_company_data_for_ticker` (`app/api/fmp_client.py`)  
* Signature → `def get_company_data_for_ticker(ticker: str) -> dict`.  
* Validate: non-empty, alphanumeric, ≤ 10 chars; raise `ValueError` immediately on bad input.  
* Call `https://financialmodelingprep.com/api/v3/profile/{ticker.upper()}?apikey={key}` via `requests`.  
* If HTTP ≠ 200, empty list, or required fields absent, raise `ValueError("Ticker not found")`.  
* Return  
  {
      "symbol": str,
      "companyName": str,
      "description": str,
      "price": float,
  }

#### 3 – Unit tests (`tests/test_fmp_client.py`)

Cover:

* Happy path (mocked API) for a valid ticker (e.g., AAPL).
* Invalid ticker, empty string, or bad characters ⇒ `ValueError`.
* Network error surfaces gracefully.

#### 4 – Docker

* Create `Dockerfile` and `docker-compose.yml` exactly as shown in the README (use `--no-cache-dir` on pip install for slim image).
* `docker-compose up --build` must start Streamlit on port 8501.

#### 5 – Frontend (`app/frontend/app.py`)

* Streamlit UI: `st.text_input` for ticker, submit button.
* On submit, call `get_company_data_for_ticker` and display:

  * Company Name as title/header
  * Description in an expander
  * Current Price via `st.metric`
* Catch `ValueError` and show `st.error(...)`.

#### 6 – Manual & automated verification

* Ensure all tests pass and ruff is clean.
* Run the container locally and confirm AAPL returns correct info.

---

### Finish line criteria

✔️ `pytest` passes
✔️ `ruff check` & `ruff format` clean
✔️ `docker-compose up` launches a working app at `http://localhost:8501`

Begin executing these steps now, reasoning aloud when helpful, and keep the repository in a consistently runnable state throughout.
```