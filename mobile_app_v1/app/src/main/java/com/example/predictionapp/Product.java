package com.example.predictionapp;

public class Product {
    private String imageUrl;
    private String itemName;
    private String itemPrice;

    public Product(String imageUrl, String itemName, String itemPrice) {
        this.imageUrl = imageUrl;
        this.itemName = itemName;
        this.itemPrice = itemPrice;
    }

    public String getImageUrl() {
        return imageUrl;
    }

    public String getItemName() {
        return itemName;
    }

    public String getItemPrice() {
        return itemPrice;
    }


}
