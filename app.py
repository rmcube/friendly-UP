from flask import Flask,request
from query.user import getUsers

app = Flask(__name__)

@app.route('/users/<user_id>')
def show_user_profile(name):
    # show the user profile for that user
    return 'User %s' % name 

@app.route('/users')
def get_users_by_condition():
    '''this router allow us to get a list of user info by name and school.
    '''
    name = request.args.get('name')
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


if __name__ == '__main__':
   
    app.debug = True
    app.run()
    
