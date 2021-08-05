from flask import Flask, render_template

app = Flask(__name__)


@app.template_filter("is_prime")
def isPrime(n):
    if n == 2 or n == 3:
        return True
    if n % 2 == 0 or n < 2:
        return False

    for i in range(3, int(n ** 0.5)+1, 2):
        if n % i == 0:
            return False
    return True


@app.route("/")
def index():
    num_list = []
    for i in range(1, 10000, 1):
        num_list.append(i)
    return render_template("index.html", num_list=num_list)
