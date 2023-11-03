from . import db, get_province_name, RoadDamage, RoadData, Users
from flask_login import current_user
from sqlalchemy.sql import func, null, case, desc, asc
from sqlalchemy import distinct

def single_road_data(road_id, user_id):
    data = db.session.query(
        RoadData.id,
        RoadData.created_at,
        RoadData.province,
        RoadData.city,
        RoadData.street_name,
        RoadData.video_path,
        func.sum(
            case((RoadDamage.type_damage == 'pathole', RoadDamage.sum_damage),
                else_=0),
        ).label("pathole"),
        func.sum(
            case((RoadDamage.type_damage == 'crocodile', RoadDamage.sum_damage),
                else_=0),
        ).label("crocodile"),
        func.sum(
            case((RoadDamage.type_damage == 'longitudinal', RoadDamage.sum_damage),
                else_=0),
        ).label("longitudinal"),
        func.sum(
            case((RoadDamage.type_damage == 'transversal', RoadDamage.sum_damage),
                else_=0),
        ).label("transversal"),
    ).join(RoadDamage, RoadData.id == RoadDamage.road_data_id
    ).filter(
        RoadData.user_id == user_id,
        RoadData.id == road_id  
    ).group_by(
        RoadData.id,
        RoadData.created_at,
        RoadData.province,
        RoadData.city,
        RoadData.street_name
    ).first()

    return data

def road_datas(id_user):
    data = db.session.query(
        RoadData.id,
        RoadData.created_at,
        RoadData.province,
        RoadData.city,
        RoadData.street_name,
        func.sum(
            case((RoadDamage.type_damage == 'pathole', RoadDamage.sum_damage),
                 else_=0),
        ).label("pathole"),
        func.sum(
            case((RoadDamage.type_damage == 'crocodile', RoadDamage.sum_damage),
                 else_=0),
        ).label("crocodile"),
        func.sum(
            case((RoadDamage.type_damage == 'longitudinal', RoadDamage.sum_damage),
                 else_=0),
        ).label("longitudinal"),
        func.sum(
            case((RoadDamage.type_damage == 'transversal', RoadDamage.sum_damage),
                 else_=0),
        ).label("transversal"),
    ).join(RoadDamage, RoadData.id == RoadDamage.road_data_id
    ).filter(RoadData.user_id==id_user
    ).group_by(
        RoadData.id,
        RoadData.created_at,
        RoadData.province,
        RoadData.city,
        RoadData.street_name
    ).all()

    return data

def get_sort_road_data(choice="desc", user_id=1):
    if choice == "asc":
        sort = asc('total_damage')
    else:
        sort = desc('total_damage')

    data = db.session.query(
        RoadData.province,
        func.sum(RoadDamage.sum_damage).label('total_damage'),
        func.sum(
            case((RoadDamage.type_damage == 'pathole', RoadDamage.sum_damage),
                 else_=0),
        ).label("pathole"),
        func.sum(
            case((RoadDamage.type_damage == 'crocodile', RoadDamage.sum_damage),
                 else_=0),
        ).label("crocodile"),
        func.sum(
            case((RoadDamage.type_damage == 'longitudinal', RoadDamage.sum_damage),
                 else_=0),
        ).label("longitudinal"),
        func.sum(
            case((RoadDamage.type_damage == 'transversal', RoadDamage.sum_damage),
                 else_=0),
        ).label("transversal"),
    ).join(RoadDamage, RoadData.id == RoadDamage.road_data_id
    ).filter(RoadData.user_id==user_id
    ).group_by(
        RoadData.province,
    ).order_by(sort).limit(4).all()

    labels = [get_province_name(row.province) for row in data]
    pathole_data = [row.pathole for row in data]
    crocodile_data = [row.crocodile for row in data]
    longitudinal_data = [row.longitudinal for row in data]
    transversal_data = [row.transversal for row in data]

    return labels, pathole_data, crocodile_data, longitudinal_data, transversal_data

def get_all_damage(user_id):
    subquery = (
        db.session.query(
            RoadDamage.type_damage,
            func.sum(RoadDamage.sum_damage).label('sum_damage')
        )
        .join(RoadData, RoadData.id == RoadDamage.road_data_id)
        .filter(RoadData.user_id == user_id)
        .group_by(RoadDamage.type_damage)
        .subquery()
    )

    # Dapatkan jumlah kerusakan untuk setiap tipe
    pathole_sum = db.session.query(subquery.c.sum_damage).filter(subquery.c.type_damage == 'pathole').scalar()
    crocodile_sum = db.session.query(subquery.c.sum_damage).filter(subquery.c.type_damage == 'crocodile').scalar()
    longitudinal_sum = db.session.query(subquery.c.sum_damage).filter(subquery.c.type_damage == 'longitudinal').scalar()
    transversal_sum = db.session.query(subquery.c.sum_damage).filter(subquery.c.type_damage == 'transversal').scalar()

    return pathole_sum, crocodile_sum, longitudinal_sum, transversal_sum

def get_all_damage_province(selected_province):
    data_graph = (
        db.session.query(
            RoadDamage.type_damage,
            func.sum(RoadDamage.sum_damage).label('total_damage')
        )
        .join(RoadData, RoadData.id == RoadDamage.road_data_id)
        .filter(RoadData.province == selected_province)
        .group_by(RoadDamage.type_damage)
        .all()
    )

    data_label = [row.total_damage for row in data_graph]
    return data_label


def get_unique_province(user_id):
    data = db.session.query(distinct(RoadData.province)).filter(RoadData.user_id==user_id).all()

    return data

