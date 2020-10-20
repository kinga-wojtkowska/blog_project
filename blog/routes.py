from flask import Flask, render_template, request, redirect, url_for, flash, session  # noqa: E501
from blog import db, app
from blog.models import Entry
from blog.forms import EntryForm, LoginForm
import functools


@app.route("/")
def homepage():
    all_posts = Entry.query.filter_by(is_published=True).order_by(Entry.pub_date.desc())  # noqa: E501
    return render_template("post_on_homepage.html", all_posts=all_posts)


def post_form(entry_id):
    errors = None
    if entry_id == None:
        form = EntryForm()
        if request.method == "POST":
            if form.validate_on_submit():
                post = Entry(title=form.title.data, body=form.body.data, is_published=form.is_published.data)  # noqa: E501
                db.session.add(post)
                db.session.commit()
                flash('Post został pomyślnie dodany!')
                return redirect(url_for("homepage"))
            else:
                errors = form.errors
        return render_template("entry_form.html", form=form, errors=errors)
    elif entry_id != 0:
        entry = Entry.query.filter_by(id=entry_id).first_or_404()
        form = EntryForm(obj=entry)
        if request.method == "POST":
            if form.validate_on_submit():
                form.populate_obj(entry)
                db.session.commit()
                flash('Post został pomyślnie zmieniony!')
                return redirect(url_for("homepage"))
            else:
                errors = form.errors
        return render_template("entry_form.html", form=form, errors=errors)


def login_required(view_func):
    @functools.wraps(view_func)
    def check_permissions(*args, **kwargs):
        if session.get('logged_in'):
            return view_func(*args, **kwargs)
        return redirect(url_for('login', next=request.path))
    return check_permissions


@app.route("/new-post/", methods=["GET", "POST"])
@login_required
def create_entry():
    return post_form(entry_id=None)


@app.route("/edit-post/<int:entry_id>", methods=["GET", "POST"])
@login_required
def edit_entry(entry_id):
    return post_form(entry_id)


@app.route("/login/", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    errors = None
    next_url = request.args.get('next')
    if request.method == 'POST':
        if form.validate_on_submit():
            session['logged_in'] = True
            session.permanent = True  # Use cookie to store session.
            flash('Lgoowanie zakończone sukcesem!', 'success')
            return redirect(next_url or url_for('homepage'))
        else:
            errors = form.errors
    return render_template("login_form.html", form=form, errors=errors)


@app.route('/logout/', methods=['GET', 'POST'])
def logout():
    if request.method == 'POST':
        session.clear()
        flash('Zostałeś wylogowany!', 'success')
    return redirect(url_for('homepage'))


@app.route('/drafts/', methods=['GET', 'POST'])
@login_required
def list_drafts():
    all_drafts = Entry.query.filter_by(is_published=False).order_by(Entry.pub_date.desc())  # noqa: E501
    return render_template("drafts.html", all_drafts=all_drafts)


@app.route("/delete-post/<int:entry_id>", methods=["POST"])
@login_required
def delete_entry(entry_id):
    entry = Entry.query.filter_by(id=entry_id).first_or_404()
    if request.method == 'POST':
        db.session.delete(entry)
        db.session.commit()
        flash('Post został pomyślnie skasowany', 'success')
    return redirect(url_for('homepage'))
