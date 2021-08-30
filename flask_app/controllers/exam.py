from flask_app import app
from flask import render_template, redirect, session, request, flash

from flask_app.models.users import User
from flask_app.models.painting import Painting 

@app.route('/paintings')
def exam_index():
    if 'user_id' not in session:
        flash("please log in to view this page")
        return redirect('/')
    paintings = Painting.get_all_paintings()

    return render_template('paintings.html', paintings = paintings)


@app.route('/paintings/new')
def new_show():
    return render_template('new_painting.html')



@app.route('/paintings/create', methods=['POST'])
def create_painting():

    if Painting.validate_painting(request.form):
        
        data = {
            'title' : request.form['title'],
            'description' : request.form ['description'],
            'price' : request.form ['price'],
            'users_id': session['user_id']
        }
        Painting.create_painting(data)
        return redirect('/paintings')
 
    return redirect('/paintings/new')


@app.route('/paintings/<int:painting_id>')
def painting_info(painting_id):

    painting = Painting.get_painting_by_id({'id': painting_id})

    return render_template('painting_info.html', painting = painting)



@app.route('/paintings/<int:painting_id>/edit')
def edit_painting(painting_id):

    painting = Painting.get_painting_by_id({'id': painting_id})

    if session['user_id'] != painting.users_id:
        return redirect(f'/paintings/{painting_id}')

    return render_template('edit_painting.html', painting = painting)
    


@app.route('/paintings/<int:painting_id>/update', methods =['POST'])
def update_painting(painting_id):

    if Painting.validate_painting(request.form):
        data = {
            'title': request.form['title'],
            'description': request.form['description'],
            'price': request.form['price'],
            'id' : painting_id
        }
        Painting.update_painting(data)
        return redirect(f'/paintings/{painting_id}')

    return redirect(f'/paintings/{painting_id}/edit')


@app.route('/paintings/<int:painting_id>/delete')
def delete_painting(painting_id):

    Painting.delete_painting({'id': painting_id})


    return redirect('/paintings')



