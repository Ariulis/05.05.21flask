from flask import render_template, redirect, url_for, flash
from flask_login import login_required, current_user

from . import main
from .forms import EditAdminProfileForm, EditProfileForm
from .. import db
from ..models import User, Role
from ..decorators import admin_required


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/profile/<username>')
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user=user)


@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user)
        db.session.commit()
        flash('The information has been edited.', 'info')
        return redirect(url_for('main.user', username=current_user.username))
    form.name.data = current_user.name
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', form=form)


@main.route('/edit-profile/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_admin_profile(id):
    user = User.query.get_or_404(id)
    form = EditAdminProfileForm(user=user)
    if form.validate_on_submit():
        user.username = form.username.data
        user.email = form.email.data.lower()
        user.confirmed = form.confirmed.data
        user.role = Role.query.get(form.role.data)
        user.name = form.name.data
        user.location = form.location.data
        user.about_me = form.about_me.data
        db.session.add(user)
        db.session.commit()
        flash('The information has been edited.', 'info')
        return redirect(url_for('main.user', username=user.username))
    form.username.data = user.username
    form.email.data = user.email
    form.confirmed.data = user.confirmed
    form.role.data = user.role_id
    form.name.data = user.name
    form.location.data = user.location
    form.about_me.data = user.about_me
    return render_template('edit_profile.html', form=form)
