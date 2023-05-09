const express = require("express");
const fs = require("fs");
const session = require("express-session");
const bodyParser = require("body-parser");
const bcrypt = require("bcrypt");

const app = express();

//serving public file
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

//serving public file
app.use(express.static(__dirname));

// Set up session management
app.use(
  session({
    secret: "thisismysecretkey",
    resave: true,
    saveUninitialized: true,
  })
);

// Set up body parser middleware
app.use(bodyParser.urlencoded({ extended: true }));

port = 3001;
app.listen(port, () => {
  console.log(`Server listening on port ${port}`);
});

// Define username and password
const username = "admin";
const password = "admin123";

app.get("/home", (req, res) => {
  // if session is started we will redirect the user to the profile page
  if (req.session.authorized) {
    // res.send(
    //   `<h1>Welcome User  <a href=\'/logout'><button type="button" class="btn btn-primary">logout</button></a>`
    // );
    res.sendFile("home.html", { root: __dirname });
  }
  // if session is not started we will show the login page to the user
  else {
    res.sendFile("public/index.html", { root: __dirname });
  }
});

// Create a middleware function to check if the user is authorized
const checkAuth = (req, res, next) => {
  if (req.session.authorized) {
    next();
  } else {
    res.redirect("public/index.html");
  }
};

// Apply the middleware to the /details endpoint
app.get("/details", checkAuth, (req, res) => {
  res.sendFile("details.html", { root: __dirname });
});

app.post("/user", (req, res) => {
  if (req.body.username == username && req.body.password == password) {
    req.session.username = req.body.username;
    req.session.authorized = true;
    console.log(req.session.username);
    // res.send(
    //   `Hey there, welcome ${req.session.username} <a href=\'/logout'><button type="button" class="btn btn-primary">logout</button></a>`
    // );
    // res.sendFile("/public/home.html", { root: __dirname });
    res.redirect("/home");
  } else {
    res.send(`
    <script>
      alert("Invalid username or password");
      window.history.back();
    </script>
  `);
  }
});

app.get("/logout", (req, res) => {
  req.session.destroy();
  res.redirect("public/index.html");
});

// Handle PUT request to /data
app.put("/data", (req, res) => {
  const data = req.body;
  fs.writeFile("data.json", JSON.stringify(data), (err) => {
    if (err) {
      console.error(err);
      res.status(500).send("Error writing to file");
    } else {
      res.send("Data written to file");
    }
  });
});
