import flask
from flask import jsonify, request
from data import db_session
from .users import User

blueprint = flask.Blueprint(
    'bot_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/bot/register', methods=['POST'])
def register():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['name', 'score', 'chat_id', 'lvl_click']):
        return jsonify({'error': 'Bad request'})
    db_sess = db_session.create_session()
    bd = db_sess.query(User).filter(User.chat_id == request.json['chat_id']).first()
    if bd:
        return jsonify({'message': f"Шучу, я знаю, что тебя зовут, {bd.name}"})
    else:
        user_bd = User(name=request.json['name'], score=request.json['score'], chat_id=request.json['chat_id'],
                       lvl_click=request.json['lvl_click'])
        db_sess.add(user_bd)
        db_sess.commit()
        return jsonify({'message': f"Хорошо, буду звать тебя: {user_bd.name}"})


@blueprint.route('/api/bot/game_info/<int:chat_id>', methods=['GET'])
def get_lvl_click(chat_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.chat_id == chat_id).first()
    if not user:
        return jsonify({'error': 'User not found'})
    return jsonify({'message': user.lvl_click})


@blueprint.route('/api/bot/game/<int:chat_id>', methods=['GET'])
def game(chat_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.chat_id == chat_id).first()
    if not user:
        return jsonify({'error': 'User not found'})
    user.score += user.lvl_click
    db_sess.commit()
    return jsonify({'message': f"Твой счет: {user.score}"})


@blueprint.route('/api/bot/user_info/<int:chat_id>', methods=['GET'])
def user_info(chat_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.chat_id == chat_id).first()
    if not user:
        return jsonify({'error': 'User not found'})
    return jsonify(
        {'message': f"Твое имя : {user.name} \nТвой счет: {user.score} \nТвой прирост за клик: {user.lvl_click}"})


@blueprint.route('/api/bot/top', methods=['GET'])
def top():
    db_sess = db_session.create_session()
    user = db_sess.query(User.score, User.name)
    dic = {}
    top = 'Топ лучших \n'
    for i in user:
        dic[i.name] = i.score
    list_keys = list(dic.keys())
    list_keys.sort()
    for i in list_keys[::-1]:
        top += f"{i} : {dic[i]} \n"
    return jsonify({'message': f"{top}"})


@blueprint.route('/api/bot/upgrade', methods=['POST'])
def upgrade():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['ans_user', 'chat_id']):
        return jsonify({'error': 'Bad request'})
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.chat_id == request.json['chat_id']).first()
    if request.json['ans_user'] == '+2 за клик - 200' and user.score >= 200:
        user.lvl_click += 2
        user.score -= 200
        db_sess.commit()
        return jsonify({'message': f"На твоем счету осталось: {user.score}"})
    elif request.json['ans_user'] == '+3 за клик - 400' and user.score >= 400:
        user.lvl_click += 3
        user.score -= 400
        db_sess.commit()
        return jsonify(
            {'message': f"На твоем счету осталось: {user.score}"})
    elif request.json['ans_user'] == '+4 за клик - 600' and user.score >= 600:
        user.lvl_click += 4
        user.score -= 600
        db_sess.commit()
        return jsonify(
            {'message': f"На твоем счету осталось: {user.score}"})
    elif request.json['ans_user'] == '+5 за клик - 800' and user.score >= 800:
        user.lvl_click += 5
        user.score -= 800
        db_sess.commit()
        return jsonify(
            {'message': f"На твоем счету осталось: {user.score}"})
    return jsonify(
        {'message': "На твоем счету недостаточно кликов"})