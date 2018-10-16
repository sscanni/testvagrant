from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant
import cgi

engine = create_engine('sqlite:///restaurantmenu.db', echo=False)
Base.metadata.bind = engine 

DBSession = sessionmaker(bind=engine)
session = DBSession()

class webserverHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
           if self.path.endswith("/restaurants"):
               self.send_response(200)
               self.send_header('Content-type', 'text/html')
               self.end_headers()
               output = ""
               output += "<html><body>"
               output += "<a href='/restaurants/new'>Make a New Restaurant</a></br></br>"                
               restaurants = session.query(Restaurant).all()
               for restaurant in restaurants:
                   output += restaurant.name
                   output += "</br>"
                   output += "<a href='/restaurants/%d/edit'>Edit</a></br>" % (restaurant.id)
                   output += "<a href='/restaurants/%d/delete'>Delete</a></br>" % (restaurant.id)
                   output += "</br>"
               session.close()
               output += "</body></html>"
               self.wfile.write(output)
               #print(output)
               return
           if self.path.endswith("/edit"):
                restaurantIDPath = self.path.split("/")[2]
                print("self.path= %s") % (self.path) 
                print("self.path.split('/')[0]= %s") % self.path.split("/")[0]
                print("self.path.split('/')[1]= %s") % self.path.split("/")[1]
                print("self.path.split('/')[2]= %s") % self.path.split("/")[2]
                myRestaurantQuery = session.query(Restaurant).filter_by(id=restaurantIDPath).one()
                if myRestaurantQuery:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    output = "<html><body>"
                    output += "<h1>"
                    output += myRestaurantQuery.name
                    output += "</h1>"
                    output += "<form method='POST' enctype='multipart/form-data' action = '/restaurants/%s/edit' >" % restaurantIDPath
                    output += "<input name = 'newRestaurantName' type='text' placeholder = '%s' >" % myRestaurantQuery.name
                    output += "<input type = 'submit' value = 'Rename'>"
                    output += "</form>"
                    output += "</body></html>"
                    self.wfile.write(output)
                    return
           if self.path.endswith("/delete"):
                restaurantIDPath = self.path.split("/")[2]
                myRestaurantQuery = session.query(Restaurant).filter_by(id=restaurantIDPath).one()
                if myRestaurantQuery:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    output = "<html><body>"
                    output += "<h1>Delete "
                    output += myRestaurantQuery.name
                    output += "</h1>"
                    output += "<h2>Are you sure?</h2>"
                    output += "<form method='POST' enctype='multipart/form-data' action = '/restaurants/%s/delete' >" % restaurantIDPath
                    output += "<input type = 'submit' value = 'Delete'>&nbsp;&nbsp;"
                    output += "</form>"
                    output += "</body></html>"
                    self.wfile.write(output)
                    return
           if self.path.endswith("/restaurants/new"):
               self.send_response(200)
               self.send_header('Content-type', 'text/html')
               self.end_headers()
               output = ""
               output += "<html><body>"
               output += "<h1>Make a New Restaurant</h1>"
               output += """<form method='POST' enctype='multipart/form-data' action='/restaurants/new'><input name='newRestuarant'
                    type='text' ><input type='submit' value='Create'> </form>"""
               output += "</body></html>"
               self.wfile.write(output)
               return
        except:
            self.send_error(404, "File Not Found %s" % self.path)

    def do_POST(self):
        try:
            if self.path.endswith("/edit"):
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('newRestaurantName')
                    restaurantIDPath = self.path.split("/")[2]
                    myRestaurantQuery = session.query(Restaurant).filter_by(id=restaurantIDPath).one()
                    # if myRestaurantQuery != []:  could also use this.
                    if myRestaurantQuery:
                        myRestaurantQuery.name = messagecontent[0]
                        session.add(myRestaurantQuery)
                        session.commit()
                        self.send_response(301)
                        self.send_header('Content-type', 'text/html')
                        self.send_header('Location', '/restaurants')
                        self.end_headers()
                        return
            if self.path.endswith("/delete"):
                restaurantIDPath = self.path.split("/")[2]
                myRestaurantQuery = session.query(Restaurant).filter_by(id=restaurantIDPath).one()
                if myRestaurantQuery:
                    session.delete(myRestaurantQuery)
                    session.commit()
                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/restaurants')
                    self.end_headers()
                    return
            if self.path.endswith("/restaurants/new"):
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields=cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('newRestuarant')

                    #Create new resturant 
                    newRestaurant = Restaurant(name=messagecontent[0])
                    session.add(newRestaurant)
                    session.commit()

                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/restaurants')
                    self.end_headers()    
                    return    
        except:
            pass
def main():
    try:
        port = 8080
        server = HTTPServer(('',port), webserverHandler)
        print ("Web server running on port %s" % port)
        server.serve_forever()

    except KeyboardInterrupt:
        print ("^C entered, stopping web server...")
        server.serve_close()

if __name__ == '__main__':
    main()