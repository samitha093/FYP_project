const { json } = require('body-parser');
const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');

const app = express();
const port = 3000;
app.use(express.json());
app.use(cors());
const swaggerJsdoc = require('swagger-jsdoc');
const swaggerUi = require('swagger-ui-express');

// Swagger configuration options
const swaggerOptions = {
  definition: {
    openapi: '3.0.0',
    info: {
      title: 'Node JS API Project for MongoDB',
      version: '1.0.0',
    },
  },
  apis: ['./app.js'], // Provide the path to your main file
};

// Initialize Swagger-jsdoc
const swaggerSpec = swaggerJsdoc(swaggerOptions);

// Serve Swagger documentation
app.use('/api-docs', swaggerUi.serve, swaggerUi.setup(swaggerSpec));

// Function to connect to MongoDB
async function connectToDatabase() {
  try {
    const uri =
      'mongodb+srv://StDB:lrJKqTsc8nNSgoIP@cluster0.izid3.mongodb.net/supermarket?retryWrites=true&w=majority';

    await mongoose.connect(uri, { useNewUrlParser: true, useUnifiedTopology: true });
    console.log('Connected to MongoDB');
  } catch (error) {
    console.error('Error connecting to MongoDB:', error);
  }
}

// Function to retrieve data from the "itemList" collection
async function getDataFromCollection1() {
  try {
    const collection = mongoose.connection.db.collection('itemList');
    const data = await collection.find({}).toArray();
    return data;
  } catch (error) {
    console.error('Error retrieving data:', error);
    return [];
  }
}

// Function to retrieve data from the "itemList" collection with ItemCategory: 2
async function getDataFromCollection(category) {
    try {
      const collection = mongoose.connection.db.collection('itemList');
      const data = await collection.find({ ItemCategory: category }).toArray();
      return data;
    } catch (error) {
      console.error('Error retrieving data:', error);
      return [];
    }
  }

// Function to retrieve data from the "itemList" collection with ItemCategory: 2
async function getImageUrlFromCollection(category) {
    try {
      const collection = mongoose.connection.db.collection('itemList');
      const data = await collection.find({ ItemCategory: category }).project({ _id: 0, ImageUrl: 1 }).toArray();
      return data;
    } catch (error) {
      console.error('Error retrieving data:', error);
      return [];
    }
  }
  
// Function to insert data into the "itemList" collection
async function insertDataIntoCollection(data) {
    try {
      const collection = mongoose.connection.db.collection('itemList');
      await collection.insertOne(data);
      console.log('Data inserted into "itemList" collection');
    } catch (error) {
      console.error('Error inserting data:', error);
    }
  }
  


/**
 * @swagger
 * /api/allItems:
 *   get:
 *     summary: Get data.
 *     description: Retrieve data from the API.
 *     parameters:
 *       - in: query
 *         name: category
 *         schema:
 *           type: integer
 *         required: true
 *         description: Category number
 *     responses:
 *       200:
 *         description: Successful response.
 */

// get all items list according to the category number
app.get('/api/allItems', async (req, res) => {
  try {
    await connectToDatabase();
    const category = Number(req.query.category); // Access the category query parameter
    const data = await getDataFromCollection(category); // Pass the category to the getDataFromCollection function

    res.json(data);
  } catch (error) {
    console.error('Error:', error);
    res.status(500).json({ error: 'Internal Server Error' });
  } finally {
    // Close the MongoDB connection
    mongoose.connection.close();
  }
});

  
/**
 * @swagger
 * /api/allItemsImageUrl:
 *   get:
 *     summary: Get item image URL.
 *     description: Retrieve item image URL based on the category number.
 *     parameters:
 *       - in: query
 *         name: category
 *         schema:
 *           type: integer
 *         required: true
 *         description: Category number
 *     responses:
 *       200:
 *         description: Successful response.
 */

// get item image URL only according to the category number
app.get('/api/allItemsImageUrl', async (req, res) => {
  try {
    await connectToDatabase();
    const category = Number(req.query.category); // Access the category query parameter
    const data = await getImageUrlFromCollection(category); // Pass the category to the getImageUrlFromCollection function

    res.json(data);
  } catch (error) {
    console.error('Error:', error);
    res.status(500).json({ error: 'Internal Server Error' });
  } finally {
    // Close the MongoDB connection
    mongoose.connection.close();
  }
});

// Define a route for the POST request
/**
 * @swagger
 * /api/addItems:
 *   post:
 *     summary: Add items to the collection.
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             type: object
 *             properties:
 *               items:
 *                 type: array
 *                 items:
 *                   type: string
 *             example:
 *               items: ["item1", "item2"]
 *     responses:
 *       201:
 *         description: Resource created successfully.
 *       500:
 *         description: Internal Server Error.
 */  
// POST data
app.post('/api/addItems', async (req, res) => {post
    try {
        const data  = req.body;

      
        console.log(typeof data);
        
        console.log('data set :', data);
        const dataset= json
        await insertDataIntoCollection(data)
      res.status(201).json({ message: 'Resource created successfully' });
    } catch (error) {
      console.error('Error:', error);
      res.status(500).json({ error: 'Internal Server Error' });
    }
  });

  app.get('/api', (req, res) => {
    res.send('Hello, from docker!');
  });

// Start the server
app.listen(port, () => {
  console.log(`Server is listening on port ${port}`);
});
