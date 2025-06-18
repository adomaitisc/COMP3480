const express = require("express");

var app = express();
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

function html(res, dir) {
  // Helper function to send HTML files
  if (!dir.startsWith("/")) {
    dir = "/" + dir;
  }
  if (!dir.endsWith(".html")) {
    dir += ".html";
  }
  return res.sendFile(__dirname + dir);
}

// 5 HTML Files:
app.get("/", (req, res) => html(res, "/pages/index.html"));
app.get("/about", (req, res) => html(res, "/pages/about.html"));
app.get("/things", (req, res) => html(res, "/pages/things.html"));
app.get("/contact", (req, res) => html(res, "/pages/contact.html"));
app.get("/portal", (req, res) => html(res, "/pages/portal.html"));

// 5 Query Parameters:
app.get("/greet", (req, res) => {
  const name = req.query.name || "Guest";
  res.send(
    `<script>alert("Hello, ${name}!"); window.location.href = "/";</script>`
  );
});
app.get("/post", (req, res) => {
  const page = req.query.page || 0;
  res.send(
    `<h1>You are now viewing Page ${page}</h1> <a href="/post?page=${
      parseInt(page) + 1
    }">Next Page</a>`
  );
});
app.get("/search", (req, res) => {
  const query = req.query.q || "";
  res.send(
    `<h1>Search Results for "${query}"</h1> <a href="/">Back to Home</a>`
  );
});
app.get("/user/:id", (req, res) => {
  const userId = req.params.id || "unknown";
  res.send(
    `<h1>User Profile</h1> <p>User ID: ${userId}</p> <a href="/">Back to Home</a>`
  );
});
app.get("/gps", (req, res) => {
  const lat = req.query.lat || "0.0";
  const lon = req.query.lon || "0.0";
  res.send(
    `<h1>GPS Coordinates</h1> <p>Latitude: ${lat}, Longitude: ${lon}</p> <a href="/">Back to Home</a>`
  );
});

// 1 Route with Header Parameter:
app.post("/header-check", (req, res) => {
  const h = req.headers["x-header"];
  if (h === "my-header") {
    res.status(200).json({ message: "Header is correct!" });
  } else {
    res.status(400).json({ message: "Header is incorrect or missing!" });
  }
});

// 1 Route with Body Input:
app.post("/portal", (req, res) => {
  const name = req.body.name || "Guest";
  res.redirect(`/greet?name=${name}`);
});

app.listen(8080, () => {
  console.log("App is online on port 8080");
});
