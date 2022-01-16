## Report

This project is made up of the following components:

- a Flask application (`main.py`) that serves a string to two routes: `/` and `/foo`;
- a continuously running Gunicorn server process (`foobar`), listening on `localhost:8000`;
- an Nginx reverse proxy that redirects visitors on port 80 to the Gunicorn server;
- a Digital Ocean web server running on IP `164.92.222.203`;

Upon pushing code to GitHub, the action specified in `/.github/workflows/action.yaml` is automatically run. This action checks out the repository, sets up Python and `pytest` and runs the tests in `test_main.py` to check the output of the Flask application.

If the tests fail, the workflow is automatically halted and an error message appears. If all tests pass, GitHub Action connects to the server using the password that is stored as a repo secret, and runs a bash script (`bash /home/script.sh`), which has the following contents:

```
echo 'Tests have succeeded. Running commands on server...'
echo 'Checking status of server.'
systemctl status foobar
cd /home/foobar/flask_continuous_development
echo 'Pulling code'
git pull origin master
echo 'Restarting server after code pull'
systemctl restart foobar
```

I had to solve a few problems while setting up this automatic workflow:

1. Logging to the server with `ssh <user>@<ip_address>` did not work in the `.yaml` file. The terminal prompts you for a password, but you cannot supply any in an automated workflow. To solve this, I used a custom action (`appleboy/ssh-action@master`) that allows you to supply a host and password saved as repo secrets.

2. Running `git fetch` did not work on my server (even outside of the Github Action), but this was my mistake: I used the HTTPS protocol, not the SSH one.

3. Using `git pull` did not succeed in my GitHub action because my server did not have access to my repo (`Check permissions`), even though I had my SSH deploy key correctly installed. I discovered that the problem was that the SSH key required a passphrase, which GitHub Actions cannot enter for you. To solve this, I made the SSH available without a passphrase.
