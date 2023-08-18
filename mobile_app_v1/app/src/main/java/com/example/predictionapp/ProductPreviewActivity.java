package com.example.predictionapp;

import android.annotation.SuppressLint;
import android.content.Intent;
import android.os.AsyncTask;
import android.os.Bundle;
import android.view.MenuItem;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;
import androidx.recyclerview.widget.GridLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import com.google.android.material.bottomnavigation.BottomNavigationView;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

public class ProductPreviewActivity extends AppCompatActivity {

    private RecyclerView recyclerView;
    private ProductAdapter adapter;
    private BottomNavigationView bottomNavigationView;

    @SuppressLint("MissingInflatedId")
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.product_preview);

        /*recyclerView = findViewById(R.id.recyclerView);
        recyclerView.setLayoutManager(new GridLayoutManager(this, 2)); // 2 columns per row

        // Sample list of image URLs
        List<String> imageUrlList = new ArrayList<>();
        imageUrlList.add("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRtMRhsTGndOqXwFe3T6PQBpqOvxKOcbG1AYA&usqp=CAU");
        imageUrlList.add("https://static.beautytocare.com/media/catalog/product/cache/global/image/650x650/85e4522595efc69f496374d01ef2bf13/l/-/l-oreal-professionnel-serie-expert-chroma-creme-blue-shampoo-300ml.jpg");
        imageUrlList.add("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRtMRhsTGndOqXwFe3T6PQBpqOvxKOcbG1AYA&usqp=CAU");
        imageUrlList.add("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRtMRhsTGndOqXwFe3T6PQBpqOvxKOcbG1AYA&usqp=CAU");
        imageUrlList.add("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRtMRhsTGndOqXwFe3T6PQBpqOvxKOcbG1AYA&usqp=CAU");
        imageUrlList.add("https://static.beautytocare.com/media/catalog/product/cache/global/image/650x650/85e4522595efc69f496374d01ef2bf13/l/-/l-oreal-professionnel-serie-expert-chroma-creme-blue-shampoo-300ml.jpg");
        imageUrlList.add("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRtMRhsTGndOqXwFe3T6PQBpqOvxKOcbG1AYA&usqp=CAU");
        imageUrlList.add("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRtMRhsTGndOqXwFe3T6PQBpqOvxKOcbG1AYA&usqp=CAU");

        adapter = new ProductAdapter(imageUrlList);
        recyclerView.setAdapter(adapter);*/

        recyclerView = findViewById(R.id.recyclerView);
        recyclerView.setLayoutManager(new GridLayoutManager(this, 2)); // 2 columns per row

        /*List<Product> productList = new ArrayList<>();
        JSONArray jsonArray;

        try {
            String yourJsonString = "[\n" +
                    "  {\n" +
                    "    \"_id\": \"6426898c53d76ec9814b08a3\",\n" +
                    "    \"ItemId\": 7,\n" +
                    "    \"ItemName\": \"Tomatoes\",\n" +
                    "    \"ItemCategory\": 2,\n" +
                    "    \"ItemPrice\": 30,\n" +
                    "    \"ImageUrl\": \"https://www.onlinekade.lk/wp-content/uploads/2021/10/8901491101844-300x300.jpg\"\n" +
                    "  },\n" +
                    "  {\n" +
                    "    \"_id\": \"6426898c53d76ec9814b08a6\",\n" +
                    "    \"ItemId\": 10,\n" +
                    "    \"ItemName\": \"Ban Chips\",\n" +
                    "    \"ItemCategory\": 2,\n" +
                    "    \"ItemPrice\": 25,\n" +
                    "    \"ImageUrl\": \"https://5.imimg.com/data5/ANDROID/Default/2020/10/YU/QD/UL/35343054/prod-20201011-0159397534769397062872599-jpg-500x500.jpg\"\n" +
                    "  },\n" +
                    "  {\n" +
                    "    \"_id\": \"6426898e53d76ec9814b08ac\",\n" +
                    "    \"ItemId\": 16,\n" +
                    "    \"ItemName\": \"Lettuce\",\n" +
                    "    \"ItemCategory\": 2,\n" +
                    "    \"ItemPrice\": 35,\n" +
                    "    \"ImageUrl\": \"https://cdn.takas.lk/media/catalog/product/cache/1/image/9df78eab33525d08d6e5fb8d27136e95/0/2/02_1.png\"\n" +
                    "  },\n" +
                    "  {\n" +
                    "    \"_id\": \"64745a6ef34d023c80be52ff\",\n" +
                    "    \"ItemId\": 25,\n" +
                    "    \"ImageUrl\": \"https://cdn.takas.lk/media/catalog/product/cache/1/image/9df78eab33525d08d6e5fb8d27136e95/0/2/02_1.png\",\n" +
                    "    \"ItemCategory\": 2,\n" +
                    "    \"ItemName\": \"Food 2\",\n" +
                    "    \"ItemPrice\": 35\n" +
                    "  },\n" +
                    "  {\n" +
                    "    \"_id\": \"64745ae13c71af8807163dcb\",\n" +
                    "    \"ItemId\": 25,\n" +
                    "    \"ItemName\": \"Food 3\",\n" +
                    "    \"ItemCategory\": 2,\n" +
                    "    \"ItemPrice\": 35,\n" +
                    "    \"ImageUrl\": \"https://cdn.takas.lk/media/catalog/product/cache/1/image/9df78eab33525d08d6e5fb8d27136e95/0/2/02_1.png\"\n" +
                    "  },\n" +
                    "  {\n" +
                    "    \"_id\": \"64745beac3ef906f53c92814\",\n" +
                    "    \"ItemId\": 26,\n" +
                    "    \"ImageUrl\": \"https://cdn.takas.lk/media/catalog/product/cache/1/image/9df78eab33525d08d6e5fb8d27136e95/0/2/02_1.png\",\n" +
                    "    \"ItemCategory\": 2,\n" +
                    "    \"ItemName\": \"Food 4\",\n" +
                    "    \"ItemPrice\": 35\n" +
                    "  },\n" +
                    "  {\n" +
                    "    \"_id\": \"64745c8576213711041e810e\",\n" +
                    "    \"ItemId\": 27,\n" +
                    "    \"ItemName\": \"Food 5\",\n" +
                    "    \"ItemCategory\": 2,\n" +
                    "    \"ItemPrice\": 35,\n" +
                    "    \"ImageUrl\": \"https://cdn.takas.lk/media/catalog/product/cache/1/image/9df78eab33525d08d6e5fb8d27136e95/0/2/02_1.png\"\n" +
                    "  },\n" +
                    "  {\n" +
                    "    \"_id\": \"64745ca076213711041e810f\",\n" +
                    "    \"ItemId\": 27,\n" +
                    "    \"ItemName\": \"Food 6\",\n" +
                    "    \"ItemCategory\": 2,\n" +
                    "    \"ItemPrice\": 35,\n" +
                    "    \"ImageUrl\": \"https://cdn.takas.lk/media/catalog/product/cache/1/image/9df78eab33525d08d6e5fb8d27136e95/0/2/02_1.png\"\n" +
                    "  },\n" +
                    "  {\n" +
                    "    \"_id\": \"64746535700adb75d04719e3\",\n" +
                    "    \"ItemId\": 30,\n" +
                    "    \"ItemName\": \"jFood 8\",\n" +
                    "    \"ItemCategory\": 2,\n" +
                    "    \"ItemPrice\": 35,\n" +
                    "    \"ImageUrl\": \"https://cdn.takas.lk/media/catalog/product/cache/1/image/9df78eab33525d08d6e5fb8d27136e95/0/2/02_1.png\"\n" +
                    "  },\n" +
                    "  {\n" +
                    "    \"_id\": \"647468b7ec12c356cb40f3c7\",\n" +
                    "    \"ItemId\": 31,\n" +
                    "    \"ItemName\": \"Food 6\",\n" +
                    "    \"ItemCategory\": 2,\n" +
                    "    \"ItemPrice\": 35,\n" +
                    "    \"ImageUrl\": \"https://cdn.takas.lk/media/catalog/product/cache/1/image/9df78eab33525d08d6e5fb8d27136e95/0/2/02_1.png\"\n" +
                    "  }\n" +
                    "]";

            jsonArray = new JSONArray(yourJsonString);

            for (int i = 0; i < jsonArray.length(); i++) {
                JSONObject jsonObject = jsonArray.getJSONObject(i);
                String imageUrl = jsonObject.getString("ImageUrl");
                String itemName = jsonObject.getString("ItemName");
                String itemPrice = jsonObject.getString("ItemPrice");

                Product product = new Product(imageUrl, itemName, "Rs. "+itemPrice+".00");
                productList.add(product);
            }
        } catch (JSONException e) {
            e.printStackTrace();
        }

        adapter = new ProductAdapter(productList);
        recyclerView.setAdapter(adapter);*/

        // Get the predicted category number (replace this with your actual prediction logic)
        int predictedCategoryNumber = 2; // Example category number

        // Fetch data from API based on predicted category number
        new FetchDataTask().execute(predictedCategoryNumber);

        bottomNavigationView = findViewById(R.id.bottom_navigation);
        bottomNavigationView.setOnNavigationItemSelectedListener(
                new BottomNavigationView.OnNavigationItemSelectedListener()

                {
                    @Override
                    public boolean onNavigationItemSelected (@NonNull MenuItem item){
                        switch (item.getItemId()) {
                            case R.id.menu_scan:
                                startActivity(new Intent(ProductPreviewActivity.this, ScanQRCodeActivity.class));
                                return true;
                            case R.id.menu_me:
                                startActivity(new Intent(ProductPreviewActivity.this, UserProfileActivity.class));
                                return true;
                            case R.id.menu_just_for_you:
                                return true;
                        }
                        return false;
                    }
                });
    }
    private class FetchDataTask extends AsyncTask<Integer, Void, String> {

        @Override
        protected String doInBackground(Integer... categoryNumbers) {
            if (categoryNumbers.length > 0) {
                int categoryNumber = categoryNumbers[0];
                try {
                    return ApiClient.fetchDataByCategory(categoryNumber);
                } catch (IOException e) {
                    e.printStackTrace();
                    return null;
                }
            }
            return null;
        }

        @Override
        protected void onPostExecute(String result) {
            super.onPostExecute(result);

            if (result != null) {
                try {
                    List<Product> productList = parseJson(result);
                    adapter = new ProductAdapter(productList);
                    recyclerView.setAdapter(adapter);
                } catch (JSONException e) {
                    e.printStackTrace();
                }
            }
        }
        private List<Product> parseJson(String json) throws JSONException {
            List<Product> productList = new ArrayList<>();
            JSONArray jsonArray = new JSONArray(json);

            for (int i = 0; i < jsonArray.length(); i++) {
                JSONObject jsonObject = jsonArray.getJSONObject(i);
                String imageUrl = jsonObject.getString("ImageUrl");
                String itemName = jsonObject.getString("ItemName");
                String itemPrice = jsonObject.getString("ItemPrice");

                Product product = new Product(imageUrl, itemName, "Rs. "+ itemPrice +".00");
                productList.add(product);
            }

            return productList;
        }
    }

}
