package com.example.predictionapp;

import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;

import androidx.appcompat.app.AppCompatActivity;

import java.io.File;

public class GetStartedActivity extends AppCompatActivity {
    //private TextView lblAccount = findViewById(R.id.lblAccount);
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.get_started);

        Button loginButton = findViewById(R.id.btnLogin);
        Button signUpButton = findViewById(R.id.btnSignUp);

        SharedPreferences sharedPreferences = getSharedPreferences("user_prefs", MODE_PRIVATE);
        boolean isLoggedIn = sharedPreferences.getBoolean("isLoggedIn", false);

        if (isLoggedIn) {
            // User is logged in, navigate to the home activity
            Intent intent = new Intent(this, ProductPreviewActivity.class);
            startActivity(intent);
            //finish(); // Optional, to prevent going back to the MainActivity
        }

        loginButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent intent = new Intent(GetStartedActivity.this, LoginActivity.class);
                startActivity(intent);
            }
        });

        signUpButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent intent = new Intent(GetStartedActivity.this, SignUpActivity.class);
                startActivity(intent);
            }
        });
        if (doesUserDataExist()) {
            signUpButton.setVisibility(View.GONE); // Hide the button
            //lblAccount.setVisibility(View.GONE);
        } else {
            signUpButton.setVisibility(View.VISIBLE); // Show the button
            //lblAccount.setVisibility(View.VISIBLE);
        }
    }

    private boolean doesUserDataExist() {
        String fileName = "user_data.json";
        File file = new File(getApplicationContext().getFilesDir(), fileName);
        return file.exists();
    }
}
