from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = "chave"


USUARIO_CORRETO = "admin"
SENHA_CORRETA = "1234"

PETS = []

@app.route("/")
def index():
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        usuario = request.form.get("usuario", "")
        senha = request.form.get("senha", "")

        if usuario == USUARIO_CORRETO and senha == SENHA_CORRETA:
            session["usuario"] = usuario
            return redirect(url_for("home"))
        else:
            return render_template("login.html", erro="Usuário ou senha incorretos.")

    return render_template("login.html", erro=None)


@app.route("/home")
def home():
    if "usuario" not in session:
        return redirect(url_for("login"))

    return render_template("home.html", usuario=session["usuario"])


@app.route("/register", methods=["GET", "POST"])
def register():
    if "usuario" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":

        pet = {
            "nome": request.form.get("nome", "").strip(),
            "especie": request.form.get("especie", "").strip(),
            "idade": request.form.get("idade", "").strip(),
            "sexo": request.form.get("sexo", "").strip(),
            "cor": request.form.get("cor", "").strip(),
            "proprietario": request.form.get("proprietario", "").strip(),
            "cpf": request.form.get("cpf", "").strip(),
            "endereco": request.form.get("endereco", "").strip(),
        }

        PETS.append(pet)
        flash("Pet cadastrado com sucesso!")
        return redirect(url_for("pets"))

    return render_template("register.html")


@app.route("/pets")
def pets():
    if "usuario" not in session:
        return redirect(url_for("login"))

    return render_template("pets.html", pets=PETS)


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)
