package com.example.predictionapp;

import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStreamReader;

public class LoginActivity extends AppCompatActivity {

    private EditText etUsername;
    private EditText etPassword;
    private Button btnLogin;
    private Button btnSignUp;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.login_layout);

        etUsername = findViewById(R.id.etEmailUsername); // Replace with your username EditText ID
        etPassword = findViewById(R.id.etPassword); // Replace with your password EditText ID
        btnLogin = findViewById(R.id.btnLogin); // Replace with your login button ID
        btnSignUp = findViewById(R.id.btnSignUp);

        btnLogin.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                // Get entered username and password
                String username = etUsername.getText().toString();
                String password = etPassword.getText().toString();

                // Validate credentials
                if (isValidCredentials(username, password)) {

                    Toast.makeText(LoginActivity.this, "user is logged in successfully", Toast.LENGTH_SHORT).show();
                    // Successful login, navigate to the next activity
                    navigateToMainActivity();
                } else {
                    // Failed login, show error message
                    Toast.makeText(LoginActivity.this, "Invalid username or password", Toast.LENGTH_SHORT).show();
                    // Clear password field and request focus
                    etPassword.getText().clear();
                    etPassword.requestFocus();
                }
            }
        });
        btnSignUp.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent intent = new Intent(LoginActivity.this, SignUpActivity.class);
                startActivity(intent);
            }
        });
    }

    private boolean isValidCredentials(String enteredUsername, String enteredPassword) {
        // Load stored user data (from JSON file or other storage mechanism)
        JSONArray userList = loadUserListFromJson(); // Implement this method to load user data
        Log.i("USER LIST", String.valueOf(userList));
        for (int i = 0; i < userList.length(); i++) {
            try {
                JSONObject user = userList.getJSONObject(i);
                String storedUsername = user.optString("email");
                String storedPassword = user.optString("password");

                // Compare entered credentials with stored data
                if (enteredUsername.equals(storedUsername) && enteredPassword.equals(storedPassword)) {
                    Log.i("ENTERED USER DATA", "UN: "+enteredUsername + " PW: "+ enteredPassword);
                    Log.i("STORED USER DATA", "UN: "+storedUsername + " PW: "+ storedPassword);
                    JSONObject userData = user;

                    // Launch ScanQRActivity and pass user's JSON data
                    Intent userProfileIntent = new Intent(LoginActivity.this, UserProfileActivity.class);
                    userProfileIntent.putExtra("userData", userData.toString());
                    startActivity(userProfileIntent);


                    return true; // Credentials match, grant access
                }
            } catch (JSONException e) {
                e.printStackTrace();
            }
        }

        return false; // No match found, validation failed
    }
    private JSONArray loadUserListFromJson() {
        JSONArray userList = new JSONArray();

        try {
            // Open the user data JSON file for reading
            FileInputStream inputStream = openFileInput("user_data.json");
            InputStreamReader inputStreamReader = new InputStreamReader(inputStream);
            BufferedReader bufferedReader = new BufferedReader(inputStreamReader);
            String line;

            // Read the JSON data from the file line by line
            while ((line = bufferedReader.readLine()) != null) {
                try {
                    JSONObject user = new JSONObject(line);
                    userList.put(user);
                } catch (JSONException e) {
                    e.printStackTrace();
                }
            }

            // Close the file streams
            bufferedReader.close();
            inputStreamReader.close();
            inputStream.close();

        } catch (IOException e) {
            e.printStackTrace();
        }

        return userList;
    }

    /*private JSONArray loadUserListFromJson() {
        JSONArray userList = new JSONArray();

        try {
            // Open the user data JSON file for reading
            FileInputStream inputStream = openFileInput("user_data.json");
            InputStreamReader inputStreamReader = new InputStreamReader(inputStream);
            BufferedReader bufferedReader = new BufferedReader(inputStreamReader);
            StringBuilder stringBuilder = new StringBuilder();
            String line;

            // Read the JSON data from the file
            while ((line = bufferedReader.readLine()) != null) {
                stringBuilder.append(line);
            }

            // Close the file streams
            bufferedReader.close();
            inputStreamReader.close();
            inputStream.close();

            // Parse the JSON data into a JSONArray
            userList = new JSONArray(stringBuilder.toString());

        } catch (IOException | JSONException e) {
            e.printStackTrace();
        }

        return userList;
    }*/


    private void navigateToMainActivity() {
        // Replace MainActivity.class with the desired activity to navigate to
        Intent intent = new Intent(LoginActivity.this, ScanQRCodeActivity.class);
        startActivity(intent);
        finish(); // Optional: finish the LoginActivity to prevent going back
    }
    private void navigateToSignUpActivity() {
        // Replace MainActivity.class with the desired activity to navigate to
        Intent intent = new Intent(LoginActivity.this, SignUpActivity.class);
        startActivity(intent);
        finish(); // Optional: finish the LoginActivity to prevent going back
    }
}

