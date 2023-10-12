package com.example.predictionapp;

import android.content.DialogInterface;
import android.content.Intent;
import android.content.SharedPreferences;
import android.content.res.ColorStateList;
import android.graphics.Color;
import android.os.Build;
import android.os.Bundle;
import android.util.Log;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.Toast;

import androidx.annotation.NonNull;
import androidx.annotation.RequiresApi;
import androidx.appcompat.app.AlertDialog;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.content.ContextCompat;

import com.google.android.material.bottomnavigation.BottomNavigationView;
import com.google.android.material.textfield.TextInputEditText;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;

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

            FileInputStream fis = openFileInput("user_data.json");
            InputStreamReader isr = new InputStreamReader(fis);
            BufferedReader br = new BufferedReader(isr);
            StringBuilder sb = new StringBuilder();
            String line;
            while ((line = br.readLine()) != null) {
                sb.append(line);
            }
            br.close();
            isr.close();
            fis.close();

            // Parse JSON data
            JSONObject userData = new JSONObject(sb.toString());
            String name = userData.getString("name");
            String gender = userData.getString("gender");
            String email = userData.getString("email");
            String age = userData.getString("age");
            String city = userData.getString("city");

            // Populate UI elements with user data
            TextInputEditText etName = findViewById(R.id.etName);
            TextInputEditText etGender = findViewById(R.id.etGender);
            TextInputEditText etEmail = findViewById(R.id.etEmail);
            TextInputEditText etAge = findViewById(R.id.etAge);
            TextInputEditText etCity = findViewById(R.id.etCity);

            etName.setText(name);
            etGender.setText(gender);
            etEmail.setText(email);
            etAge.setText(age);
            etCity.setText(city);
        } catch (JSONException e) {
            e.printStackTrace();
        } catch (FileNotFoundException e) {
            throw new RuntimeException(e);
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
        ImageView ivLogout = findViewById(R.id.ivLogout);
        ivLogout.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                showLogoutConfirmationDialog(v);
            }
        });
        Button btnDeleteAccount = findViewById(R.id.btnDeleteAccount); // Replace with your button ID
        btnDeleteAccount.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                showDeleteAccountConfirmationDialog(v);
            }
        });


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
    private void deleteAccountAndRedirect() {
        try {
            String fileName = "user_data.json";
            File file = new File(getFilesDir(), fileName);

            if (file.exists()) {
                if (file.delete()) {
                    SharedPreferences sharedPreferences = getSharedPreferences("user_prefs", MODE_PRIVATE);
                    SharedPreferences.Editor editor = sharedPreferences.edit();

                    // Clear user data and set login state to false
                    editor.clear();
                    editor.putBoolean("isLoggedIn", false);

                    editor.apply();
                    Intent intent = new Intent(this, GetStartedActivity.class);
                    startActivity(intent);
                    finish();
                } else {
                    Log.i("DELETE ACCOUNT", "FAILED TO DELETE USER ACCOUNT");
                }
            } else {
                Log.i("DELETE ACCOUNT", "NO USER TO DELETE");
            }

        } catch (Exception e) {
            e.printStackTrace();
        }
    }


    private void showDeleteAccountConfirmationDialog(View view) {
        AlertDialog.Builder builder = new AlertDialog.Builder(this);
        builder.setTitle("Delete Account");
        builder.setMessage("Are you sure you want to delete your account?");
        builder.setPositiveButton("Delete", new DialogInterface.OnClickListener() {
            @Override
            public void onClick(DialogInterface dialog, int which) {
                // Perform logout action here
                deleteAccountAndRedirect();
            }
        });
        builder.setNegativeButton("Cancel", null);
        AlertDialog dialog = builder.create();
        dialog.show();
    }


}

