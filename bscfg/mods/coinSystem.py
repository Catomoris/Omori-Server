import bs
import bsInternal
from random import randrange
correctAnswer = None
answeredBy = None

settings = {
    'enableCoinSystem': True,
    'questionDelay': 100,
}
questionsList = {
    'add':None,
    'multiply':None,
}




def askQuestion():
    global answeredBy
    global correctAnswer
    keys = []
    for x in questionsList:
        keys.append(x)

    question = keys[randrange(len(keys))]
    correctAnswer = questionsList[question]
    if question == 'add':
        a = randrange(100, 999)
        b = randrange(10, 99)
        correctAnswer = str(a + b)
        question = 'What is ' + str(a) + ' + ' + str(b) + '?'
    elif question == 'multiply':
        a = randrange(100, 999)
        availableB = [0, 1, 10, 5]
        b = availableB[randrange(4)]
        correctAnswer = str(a * b)
        question = 'What is ' + str(a) + ' x ' + str(b) + '?'
    bsInternal._chatMessage(question)
    answeredBy = None
    return


def checkAnswer(msg, clientID):
    global answeredBy
    if True:#msg.lower() == correctAnswer:
        if answeredBy is not None:
            bs.screenMessage(u'Already awarded to ' + answeredBy)
        else:
            for i in bsInternal._getForegroundHostActivity().players:
                if i.getInputDevice().getClientID() == clientID:
                    answeredBy = i.getName()
                    accountID = i.get_account_id()
            bs.screenMessage(
                u'%s : %s' % (answeredBy, msg),
                color = (0,0.6,0.2),
                clients=[clientID],
                transient=True)
            try:
                bs.screenMessage(
                    u'Congratulations ' + answeredBy + '! You won ' + bs.getSpecialChar('ticket') + '10.',
                    color=(0, 0.6, 0.2),
                    clients=[clientID],
                    transient=True)
                addCoins(accountID, 10)
            except:
                pass

    '''else:
        bs.screenMessage('Wrong', color=(1, 0, 0), transient=True, clients=[clientID])'''
    return

def addCoins(accountID, amount):
    import DB_Manager as db
    # obten lo datos del jugador
    coins = db.getData(accountID)
    # sumamos el monto a su cuenta
    coins['p'] += amount
    # luego lo guardamos <:
    db.saveData(accountID, coins)



if settings['enableCoinSystem']: 
    timer = bs.Timer(settings['questionDelay'] * 1000, askQuestion, timeType='real', repeat=True)
    print 'Coin system loaded...'


