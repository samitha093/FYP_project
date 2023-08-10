package com.example.predictionapp;

import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.view.MenuItem;
import android.view.View;
import android.widget.TextView;
import android.widget.Toast;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;

import com.google.android.material.bottomnavigation.BottomNavigationView;

import org.json.JSONException;
import org.json.JSONObject;

public class UserProfileActivity extends AppCompatActivity {
    private BottomNavigationView bottomNavigationView;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.profile_layout);

        // Retrieve user's JSON data from Intent extras
        Intent intent = getIntent();


        //Log.i("STORED USER DATA", userDataJsonString);

            try {
                String userDataJsonString = intent.getStringExtra("userData");
                // Parse user's JSON data
                JSONObject userData = new JSONObject(userDataJsonString);

                // Populate UI elements with user's JSON data
                TextView tvName = findViewById(R.id.tvName);
                TextView tvGender = findViewById(R.id.tvGender);
                TextView tvEmail = findViewById(R.id.tvEmail);
                TextView tvAge = findViewById(R.id.tvAge);
                TextView tvCity = findViewById(R.id.tvCity);

                tvName.setText("Name: " + userData.optString("name"));
                tvGender.setText("Gender: " + userData.optString("gender"));
                tvEmail.setText("Email: " + userData.optString("email"));
                tvAge.setText("Age: " + userData.optString("age"));
                tvCity.setText("City: " + userData.optString("city"));
            } catch (JSONException e) {
                e.printStackTrace();
            }


        bottomNavigationView = findViewById(R.id.bottom_navigation);

        bottomNavigationView.setOnNavigationItemSelectedListener(
                new BottomNavigationView.OnNavigationItemSelectedListener()

                {
                    @Override
                    public boolean onNavigationItemSelected (@NonNull MenuItem item){
                        switch (item.getItemId()) {
                            case R.id.menu_scan:
                                startActivity(new Intent(UserProfileActivity.this, ScanQRCodeActivity.class));
                                return true;
                            case R.id.menu_me:
                                return true;
                            case R.id.menu_just_for_you:
                                startActivity(new Intent(UserProfileActivity.this, ProductPreviewActivity.class));
                                return true;
                        }
                        return false;
                    }
                });
    }
    public void logout(View view) {
        // Clear any user session or data here, if needed

        // Navigate back to the GetStartedActivity or LoginActivity
        Intent intent = new Intent(this, GetStartedActivity.class); // Change to your desired destination activity
        intent.setFlags(Intent.FLAG_ACTIVITY_CLEAR_TOP | Intent.FLAG_ACTIVITY_NEW_TASK);
        startActivity(intent);
        finish(); // Optional, depending on your navigation flow
    }

}

