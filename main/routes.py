import secrets
from tokenize import Triple
from flask import url_for, redirect
from main import app, db, bcrypt
from .models import ShoppingList, User, ShoppingListItem
from .forms import LoginForm, RegistrationForm, UpdateAccountForm, AddListForm, AddListItemForm, UpdateListForm
from flask_login import login_user, logout_user, login_required, current_user
from flask import render_template, url_for, request, redirect, flash

#################################
#                               #
#           Site Stuff          #
#                               #
#################################

@app.route("/")
def index():
    return render_template(
        'index.html',
        title='Home'
    )

# when '/home' or '/index' are typed in the URL or redirected, it will the redirect to the url without anything after the /
@app.route("/index")
@app.route("/home")
def home_redirect():
    return redirect(url_for('index'))


# Reference: https://flask.palletsprojects.com/en/1.1.x/patterns/errorpages/
@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html', title='Page Not Found'), 404


#################################
#                               #
#           User Stuff          #
#                               #
#################################

@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        db.session.commit()
        flash('Your account was updated')

        return redirect(url_for('account'))

    elif request.method == 'GET':
        form.username.data = current_user.username
        
    return render_template(
        'user/account.html',
        title = 'Account',
        form = form
    )

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            id = secrets.token_hex(10),
            username = form.username.data,
            email = form.email.data,
            password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        )

        db.session.add(user)
        db.session.commit()
        flash('Account Created - You can now Login in')
        return redirect(url_for('login'))
    return render_template(
        'user/register.html',
        title = 'Register',
        form = form
    )


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('all_shopping_lists'))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            else:
                return redirect(url_for("index"))
        else:
            flash('Login Unsuccessful. Check Username and Password')
    
    return render_template(
        'user/login.html',
        title = 'Login',
        form = form
    )

@app.route("/logout")
def logout():
    logout_user()
    return redirect(request.referrer)

def permission_check_false(shopping_list):
    if current_user.id == shopping_list.user.id: return False
    flash('You do not have permission to access that!')
    return True

#################################
#                               #
#           List Stuff          #
#                               #
#################################
@app.route("/shopping-list", methods=['GET', 'POST'])
@login_required
def all_shopping_lists():

    users_s_lists = ShoppingList.query.filter_by(user_id=current_user.id).all()

    form = AddListForm()
    if form.validate_on_submit():
        s_list = ShoppingList(
            id = secrets.token_hex(10),
            name = form.name.data,
            user_id = current_user.id
        )

        db.session.add(s_list)
        db.session.commit()
        flash(f'{form.name.data} was created')

        return redirect(url_for('all_shopping_lists'))
    
    return render_template(
        'shopping_list/home.html',
        title = f'Shopping Lists',
        users_shopping_lists = users_s_lists,
        form = form
    )

@app.route("/shopping-list/<string:shopping_list_id>", methods=['GET', 'POST'])
@login_required
def shopping_list(shopping_list_id):
    shopping_list = ShoppingList.query.get_or_404(shopping_list_id)
    
    if permission_check_false(shopping_list): return redirect(url_for('index'))

    list_items = ShoppingListItem.query.filter_by(shopping_list_id=shopping_list_id, in_trolley=False).all()
    list_items_trolley = ShoppingListItem.query.filter_by(shopping_list_id=shopping_list_id, in_trolley=True).all()


    form = AddListItemForm()
    if request.method == 'GET':
        form.quantity.data = 1
    if form.validate_on_submit():
        s_list_item = ShoppingListItem(
            id = secrets.token_hex(10),
            name = form.name.data,
            quantity = form.quantity.data,
            shopping_list_id = shopping_list_id
        )

        shopping_list.item_count += 1

        db.session.add(s_list_item)
        db.session.commit()
        if int(form.quantity.data) > 1:
            flash(f'{form.quantity.data} {form.name.data}s were added to Shopping List')
        else:
            flash(f'1 {form.name.data} was added to your Shopping List')

        return redirect(url_for('shopping_list', shopping_list_id=shopping_list_id))

    list_form = UpdateListForm()
    if request.method == 'GET':
        list_form.list_name.data = shopping_list.name

    if list_form.validate_on_submit():
        if shopping_list.name != list_form.list_name.data: 
            shopping_list.name = list_form.list_name.data
            db.session.commit()
        return redirect(url_for('shopping_list', shopping_list_id=shopping_list_id))
    
    return render_template(
        'shopping_list/list_item.html',
        form = form,
        list_form = list_form,
        title = f'Shopping List - {shopping_list.name}',
        shopping_list = shopping_list,
        list_items = list_items,
        list_items_trolley = list_items_trolley
    )

@app.route("/shopping-list/<string:shopping_list_id>/<string:list_item_id>", methods=['GET', 'POST'])
@login_required
def edit_list_item(shopping_list_id, list_item_id):
    shopping_list = ShoppingList.query.get_or_404(shopping_list_id)
    list_item = ShoppingListItem.query.get_or_404(list_item_id)

    if permission_check_false(shopping_list): return redirect(url_for('index'))

    form = AddListItemForm()
    if request.method == 'GET':
        form.name.data = list_item.name
        form.quantity.data = list_item.quantity

    if form.validate_on_submit():
        list_item.name = form.name.data
        list_item.quantity = form.quantity.data

        db.session.commit()
        flash('Item was updated')
        return redirect(url_for('shopping_list', shopping_list_id=shopping_list_id))
    
    return render_template(
        'shopping_list/list_item_edit.html',
        form = form,
        title = f'Shopping List - {shopping_list.name}',
        item = list_item,
        shopping_list=shopping_list
    )

@app.route("/shopping-list/delete/<string:shopping_list_id>/<string:list_item_id>", methods=['GET', 'POST'])
@login_required
def delete_list_item(shopping_list_id, list_item_id):
    shopping_list = ShoppingList.query.get_or_404(shopping_list_id)
    list_item = ShoppingListItem.query.get_or_404(list_item_id)

    if permission_check_false(shopping_list): return redirect(url_for('index'))

    shopping_list.item_count -= 1

    db.session.delete(list_item)
    db.session.commit()

    flash('Item was removed from your Shopping List')

    return redirect(url_for('shopping_list', shopping_list_id=shopping_list_id))
    
    

@app.route("/shopping-list/delete/<string:shopping_list_id>", methods=['GET', 'POST'])
@login_required
def delete_list(shopping_list_id):
    shopping_list = ShoppingList.query.get_or_404(shopping_list_id)
    temp_name = shopping_list.name

    if permission_check_false(shopping_list): return redirect(url_for('index'))
    
    list_item = ShoppingListItem.query.filter_by(shopping_list_id=shopping_list_id).all()

    for item in list_item:
        db.session.delete(item)

    db.session.delete(shopping_list)
    db.session.commit()
    
    flash(f'Your \'{temp_name}\' Shopping List was removed along with all it\'s items')

    return redirect(url_for('all_shopping_lists'))


@app.route("/shopping-list/trolley-add/<string:shopping_list_id>/<string:list_item_id>", methods=['GET', 'POST'])
@login_required
def add_item_to_trolley(shopping_list_id, list_item_id):
    shopping_list = ShoppingList.query.get_or_404(shopping_list_id)

    if permission_check_false(shopping_list): return redirect(url_for('index'))
    
    list_item = ShoppingListItem.query.get_or_404(list_item_id)

    list_item.in_trolley = True
    db.session.commit()
    
    flash(f'{list_item.name} added to Trolley')

    return redirect(url_for('shopping_list', shopping_list_id=shopping_list_id))

@app.route("/shopping-list/trolley-remove/<string:shopping_list_id>/<string:list_item_id>", methods=['GET', 'POST'])
@login_required
def remove_item_from_trolley(shopping_list_id, list_item_id):
    shopping_list = ShoppingList.query.get_or_404(shopping_list_id)

    if permission_check_false(shopping_list): return redirect(url_for('index'))
    
    list_item = ShoppingListItem.query.get_or_404(list_item_id)

    list_item.in_trolley = False
    db.session.commit()
    
    flash(f'{list_item.name} removed from Trolley')

    return redirect(url_for('shopping_list', shopping_list_id=shopping_list_id))

@app.route("/shopping-list/trolley-remove-all/<string:shopping_list_id>", methods=['GET', 'POST'])
@login_required
def remove_all_items_from_trolley(shopping_list_id):
    shopping_list = ShoppingList.query.get_or_404(shopping_list_id)

    if permission_check_false(shopping_list): return redirect(url_for('index'))
    
    list_item = ShoppingListItem.query.filter_by(shopping_list_id=shopping_list_id).all()

    for item in list_item:
        item.in_trolley = False
    db.session.commit()
    
    flash('All items removed from Trolley')

    return redirect(url_for('shopping_list', shopping_list_id=shopping_list_id))