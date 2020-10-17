from flask import Flask, render_template, request, redirect, url_for, flash
from blog import db, app
from blog.models import Entry
from blog.forms import EntryForm

@app.route("/")
def homepage():
    all_posts = Entry.query.filter_by(is_published=True).order_by(Entry.pub_date.desc())
    return render_template("post_on_homepage.html", all_posts=all_posts)


def post_form(entry_id):
    errors = None
    if entry_id == None:
        form = EntryForm()
        if request.method == "POST":
            if form.validate_on_submit():
                post = Entry(title=form.title.data, body=form.body.data, is_published=form.is_published.data)
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



@app.route("/new-post/", methods=["GET", "POST"])
def create_entry():
    return post_form(entry_id=None)


@app.route("/edit-post/<int:entry_id>", methods=["GET", "POST"])
def edit_entry(entry_id):
    return post_form(entry_id)
