import os
import re
import requests
import json
from flask_login import login_required, current_user
from flask import Blueprint, render_template, redirect, url_for, request, flash
from . import db
import urllib.parse

main = Blueprint('main', __name__)
telegram_bot_token = "5878473281:AAGAmMo2fxvXW-LimNIXDaUOXB9u5txBhyo"
telegram_channel = 'kyivlime_test'

@main.route('/')
@login_required
def index():
	return render_template('index.html', name=current_user.name)

@main.route('/admins')
@login_required
def admins():
	return render_template('admins.html', name=current_user.name, admins=infoAdminsPriv(telegram_channel), len=len(infoAdminsPriv(telegram_channel)))

@main.route('/info')
@login_required
def info():
	return render_template('info.html', name=current_user.name, info=infoChannel(telegram_channel))

@main.route('/c/alert-start')
@login_required
def alertStart():
	text = "#повітрянатривога #оголошення \n 〰️〰️〰️ \n [💌 Підписатись](https://t.me/kyivlime) | [💬 Чат](https://t.me/kyivlimechat) \n [✏️ Запропонувати новину](https://t.me/kyivlimebot)"
	sendImage(telegram_channel, 'as.jpg', text, 'md1')
	flash('Успішно відправлено!', 'success')
	return redirect(url_for('main.index'))

@main.route('/c/alert-end')
@login_required
def alertEnd():
	text = "#повітрянатривога #відбій \n 〰️〰️〰️ \n [💌 Підписатись](https://t.me/kyivlime) | [💬 Чат](https://t.me/kyivlimechat) \n [✏️ Запропонувати новину](https://t.me/kyivlimebot)"
	sendImage(telegram_channel, 'ae.jpg', text, 'md1')
	flash('Успішно відправлено!', 'success')
	return redirect(url_for('main.index'))

@main.route('/c/mos')
@login_required
def mos():
	text = "#хвилинамовчання \n 〰️〰️〰️ \n [💌 Підписатись](https://t.me/kyivlime) | [💬 Чат](https://t.me/kyivlimechat) \n [✏️ Запропонувати новину](https://t.me/kyivlimebot)"
	sendImage(telegram_channel, 'mos.jpg', text, 'md1')
	flash('Успішно відправлено!', 'success')
	return redirect(url_for('main.index'))

@main.route('/c/pt-start')
@login_required
def ptStart():
	text = "#комендантськагодина #початок \n 〰️〰️〰️ \n [💌 Підписатись](https://t.me/kyivlime) | [💬 Чат](https://t.me/kyivlimechat) \n [✏️ Запропонувати новину](https://t.me/kyivlimebot)"
	sendImage(telegram_channel, 'pts.jpg', text, 'md1')
	flash('Успішно відправлено!', 'success')
	return redirect(url_for('main.index'))

@main.route('/c/pt-end')
@login_required
def ptEnd():
	text = "#комендантськагодина #кінець \n 〰️〰️〰️ \n [💌 Підписатись](https://t.me/kyivlime) | [💬 Чат](https://t.me/kyivlimechat) \n [✏️ Запропонувати новину](https://t.me/kyivlimebot)"
	sendImage(telegram_channel, 'pte.jpg', text, 'md1')
	flash('Успішно відправлено!', 'success')
	return redirect(url_for('main.index'))

@main.route('/c/ppo-area')
@login_required
def ppoArea():
	text = "⚠️ *Увага!* Місто Київ! ЗМІ повідомляють про вибухи. \n Будьте обережні!"
	sendText(telegram_channel, text, 'md1')
	flash('Успішно відправлено!', 'success')
	return redirect(url_for('main.index'))

@main.route('/c/ppo-city')
@login_required
def ppoCity():
	text = "⚠️ *Увага!* Київська область! ЗМІ повідомляють про вибухи. \n Будьте обережні!"
	sendText(telegram_channel, text, 'md1')
	flash('Успішно відправлено!', 'success')
	return redirect(url_for('main.index'))

def sendText(chat_id, text, syntax) -> bool:
	parse = ''
	if syntax=='md': parse = '&parse_mode=MarkdownV2'
	elif syntax=='md1': parse = '&parse_mode=Markdown'
	elif syntax=='h': parse = '&parse_mode=HTML'

	params = {
		'chat_id': '@' + chat_id,
		'text': text,
		'disable_web_page_preview': 'true'
	}

	response = requests.get('https://api.telegram.org/bot' + telegram_bot_token + '/sendMessage?' + urllib.parse.urlencode(params) + parse)
	return True

def sendImage(chat_id, photo, text, syntax) -> bool:
	parse = ''
	if syntax=='md': parse = '&parse_mode=MarkdownV2'
	elif syntax=='md1': parse = '&parse_mode=Markdown'
	elif syntax=='h': parse = '&parse_mode=HTML'

	params = {
		'chat_id': '@' + chat_id,
		'photo': 'https://goralex97.pythonanywhere.com/static/img/' + photo,
		'caption': text
	}

	response = requests.get('https://api.telegram.org/bot' + telegram_bot_token + '/sendPhoto?' + urllib.parse.urlencode(params) + parse)
	return True

def infoChannel(chat_id):
	params = {
		# 'chat_id': '@' + chat_id
		'chat_id': '@kyivlime'
	}

	response = requests.get('https://api.telegram.org/bot' + telegram_bot_token + '/getChat?' + urllib.parse.urlencode(params))
	return response.json()['result']

def infoAdminsPriv(chat_id):
	params = {
		# 'chat_id': '@' + chat_id
		'chat_id': '@kyivlime'
	}

	response = requests.get('https://api.telegram.org/bot' + telegram_bot_token + '/getChatAdministrators?' + urllib.parse.urlencode(params))
	users = response.json()['result']
	return users


# /getChat?chat_id=@kyivlime
# /getChatAdministrators?chat_id=@kyivlime
# /getChatMemberCount?chat_id=@kyivlime
# /getUserProfilePhotos?&user_id=&limit=1
# /getFile?file_id=
