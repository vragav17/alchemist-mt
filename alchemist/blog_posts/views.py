from flask import render_template,url_for,flash, redirect,request,Blueprint
from flask_login import current_user,login_required
from alchemist import db, basedir
from alchemist.models import BlogPost
from github import Github, InputGitTreeElement
from alchemist.blog_posts.forms import BlogPostForm
import datetime
import os, base64

blog_posts = Blueprint('blog_posts',__name__)

@blog_posts.route('/create',methods=['GET','POST'])
@login_required
def create_post():
    form = BlogPostForm()
    user_name_f = current_user.username
    now = datetime.datetime.now()
    now = str(now.strftime("%Y-%m-%d %H_%M_%S"))
    title = form.title.data
    text = form.text.data
    filename = user_name_f+"_"+now+".txt"
    if form.validate_on_submit():

        f = open("data.txt", "w")
        f.write("Now the file has more content! Title = " + title+ "   text =" + text)

        f.close()
        os.rename("data.txt", filename)

        filepath = os.path.join(basedir, filename)
        g = Github("be9d6372f2a0118fa41289460d4bff490c5ac007")
        repo = g.get_repo("vragav17/Onto_Test")
        repo.create_file(filename, title, text,  branch="master")

        os.remove(filename)
        blog_post = BlogPost(title=form.title.data,
                             text=form.text.data,
                             user_id=current_user.id
                             )
        db.session.add(blog_post)
        db.session.commit()
        flash("Blog Post Created")
        return redirect(url_for('core.index'))

    return render_template('create_post.html',form=form)


# int: makes sure that the blog_post_id gets passed as in integer
# instead of a string so we can look it up later.
@blog_posts.route('/<int:blog_post_id>')
def blog_post(blog_post_id):
    # grab the requested blog post by id number or return 404
    blog_post = BlogPost.query.get_or_404(blog_post_id)
    return render_template('blog_post.html',title=blog_post.title,
                            date=blog_post.date,post=blog_post
    )

@blog_posts.route("/<int:blog_post_id>/update", methods=['GET', 'POST'])
@login_required
def update(blog_post_id):
    blog_post = BlogPost.query.get_or_404(blog_post_id)
    if blog_post.author != current_user:
        # Forbidden, No Access
        abort(403)

    form = BlogPostForm()
    if form.validate_on_submit():
        blog_post.title = form.title.data
        blog_post.text = form.text.data
        db.session.commit()
        flash('Post Updated')
        return redirect(url_for('blog_posts.blog_post', blog_post_id=blog_post.id))
    # Pass back the old blog post information so they can start again with
    # the old text and title.
    elif request.method == 'GET':
        form.title.data = blog_post.title
        form.text.data = blog_post.text
    return render_template('create_post.html', title='Update',
                           form=form)


@blog_posts.route("/<int:blog_post_id>/delete", methods=['POST'])
@login_required
def delete_post(blog_post_id):
    blog_post = BlogPost.query.get_or_404(blog_post_id)
    if blog_post.author != current_user:
        abort(403)
    db.session.delete(blog_post)
    db.session.commit()
    flash('Post has been deleted')
    return redirect(url_for('core.index'))
