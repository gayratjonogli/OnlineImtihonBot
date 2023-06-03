
def language():
    text = """
<b>Assalomu alaykum!</b>
Tilni tanlang: 👇

--------------------

<b>Hello!</b>
Choose language: 👇
    """
    return text


def qoshish_yoriqnomasi_uz():
    text = """
❗️<b>Test qo'shish yo'riqnomasi</b>

Test qo'shish uchun

Fan nomi*to'g'ri javoblar

ko'rinishida yuboring

-----------------------

<b>Misol:</b>
Matematika*1a2a3b4b
<b>yoki</b>
Matematika*abcfed
    """
    return text

def qoshish_yoriqnomasi_en():
    text = """
❗️<b>Instructions for adding a test</b>

To add a test send as

Subject name*correct answers

-----------------------

<b>Example:</b>
Math*1a2a3b4b
<b>or</b>
Math*abcfed
    """
    return text






def after_test_high(username, name, subject, test_code, questionLength, userAnswers, ball, formatted_now):
    text = f"""

👤 Foydalanuvchi: <a href='https://t.me/{username}'>{name}</a>

📕 Fan: <b>{subject}</b>
🎛 Test kodi: <b>{test_code}</b>
🗳 Jami savollar soni: <b>{questionLength}-ta</b>
✅ To'g'ri javoblar soni: <b>{userAnswers}-ta</b>
🔣 Foiz: <b>{ball}</b> %

🕰 Sana va vaqt: {formatted_now}

"""
    return text

def after_test_highPM(username, name, subject, test_code, questionLength, userAnswers, ball, formatted_now, part1, part2):
    text = f"""
👤 Foydalanuvchi: <a href='https://t.me/{username}'>{name}</a>

📕 Fan: <b>{subject}</b>
🎛 Test kodi: <b>{test_code}</b>
🗳 Jami savollar soni: <b>{questionLength}-ta</b>
✅ To'g'ri javoblar soni: <b>{userAnswers}-ta</b>
➡️ Tanqidiy va Muammolida xatolar soni: <b>{part1}</b>
➡️ Ingliz tilidagi xatolar soni: <b>{part2}</b>
📊 Ball: <b>{ball}</b>

🕰 Sana va vaqt: {formatted_now}

----------------------------------

Testlar muhokamasi uchun guruhimiz:
@grand_akademiyasi_chat

"""
    return text


def after_test_lowPM(username, name, subject, test_code, questionLength, userAnswers, ball, formatted_now, part1, part2):
    text = f"""
👤 Foydalanuvchi: <a href='https://t.me/{username}'>{name}</a>

📕 Fan: <b>{subject}</b>
🎛 Test kodi: <b>{test_code}</b>
🗳 Jami savollar soni: <b>{questionLength}-ta</b>
✅ To'g'ri javoblar soni: <b>{userAnswers}-ta</b>
➡️ Tanqidiy va Muammolida xatolar soni: <b>{part1}</b>
➡️ Ingliz tilidagi xatolar soni: <b>{part2}</b>
📊 Ball: <b>{ball}</b>

🕰 Sana va vaqt: {formatted_now}

☝️ <b>Natijangizni yaxshilash uchun testlarimizda doimiy qatnashib boring!</b>
----------------------------------

Testlar muhokamasi uchun guruhimiz:
@grand_akademiyasi_chat

"""
    return text




def bazaga_qoshildi_uz(subject, test_id, user_answers):
    text = f"""

<b>✅Test bazaga qo`shildi.</b>

Fan: <b>{subject if subject else 'Fan nomi mavjud emas'}</b>
Test kodi: <b>{test_id}</b>
Savollar soni: <b>{len(user_answers)} ta</b>

Testda qatnashuvchilar quyidagi ko`rinishda javob yuborishlari mumkin:

{test_id}*abcde... ({len(user_answers)} ta)
<b>yoki</b>
{test_id}*1a2b3c4d... ({len(user_answers)} ta)
    """

    return text


def bazaga_qoshildi_en(subject, test_id, user_answers):
    text = f"""
<b>✅ The test has been added to the database</b>

Subject: <b>{subject if subject else 'Subject not provided'}</b>
Test code: <b>{test_id}</b>
Number of questions: <b>{len(user_answers)}</b>

Test participants can send answers in the following form:

{test_id}*abcde... ({len(user_answers)})
<b>or</b>
{test_id}*1a2b3c4d... ({len(user_answers)})
    """

    return text


def send_to_creator(name, subject, test_id, test_length, errors, username):
    right = test_length - errors
    text = f'''
<a href='https://t.me/{username}'>{name}</a> <b>"{subject}"</b>-fanidan o'z javoblarini yubordi!

🎛 Test kodi: <b>{test_id}</b>
🗳 Jami savollar soni: <b>{test_length}-ta</b>
✅ To'g'ri javoblar soni: <b>{right}-ta</b>
❌ Xatolar soni: <b>{errors}</b>
    
    '''
    return text


def status():
    text = f"""
<b>😔 Afsus!</b>

Test vaqtini tugadi va siz javob yuborishga kechiktingiz!
🕊 Keyingi urinishlarizda sizga omad tilaymiz!
    """
    return text



def after_test_high_en(username, name, subject, test_code, questionLength, userAnswers, ball, formatted_now):
    text = f"""
👤 User: <a href='https://t.me/{username}'>{name}</a>

📕 Subject: <b>{subject}</b>
🎛 Test code: <b>{test_code}</b>
🗳 Total number of questions: <b>{questionLength}</b>
✅ Number of correct answers: <b>{userAnswers}</b>
🔣 Percentage: <b>{ball}</b> %

🕰 Date and time: {formatted_now}

"""
    return text


def send_to_creator_en(name, subject, test_id, test_length, errors, username):
    right = test_length - errors
    text = f'''
<a href='https://t.me/{username}'>{name}</a> sent his answers from subject <b>"{subject}"</b>!

🎛 Test code: <b>{test_id}</b>
🗳 Total number of questions: <b>{test_length}-ta</b>
✅ Number of correct answers: <b>{right}-ta</b>
❌ Number of errors: <b>{errors}</b>
    
    '''
    return text


def test_info_uz(subject, test_id, test_length, participants, datetime):
    text = f"""
📕 Fan: <b>{subject}</b>
🎛 Test kodi: <b>{test_id}</b>
🗳 Jami savollar soni: <b>{test_length}-ta</b>

🧑 Qatnashuvchilar soni: <b>{participants}-ta</b>
🕰 Sana: <b>{datetime}</b>
    """
    return text

def test_info_en(subject, test_id, test_length, participants, datetime):
    text = f"""
📕 Subject: <b>{subject}</b>
🎛 Test code: <b>{test_id}</b>
🗳 Total number of questions: <b>{test_length}</b>

🧑 Number of participants: <b>{participants}</b>
🕰 Date: <b>{datetime}</b>
    """
    return text


def bazaga_qoshildi_uz_pm(subject, test_id, user_answers):
    text = f"""

<b>✅Test bazaga qo`shildi.</b>

Fan: <b>{subject if subject else 'Fan nomi mavjud emas'}</b>
Test kodi: <b>{test_id}</b>
Savollar soni: <b>{len(user_answers)} ta</b>

Testda qatnashuvchilar quyidagi ko`rinishda javob yuborishlari mumkin:

{test_id}*abcd...+...ccbb ({len(user_answers)} ta)
<b>yoki</b>
{test_id}*1a2b...39a40d+41c42a...79a80b ({len(user_answers)} ta)
    """

    return text




def bazaga_qoshildi_en_pm(subject, test_id, user_answers):
    text = f"""
<b>✅ The test has been added to the database</b>

Subject: <b>{subject if subject else 'Subject not provided'}</b>
Test code: <b>{test_id}</b>
Number of questions: <b>{len(user_answers)}</b>

Test participants can send answers in the following form:

{test_id}*abcd...+...ccbb ({len(user_answers)})
<b>or</b>
{test_id}*1a2b...39a40d+41c42a...79a80b ({len(user_answers)})
    """

    return text


def bazaga_qoshildi_uz_a(subject, test_id, user_answers):
    text = f"""

<b>✅Test bazaga qo`shildi.</b>

Fan: <b>{subject if subject else 'Fan nomi mavjud emas'}</b>
Test kodi: <b>{test_id}</b>
Savollar soni: <b>{len(user_answers)} ta</b>

Testda qatnashuvchilar quyidagi ko`rinishda javob yuborishlari mumkin:

{test_id}*aabb...+...ccdd...+......ccdaa ({len(user_answers)} ta)
<b>yoki</b>
{test_id}*1a2b3c...29a30b+31c32d...59c60a+61c62a...89d90a ({len(user_answers)} ta)
    """

    return text




def bazaga_qoshildi_en_a(subject, test_id, user_answers):
    text = f"""
<b>✅ The test has been added to the database</b>

Subject: <b>{subject if subject else 'Subject not provided'}</b>
Test code: <b>{test_id}</b>
Number of questions: <b>{len(user_answers)}</b>

Test participants can send answers in the following form:

{test_id}*aabb...+...ccdd...+......ccdaa ({len(user_answers)})
<b>or</b>
{test_id}*1a2b3c...29a30b+31c32d...59c60a+61c62a...89d90a ({len(user_answers)})
    """

    return text



def show_infor_uz(name):
    text = f"""
📋 <b>Sizning ma'lumotlaringiz:</b>

Ismingiz: <b>{name}</b>


⚠️ Diqqat!
<i>Agar ma'lumotlaringizni o'zgartirmoqchi bo'lsangiz, 
quyidagi o'zgartirmoqchi bo'lgan tugmalardan birini bosing</i>👇

"""
    return text




def show_infor_updated_uz(name):
    text = f"""
✅ O'zgartirildi!!!

📋 <b>Sizning ma'lumotlaringiz:</b>

Ismingiz: <b>{name}</b>


⚠️ Diqqat!
<i>Agar ma'lumotlaringizni o'zgartirmoqchi bo'lsangiz, 
quyidagi o'zgartirmoqchi bo'lgan tugmalardan birini bosing</i>👇

"""
    return text


def show_infor_en(name):
    text = f"""
📋 <b>Your information:</b>

Your name: <b>{name}</b>


⚠️ Attention!
<i>If you want to change your information,
Click on one of the buttons below that you want to change</i>👇

"""
    return text

def show_infor_updated_en(name):
    text = f"""
✅ Changed!!!

📋 <b>Your information:</b>

Your name: <b>{name}</b>


⚠️ Attention!
<i>If you want to change your information,
Click on one of the buttons below that you want to change</i>👇

"""
    return text