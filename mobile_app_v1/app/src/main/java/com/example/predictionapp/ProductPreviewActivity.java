package com.example.predictionapp;

import android.annotation.SuppressLint;
import android.content.Intent;
import android.content.SharedPreferences;
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


        recyclerView = findViewById(R.id.recyclerView);
        recyclerView.setLayoutManager(new GridLayoutManager(this, 2)); // 2 columns per row

        SharedPreferences sharedPreferences = getSharedPreferences("MyPrefs", MODE_PRIVATE);
        int predictedCategoryNumber = sharedPreferences.getInt("predictedCategory", -1);

        if (predictedCategoryNumber != -1) {
            new FetchDataTask().execute(predictedCategoryNumber);
        }


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
