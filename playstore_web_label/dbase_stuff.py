'''
Created on 22 Dec 2016

@author: Hazim Hanif
'''
import pymysql

global db
global cursor

cursor=None
db=None

def prepare_Database():
    global db
    global cursor
    db = pymysql.connect("localhost","root","toor0987654321","test" )
    cursor=db.cursor()

def login(nameIncoming):
    db.commit()
    sql = "SELECT * FROM user"
    try:
        # Execute the SQL command
        cursor.execute(sql)
        # Fetch all the rows in a list of lists.
        results = cursor.fetchall()
        for row in results:
            uname = row[1]
            pwd = row[2]
            t_review = row[3]
            t_drop = row[4]
            
            if(uname==nameIncoming):
                return([uname,pwd,t_review,t_drop])
    except:
        print ("Error: unable to fecth data")
        
    return "NONE"

def getTotalReviewsDrop(nameIncoming):
    sql = "SELECT total_review,total_drop FROM user WHERE username='%s'" % (nameIncoming)
    db.commit()
    try:
        cursor.execute(sql)
        result = cursor.fetchone()
        return result
    except:
        print ("Error: unable to fecth data")
        

def addReviewsCount(nameIncoming):
    sql = "UPDATE user SET total_review=total_review+1 WHERE username='%s'" % (nameIncoming)
    try:
        cursor.execute(sql)
        db.commit()
    except:
        print ("Error: unable to fecth data")

def addDropsCount(nameIncoming):
    sql = "UPDATE user SET total_drop=total_drop+1 WHERE username='%s'" % (nameIncoming)
    try:
        cursor.execute(sql)
        db.commit()
    except:
        print ("Error: unable to fecth data")
        
        
def getReview():
    sql="SELECT id,appId,appPrice,appScore,appTitle,revAuthor,revDate,revRating,revText,revTitle FROM playstore1 WHERE labeller_name IS NULL LIMIT 1"
    db.commit()
    try:
        cursor.execute(sql)
        result = cursor.fetchone()
        return result
    except:
        print ("Error: unable to fecth data")
        
def setLabel(sentiment,authenticity,rating,nameIncoming,revId):
    sql="UPDATE playstore1 SET label_sentiment='%s',label_authenticity='%s',label_rating=%f,labeller_name='%s' WHERE id=%d" % (sentiment,authenticity,float(rating),nameIncoming,revId)
    try:
        cursor.execute(sql)
        db.commit()
    except:
        print ("Error: unable to fecth data")

def setDrop(nameIncoming,revId):
    sql="UPDATE playstore1 SET label_drop='Drop',labeller_name='%s' WHERE id=%d" % (nameIncoming,revId)
    try:
        cursor.execute(sql)
        db.commit()
    except:
        print ("Error: unable to fecth data")
    