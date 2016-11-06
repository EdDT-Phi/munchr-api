package main

import "fmt"
// import	"io/ioutil"
import "net/http"
import "html/template"
// import "database/sql"
import "github.com/jmoiron/sqlx"
import _ "github.com/lib/pq"
import "log"

var schema = `
CREATE TABLE users (
	user_id		uuid,
	fb_id		text,
    first_name 	text,
    last_name 	text,
    user_name	text,
    email 		text
);

CREATE TABLE place (
	place_id	uuid,
    name 		text,
    lat 		float,
    long 		float
);

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

func getRestaurants(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	fmt.Fprintf(w, "{response: \"Hi there, I love %s!\"}", r.URL.Path[len("/restaurants/"):])
}

func loginPage(w http.ResponseWriter, r *http.Request) {
	t, _ := template.ParseFiles("fb_test.html")
	t.Execute(w, nil)
}

func saveUser(w http.ResponseWriter, r *http.Request) {
	log.Println("hey")
	fmt.Println("there")
	fmt.Println(r.FormValue("first_name"), 
		r.FormValue("last_name"), 
		r.FormValue("user_name"), 
		r.FormValue("fb_id"), 
		r.FormValue("email"))
	http.Redirect(w, r, "/users/new", http.StatusFound)
}

func newUser(w http.ResponseWriter, r *http.Request) {
	fmt.Fprintf(w, "<h1>New User</h1>" +
		"<form acion=\"/users/save/\" method=\"POST\">" +
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

func main() {
    db, err := sqlx.Connect("postgres", "user=postgres dbname=letsgo sslmode=disable")
    if err != nil {
        log.Fatalln(err)
    }
    _ = db
    // db.MustExec(schema)

	http.HandleFunc("/restaurants/", getRestaurants)
	http.HandleFunc("/users/new/", newUser)
	http.HandleFunc("/users/save/", saveUser)
	// http.HandleFunc("/users/viewAll/", viewUser)
	http.Handle("/login/", http.StripPrefix("/login/", http.FileServer(http.Dir("./"))))
	http.ListenAndServe(":8080", nil)
}

