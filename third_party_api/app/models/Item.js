const mongoose = require('mongoose');

const itemSchema = new mongoose.Schema({
  ItemId: {
    type: Number,
    required: true,
  },
  ItemName: {
    type: String,
    required: true,
  },
  ItemCategory: {
    type: Number,
    required: true,
  },
  ItemPrice: {
    type: Number,
    required: true,
  },
  ImageUrl: {
    type: String,
    required: true,
  },
});

const Item = mongoose.model('Item', itemSchema);

module.exports = Item;
