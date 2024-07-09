from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from bson.objectid import ObjectId  # For handling ObjectIds in MongoDB
from .mongo import users_collection, messages_collection
from datetime import datetime

message = Blueprint('message', __name__)

@message.route('/message/<string:user_id>', methods=['GET', 'POST'])
@login_required
def message_user(user_id):
    other_user = users_collection.find_one({'_id': ObjectId(user_id)})

    if not other_user:
        flash("User not found.", "error")
        return redirect(url_for('views.index'))

    if request.method == 'POST':
        message_content = request.form.get('message_content')

        if message_content:
            message = {
                'sender_id': str(current_user._id),  # Assuming current_user has an ObjectId
                'receiver_id': user_id,
                'content': message_content,
                'timestamp': datetime.utcnow()
            }
            messages_collection.insert_one(message)
            flash('Message sent successfully!', 'success')
            return redirect(url_for('message.message_user', user_id=user_id))
        else:
            flash('Message content cannot be empty.', 'error')

    # Fetch messages between current_user and other_user
    messages = list(messages_collection.find({
        '$or': [
            {'sender_id': str(current_user._id), 'receiver_id': user_id},
            {'sender_id': user_id, 'receiver_id': str(current_user._id)}
        ]
    }).sort('timestamp', 1))

    return render_template('message.html', messages=messages, other_user=other_user)

@message.route('/messages', methods=['GET'])
@login_required
def messages():
    # Query to find all unique users that current_user has messaged with, sorted by recent message
    users = users_collection.aggregate([
        {'$lookup': {
            'from': 'messages',
            'let': {'user_id': '$_id'},
            'pipeline': [
                {'$match': {
                    '$expr': {
                        '$or': [
                            {'$eq': ['$sender_id', '$$user_id']},
                            {'$eq': ['$receiver_id', '$$user_id']}
                        ]
                    }
                }},
                {'$sort': {'timestamp': -1}},
                {'$limit': 1}
            ],
            'as': 'latest_message'
        }},
        {'$match': {'latest_message': {'$ne': []}}},  # Filter out users without any messages
        {'$project': {
            'full_name': 1,
            'email': 1,
            'latest_message': {'$arrayElemAt': ['$latest_message', 0]}
        }},
        {'$sort': {'latest_message.timestamp': -1}}
    ])

    return render_template('messagelist.html', users=users)
