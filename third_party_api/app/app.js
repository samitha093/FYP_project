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
*             $ref: '#/components/schemas/Item'
*     responses:
*       201:
*         description: Resource created successfully.
*       500:
*         description: Internal Server Error.
*/

const Item = require('./models/Item'); // Assuming you have a Mongoose model for your items

// Function to save an Item in the "itemList" collection
async function saveItemToCollection(item) {
  try {
    const collection = mongoose.connection.db.collection('itemList');
    await collection.insertOne(item);
  } catch (error) {
    console.error('Error saving item:', error);
    throw error;
  }
}
// Function to update an Item in the "itemList" collection based on _id
// Function to update an Item by ID in the "itemList" collection
async function updateItemById(itemId, updatedItem) {
  try {
    const collection = mongoose.connection.db.collection('itemList');
    const integerNumber = parseInt(itemId, 10);

    const result = await collection.updateOne({ ItemId: integerNumber }, { $set: updatedItem });
    console.log('Item updated successfully...');
    return result.modifiedCount > 0; // Check if any document was modified
    return true;
  } catch (error) {
    console.error('Error updating item:', error);
    throw error;
  }
}
// POST data
// Function to check if an item with the given ItemId exists in the "itemList" collection
async function doesItemIdExist(itemId) {
  try {
    const collection = mongoose.connection.db.collection('itemList');

    // Find the item by ItemId
    const query = { ItemId: itemId };
    const item = await collection.findOne(query);

    return item !== null; // Return true if the item exists, false otherwise

  } catch (error) {
    console.error('Error checking item existence:', error);
    throw error;
  }
}

// POST data
app.post('/api/addItems', async (req, res) => {
  try {
    const data = req.body;
    console.log('Data received:', data);

    const itemId = data.ItemId;

    await connectToDatabase(); // Connect to the database using Mongoose

    // Check if the item with the given ItemId exists
    const itemExists = await doesItemIdExist(itemId);

    // Create a new Item object
    const newItem = new Item({
      ItemId: data.ItemId,
      ItemName: data.ItemName,
      ItemCategory: data.ItemCategory,
      ItemPrice: data.ItemPrice,
      ImageUrl: data.ImageUrl,
    });
    var status ="created";
    // Save or update the item in the database
    if (itemExists) {
      // Item exists, update it
      console.log(" it exits");
      console.log(newItem.ItemId);
      console.log(newItem);
      const updatedItem = {
        ItemId: data.ItemId,
        ItemName: data.ItemName,
        ItemCategory: data.ItemCategory,
        ItemPrice: data.ItemPrice,
        ImageUrl: data.ImageUrl,
      };
      await updateItemById(updatedItem.ItemId, updatedItem);
      status ="updated";
    } else {
      console.log(" Not exits");
      console.log(newItem.ItemId);
      console.log(newItem);
      // Item does not exist, insert it
     await saveItemToCollection(newItem);

    }

    // Close the MongoDB connection
    mongoose.connection.close();

    res.status(201).json({ message: `Resource ${status} successfully` });
  } catch (error) {
    console.error('Error:', error);
    res.status(500).json({ error: 'Internal Server Error' });
  }
});


  app.get('/api', (req, res) => {
    res.send('Hello, from docker!');
  });

/**
 * @swagger
 * /api/updateItem/{id}:
 *   put:
 *     summary: Update an item in the collection.
 *     parameters:
 *       - in: path
 *         name: id
 *         required: true
 *         schema:
 *           type: string
 *         description: The ID of the item to update.
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             $ref: '#/components/schemas/UpdateItemInput'
 *     responses:
 *       200:
 *         description: Item updated successfully.
 *       500:
 *         description: Internal Server Error.
 */


// PUT data to update an Item
app.put('/api/updateItem/:id', async (req, res) => {
  try {
    const itemId = req.params.id;
    const data = req.body;


    // Create a new Item object
    const updatedItem = {
      ItemId: data.ItemId,
      ItemName: data.ItemName,
      ItemCategory: data.ItemCategory,
      ItemPrice: data.ItemPrice,
      ImageUrl: data.ImageUrl,
    };
    console.log(itemId);
    console.log(updatedItem);
    await connectToDatabase(); // Connect to the database using Mongoose

    // Update the item in the database and check the result
    const isUpdated = await updateItemById(itemId, updatedItem);

    // Close the MongoDB connection
    mongoose.connection.close();

    if (isUpdated) {
      res.json({ message: 'Item updated successfully' });
    } else {
      res.status(404).json({ error: 'Item not found or no changes made' });
    }
  } catch (error) {
    console.error('Error:', error);
    res.status(500).json({ error: 'Internal Server Error' });
  }
});




/**
 * @swagger
 * /api/deleteItem/{id}:
 *   delete:
 *     summary: Delete an item by ID.
 *     parameters:
 *       - in: path
 *         name: id
 *         required: true
 *         schema:
 *           type: string
 *         description: The ID of the item to delete.
 *     responses:
 *       200:
 *         description: Item deleted successfully.
 *       500:
 *         description: Internal Server Error.
 */
// Function to delete an item from the "itemList" collection by ID
async function deleteItemFromCollection(itemId) {
  try {
    const collection = mongoose.connection.db.collection('itemList');
    const integerNumber = parseInt(itemId, 10);

    const result = await collection.deleteOne({ ItemId: integerNumber });

    if (result.deletedCount > 0) {
      return true; // Item deleted successfully
    } else {
      return false; // Item not found or no changes made
    }
  } catch (error) {
    console.error('Error deleting item:', error);
    throw error;
  }
}

// DELETE an item by ID
app.delete('/api/deleteItem/:id', async (req, res) => {
  try {
    const itemId = req.params.id;
    console.log('Id:', itemId);
    await connectToDatabase(); // Connect to the database using Mongoose

    // Delete the item from the database and check the result
    const isDeleted = await deleteItemFromCollection(itemId);

    // Close the MongoDB connection
    mongoose.connection.close();

    if (isDeleted) {
      res.json({ message: 'Item deleted successfully' });
    } else {
      res.status(404).json({ error: 'Item not found or no changes made' });
    }
  } catch (error) {
    console.error('Error:', error);
    res.status(500).json({ error: 'Internal Server Error' });
  }
});




// Start the server
app.listen(port, () => {
  console.log(`Server is listening on port ${port}`);
});
