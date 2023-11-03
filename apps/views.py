from flask import Blueprint, flash, request, redirect, url_for, render_template
from flask_login import login_required, current_user
import os

from . import db
from .models_db import RoadData
from apps.libserver import provinces_data, get_province_name
from apps import app
from apps.libserver.lib import get_available_cameras_linux, get_available_cameras_windows, check_os
from apps.libserver.query_lib import road_datas, get_unique_province, get_sort_road_data, get_all_damage



views = Blueprint('views', __name__)

@views.route('/')
@login_required
def index():
    return render_template('home/dashboard.html', 
                           segment='index', 
                           user_id=current_user.id)

@views.route('/report', methods=['GET', 'POST'])
@login_required
def report():
    user_id = current_user.id
    data = road_datas(user_id)

    pathole_sum, crocodile_sum, longitudinal_sum, transversal_sum = get_all_damage(user_id)

    unique_province = get_unique_province(user_id)

    if request.method == 'POST':
        id_data = request.form.get('id_data')
        check_id = RoadData.query.get(id_data)

        if check_id is not None:
            file_path = os.path.join(app.config['DETECT_FOLDER'], check_id.video_path)
            if os.path.exists(file_path):
                os.remove(file_path)
                
            for child_data in check_id.children:
                db.session.delete(child_data)
            
            db.session.delete(check_id)
            db.session.commit()

            return redirect(url_for('views.report'))
        else:
            flash('ID not found', 'danger')


    return render_template('home/report.html', 
                           segment='report',
                           road_datas=data,
                           pathole_sum=pathole_sum,
                           crocodile_sum=crocodile_sum,
                           data_label=None,
                           unique_provinces=unique_province,
                           longitudinal_sum=longitudinal_sum,
                           transversal_sum=transversal_sum,
                           labels=None, 
                           pathole_data=None, 
                           crocodile_data=None, 
                           longitudinal_data=None, 
                           transversal_data=None,
                           get_province_name=get_province_name,
                           user_id=current_user.id)


@views.route('/about')
@login_required
def about():
    return render_template('home/about.html', 
                           segment='about',
                           user_id=current_user.id)

@views.route('/detect')
@login_required
def detect():
    check = check_os()
    if check == 'Linux':
        available_cameras = get_available_cameras_linux()
    elif check == 'Windows':
        available_cameras = get_available_cameras_windows()
    return render_template('home/detect.html', 
                           segment='index',
                           port_camera=available_cameras,
                           provinces=provinces_data,
                           user_id=current_user.id)


