package main

import "fmt"
// import	"io/ioutil"
import "net/http"
import "html/template"
// import "database/sql"
import "github.com/jmoiron/sqlx"
import _ "github.com/lib/pq"
import "log"
import "encoding/json"

var schema = `
DROP TABLE users;
CREATE TABLE users (
	user_id		serial,
	fb_id		text,
    first_name 	text,
    last_name 	text,
    user_name	text,
    email 		text
);

DROP TABLE place;
CREATE TABLE place (
	place_id	serial,
    name 		text,
    lat 		float,
    long 		float
);

DROP TABLE likes;
CREATE TABLE likes (
	user_id		uuid,
	place_id	uuid,
	swipe		boolean,
	liked 		boolean,
	rating		int,
	times		int
)`

// type Person struct {
//     FirstName string `db:"first_name"`
//     LastName  string `db:"last_name"`
//     Email     string
// }

// type Place struct {
//     Country string
//     City    sql.NullString
//     TelCode int
// }

type Place struct {
	Restid	string `db:"place_id"`
	Name	string 
	lat		float32
	long	float32
}

type User struct {
	Userid	string `db:"user_id"` 	
	Uname	string `db:"user_name"`	
	Fname	string `db:"first_name"`
	Lname	string `db:"last_name"`	
	FBid	string `db:"fb_id"`		
	Email	string
}

var db *sqlx.DB

func getRestaurants(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	fmt.Fprintf(w, "{response: \"Hi there, I love %s!\"}", r.URL.Path[len("/restaurants/"):])
}

func loginPage(w http.ResponseWriter, r *http.Request) {
	t, _ := template.ParseFiles("fb_test.html")
	t.Execute(w, nil)
}

var newUserQuery = "INSERT INTO users (first_name, last_name, user_name, fb_id, email)"+
					" VALUES ($1, $2, $3, $4, $5)"
func saveUser(w http.ResponseWriter, r *http.Request) {
	fmt.Println("New User: " +
		r.FormValue("first_name"), 
		r.FormValue("last_name"), 
		r.FormValue("user_name"), 
		r.FormValue("fb_id"), 
		r.FormValue("email"))
	tx := db.MustBegin()
    tx.MustExec(newUserQuery, r.FormValue("first_name"), 
		r.FormValue("last_name"), 
		r.FormValue("user_name"), 
		r.FormValue("fb_id"), 
		r.FormValue("email"))
    tx.Commit()
	http.Redirect(w, r, "/users/viewAll/", http.StatusFound)
}

func newUser(w http.ResponseWriter, r *http.Request) {
	fmt.Fprintf(w, "<h1>New User</h1>" +
		"<form action=\"/users/save/\" method=\"POST\">" +
		"<label>first_name</label><br>" +
		"<input type=\"text\" name=\"first_name\" ><br>" +
		"<label>last_name</label><br>" +
		"<input type=\"text\" name=\"last_name\" ><br>" +
		"<label>user_name</label><br>" +
		"<input type=\"text\" name=\"user_name\" ><br>" +
		"<label>fb_id</label><br>" +
		"<input type=\"text\" name=\"fb_id\" ><br>" +
		"<label>email</label><br>" +
		"<input type=\"text\" name=\"email\" ><br>" +
		"<input type=\"submit\" value=\"Save\">" +
		"</form>");
}

func viewAllUsers(w http.ResponseWriter, r *http.Request) {
	users := []User{}
	err := db.Select(&users, "SELECT * FROM users ORDER BY user_id")
    if err != nil {
        fmt.Println(err)
        return
    }
    resp, err := json.Marshal(users)
    if err != nil {
        fmt.Println(err)
        return
    }
    fmt.Println(resp)
    fmt.Println(w, resp)
}

func main() {
	var err error
    db, err = sqlx.Connect("postgres", "user=postgres dbname=letsgo sslmode=disable")
    if err != nil {
        log.Fatalln(err)
    }
    _ = db
    // db.MustExec(schema)

	http.HandleFunc("/restaurants/", getRestaurants)
	http.HandleFunc("/users/new/", newUser)
	http.HandleFunc("/users/save/", saveUser)
	http.HandleFunc("/users/viewAll/", viewAllUsers)
	http.Handle("/login/", http.StripPrefix("/login/", http.FileServer(http.Dir("./"))))
	http.ListenAndServe(":8080", nil)
}

