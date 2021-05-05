from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user, login_required, login_user, logout_user

from . import auth
from .forms import LoginForm, RegistrationForm, ResetPasswordForm, ResetPasswordRequestForm, ChangePasswordForm, ChangeEmailForm
from .. import db, logger
from ..models import User
from ..email import send_email


@auth.route('/login', methods=['GET', 'POST'])
@logger.catch
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(url_for('main.index'))
        flash('Invalid email or password.', 'warning')
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
@logger.catch
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.index'))


@auth.route('/register', methods=['GET', 'POST'])
@logger.catch
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        new_user = User(
            username=form.username.data,
            email=form.email.data.lower(),
            password=form.password.data,
        )
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user, remember=True)

        token = new_user.generate_confirmation_token()

        send_email(
            new_user.email,
            'Confirm your account',
            'auth/email/confirm',
            user=new_user,
            token=token
        )

        flash('Confirmation email has been sent to you by email.', 'info')
        return redirect(url_for('auth.unconfirmed'))
    return render_template('auth/register.html', form=form)


@auth.route('/unconfirmed')
@login_required
@logger.catch
def unconfirmed():
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html')


@auth.route('/confirm')
@login_required
@logger.catch
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email(
        current_user.email,
        'Confirm your account',
        'auth/email/confirm',
        user=current_user,
        token=token
    )
    flash('A new confirmation email has been sent to you.', 'info')
    return redirect(url_for('auth.unconfirmed'))


@auth.route('/confirm/<token>')
@login_required
@logger.catch
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        db.session.commit()
        flash('You have confirmed your account. Thanks!', 'success')
        return redirect(url_for('main.index'))
    flash('A confirmation link is invalid or has expired.', 'warning')
    return redirect(url_for('auth.unconfirmed'))


@auth.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.ping()
        if not current_user.confirmed and request.endpoint and request.blueprint != 'auth' and request.endpoint != 'static':
            return redirect(url_for('auth.unconfirmed'))


@auth.route('/reset', methods=['GET', 'POST'])
def reset_password_request():
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(
            email=form.email.data.lower()).first_or_404()
        token = user.generate_reset_password_token()
        send_email(
            user.email,
            'Reset password',
            'auth/email/reset_password',
            user=user,
            token=token
        )
        flash('An email with instructions to reset email has been sent to you.', 'info')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', form=form)


@auth.route('/reset/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        if User.reset_password(token, form.password.data):
            db.session.commit()
            flash('Your password has been changed.', 'success')
            return redirect(url_for('auth.login'))
        flash('Invalid request.', 'warning')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', form=form)


@auth.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.password.data):
            current_user.password = form.new_password.data
            db.session.add(current_user)
            db.session.commit()
            flash('Your password has been changed.', 'success')
            return redirect(url_for('main.index'))
        flash('Invalid password.', 'warning')
    return render_template('auth/change_password.html', form=form)


@auth.route('/change-email', methods=['GET', 'POST'])
@login_required
def change_email_request():
    form = ChangeEmailForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.password.data):
            new_email = form.email.data.lower()
            token = current_user.generate_change_email_token(new_email)
            send_email(
                new_email,
                'Change email',
                'auth/email/change_email',
                user=current_user,
                token=token
            )
            flash(
                'An email with instructions to change email has been sent to you.', 'info')
            return redirect(url_for('main.index'))
        flash('Incorrect password.', 'warning')
    return render_template('auth/change_email.html', form=form)


@auth.route('/change-email/<token>')
@login_required
def change_email(token):
    if current_user.change_email(token):
        db.session.commit()
        flash('Your email has been changed.', 'success')
    else:
        flash('Invalid request.', 'danger')
    return redirect(url_for('main.index'))
