package com.example.predictionapp;

import android.annotation.SuppressLint;
import android.content.DialogInterface;
import android.content.Intent;
import android.content.SharedPreferences;
import android.content.res.ColorStateList;
import android.graphics.Color;
import android.os.AsyncTask;
import android.os.Build;
import android.os.Bundle;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.ImageView;
import android.widget.ProgressBar;

import androidx.annotation.NonNull;
import androidx.annotation.RequiresApi;
import androidx.appcompat.app.AlertDialog;
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
    private ProgressBar loadingIndicator;

    @SuppressLint("MissingInflatedId")
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.product_preview);
        ImageView ivLogout = findViewById(R.id.ivLogout);
        loadingIndicator = findViewById(R.id.loadingIndicator);

        ivLogout.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                showLogoutConfirmationDialog(v);
            }
        });
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

        List<Product> productList = new ArrayList<>();
        JSONArray jsonArray;

        try {
            String yourJsonString = "[\n" +
                    "  {\n" +
                    "    \"_id\": \"6426898c53d76ec9814b08a3\",\n" +
                    "    \"ItemId\": 7,\n" +
                    "    \"ItemName\": \"Tomatoes\",\n" +
                    "    \"ItemCategory\": 2,\n" +
                    "    \"ItemPrice\": 30,\n" +
                    "    \"ImageUrl\": \"https://savecobradford.co.uk/cdn/shop/products/Tomatoes.jpg?v=1590628551&width=1200\"\n" +
                    "  },\n" +
                    "  {\n" +
                    "    \"_id\": \"6426898c53d76ec9814b08a6\",\n" +
                    "    \"ItemId\": 10,\n" +
                    "    \"ItemName\": \"Mango\",\n" +
                    "    \"ItemCategory\": 2,\n" +
                    "    \"ItemPrice\": 25,\n" +
                    "    \"ImageUrl\": \"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRDO0Aov4hDGIXdZKxJ12lMckr7o6nwaCvhRQ&usqp=CAU\"\n" +
                    "  },\n" +
                    "  {\n" +
                    "    \"_id\": \"64745a6ef34d023c80be52ff\",\n" +
                    "    \"ItemId\": 25,\n" +
                    "    \"ImageUrl\": \"https://european-seed.com/wp-content/uploads/2022/02/GettyImages-523635727-696x696-1.jpg\",\n" +
                    "    \"ItemCategory\": 2,\n" +
                    "    \"ItemName\": \"Cabbage\",\n" +
                    "    \"ItemPrice\": 35\n" +
                    "  },\n" +
                    "  {\n" +
                    "    \"_id\": \"64745ae13c71af8807163dcb\",\n" +
                    "    \"ItemId\": 25,\n" +
                    "    \"ItemName\": \"Ambewela Milk\",\n" +
                    "    \"ImageUrl\": \"https://backend.lassana.com/images//products/18nste0008--1675161553.jpg\",\n" +
                    "    \"ItemCategory\": 2,\n" +
                    "    \"ItemPrice\": 420\n" +
                    "  },\n" +
                    "  {\n" +
                    "    \"_id\": \"64745beac3ef906f53c92814\",\n" +
                    "    \"ItemId\": 26,\n" +
                    "    \"ItemCategory\": 2,\n" +
                    "    \"ImageUrl\": \"https://happycow.at/media/gallery_img_161/medium/HC120g_Freisteller.jpg?ck=64c52ccb9312d\",\n" +
                    "    \"ItemName\": \"Happycow Cheese\",\n" +
                    "    \"ItemPrice\": 1200\n" +
                    "  },\n" +
                    "  {\n" +
                    "    \"_id\": \"64745c8576213711041e810e\",\n" +
                    "    \"ItemId\": 27,\n" +
                    "    \"ItemName\": \"Burger Bun\",\n" +
                    "    \"ItemCategory\": 2,\n" +
                    "    \"ItemPrice\": 350,\n" +
                    "    \"ImageUrl\": \"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT30cuUC0X8JWlcFAik1zHiQvLTWDPpSpa5Xg&usqp=CAU\"\n" +
                    "  },\n" +
                    "  {\n" +
                    "    \"_id\": \"64745ca076213711041e810f\",\n" +
                    "    \"ItemId\": 27,\n" +
                    "    \"ItemName\": \"Lindt milk\",\n" +
                    "    \"ImageUrl\": \"https://supersavings.lk/wp-content/uploads/2023/04/lindt-classic-recipe-milk.jpg\",\n" +
                    "    \"ItemCategory\": 2,\n" +
                    "    \"ItemPrice\": 2420\n" +
                    "  },\n" +
                    "  {\n" +
                    "    \"_id\": \"64746535700adb75d04719e3\",\n" +
                    "    \"ItemId\": 30,\n" +
                    "    \"ItemName\": \"Munchee Kome\",\n" +
                    "    \"ImageUrl\": \"https://objectstorage.ap-mumbai-1.oraclecloud.com/n/softlogicbicloud/b/cdn/o/products/114810--01--1623926482.webp\",\n" +
                    "    \"ItemCategory\": 2,\n" +
                    "    \"ItemPrice\": 350\n" +
                    "  },\n" +
                    "  {\n" +
                    "    \"_id\": \"64746535700adb75d04719e3\",\n" +
                    "    \"ItemId\": 30,\n" +
                    "    \"ItemName\": \"Munchee Kome\",\n" +
                    "    \"ImageUrl\": \"https://objectstorage.ap-mumbai-1.oraclecloud.com/n/softlogicbicloud/b/cdn/o/products/114810--01--1623926482.webp\",\n" +
                    "    \"ItemCategory\": 2,\n" +
                    "    \"ItemPrice\": 350\n" +
                    "  }\n" +
                    "]\n";

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
        recyclerView.setAdapter(adapter);

      /*  // Get the predicted category number (replace this with your actual prediction logic)
        int predictedCategoryNumber = 2; // Example category number

        // Fetch data from API based on predicted category number
        new FetchDataTask().execute(predictedCategoryNumber);*/

        //-------new update ------------
        /*SharedPreferences sharedPreferences = getSharedPreferences("MyPrefs", MODE_PRIVATE);
        int predictedCategoryNumber = sharedPreferences.getInt("predictedCategory", -1);

        if (predictedCategoryNumber != -1) {
            new FetchDataTask().execute(predictedCategoryNumber);
        }*/

        bottomNavigationView = findViewById(R.id.bottom_navigation);

        bottomNavigationView.setOnNavigationItemSelectedListener(
                new BottomNavigationView.OnNavigationItemSelectedListener()

                {
                    @RequiresApi(api = Build.VERSION_CODES.O)
                    @Override
                    public boolean onNavigationItemSelected (@NonNull MenuItem item){
                        BottomNavigationView navigationView = findViewById(R.id.bottom_navigation);
                        Menu menu = navigationView.getMenu();

                        // Reset icon tint of all items to the default color
                        for (int i = 0; i < menu.size(); i++) {
                            MenuItem menuItem = menu.getItem(i);
                            menuItem.setIconTintList(null); // Reset to default color
                        }

                        // Set the icon tint of the selected item to the desired color
                        item.setIconTintList(ColorStateList.valueOf(Color.parseColor("#87978F")));
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
        protected void onPreExecute() {
            super.onPreExecute();
            loadingIndicator.setVisibility(View.VISIBLE); // Show the loading indicator
        }
        @Override
        protected void onPostExecute(String result) {
            super.onPostExecute(result);
            // Hide the loading indicator
            loadingIndicator.setVisibility(View.GONE);
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
    public void logout() {
        // Clear any user session or data here, if needed

        SharedPreferences sharedPreferences = getSharedPreferences("user_prefs", MODE_PRIVATE);
        SharedPreferences.Editor editor = sharedPreferences.edit();

        // Clear user data and set login state to false
        editor.clear();
        editor.putBoolean("isLoggedIn", false);

        editor.apply();
        // Navigate back to the GetStartedActivity or LoginActivity
        Intent intent = new Intent(this, GetStartedActivity.class); // Change to your desired destination activity
        intent.setFlags(Intent.FLAG_ACTIVITY_CLEAR_TOP | Intent.FLAG_ACTIVITY_NEW_TASK);
        startActivity(intent);
        finish(); // Optional, depending on your navigation flow
    }
    private void showLogoutConfirmationDialog(View view) {
        AlertDialog.Builder builder = new AlertDialog.Builder(this);
        builder.setTitle("Logout");
        builder.setMessage("Are you sure you want to logout?");
        builder.setPositiveButton("Logout", new DialogInterface.OnClickListener() {
            @Override
            public void onClick(DialogInterface dialog, int which) {
                // Perform logout action here
                logout();
            }
        });
        builder.setNegativeButton("Cancel", null);
        AlertDialog dialog = builder.create();
        dialog.show();
    }

}
