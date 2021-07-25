from .authgen import generate_otp
from twilio.rest import Client
import sqlite3
import time
from . import env
from twilio.base.exceptions import TwilioRestException

with sqlite3.connect('otp.db') as con: # can ise ":memory:" to run in mem
    cur = con.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS otp_info (Phone TEXT PRIMARY KEY ,OTP,Exp_on)')
    con.commit() 


def send_otp(to : str = None,sender: str = None, otp_len= 6)-> bool:
    otp = generate_otp(otp_len = otp_len)
    if _map_otp(to,otp):
        try :
            client = Client(env.TWILIO_ACC_SID, env.TWILIO_AUTH_TOKEN)
            message = client.messages.create(
                to=to, 
                from_=env.SENDER_NUMBER,
                body=f"Your One Time Password (OTP) is :- {otp}")
        except TwilioRestException as e:
            msg = f'[X] Fatal error\n[X] Detailed error:- ({e}) '
            raise RuntimeError(msg)
    else:
        return False
    return True


def verify_otp(otp : str = '', ph : str = '')-> bool:
    with sqlite3.connect('otp.db') as db:
        cur = db.cursor()
        cur.execute("SELECT OTP , Exp_on FROM otp_info WHERE Phone = (?)",(ph,))
        res = cur.fetchone()
        if res:
            print(res)
            stored_otp,exp_time = res
            curtime_stamp =  _get_timestamp()
            if  curtime_stamp >= exp_time:
                cur.execute("DELETE FROM otp_info where Phone=(?)",(ph,))
                db.commit()
                return False
            elif stored_otp != str(otp):
                return False  
            return True
    return False
        

def _map_otp(ph,otp):
    curtime_stamp =  _get_timestamp()
    exp_on = curtime_stamp + env.OTP_DURATION
    with sqlite3.connect('otp.db') as db:
        cur= db.cursor()
        try:
            cur.execute('INSERT INTO otp_info values(?,?,?)',(ph,otp,exp_on))
        except sqlite3.IntegrityError:
            cur.execute('UPDATE otp_info SET  OTP=(?),Exp_on=(?) WHERE Phone =(?)',(otp,exp_on,ph))
        db.commit() 
    return True


def _get_timestamp():
    return int(time.time())

def purgeOtpDb():
    curtime_stamp = _get_timestamp()
    try:
        with sqlite3.connect('otp.db') as db:
            cur = db.cursor()
            cur.execute("DELETE FROM otp_info WHERE Exp_on < (?)",(curtime_stamp,))
            db.commit()
    except sqlite3.Error as error:
        print("Failed to delete multiple records with error : -- >> ", error)
