from flask import Flask,request
from query.user import getUsers

app = Flask(__name__)

@app.route('/users/<user_id>',method=["GET"])
def show_user_profile(name):
    # show the user profile for that user
    return 'User %s' % name 

@app.route('/users')
def get_users_by_condition():
    '''this router allow us to get a list of user info by name and school.
    '''
    school = request.args.get('school')
    
    query = getUsers.query1
    where = ""
    if(name!=None):
        where+="where name = %s"
    
    if(school!=None):
        if(where==""):
            where+="where school = %s"
        else:
            where+= "and school = %s"
    
    cur.execute(query + where , name, school)
    
    "select * from users where name = %s and school = %s" , name, school
    
    [
        {
            "user_id" : 1231231,
            "name":"solmin",
            "school":"yeonsong high school"
        },
        {
            "user_id" : 13123,
            "name":"so123123lmin",
            "school":"yeonsong123123 high school"
        }
    ]
# show the user profile for that user
    return 'User %s' % name 


<<<<<<< HEAD
@app.route('/users/by/grade', method=["GET"])
def get_user_by_condition(grade):
    '''this router allow us to get a list of user info by grade and school.
    '''
    school = request.args.get('school')
    grade = request.args.get('grade')
   
    query = getUsers.query1
   
    where = ""
    if(grade!=None):
        where+="where name = %s"
    
    if(school!=None):
        if(where==""):
            where+="where school = %s"
        else:
            where+= "and school = %s"
    
    cur.execute(query + where , grade, school)
    
    "select * from users where grade = %s and school = %s" , grade, school
    return 'users %s' % grade   

@app.route('/users/by/school', method=["GET"])
def get_user_by_condition(school):
    '''this router allow us to get a list of user info by school.
    '''
    school = request.args.get('school')
   
    query = getUsers.query1
   
    where = ""
    
    if(school!=None):
        if(where==""):
            where+="where school = %s"
        else:
            where+= "and school = %s"
    
    cur.execute(query + where , school)
    
    "select * from users where grade = %s and school = %s" , school
    return 'users %s' % school   

=======
>>>>>>> 96d0ff3fc03e69a9c967e16187b90a2ae7449c67
if __name__ == '__main__':
   
    app.debug = True
    app.run(host='127.0.0.1', port=5000)

    
    
