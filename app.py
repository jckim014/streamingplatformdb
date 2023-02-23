# Citation for the structure of all route handlers and related methods
# Date: 05/24/2022 - 06/05/2022
# Adapted/Based on tutorial: 
# https://github.com/osu-cs340-ecampus/flask-starter-app
# https://github.com/osu-cs340-ecampus/flask-starter-app/blob/master/bsg_people_app/app.py

# Citation for all jinja templates:
# Date: 05/24/2022 - 06/05/2022
# Adapted/Based on:
# https://github.com/osu-cs340-ecampus/flask-starter-app/blob/master/bsg_people_app/templates/people.j2
# https://github.com/osu-cs340-ecampus/flask-starter-app/blob/master/bsg_people_app/templates/edit_people.j2

import email
from flask import Flask, render_template, json, redirect
from flask_mysqldb import MySQL
from flask import request
import os


app = Flask(__name__)

# database connection
# Template:
# app.config["MYSQL_HOST"] = "classmysql.engr.oregonstate.edu"
# app.config["MYSQL_USER"] = "cs340_OSUusername"
# app.config["MYSQL_PASSWORD"] = "XXXX" | last 4 digits of OSU id
# app.config["MYSQL_DB"] = "cs340_OSUusername"
# app.config["MYSQL_CURSORCLASS"] = "DictCursor"

# database connection info
app.config["MYSQL_HOST"] = "classmysql.engr.oregonstate.edu"
app.config["MYSQL_USER"] = "cs340_kimjoshu"
app.config["MYSQL_PASSWORD"] = "1738"
app.config["MYSQL_DB"] = "cs340_kimjoshu"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql = MySQL(app)

@app.route('/')
def root():
    return render_template("index.j2")


@app.route('/shows', methods=["POST", "GET"])
def shows():

    # query = "SELECT * FROM Shows"
    query = "SELECT showID, showName, Shows.typeID, ContentTypes.description AS 'Content Type', Shows.GenreID, Genres.description AS Genre, showRating, releaseDate FROM Shows INNER JOIN ContentTypes on Shows.typeID = ContentTypes.typeID INNER JOIN Genres on Shows.genreID = Genres.genreID"

    cur = mysql.connection.cursor()
    cur.execute(query)
    data = cur.fetchall()

    query2 = "SELECT * FROM Genres"
    cur = mysql.connection.cursor()
    cur.execute(query2)
    genredata = cur.fetchall()

    query3 = "SELECT * FROM ContentTypes"
    cur = mysql.connection.cursor()
    cur.execute(query3)
    typedata = cur.fetchall()

    if request.method == "GET":
        return render_template("shows.j2", data=data, genredata=genredata, typedata=typedata)
    
    if request.method == "POST":
        if request.form.get("Add_Show"):
            showName = request.form["showName"]
            typeID = request.form["addType"]
            genreID = request.form["addGenre"]
            showRating = request.form["showRating"]
            releaseDate = request.form["releaseDate"]

            query = "INSERT INTO Shows (showName, typeID, genreID, showRating, releaseDate) VALUES (%s, %s, %s, %s, %s)"
            cur = mysql.connection.cursor()
            cur.execute(query, (showName, typeID, genreID, showRating, releaseDate))
            mysql.connection.commit()

            return redirect("/shows")
        
        if request.form.get("Search_Show"):
            type = request.form["searchType"]
            genre = request.form["searchGenre"]

            # both empty
            if type == "" and genre == "":
                # query = "SELECT * FROM Shows WHERE typeID = %s and genreID = %s"
                # cur = mysql.connection.cursor()
                # cur.execute(query, (type, genre))
                # data = cur.fetchall()

                return render_template("search_shows.j2", genredata=genredata, typedata=typedata)

            # search type
            elif genre == "":
                query = "SELECT showID, showName, Shows.typeID, ContentTypes.description AS 'Content Type', Shows.GenreID, Genres.description AS Genre, showRating, releaseDate FROM Shows INNER JOIN ContentTypes on Shows.typeID = ContentTypes.typeID INNER JOIN Genres on Shows.genreID = Genres.genreID WHERE Shows.typeID = %s"
                # query = "SELECT * FROM Shows WHERE typeID = %s"
                cur = mysql.connection.cursor()
                cur.execute(query, (type,))
                data = cur.fetchall()

                return render_template("search_shows.j2", data=data, genredata=genredata, typedata=typedata)

            # search genre
            elif type == "":
                query = "SELECT showID, showName, Shows.typeID, ContentTypes.description AS 'Content Type', Shows.GenreID, Genres.description AS Genre, showRating, releaseDate FROM Shows INNER JOIN ContentTypes on Shows.typeID = ContentTypes.typeID INNER JOIN Genres on Shows.genreID = Genres.genreID WHERE Shows.genreID = %s"
                # query = "SELECT * FROM Shows WHERE genreID = %s"
                cur = mysql.connection.cursor()
                cur.execute(query, (genre,))
                data = cur.fetchall()

                return render_template("search_shows.j2", data=data, genredata=genredata, typedata=typedata)
                    # search both
            else:
                query = "SELECT showID, showName, Shows.typeID, ContentTypes.description AS 'Content Type', Shows.GenreID, Genres.description AS Genre, showRating, releaseDate FROM Shows INNER JOIN ContentTypes on Shows.typeID = ContentTypes.typeID INNER JOIN Genres on Shows.genreID = Genres.genreID WHERE Shows.typeID = %s and Shows.genreID = %s"
                cur = mysql.connection.cursor()
                cur.execute(query, (type, genre))
                data = cur.fetchall()

                return render_template("search_shows.j2", data=data, genredata=genredata, typedata=typedata)

@app.route('/search_shows', methods=["POST", "GET"])
def search_shows():
    query = "SELECT * FROM Shows"
    cur = mysql.connection.cursor()
    cur.execute(query)
    data = cur.fetchall()

    query2 = "SELECT * FROM Genres"
    cur = mysql.connection.cursor()
    cur.execute(query2)
    genredata = cur.fetchall()

    query3 = "SELECT * FROM ContentTypes"
    cur = mysql.connection.cursor()
    cur.execute(query3)
    typedata = cur.fetchall()

    if request.form.get("Search_Show"):
        type = request.form["searchType"]
        genre = request.form["searchGenre"]

        # both empty
        if type == "" and genre == "":
            # query = "SELECT * FROM Shows WHERE typeID = %s and genreID = %s"
            # cur = mysql.connection.cursor()
            # cur.execute(query, (type, genre))
            # data = cur.fetchall()

            return render_template("search_shows.j2", data=data, genredata=genredata, typedata=typedata)

        # search type
        elif genre == "":
            query = "SELECT showID, showName, Shows.typeID, ContentTypes.description AS 'Content Type', Shows.GenreID, Genres.description AS Genre, showRating, releaseDate FROM Shows INNER JOIN ContentTypes on Shows.typeID = ContentTypes.typeID INNER JOIN Genres on Shows.genreID = Genres.genreID WHERE Shows.typeID = %s"
            # query = "SELECT * FROM Shows WHERE typeID = %s"
            cur = mysql.connection.cursor()
            cur.execute(query, (type,))
            data = cur.fetchall()

            return render_template("search_shows.j2", data=data, genredata=genredata, typedata=typedata)

        # search genre
        elif type == "":
            query = "SELECT showID, showName, Shows.typeID, ContentTypes.description AS 'Content Type', Shows.GenreID, Genres.description AS Genre, showRating, releaseDate FROM Shows INNER JOIN ContentTypes on Shows.typeID = ContentTypes.typeID INNER JOIN Genres on Shows.genreID = Genres.genreID WHERE Shows.genreID = %s"
            # query = "SELECT * FROM Shows WHERE genreID = %s"
            cur = mysql.connection.cursor()
            cur.execute(query, (genre,))
            data = cur.fetchall()

            return render_template("search_shows.j2", data=data, genredata=genredata, typedata=typedata)
        
        # search both
        else:
            query = "SELECT showID, showName, Shows.typeID, ContentTypes.description AS 'Content Type', Shows.GenreID, Genres.description AS Genre, showRating, releaseDate FROM Shows INNER JOIN ContentTypes on Shows.typeID = ContentTypes.typeID INNER JOIN Genres on Shows.genreID = Genres.genreID WHERE Shows.typeID = %s and Shows.genreID = %s"
            cur = mysql.connection.cursor()
            cur.execute(query, (type, genre))
            data = cur.fetchall()

            return render_template("search_shows.j2", data=data, genredata=genredata, typedata=typedata)

@app.route('/delete_show/<int:showID>') 
def delete_show(showID):
    query = "DELETE from Shows where showID = '%s';"
    cur = mysql.connection.cursor()
    cur.execute(query, (showID,))
    mysql.connection.commit()

    return redirect("/shows")    

@app.route('/edit_show/<int:showID>', methods=["POST", "GET"])
def edit_show(showID):
    # initially grab info of user
    if request.method == "GET":
        # query = "SELECT * from Shows where showID = %s" % (showID)
        query = "SELECT showID, showName, Shows.typeID, ContentTypes.description AS 'Content Type', Shows.GenreID, Genres.description AS Genre, showRating, releaseDate FROM Shows INNER JOIN ContentTypes on Shows.typeID = ContentTypes.typeID INNER JOIN Genres on Shows.genreID = Genres.genreID WHERE Shows.showID = %s" % (showID)
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        query2 = "SELECT * FROM Genres"
        cur = mysql.connection.cursor()
        cur.execute(query2)
        genredata = cur.fetchall()

        query3 = "SELECT * FROM ContentTypes"
        cur = mysql.connection.cursor()
        cur.execute(query3)
        typedata = cur.fetchall()

        return render_template("edit_show.j2", data=data, genredata=genredata, typedata=typedata)
    
    if request.method == "POST":
        if request.form.get("Edit_Show"):
            showID = request.form["showID"]
            showName = request.form["showName"]
            typeID = request.form["typeID"]
            genreID = request.form["genreID"]
            showRating = request.form["showRating"]
            releaseDate = request.form["releaseDate"]

            # no null inputs
            query = "UPDATE Shows SET Shows.showName = %s, Shows.typeID = %s, Shows.genreID = %s, Shows.showRating = %s, Shows.releaseDate = %s WHERE Shows.showID = %s"
            cur = mysql.connection.cursor()
            cur.execute(query, (showName, typeID, genreID, showRating, releaseDate, showID))
            mysql.connection.commit()

            return redirect("/shows")

@app.route('/platforms', methods=["POST", "GET"])
def platforms():
    if request.method == "GET":
        query = "SELECT * FROM Platforms"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()
        return render_template("platforms.j2", data=data)
    
    if request.method == "POST":
        if request.form.get("Add_Platform"):
            platformName = request.form["platformName"]
            numberShows = request.form["numberShows"]

            # there should be no null inputs
            query = "INSERT INTO Platforms (platformName, numberShows) VALUES (%s, %s)"
            cur = mysql.connection.cursor()
            cur.execute(query, (platformName, numberShows))
            mysql.connection.commit()

            return redirect("/platforms")

@app.route('/delete_platform/<int:platformID>') 
def delete_platform(platformID):
    query = "DELETE from Platforms where platformID = '%s';"
    cur = mysql.connection.cursor()
    cur.execute(query, (platformID,))
    mysql.connection.commit()

    return redirect("/platforms")

@app.route('/edit_platform/<int:platformID>', methods=["POST", "GET"])
def edit_platform(platformID):
    # initially grab info of user
    if request.method == "GET":
        query = "SELECT * from Platforms where platformID = %s" % (platformID)
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        return render_template("edit_platform.j2", data=data)
    
    if request.method == "POST":
        if request.form.get("Edit_Platform"):
            platformID = request.form["platformID"]
            platformName = request.form["platformName"]
            numberShows = request.form["numberShows"]

            # no null inputs
            query = "UPDATE Platforms SET Platforms.platformName = %s, Platforms.numberShows = %s WHERE Platforms.platformID = %s"
            cur = mysql.connection.cursor()
            cur.execute(query, (platformName, numberShows, platformID))
            mysql.connection.commit()

            return redirect("/platforms")


@app.route('/showsonplatforms', methods=["POST", "GET"])
def shows_on_platforms():
    if request.method == "GET":
        query = "SELECT showsPlatformsID, ShowsOnPlatforms.showID, Shows.showName AS showName, ShowsOnPlatforms.platformID, Platforms.platformName AS platformName FROM ShowsOnPlatforms INNER JOIN Shows on ShowsOnPlatforms.showID = Shows.showID INNER JOIN Platforms on ShowsOnPlatforms.platformID = Platforms.platformID"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        query2 = "SELECT * FROM Shows"
        cur = mysql.connection.cursor()
        cur.execute(query2)
        showdata = cur.fetchall()

        query3 = "SELECT * FROM Platforms"
        cur = mysql.connection.cursor()
        cur.execute(query3)
        platformdata = cur.fetchall()

        return render_template("showsonplatforms.j2", data=data, showdata=showdata, platformdata=platformdata)
    
    if request.method == "POST":
        if request.form.get("Add_Show_To_Platform"):
            showID = request.form["showID"]
            platformID = request.form["platformID"]

            # there should be no null inputs
            query = "INSERT INTO ShowsOnPlatforms (showID, platformID) VALUES (%s, %s)"
            cur = mysql.connection.cursor()
            cur.execute(query, (showID, platformID))
            mysql.connection.commit()

        return redirect("/showsonplatforms")

@app.route('/delete_show_on_platform/<int:showsPlatformsID>')
def delete_show_on_platform(showsPlatformsID):
    query = "DELETE from ShowsOnPlatforms where showsPlatformsID = %s;"
    cur = mysql.connection.cursor()
    cur.execute(query, (showsPlatformsID,))
    mysql.connection.commit()

    return redirect("/showsonplatforms")

@app.route('/edit_show_on_platform/<int:showsPlatformsID>', methods=["POST", "GET"])
def edit_show_on_platform(showsPlatformsID):
    # initially grab info of user
    if request.method == "GET":
        query = "SELECT showsPlatformsID, ShowsOnPlatforms.showID, Shows.showName AS showName, ShowsOnPlatforms.platformID, Platforms.platformName AS platformName FROM ShowsOnPlatforms INNER JOIN Shows on ShowsOnPlatforms.showID = Shows.showID INNER JOIN Platforms on ShowsOnPlatforms.platformID = Platforms.platformID WHERE ShowsOnPlatforms.showsPlatformsID = %s"
        cur = mysql.connection.cursor()
        cur.execute(query, (showsPlatformsID, ))
        data = cur.fetchall()

        query2 = "SELECT * FROM Shows"
        cur = mysql.connection.cursor()
        cur.execute(query2)
        showdata = cur.fetchall()

        query3 = "SELECT * FROM Platforms"
        cur = mysql.connection.cursor()
        cur.execute(query3)
        platformdata = cur.fetchall()

        return render_template("edit_show_on_platform.j2", data=data, showdata=showdata, platformdata=platformdata)
    
    if request.method == "POST":
        if request.form.get("Edit_Show_And_Platform"):
            showsPlatformsID = request.form["showsPlatformsID"]
            platformID = request.form["platformID"]
            showID = request.form["showID"]

            # no null inputs
            query = "UPDATE ShowsOnPlatforms SET ShowsOnPlatforms.platformID = %s, ShowsOnPlatforms.showID = %s WHERE ShowsOnPlatforms.showsPlatformsID = %s"
            cur = mysql.connection.cursor()
            cur.execute(query, (platformID, showID, showsPlatformsID))
            mysql.connection.commit()

            return redirect("/showsonplatforms")

@app.route('/users', methods=["POST", "GET"])
def users():
    if request.method == "GET":
        query = "SELECT * FROM Users"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()
        return render_template("users.j2", Users=data)
    
    if request.method == "POST":
        if request.form.get("Add_User"):
            userName = request.form["userName"]
            email = request.form["email"]
            dateCreated = request.form["dateCreated"]

            # there should be no null inputs
            query = "INSERT INTO Users (userName, email, dateCreated) VALUES (%s, %s, %s)"
            cur = mysql.connection.cursor()
            cur.execute(query, (userName, email, dateCreated))
            mysql.connection.commit()

            return redirect("/users")


@app.route('/delete_user/<int:userID>') 
def delete_user(userID): # I ~think~ the userID argument can be named anything
    query = "DELETE from Users where userID = '%s';"
    cur = mysql.connection.cursor()
    cur.execute(query, (userID,))
    mysql.connection.commit()

    return redirect("/users")

@app.route('/edit_user/<int:userID>', methods=["POST", "GET"])
def edit_user(userID):
    # initially grab info of user
    if request.method == "GET":
        query = "SELECT * from Users where userID = %s" % (userID)
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        return render_template("edit_user.j2", data=data)
    
    if request.method == "POST":
        if request.form.get("Edit_User"):
            userID = request.form["userID"]
            userName = request.form["userName"]
            email = request.form["email"]
            dateCreated = request.form["dateCreated"]

            # no null inputs
            query = "UPDATE Users SET Users.userName = %s, Users.email = %s, Users.dateCreated = %s WHERE Users.userID = %s"
            cur = mysql.connection.cursor()
            cur.execute(query, (userName, email, dateCreated, userID))
            mysql.connection.commit()

            return redirect("/users")

@app.route('/reviews', methods=["POST", "GET"])
def reviews():
    if request.method == "GET":
        # query = "SELECT reviewID, Reviews.userID, Users.userName AS userName, Reviews.showID, Shows.showName AS showName, Reviews.dateCreated, rating, reviewText FROM Reviews INNER JOIN Users on Reviews.userID = Users.userID INNER JOIN Shows on Reviews.showID = Shows.showID"
        query = "SELECT reviewID, Reviews.userID, Users.userName AS userName, Reviews.showID, Shows.showName AS showName, Reviews.dateCreated, rating, reviewText FROM Reviews LEFT JOIN Users on Reviews.userID = Users.userID INNER JOIN Shows on Reviews.showID = Shows.showID"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        query2 = "SELECT * FROM Users"
        cur = mysql.connection.cursor()
        cur.execute(query2)
        userdata = cur.fetchall()

        query3 = "SELECT * FROM Shows"
        cur = mysql.connection.cursor()
        cur.execute(query3)
        showdata = cur.fetchall()
        
        return render_template("reviews.j2", data=data, userdata=userdata, showdata=showdata)
    
    if request.method == "POST":
        if request.form.get("Add_Review"):
            userID = request.form["userID"]
            showID = request.form["showID"]
            dateCreated = request.form["dateCreated"]
            rating = request.form["rating"]
            reviewText = request.form["reviewText"]

            query = "INSERT INTO Reviews (userID, showID, dateCreated, rating, reviewText) VALUES (%s, %s, %s, %s, %s)"
            cur = mysql.connection.cursor()
            cur.execute(query, (userID, showID, dateCreated, rating, reviewText))
            mysql.connection.commit()


            return redirect("/reviews")

@app.route('/delete_review/<int:reviewID>') 
def delete_review(reviewID):
    query = "DELETE from Reviews where reviewID = '%s';"
    cur = mysql.connection.cursor()
    cur.execute(query, (reviewID,))
    mysql.connection.commit()

    return redirect("/reviews")

@app.route('/edit_review/<int:reviewID>', methods=["POST", "GET"])
def edit_review(reviewID):
    # initially grab info of user
    if request.method == "GET":
        # query = "SELECT reviewID, Reviews.userID, Users.userName AS userName, Reviews.showID, Shows.showName AS showName, Reviews.dateCreated, rating, reviewText FROM Reviews INNER JOIN Users on Reviews.userID = Users.userID INNER JOIN Shows on Reviews.showID = Shows.showID WHERE reviewID = %s" % (reviewID)
        # query = "SELECT reviewID, Reviews.userID, Reviews.showID, Shows.showName AS showName, Reviews.dateCreated, rating, reviewText FROM Reviews INNER JOIN Shows on Reviews.showID = Shows.showID WHERE reviewID = %s" % (reviewID)
        # query = "SELECT reviewID, userID, showID, dateCreated, rating FROM Reviews WHERE reviewID = %s" % (reviewID)
        query = "SELECT reviewID, Reviews.userID, Users.userName AS userName, Reviews.showID, Shows.showName AS showName, Reviews.dateCreated, rating, reviewText FROM Reviews LEFT JOIN Users on Reviews.userID = Users.userID INNER JOIN Shows on Reviews.showID = Shows.showID WHERE reviewID = %s" % (reviewID)
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        query2 = "SELECT * FROM Users"
        cur = mysql.connection.cursor()
        cur.execute(query2)
        userdata = cur.fetchall()

        query3 = "SELECT * FROM Shows"
        cur = mysql.connection.cursor()
        cur.execute(query3)
        showdata = cur.fetchall()
        
        return render_template("edit_review.j2", data=data, userdata=userdata, showdata=showdata)

    if request.method == "POST":
        if request.form.get("Edit_Review"):
            userID = request.form["userID"]
            showID = request.form["showID"]
            dateCreated = request.form["dateCreated"]
            rating = request.form["rating"]
            reviewText = request.form["reviewText"]

            # nullable relationship
            if userID == "":
                query = "UPDATE Reviews SET Reviews.userID = NULL, Reviews.showID = %s, Reviews.dateCreated = %s, Reviews.rating = %s, Reviews.reviewText = %s WHERE Reviews.reviewID = %s"
                cur = mysql.connection.cursor()
                cur.execute(query, (showID, dateCreated, rating, reviewText, reviewID))
                mysql.connection.commit()

                return redirect("/reviews")
            else:                
                query = "UPDATE Reviews SET Reviews.userID = %s, Reviews.showID = %s, Reviews.dateCreated = %s, Reviews.rating = %s, Reviews.reviewText = %s WHERE Reviews.reviewID = %s"
                cur = mysql.connection.cursor()
                cur.execute(query, (userID, showID, dateCreated, rating, reviewText, reviewID))
                mysql.connection.commit()

                return redirect("/reviews")

@app.route('/contenttypes', methods=["POST", "GET"])
def contenttypes():
    if request.method == "GET":
        query = "SELECT * FROM ContentTypes"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()
        return render_template("contenttypes.j2", data=data)
    
    if request.method == "POST":
        if request.form.get("Add_ContentType"):
            description = request.form["description"]

            # there should be no null inputs
            query = "INSERT INTO ContentTypes (description) VALUES (%s)"
            cur = mysql.connection.cursor()
            cur.execute(query, (description,))
            mysql.connection.commit()

            return redirect("/contenttypes")

@app.route('/delete_contenttype/<int:typeID>') 
def delete_contenttype(typeID):
    query = "DELETE from ContentTypes where typeID = '%s';"
    cur = mysql.connection.cursor()
    cur.execute(query, (typeID,))
    mysql.connection.commit()

    return redirect("/contenttypes")

@app.route('/edit_contenttype/<int:typeID>', methods=["POST", "GET"])
def edit_contenttype(typeID):
    # initially grab info of user
    if request.method == "GET":
        query = "SELECT * from ContentTypes where typeID = %s" % (typeID)
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        return render_template("edit_contenttype.j2", data=data)
    
    if request.method == "POST":
        if request.form.get("Edit_ContentType"):
            typeID = request.form["typeID"]
            description = request.form["description"]

            query = "UPDATE ContentTypes SET ContentTypes.description = %s WHERE ContentTypes.typeID = %s"
            cur = mysql.connection.cursor()
            cur.execute(query, (description, typeID))
            mysql.connection.commit()

            return redirect("/contenttypes")

@app.route('/genres', methods=["POST", "GET"])
def genres():
    if request.method == "GET":
        query = "SELECT * FROM Genres"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()
        return render_template("genres.j2", data=data)
    
    if request.method == "POST":
        if request.form.get("Add_Genre"):
            description = request.form["description"]

            # there should be no null inputs
            query = "INSERT INTO Genres (description) VALUES (%s)"
            cur = mysql.connection.cursor()
            cur.execute(query, (description,))
            mysql.connection.commit()

            return redirect("/genres")

@app.route('/delete_genre/<int:genreID>') 
def delete_genre(genreID):
    query = "DELETE from Genres where genreID = '%s';"
    cur = mysql.connection.cursor()
    cur.execute(query, (genreID,))
    mysql.connection.commit()

    return redirect("/genres")

@app.route('/edit_genre/<int:genreID>', methods=["POST", "GET"])
def edit_genre(genreID):
    # initially grab info of user
    if request.method == "GET":
        query = "SELECT * from Genres where genreID = %s" % (genreID)
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        return render_template("edit_genre.j2", data=data)
    
    if request.method == "POST":
        if request.form.get("Edit_Genre"):
            genreID = request.form["genreID"]
            description = request.form["description"]

            query = "UPDATE Genres SET Genres.description = %s WHERE Genres.genreID = %s"
            cur = mysql.connection.cursor()
            cur.execute(query, (description, genreID))
            mysql.connection.commit()

            return redirect("/genres")

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 18828))
    app.run(port=port, debug=True)
