const express = require('express');
const mongoose = require('mongoose');
const app = express();
const {notFound, errorHandler} = require('./middlewares/errorMiddleware');
const sellerAuth = require('./routes/sellerAuth');
const customerAuth = require('./routes/customerAuth');
const products = require('./routes/products');
const cors = require('cors');

require('dotenv').config();

app.use(function(req, res, next) {
    res.header("Access-Control-Allow-Origin", "*");
    res.header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS, PUT, PATCH, DELETE');
    res.header("Access-Control-Allow-Headers", "x-access-token, Origin, X-Requested-With, Content-Type, Accept");
    next();
  });

app.use(cors()); 
app.use(express.json());

app.get("/", (req, res) => {
    res.json("Hello ziKwingy")
})

app.use("/api/auth2", customerAuth);
app.use("/api/auth", sellerAuth);

app.use("/api/products", products)

app.use(notFound);
app.use(errorHandler);

//connect to Database
 // db connection
mongoose.connect(process.env.MONGODB_URI, {useNewUrlParser: true});

const db = mongoose.connection
db.on('error', (error) => {
    console.log(error)
});

db.once('open', ()=> {
    console.log('database open and running')
});

// listen to port
const port = process.env.PORT
app.listen(port, () =>{
    console.log(`listening on port ${port}`);
});